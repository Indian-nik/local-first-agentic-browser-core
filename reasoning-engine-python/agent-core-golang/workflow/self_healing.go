package workflow

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"
)

// SelfHealingConfig defines configuration for self-healing mechanisms
type SelfHealingConfig struct {
	MaxRetries          int
	RetryBackoffBase    time.Duration
	HealthCheckInterval time.Duration
	RecoveryTimeout     time.Duration
	EnableAutoRestart   bool
}

// HealthStatus represents the health state of a component
type HealthStatus struct {
	ComponentName string
	IsHealthy     bool
	LastChecked   time.Time
	ErrorCount    int
	LastError     error
	RecoveryAttempts int
}

// SelfHealingManager manages self-healing operations across the system
type SelfHealingManager struct {
	config         SelfHealingConfig
	components     map[string]*HealthStatus
	mu             sync.RWMutex
	recoveryQueue  chan string
	ctx            context.Context
	cancel         context.CancelFunc
	recoveryFuncs  map[string]func() error
}

// NewSelfHealingManager creates a new self-healing manager
func NewSelfHealingManager(config SelfHealingConfig) *SelfHealingManager {
	ctx, cancel := context.WithCancel(context.Background())
	return &SelfHealingManager{
		config:        config,
		components:    make(map[string]*HealthStatus),
		recoveryQueue: make(chan string, 100),
		ctx:           ctx,
		cancel:        cancel,
		recoveryFuncs: make(map[string]func() error),
	}
}

// RegisterComponent registers a component for health monitoring
func (shm *SelfHealingManager) RegisterComponent(name string, recoveryFunc func() error) {
	shm.mu.Lock()
	defer shm.mu.Unlock()
	
	shm.components[name] = &HealthStatus{
		ComponentName: name,
		IsHealthy:     true,
		LastChecked:   time.Now(),
		ErrorCount:    0,
	}
	shm.recoveryFuncs[name] = recoveryFunc
	log.Printf("[SelfHealing] Registered component: %s", name)
}

// Start begins the self-healing monitoring and recovery processes
func (shm *SelfHealingManager) Start() {
	go shm.monitorHealth()
	go shm.processRecoveryQueue()
	log.Println("[SelfHealing] Manager started")
}

// Stop gracefully stops the self-healing manager
func (shm *SelfHealingManager) Stop() {
	shm.cancel()
	close(shm.recoveryQueue)
	log.Println("[SelfHealing] Manager stopped")
}

// monitorHealth continuously monitors component health
func (shm *SelfHealingManager) monitorHealth() {
	ticker := time.NewTicker(shm.config.HealthCheckInterval)
	defer ticker.Stop()
	
	for {
		select {
		case <-shm.ctx.Done():
			return
		case <-ticker.C:
			shm.performHealthChecks()
		}
	}
}

// performHealthChecks checks all registered components
func (shm *SelfHealingManager) performHealthChecks() {
	shm.mu.RLock()
	components := make([]string, 0, len(shm.components))
	for name := range shm.components {
		components = append(components, name)
	}
	shm.mu.RUnlock()
	
	for _, name := range components {
		if !shm.checkComponentHealth(name) {
			shm.scheduleRecovery(name)
		}
	}
}

// checkComponentHealth checks a specific component's health
func (shm *SelfHealingManager) checkComponentHealth(name string) bool {
	shm.mu.Lock()
	defer shm.mu.Unlock()
	
	status, exists := shm.components[name]
	if !exists {
		return true
	}
	
	status.LastChecked = time.Now()
	
	// Simulate health check logic (replace with actual health check)
	if status.ErrorCount > 0 {
		status.IsHealthy = false
		log.Printf("[SelfHealing] Component %s is unhealthy (errors: %d)", name, status.ErrorCount)
		return false
	}
	
	status.IsHealthy = true
	return true
}

// ReportError reports an error for a component
func (shm *SelfHealingManager) ReportError(componentName string, err error) {
	shm.mu.Lock()
	defer shm.mu.Unlock()
	
	if status, exists := shm.components[componentName]; exists {
		status.ErrorCount++
		status.LastError = err
		status.IsHealthy = false
		log.Printf("[SelfHealing] Error reported for %s: %v (total errors: %d)", 
			componentName, err, status.ErrorCount)
	}
}

// scheduleRecovery schedules a component for recovery
func (shm *SelfHealingManager) scheduleRecovery(componentName string) {
	select {
	case shm.recoveryQueue <- componentName:
		log.Printf("[SelfHealing] Scheduled recovery for %s", componentName)
	case <-shm.ctx.Done():
		return
	default:
		log.Printf("[SelfHealing] Recovery queue full, skipping %s", componentName)
	}
}

// processRecoveryQueue processes components needing recovery
func (shm *SelfHealingManager) processRecoveryQueue() {
	for {
		select {
		case <-shm.ctx.Done():
			return
		case componentName := <-shm.recoveryQueue:
			shm.attemptRecovery(componentName)
		}
	}
}

// attemptRecovery attempts to recover a failed component
func (shm *SelfHealingManager) attemptRecovery(componentName string) {
	shm.mu.RLock()
	recoveryFunc, exists := shm.recoveryFuncs[componentName]
	status := shm.components[componentName]
	shm.mu.RUnlock()
	
	if !exists || recoveryFunc == nil {
		log.Printf("[SelfHealing] No recovery function for %s", componentName)
		return
	}
	
	log.Printf("[SelfHealing] Attempting recovery for %s (attempt %d)", 
		componentName, status.RecoveryAttempts+1)
	
	for attempt := 0; attempt < shm.config.MaxRetries; attempt++ {
		backoff := shm.config.RetryBackoffBase * time.Duration(1<<uint(attempt))
		time.Sleep(backoff)
		
		ctx, cancel := context.WithTimeout(shm.ctx, shm.config.RecoveryTimeout)
		err := shm.executeRecoveryWithContext(ctx, recoveryFunc)
		cancel()
		
		if err == nil {
			shm.markRecovered(componentName)
			log.Printf("[SelfHealing] Successfully recovered %s", componentName)
			return
		}
		
		log.Printf("[SelfHealing] Recovery attempt %d failed for %s: %v", 
			attempt+1, componentName, err)
	}
	
	log.Printf("[SelfHealing] Failed to recover %s after %d attempts", 
		componentName, shm.config.MaxRetries)
	shm.handleRecoveryFailure(componentName)
}

// executeRecoveryWithContext executes recovery function with context
func (shm *SelfHealingManager) executeRecoveryWithContext(ctx context.Context, recoveryFunc func() error) error {
	errChan := make(chan error, 1)
	
	go func() {
		errChan <- recoveryFunc()
	}()
	
	select {
	case err := <-errChan:
		return err
	case <-ctx.Done():
		return fmt.Errorf("recovery timeout exceeded")
	}
}

// markRecovered marks a component as recovered
func (shm *SelfHealingManager) markRecovered(componentName string) {
	shm.mu.Lock()
	defer shm.mu.Unlock()
	
	if status, exists := shm.components[componentName]; exists {
		status.IsHealthy = true
		status.ErrorCount = 0
		status.LastError = nil
		status.RecoveryAttempts++
	}
}

// handleRecoveryFailure handles permanent recovery failures
func (shm *SelfHealingManager) handleRecoveryFailure(componentName string) {
	if shm.config.EnableAutoRestart {
		log.Printf("[SelfHealing] Initiating auto-restart for %s", componentName)
		// Implement auto-restart logic here
	} else {
		log.Printf("[SelfHealing] Manual intervention required for %s", componentName)
	}
}

// GetHealthStatus returns the current health status of all components
func (shm *SelfHealingManager) GetHealthStatus() map[string]HealthStatus {
	shm.mu.RLock()
	defer shm.mu.RUnlock()
	
	status := make(map[string]HealthStatus)
	for name, health := range shm.components {
		status[name] = *health
	}
	return status
}

// ClearErrors clears error count for a component
func (shm *SelfHealingManager) ClearErrors(componentName string) {
	shm.mu.Lock()
	defer shm.mu.Unlock()
	
	if status, exists := shm.components[componentName]; exists {
		status.ErrorCount = 0
		status.LastError = nil
		log.Printf("[SelfHealing] Cleared errors for %s", componentName)
	}
}
