package workflow

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// Task represents a unit of work with dependencies
type Task struct {
	ID           string
	Name         string
	Dependencies []string
	Execute      func(ctx context.Context) error
	Status       TaskStatus
	Result       interface{}
	Error        error
}

type TaskStatus string

const (
	Pending   TaskStatus = "pending"
	Running   TaskStatus = "running"
	Completed TaskStatus = "completed"
	Failed    TaskStatus = "failed"
)

// Scheduler manages task execution with dependency resolution
type Scheduler struct {
	mu            sync.RWMutex
	tasks         map[string]*Task
	graph         map[string][]string // dependency graph
	results       map[string]interface{}
	errorHandler  func(taskID string, err error)
}

func NewScheduler() *Scheduler {
	return &Scheduler{
		tasks:   make(map[string]*Task),
		graph:   make(map[string][]string),
		results: make(map[string]interface{}),
	}
}

func (s *Scheduler) AddTask(task *Task) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	if _, exists := s.tasks[task.ID]; exists {
		return fmt.Errorf("task %s already exists", task.ID)
	}
	
	s.tasks[task.ID] = task
	s.graph[task.ID] = task.Dependencies
	task.Status = Pending
	
	return nil
}

// ResolveDependencies returns tasks in execution order
func (s *Scheduler) ResolveDependencies() ([]*Task, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	
	var ordered []*Task
	visited := make(map[string]bool)
	inProgress := make(map[string]bool)
	
	var visit func(taskID string) error
	visit = func(taskID string) error {
		if visited[taskID] {
			return nil
		}
		
		if inProgress[taskID] {
			return fmt.Errorf("circular dependency detected: %s", taskID)
		}
		
		inProgress[taskID] = true
		
		for _, depID := range s.graph[taskID] {
			if err := visit(depID); err != nil {
				return err
			}
		}
		
		delete(inProgress, taskID)
		visited[taskID] = true
		
		if task, ok := s.tasks[taskID]; ok {
			ordered = append(ordered, task)
		}
		
		return nil
	}
	
	for taskID := range s.tasks {
		if err := visit(taskID); err != nil {
			return nil, err
		}
	}
	
	return ordered, nil
}

// Execute runs all tasks respecting dependencies
func (s *Scheduler) Execute(ctx context.Context) error {
	orderedTasks, err := s.ResolveDependencies()
	if err != nil {
		return fmt.Errorf("dependency resolution failed: %w", err)
	}
	
	for _, task := range orderedTasks {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			if err := s.executeTask(ctx, task); err != nil {
				return err
			}
		}
	}
	
	return nil
}

func (s *Scheduler) executeTask(ctx context.Context, task *Task) error {
	s.mu.Lock()
	task.Status = Running
	s.mu.Unlock()
	
	err := task.Execute(ctx)
	
	s.mu.Lock()
	defer s.mu.Unlock()
	
	if err != nil {
		task.Status = Failed
		task.Error = err
		if s.errorHandler != nil {
			s.errorHandler(task.ID, err)
		}
		return fmt.Errorf("task %s failed: %w", task.ID, err)
	}
	
	task.Status = Completed
	s.results[task.ID] = task.Result
	
	return nil
}
