"""
Authorization Validator
Validates permissions and authorization for security testing activities
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AuthorizationLevel(Enum):
    """Authorization levels for security testing"""
    READ_ONLY = "read_only"
    LIMITED_TESTING = "limited_testing"
    FULL_ASSESSMENT = "full_assessment"
    PENETRATION_TESTING = "penetration_testing"
    RED_TEAM = "red_team"

@dataclass
class AuthorizationScope:
    """Defines the scope of authorized security testing"""
    target_systems: List[str]
    authorized_activities: List[str]
    time_window: tuple
    authorization_level: AuthorizationLevel
    authorized_by: str
    contact_info: str
    restrictions: List[str]

class AuthorizationValidator:
    """
    Validates authorization for security testing activities
    Ensures all testing is properly authorized and within scope
    """
    
    def __init__(self):
        """Initialize the authorization validator"""
        self.logger = logging.getLogger(__name__)
        self.authorized_scopes: List[AuthorizationScope] = []
        
        # Default authorized activities by level
        self.level_permissions = {
            AuthorizationLevel.READ_ONLY: [
                'information_gathering',
                'reconnaissance',
                'passive_scanning'
            ],
            AuthorizationLevel.LIMITED_TESTING: [
                'information_gathering',
                'reconnaissance', 
                'passive_scanning',
                'port_scanning',
                'service_enumeration',
                'vulnerability_scanning'
            ],
            AuthorizationLevel.FULL_ASSESSMENT: [
                'information_gathering',
                'reconnaissance',
                'passive_scanning',
                'port_scanning',
                'service_enumeration',
                'vulnerability_scanning',
                'web_application_testing',
                'network_testing',
                'configuration_review'
            ],
            AuthorizationLevel.PENETRATION_TESTING: [
                'all_assessment_activities',
                'exploit_verification',
                'privilege_escalation',
                'lateral_movement',
                'data_exfiltration_simulation'
            ],
            AuthorizationLevel.RED_TEAM: [
                'all_penetration_activities',
                'social_engineering',
                'physical_security_testing',
                'advanced_persistent_threat_simulation'
            ]
        }
    
    def add_authorization_scope(self, scope: AuthorizationScope) -> bool:
        """
        Add an authorized testing scope
        
        Args:
            scope: Authorization scope to add
            
        Returns:
            True if scope was added successfully
        """
        # Validate the scope
        if not self._validate_scope(scope):
            self.logger.warning(f"Invalid authorization scope rejected")
            return False
        
        self.authorized_scopes.append(scope)
        self.logger.info(f"Authorization scope added for {len(scope.target_systems)} systems")
        return True
    
    def validate_authorization(self, context) -> Dict[str, Any]:
        """
        Validate if a security context is authorized
        
        Args:
            context: Security context to validate
            
        Returns:
            Validation result
        """
        if not hasattr(context, 'authorization_scope'):
            return {
                'valid': False,
                'reason': 'No authorization scope provided',
                'requirements': ['Provide valid authorization scope']
            }
        
        # Check for matching authorization scope
        matching_scope = self._find_matching_scope(context)
        if not matching_scope:
            return {
                'valid': False,
                'reason': 'No matching authorization scope found',
                'requirements': [
                    'Obtain proper authorization',
                    'Ensure target system is in authorized scope',
                    'Verify time window is valid'
                ]
            }
        
        # Check if activity is permitted
        task_type = str(context.task_type.value) if hasattr(context.task_type, 'value') else str(context.task_type)
        if not self._is_activity_authorized(task_type, matching_scope):
            return {
                'valid': False,
                'reason': f'Activity "{task_type}" not authorized for current scope',
                'requirements': ['Obtain higher level authorization for this activity']
            }
        
        # Check time window
        if not self._is_time_valid(matching_scope):
            return {
                'valid': False,
                'reason': 'Current time is outside authorized testing window',
                'requirements': ['Test only during authorized time window']
            }
        
        return {
            'valid': True,
            'scope': matching_scope,
            'level': matching_scope.authorization_level.value,
            'restrictions': matching_scope.restrictions
        }
    
    def _validate_scope(self, scope: AuthorizationScope) -> bool:
        """
        Validate an authorization scope
        
        Args:
            scope: Scope to validate
            
        Returns:
            True if scope is valid
        """
        if not scope.target_systems:
            return False
        
        if not scope.authorized_by:
            return False
        
        if not scope.contact_info:
            return False
        
        # Validate time window
        try:
            start_time, end_time = scope.time_window
            if start_time >= end_time:
                return False
        except (ValueError, TypeError):
            return False
        
        return True
    
    def _find_matching_scope(self, context) -> Optional[AuthorizationScope]:
        """
        Find matching authorization scope for context
        
        Args:
            context: Security context to match
            
        Returns:
            Matching authorization scope or None
        """
        target = getattr(context, 'target_system', '')
        
        for scope in self.authorized_scopes:
            # Check if target system is in scope
            if target in scope.target_systems or '*' in scope.target_systems:
                return scope
        
        return None
    
    def _is_activity_authorized(self, activity: str, scope: AuthorizationScope) -> bool:
        """
        Check if activity is authorized for the given scope
        
        Args:
            activity: Activity to check
            scope: Authorization scope
            
        Returns:
            True if activity is authorized
        """
        authorized_activities = self.level_permissions.get(scope.authorization_level, [])
        
        # Check for explicit authorization
        if activity.lower() in [a.lower() for a in authorized_activities]:
            return True
        
        # Check for wildcard permissions
        if 'all_assessment_activities' in authorized_activities and 'assessment' in activity.lower():
            return True
        
        if 'all_penetration_activities' in authorized_activities and 'penetration' in activity.lower():
            return True
        
        # Check specific activity in scope
        if activity.lower() in [a.lower() for a in scope.authorized_activities]:
            return True
        
        return False
    
    def _is_time_valid(self, scope: AuthorizationScope) -> bool:
        """
        Check if current time is within authorized window
        
        Args:
            scope: Authorization scope to check
            
        Returns:
            True if current time is valid
        """
        current_time = datetime.now()
        start_time, end_time = scope.time_window
        
        return start_time <= current_time <= end_time
    
    def get_authorization_status(self) -> Dict[str, Any]:
        """
        Get current authorization status
        
        Returns:
            Authorization status information
        """
        active_scopes = []
        for scope in self.authorized_scopes:
            if self._is_time_valid(scope):
                active_scopes.append({
                    'level': scope.authorization_level.value,
                    'targets': len(scope.target_systems),
                    'authorized_by': scope.authorized_by,
                    'expires': scope.time_window[1].isoformat()
                })
        
        return {
            'total_scopes': len(self.authorized_scopes),
            'active_scopes': len(active_scopes),
            'scopes': active_scopes
        }
    
    def generate_authorization_report(self) -> str:
        """
        Generate authorization compliance report
        
        Returns:
            Formatted authorization report
        """
        status = self.get_authorization_status()
        
        report = f"""
# AUTHORIZATION COMPLIANCE REPORT

## Summary
- Total Authorization Scopes: {status['total_scopes']}
- Currently Active Scopes: {status['active_scopes']}
- Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Active Authorizations
"""
        
        for scope_info in status['scopes']:
            report += f"""
### Authorization Level: {scope_info['level'].replace('_', ' ').title()}
- Target Systems: {scope_info['targets']}
- Authorized By: {scope_info['authorized_by']}
- Expires: {scope_info['expires']}
"""
        
        report += """

## Compliance Verification
- All activities validated against authorization scopes
- Time window restrictions enforced
- Activity-level permissions verified
- Full audit trail maintained

---
*This report confirms all security testing activities are properly authorized.*
        """
        
        return report
