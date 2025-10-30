"""
HIPAA Compliance Module for Dr. Kishan Bhalani Medical Documentation Services

This module implements HIPAA compliance measures including:
- Data encryption
- Audit logging
- Access controls
- PHI handling
- Security measures
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from pydantic import BaseModel
from enum import Enum


class AuditEventType(str, Enum):
    """HIPAA Audit Event Types"""
    PHI_ACCESS = "phi_access"
    PHI_CREATE = "phi_create"
    PHI_UPDATE = "phi_update"
    PHI_DELETE = "phi_delete"
    PHI_EXPORT = "phi_export"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH_ATTEMPT = "data_breach_attempt"
    SYSTEM_ACCESS = "system_access"


class AuditLog(BaseModel):
    """HIPAA Audit Log Entry"""
    timestamp: str
    event_type: AuditEventType
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    action: str
    outcome: str  # SUCCESS, FAILURE, WARNING
    details: Optional[Dict[str, Any]] = None
    phi_involved: bool = False


class HIPAAEncryption:
    """HIPAA-compliant encryption utilities"""

    def __init__(self, password: str = None):
        if password is None:
            password = os.environ.get('HIPAA_ENCRYPTION_KEY', 'default-key-change-in-production')

        # Generate key from password
        password_bytes = password.encode()
        salt = b'hipaa_salt_2024'  # In production, use random salt per encryption
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        self.cipher_suite = Fernet(key)

    def encrypt_phi(self, data: str) -> str:
        """Encrypt PHI data"""
        if not data:
            return data
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_phi(self, encrypted_data: str) -> str:
        """Decrypt PHI data"""
        if not encrypted_data:
            return encrypted_data
        try:
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logging.error(f"Failed to decrypt PHI data: {e}")
            raise ValueError("Invalid encrypted data")

    def hash_phi(self, data: str) -> str:
        """Create irreversible hash of PHI for indexing"""
        if not data:
            return data
        return hashlib.sha256(data.encode()).hexdigest()


class HIPAAAuditLogger:
    """HIPAA-compliant audit logging"""

    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.logger = logging.getLogger('hipaa_audit')

        # Configure audit logger
        handler = logging.FileHandler('hipaa_audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - HIPAA_AUDIT - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_event(self, audit_log: AuditLog):
        """Log HIPAA audit event"""
        try:
            # Log to file
            log_message = f"Event: {audit_log.event_type} | User: {audit_log.user_email} | " \
                         f"IP: {audit_log.ip_address} | Action: {audit_log.action} | " \
                         f"Outcome: {audit_log.outcome} | PHI: {audit_log.phi_involved}"

            if audit_log.outcome == "FAILURE":
                self.logger.error(log_message)
            elif audit_log.outcome == "WARNING":
                self.logger.warning(log_message)
            else:
                self.logger.info(log_message)

            # Store in database for compliance reporting
            audit_data = audit_log.model_dump()
            self.supabase.table('hipaa_audit_logs').insert(audit_data).execute()

        except Exception as e:
            # Critical: audit logging must not fail
            self.logger.critical(f"AUDIT LOGGING FAILED: {e}")

    def log_phi_access(self, user_email: str, resource_type: str, resource_id: str,
                      ip_address: str, user_agent: str = None):
        """Log PHI access event"""
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.PHI_ACCESS,
            user_email=user_email,
            ip_address=ip_address,
            user_agent=user_agent,
            resource_type=resource_type,
            resource_id=resource_id,
            action=f"Accessed {resource_type}",
            outcome="SUCCESS",
            phi_involved=True
        )
        self.log_event(audit_log)

    def log_unauthorized_access(self, ip_address: str, attempted_resource: str,
                              user_agent: str = None):
        """Log unauthorized access attempt"""
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.UNAUTHORIZED_ACCESS,
            ip_address=ip_address,
            user_agent=user_agent,
            action=f"Attempted unauthorized access to {attempted_resource}",
            outcome="FAILURE",
            phi_involved=True
        )
        self.log_event(audit_log)


class HIPAAValidator:
    """HIPAA compliance validation utilities"""

    @staticmethod
    def is_phi_data(data: Dict[str, Any]) -> bool:
        """Check if data contains PHI"""
        phi_fields = {
            'name', 'email', 'phone', 'address', 'ssn', 'medical_record_number',
            'date_of_birth', 'medical_condition', 'diagnosis', 'treatment',
            'medication', 'doctor_name', 'hospital_name', 'insurance_info'
        }

        data_keys = set(str(key).lower() for key in data.keys())
        return bool(phi_fields.intersection(data_keys))

    @staticmethod
    def validate_minimum_necessary(requested_fields: list, user_role: str) -> list:
        """Implement minimum necessary standard"""
        role_permissions = {
            'admin': ['*'],  # Full access
            'physician': ['name', 'email', 'phone', 'medical_condition', 'diagnosis', 'treatment'],
            'staff': ['name', 'email', 'phone'],
            'patient': ['name', 'email', 'phone', 'medical_condition']  # Own data only
        }

        allowed_fields = role_permissions.get(user_role, [])

        if '*' in allowed_fields:
            return requested_fields

        return [field for field in requested_fields if field in allowed_fields]

    @staticmethod
    def sanitize_phi_for_logging(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove PHI from data for safe logging"""
        phi_fields = {
            'name', 'email', 'phone', 'address', 'ssn', 'medical_record_number',
            'date_of_birth', 'medical_condition', 'diagnosis', 'treatment'
        }

        sanitized = {}
        for key, value in data.items():
            if key.lower() in phi_fields:
                sanitized[key] = "[PHI_REDACTED]"
            else:
                sanitized[key] = value

        return sanitized


class HIPAASecurityHeaders:
    """HIPAA-compliant security headers"""

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get HIPAA-compliant security headers"""
        return {
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Cache-Control': 'no-store, no-cache, must-revalidate, private',
            'Pragma': 'no-cache',
            'Expires': '0'
        }


class HIPAADataRetention:
    """HIPAA data retention and disposal"""

    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def schedule_data_deletion(self, table_name: str, record_id: str,
                             retention_years: int = 6):
        """Schedule data for deletion per HIPAA retention requirements"""
        deletion_date = datetime.now(timezone.utc).replace(
            year=datetime.now().year + retention_years
        ).isoformat()

        retention_record = {
            'table_name': table_name,
            'record_id': record_id,
            'scheduled_deletion_date': deletion_date,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'status': 'scheduled'
        }

        self.supabase.table('hipaa_data_retention').insert(retention_record).execute()

    def execute_scheduled_deletions(self):
        """Execute scheduled data deletions"""
        current_date = datetime.now(timezone.utc).isoformat()

        # Get records scheduled for deletion
        response = self.supabase.table('hipaa_data_retention')\
            .select('*')\
            .eq('status', 'scheduled')\
            .lte('scheduled_deletion_date', current_date)\
            .execute()

        for record in response.data:
            try:
                # Delete the actual data
                self.supabase.table(record['table_name'])\
                    .delete()\
                    .eq('id', record['record_id'])\
                    .execute()

                # Mark retention record as completed
                self.supabase.table('hipaa_data_retention')\
                    .update({'status': 'completed', 'deleted_at': current_date})\
                    .eq('id', record['id'])\
                    .execute()

                logging.info(f"HIPAA: Deleted record {record['record_id']} from {record['table_name']}")

            except Exception as e:
                logging.error(f"HIPAA: Failed to delete record {record['record_id']}: {e}")


# Global instances
encryption = HIPAAEncryption()
validator = HIPAAValidator()
security_headers = HIPAASecurityHeaders()
