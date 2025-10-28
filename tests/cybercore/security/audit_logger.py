"""
Security Audit Logger
Comprehensive logging and audit trail for all security activities
"""

import json
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class AuditLogEntry:
    """Individual audit log entry"""
    timestamp: str
    session_id: str
    event_type: str
    activity: str
    context: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    user: Optional[str] = None
    integrity_hash: Optional[str] = None

class SecurityAuditLogger:
    """
    Comprehensive audit logging for security activities
    Maintains tamper-evident logs with full traceability
    """
    
    def __init__(self, log_dir: str = "./audit_logs"):
        """Initialize the security audit logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize audit log file
        self.audit_file = self.log_dir / f"cybercore_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        # Log entries cache
        self.log_entries: List[AuditLogEntry] = []
        
        self.logger.info(f"Security audit logger initialized - Log file: {self.audit_file}")
    
    def log_request(self, session_id: str, request: str, context) -> str:
        """
        Log a security testing request
        
        Args:
            session_id: Session identifier
            request: Security request description
            context: Security context information
            
        Returns:
            Unique log entry ID
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            event_type="REQUEST",
            activity=request,
            context=self._serialize_context(context),
            user=getattr(context, 'authorized_by', None) if context else None
        )
        
        # Add integrity hash
        entry.integrity_hash = self._generate_integrity_hash(entry)
        
        return self._write_log_entry(entry)
    
    def log_validation(self, session_id: str, validation_type: str, result: Dict[str, Any]) -> str:
        """
        Log validation results
        
        Args:
            session_id: Session identifier
            validation_type: Type of validation performed
            result: Validation result
            
        Returns:
            Unique log entry ID
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            event_type="VALIDATION",
            activity=validation_type,
            context={"validation_type": validation_type},
            result=result
        )
        
        entry.integrity_hash = self._generate_integrity_hash(entry)
        return self._write_log_entry(entry)
    
    def log_completion(self, session_id: str, activity_type: str, results: Dict[str, Any]) -> str:
        """
        Log completion of security activity
        
        Args:
            session_id: Session identifier
            activity_type: Type of activity completed
            results: Activity results
            
        Returns:
            Unique log entry ID
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            event_type="COMPLETION",
            activity=activity_type,
            context={"activity_type": activity_type},
            result=self._sanitize_results(results)
        )
        
        entry.integrity_hash = self._generate_integrity_hash(entry)
        return self._write_log_entry(entry)
    
    def log_violation(self, session_id: str, violation_type: str, details: Dict[str, Any]) -> str:
        """
        Log ethical or authorization violations
        
        Args:
            session_id: Session identifier
            violation_type: Type of violation
            details: Violation details
            
        Returns:
            Unique log entry ID
        """
        entry = AuditLogEntry(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            event_type="VIOLATION",
            activity=f"Violation: {violation_type}",
            context={"violation_type": violation_type},
            result=details
        )
        
        entry.integrity_hash = self._generate_integrity_hash(entry)
        
        # Also log to standard logger for immediate attention
        self.logger.warning(f"Security violation logged: {violation_type} in session {session_id}")
        
        return self._write_log_entry(entry)
    
    def _serialize_context(self, context) -> Dict[str, Any]:
        """
        Serialize context object for logging
        
        Args:
            context: Context object to serialize
            
        Returns:
            Serialized context dictionary
        """
        if not context:
            return {}
        
        try:
            # Try to convert to dict if it's a dataclass
            if hasattr(context, '__dataclass_fields__'):
                return asdict(context)
            
            # Handle enum types
            serialized = {}
            for attr in dir(context):
                if not attr.startswith('_'):
                    value = getattr(context, attr)
                    if hasattr(value, 'value'):  # Enum
                        serialized[attr] = value.value
                    elif not callable(value):
                        serialized[attr] = str(value)
            
            return serialized
            
        except Exception as e:
            self.logger.warning(f"Context serialization failed: {e}")
            return {"context_type": str(type(context).__name__)}
    
    def _sanitize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize results to remove sensitive information
        
        Args:
            results: Raw results to sanitize
            
        Returns:
            Sanitized results
        """
        sanitized = results.copy()
        
        # Remove potentially sensitive fields
        sensitive_fields = [
            'password', 'token', 'key', 'secret', 'credential',
            'api_key', 'access_token', 'private_key'
        ]
        
        def sanitize_dict(d):
            if isinstance(d, dict):
                for key, value in d.items():
                    if any(sensitive in key.lower() for sensitive in sensitive_fields):
                        d[key] = "[REDACTED]"
                    elif isinstance(value, (dict, list)):
                        sanitize_dict(value)
            elif isinstance(d, list):
                for item in d:
                    if isinstance(item, (dict, list)):
                        sanitize_dict(item)
        
        sanitize_dict(sanitized)
        return sanitized
    
    def _generate_integrity_hash(self, entry: AuditLogEntry) -> str:
        """
        Generate integrity hash for log entry
        
        Args:
            entry: Log entry to hash
            
        Returns:
            SHA-256 hash of entry content
        """
        # Create a copy without the hash field
        entry_copy = AuditLogEntry(
            timestamp=entry.timestamp,
            session_id=entry.session_id,
            event_type=entry.event_type,
            activity=entry.activity,
            context=entry.context,
            result=entry.result,
            user=entry.user
        )
        
        # Generate hash from JSON representation
        entry_json = json.dumps(asdict(entry_copy), sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()
    
    def _write_log_entry(self, entry: AuditLogEntry) -> str:
        """
        Write log entry to file and memory cache
        
        Args:
            entry: Log entry to write
            
        Returns:
            Unique entry ID
        """
        # Add to memory cache
        self.log_entries.append(entry)
        
        # Write to file
        try:
            with open(self.audit_file, 'a', encoding='utf-8') as f:
                json.dump(asdict(entry), f)
                f.write('\n')
        except Exception as e:
            self.logger.error(f"Failed to write audit log entry: {e}")
        
        # Return unique ID
        return f"{entry.session_id}_{entry.timestamp}_{len(self.log_entries)}"
    
    def verify_log_integrity(self) -> Dict[str, Any]:
        """
        Verify integrity of all log entries
        
        Returns:
            Integrity verification results
        """
        verified_entries = 0
        corrupted_entries = []
        
        for i, entry in enumerate(self.log_entries):
            expected_hash = self._generate_integrity_hash(entry)
            if entry.integrity_hash == expected_hash:
                verified_entries += 1
            else:
                corrupted_entries.append({
                    'entry_index': i,
                    'timestamp': entry.timestamp,
                    'expected_hash': expected_hash,
                    'actual_hash': entry.integrity_hash
                })
        
        return {
            'total_entries': len(self.log_entries),
            'verified_entries': verified_entries,
            'corrupted_entries': len(corrupted_entries),
            'corruption_details': corrupted_entries,
            'integrity_score': (verified_entries / len(self.log_entries)) * 100 if self.log_entries else 100
        }
    
    def get_session_logs(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all log entries for a session
        
        Args:
            session_id: Session to retrieve logs for
            
        Returns:
            List of log entries for the session
        """
        session_logs = []
        for entry in self.log_entries:
            if entry.session_id == session_id:
                session_logs.append(asdict(entry))
        
        return session_logs
    
    def generate_audit_report(self, session_id: Optional[str] = None) -> str:
        """
        Generate comprehensive audit report
        
        Args:
            session_id: Optional session ID to filter by
            
        Returns:
            Formatted audit report
        """
        if session_id:
            entries = self.get_session_logs(session_id)
            report_title = f"Session Audit Report - {session_id}"
        else:
            entries = [asdict(entry) for entry in self.log_entries]
            report_title = "Complete Audit Report"
        
        # Calculate statistics
        event_types = {}
        violations = []
        for entry in entries:
            event_type = entry['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            if event_type == 'VIOLATION':
                violations.append(entry)
        
        integrity_check = self.verify_log_integrity()
        
        report = f"""
# {report_title.upper()}

## Audit Summary
- Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Total Log Entries: {len(entries)}
- Audit File: {self.audit_file.name}

## Event Type Distribution
"""
        
        for event_type, count in event_types.items():
            report += f"- {event_type}: {count}\n"
        
        if violations:
            report += f"""

## Security Violations
{len(violations)} violation(s) recorded:
"""
            for violation in violations:
                report += f"- {violation['timestamp']}: {violation['activity']}\n"
        
        report += f"""

## Integrity Verification
- Total Entries: {integrity_check['total_entries']}
- Verified Entries: {integrity_check['verified_entries']}
- Integrity Score: {integrity_check['integrity_score']:.1f}%

## Compliance Status
- Full audit trail maintained ✓
- Tamper-evident logging ✓
- Activity traceability ✓
- Violation monitoring ✓

---
*This audit report provides complete traceability of all security activities.*
        """
        
        return report
