package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

type Agent struct {
	ID      string    `json:"id"`
	Name    string    `json:"name"`
	Status  string    `json:"status"`
	LastRun time.Time `json:"last_run"`
}

type Task struct {
	ID       string    `json:"id"`
	AgentID  string    `json:"agent_id"`
	Name     string    `json:"name"`
	Schedule string    `json:"schedule"`
	Status   string    `json:"status"`
	LastRun  time.Time `json:"last_run"`
	NextRun  time.Time `json:"next_run"`
	Result   string    `json:"result"`
}

var db *sql.DB

func mustInitDB() {
	dsn := getenv("AGENT_DB_DSN", "/data/agent.db")
	driver := getenv("AGENT_DB_DRIVER", "sqlite")
	var err error
	db, err = sql.Open(driver, dsn)
	if err != nil { log.Fatal(err) }
	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS agents(
			id TEXT PRIMARY KEY,
			name TEXT,
			status TEXT,
			last_run TIMESTAMP
		);
		CREATE TABLE IF NOT EXISTS tasks(
			id TEXT PRIMARY KEY,
			agent_id TEXT,
			name TEXT,
			schedule TEXT,
			status TEXT,
			last_run TIMESTAMP,
			next_run TIMESTAMP,
			result TEXT
		);
	`)
	if err != nil { log.Fatal(err) }
}

func getenv(k, def string) string { v := os.Getenv(k); if v == "" { return def }; return v }

func main() {
	mustInitDB()
	go scheduler()

	http.HandleFunc("/agent", agentsHandler)
	http.HandleFunc("/agent/", agentHandler)
	http.HandleFunc("/task", tasksHandler)
	http.HandleFunc("/task/", taskHandler)
	addr := getenv("ADDR", ":8080")
	log.Printf("agent-core listening on %s", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}

func agentsHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		rows, _ := db.Query("SELECT id, name, status, IFNULL(last_run,'1970-01-01') FROM agents")
		var list []Agent
		for rows.Next() { var a Agent; rows.Scan(&a.ID,&a.Name,&a.Status,&a.LastRun); list = append(list,a) }
		json.NewEncoder(w).Encode(list)
	case http.MethodPost:
		var a Agent; json.NewDecoder(r.Body).Decode(&a)
		if a.ID == "" { a.ID = fmt.Sprintf("a_%d", time.Now().UnixNano()) }
		_, err := db.Exec("INSERT INTO agents(id,name,status,last_run) VALUES(?,?,?,?)", a.ID,a.Name,coalesce(a.Status,"idle"),time.Now())
		if err != nil { http.Error(w, err.Error(), 500); return }
		json.NewEncoder(w).Encode(a)
	default:
		w.WriteHeader(405)
	}
}

func agentHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/agent/"):]
	switch r.Method {
	case http.MethodPut:
		var a Agent; json.NewDecoder(r.Body).Decode(&a)
		_, err := db.Exec("UPDATE agents SET name=?, status=? WHERE id=?", a.Name, a.Status, id)
		if err != nil { http.Error(w, err.Error(), 500); return }
		w.WriteHeader(204)
	case http.MethodDelete:
		_, err := db.Exec("DELETE FROM agents WHERE id=?", id)
		if err != nil { http.Error(w, err.Error(), 500); return }
		w.WriteHeader(204)
	case http.MethodPost:
		// run agent now
		go runAgent(id)
		w.WriteHeader(202)
	default:
		w.WriteHeader(405)
	}
}

func tasksHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		rows, _ := db.Query("SELECT id, agent_id, name, schedule, status, IFNULL(last_run,'1970-01-01'), IFNULL(next_run,'1970-01-01'), IFNULL(result,'') FROM tasks")
		var list []Task
		for rows.Next() { var t Task; rows.Scan(&t.ID,&t.AgentID,&t.Name,&t.Schedule,&t.Status,&t.LastRun,&t.NextRun,&t.Result); list = append(list,t) }
		json.NewEncoder(w).Encode(list)
	case http.MethodPost:
		var t Task; json.NewDecoder(r.Body).Decode(&t)
		if t.ID == "" { t.ID = fmt.Sprintf("t_%d", time.Now().UnixNano()) }
		if t.Status == "" { t.Status = "scheduled" }
		if t.NextRun.IsZero() { t.NextRun = time.Now() }
		_, err := db.Exec("INSERT INTO tasks(id,agent_id,name,schedule,status,last_run,next_run,result) VALUES(?,?,?,?,?,?,?,?)",
			t.ID,t.AgentID,t.Name,t.Schedule,t.Status,t.LastRun,t.NextRun,t.Result)
		if err != nil { http.Error(w, err.Error(), 500); return }
		json.NewEncoder(w).Encode(t)
	default:
		w.WriteHeader(405)
	}
}

func taskHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/task/"):]
	switch r.Method {
	case http.MethodPut:
		var t Task; json.NewDecoder(r.Body).Decode(&t)
		_, err := db.Exec("UPDATE tasks SET agent_id=?, name=?, schedule=?, status=?, next_run=?, result=? WHERE id=?",
			t.AgentID,t.Name,t.Schedule,t.Status,t.NextRun,t.Result,id)
		if err != nil { http.Error(w, err.Error(), 500); return }
		w.WriteHeader(204)
	case http.MethodDelete:
		_, err := db.Exec("DELETE FROM tasks WHERE id=?", id)
		if err != nil { http.Error(w, err.Error(), 500); return }
		w.WriteHeader(204)
	case http.MethodPost:
		go runTask(id)
		w.WriteHeader(202)
	default:
		w.WriteHeader(405)
	}
}

func scheduler() {
	interval, _ := time.ParseDuration(fmt.Sprintf("%ss", getenv("SCHEDULER_INTERVAL_SECONDS","15")))
	if interval == 0 { interval = 15 * time.Second }
	t := time.NewTicker(interval)
	for range t.C {
		rows, err := db.Query("SELECT id FROM tasks WHERE status IN ('scheduled','retry') AND next_run <= ?", time.Now())
		if err != nil { log.Println("scheduler query err:", err); continue }
		for rows.Next() {
			var id string; rows.Scan(&id); go runTask(id)
		}
	}
}

func runAgent(id string) {
	log.Printf("running agent %s", id)
	db.Exec("UPDATE agents SET status=?, last_run=? WHERE id=?", "running", time.Now(), id)
	// simulate work
	time.Sleep(500 * time.Millisecond)
	db.Exec("UPDATE agents SET status=?, last_run=? WHERE id=?", "idle", time.Now(), id)
	emitLog(map[string]any{"type":"agent_run","agent_id":id,"ts":time.Now()})
}

func runTask(id string) {
	log.Printf("running task %s", id)
	db.Exec("UPDATE tasks SET status=?, last_run=? WHERE id=?", "running", time.Now(), id)
	// simulate execution
	time.Sleep(750 * time.Millisecond)
	result := fmt.Sprintf("task %s completed", id)
	next := time.Now().Add(1 * time.Hour)
	db.Exec("UPDATE tasks SET status=?, result=?, next_run=? WHERE id=?", "completed", result, next, id)
	emitLog(map[string]any{"type":"task_run","task_id":id,"result":result,"ts":time.Now()})
}

func emitLog(payload map[string]any) {
	url := getenv("OBSERVABILITY_URL", "http://localhost:9000") + "/log"
	b, _ := json.Marshal(payload)
	http.Post(url, "application/json", bytesReader(b))
}

func bytesReader(b []byte) *bytesReaderT { return &bytesReaderT{b: b} }

type bytesReaderT struct{ b []byte; i int }
func (r *bytesReaderT) Read(p []byte) (int, error) { if r.i >= len(r.b) { return 0, io.EOF }; n := copy(p, r.b[r.i:]); r.i += n; return n, nil }
func (r *bytesReaderT) Close() error { return nil }

// imports for bytesReader
//go:linkname _ io
import io "io"
//go:linkname _ bytes
import bytes "bytes"
