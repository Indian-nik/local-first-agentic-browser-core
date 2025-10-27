import time
import threading
import statistics
from typing import Dict, Any, List, Callable, Optional

class AdaptiveProfiler:
    """
    Collects runtime metrics and adapts learning/execution parameters online.
    Provides hooks for the online learner and workflow optimizer.
    """

    def __init__(self,
                 window_size: int = 50,
                 emit_interval_sec: float = 5.0,
                 observers: Optional[List[Callable[[Dict[str, Any]], None]]] = None):
        self.window_size = window_size
        self.emit_interval_sec = emit_interval_sec
        self.metrics: Dict[str, List[float]] = {}
        self.tags: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.observers = observers or []

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="adaptive_profiler", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        while not self._stop.is_set():
            time.sleep(self.emit_interval_sec)
            snapshot = self.snapshot()
            if snapshot:
                for cb in self.observers:
                    try:
                        cb(snapshot)
                    except Exception:
                        # best-effort emit
                        pass

    def observe(self, name: str, value: float):
        with self._lock:
            arr = self.metrics.setdefault(name, [])
            arr.append(value)
            if len(arr) > self.window_size:
                del arr[0:len(arr) - self.window_size]

    def set_tag(self, key: str, value: Any):
        with self._lock:
            self.tags[key] = value

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            stats: Dict[str, Any] = {"tags": dict(self.tags)}
            for k, arr in self.metrics.items():
                if not arr:
                    continue
                stats[k] = {
                    "count": len(arr),
                    "min": min(arr),
                    "max": max(arr),
                    "mean": statistics.fmean(arr),
                    "p50": statistics.median(arr),
                    "p90": self._percentile(arr, 90),
                    "p99": self._percentile(arr, 99),
                }
            # Derived adaptive hints
            stats["adaptive_hints"] = self._derive_hints(stats)
            return stats

    @staticmethod
    def _percentile(arr: List[float], p: float) -> float:
        if not arr:
            return 0.0
        arr_sorted = sorted(arr)
        k = (len(arr_sorted)-1) * (p/100.0)
        f = int(k)
        c = min(f+1, len(arr_sorted)-1)
        if f == c:
            return arr_sorted[int(k)]
        d0 = arr_sorted[f] * (c - k)
        d1 = arr_sorted[c] * (k - f)
        return d0 + d1

    def _derive_hints(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        hints: Dict[str, Any] = {}
        # Example heuristics: adapt batch size and exploration based on latency and success
        lat = stats.get("latency_ms")
        succ = stats.get("success_rate")
        if lat and lat.get("p90", 0) > 800:
            hints["reduce_batch_size"] = True
        if succ and succ.get("mean", 1.0) < 0.7:
            hints["increase_exploration"] = True
        return hints

# Global singleton helper
_profiler: Optional[AdaptiveProfiler] = None

def get_profiler() -> AdaptiveProfiler:
    global _profiler
    if _profiler is None:
        _profiler = AdaptiveProfiler()
        _profiler.start()
    return _profiler
