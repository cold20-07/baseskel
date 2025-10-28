"""
HIPAA Compliance Tests

Test suite to verify HIPAA compliance implementation
"""

import pytest
import json
from datetime import datetime, timezone
from hipaa_compliance import (
    HIPAAEncryption, HIPAAValidator, HIPAASecurityHeaders,
    AuditEventType, AuditLog
)


class TestHIPAAEncryption:
    """Test HIPAA encryption functionality"""
    
    def setup_method(self):
        self.encryption = HIPAAEncryption("test-key-for-testing")
    
    def test_encrypt_decrypt_phi(self):
        """Test PHI encryption and decryption"""
        original_data = "John Doe"
        encrypted_data = self.encryption.encrypt_phi(original_data)
        decrypted_data = self.encryption.decrypt_phi(encrypted_data)
        
        assert encrypted_data != original_data
        assert decrypted_data == original_data
    
    def test_encrypt_empty_data(self):
        """Test encryption of empty data"""
        assert self.encryption.encrypt_phi("") == ""
        assert self.encryption.encrypt_phi(None) is None
    
    def test_hash_phi(self):
        """Test PHI hashing for indexing"""
        data = "sensitive@email.com"
        hash1 = self.encryption.hash_phi(data)
        hash2 = self.encryption.hash_phi(data)
        
        assert hash1 == hash2  # Consistent hashing
        assert hash1 != data   # Hash is different from original
        assert len(hash1) == 64  # SHA-256 produces 64-char hex string
    
    def test_invalid_decryption(self):
        """Test handling of invalid encrypted data"""
        with pytest.raises(ValueError):
            self.encryption.decrypt_phi("invalid-encrypted-data")


class TestHIPAAValidator:
    """Test HIPAA validation functionality"""
    
    def setup_method(self):
        self.validator = HIPAAValidator()
    
    def test_is_phi_data_positive(self):
        """Test PHI detection - positive cases"""
        phi_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "medical_condition": "Diabetes"
        }
        assert self.validator.is_phi_data(phi_data) is True
    
    def test_is_phi_data_negative(self):
        """Test PHI detection - negative cases"""
        non_phi_data = {
            "service_type": "consultation",
            "price": 100,
            "duration": "30 minutes"
        }
        assert self.validator.is_phi_data(non_phi_data) is False
    
    def test_validate_minimum_necessary(self):
        """Test minimum necessary access control"""
        requested_fields = ["name", "email", "phone", "ssn", "medical_condition"]
        
        # Test physician access
        physician_fields = self.validator.validate_minimum_necessary(
            requested_fields, "physician"
        )
        assert "medical_condition" in physician_fields
        assert "ssn" not in physician_fields
        
        # Test staff access
        staff_fields = self.validator.validate_minimum_necessary(
            requested_fields, "staff"
        )
        assert "medical_condition" not in staff_fields
        assert "name" in staff_fields
        
        # Test admin access
        admin_fields = self.validator.validate_minimum_necessary(
            requested_fields, "admin"
        )
        assert admin_fields == requested_fields  # Full access
    
    def test_sanitize_phi_for_logging(self):
        """Test PHI sanitization for logging"""
        data_with_phi = {
            "name": "John Doe",
            "email": "john@example.com",
            "service_type": "consultation",
            "price": 100
        }
        
        sanitized = self.validator.sanitize_phi_for_logging(data_with_phi)
        
        assert sanitized["name"] == "[PHI_REDACTED]"
        assert sanitized["email"] == "[PHI_REDACTED]"
        assert sanitized["service_type"] == "consultation"
        assert sanitized["price"] == 100


class TestHIPAASecurityHeaders:
    """Test HIPAA security headers"""
    
    def setup_method(self):
        self.security_headers = HIPAASecurityHeaders()
    
    def test_security_headers_present(self):
        """Test that all required security headers are present"""
        headers = self.security_headers.get_security_headers()
        
        required_headers = [
            'Strict-Transport-Security',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Content-Security-Policy',
            'Referrer-Policy',
            'Cache-Control'
        ]
        
        for header in required_headers:
            assert header in headers
    
    def test_security_header_values(self):
        """Test security header values are HIPAA compliant"""
        headers = self.security_headers.get_security_headers()
        
        assert headers['X-Frame-Options'] == 'DENY'
        assert headers['X-Content-Type-Options'] == 'nosniff'
        assert 'no-store' in headers['Cache-Control']
        assert 'max-age=31536000' in headers['Strict-Transport-Security']


class TestAuditLog:
    """Test audit log functionality"""
    
    def test_audit_log_creation(self):
        """Test audit log entry creation"""
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.PHI_ACCESS,
            user_email="test@example.com",
            ip_address="127.0.0.1",
            action="Accessed patient record",
            outcome="SUCCESS",
            phi_involved=True
        )
        
        assert audit_log.event_type == AuditEventType.PHI_ACCESS
        assert audit_log.phi_involved is True
        assert audit_log.outcome == "SUCCESS"
    
    def test_audit_log_serialization(self):
        """Test audit log can be serialized to JSON"""
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.PHI_CREATE,
            user_email="test@example.com",
            ip_address="127.0.0.1",
            action="Created contact form",
            outcome="SUCCESS",
            phi_involved=True
        )
        
        # Should be able to convert to dict and JSON
        audit_dict = audit_log.model_dump()
        json_str = json.dumps(audit_dict)
        
        assert isinstance(audit_dict, dict)
        assert isinstance(json_str, str)
        assert "phi_create" in json_str


class TestHIPAACompliance:
    """Integration tests for HIPAA compliance"""
    
    def test_phi_data_flow(self):
        """Test complete PHI data flow: encrypt -> store -> retrieve -> decrypt"""
        encryption = HIPAAEncryption("test-key")
        validator = HIPAAValidator()
        
        # Original PHI data
        phi_data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "555-1234"
        }
        
        # Verify it's detected as PHI
        assert validator.is_phi_data(phi_data) is True
        
        # Encrypt PHI fields
        encrypted_data = {}
        for key, value in phi_data.items():
            if validator.is_phi_data({key: value}):
                encrypted_data[key] = encryption.encrypt_phi(value)
            else:
                encrypted_data[key] = value
        
        # Verify encryption worked
        assert encrypted_data["name"] != phi_data["name"]
        assert encrypted_data["email"] != phi_data["email"]
        
        # Decrypt and verify
        decrypted_data = {}
        for key, value in encrypted_data.items():
            if key in ["name", "email", "phone"]:
                decrypted_data[key] = encryption.decrypt_phi(value)
            else:
                decrypted_data[key] = value
        
        assert decrypted_data == phi_data
    
    def test_audit_event_types(self):
        """Test all audit event types are defined"""
        event_types = [
            AuditEventType.PHI_ACCESS,
            AuditEventType.PHI_CREATE,
            AuditEventType.PHI_UPDATE,
            AuditEventType.PHI_DELETE,
            AuditEventType.PHI_EXPORT,
            AuditEventType.LOGIN_SUCCESS,
            AuditEventType.LOGIN_FAILURE,
            AuditEventType.UNAUTHORIZED_ACCESS,
            AuditEventType.DATA_BREACH_ATTEMPT,
            AuditEventType.SYSTEM_ACCESS
        ]
        
        for event_type in event_types:
            assert isinstance(event_type, str)
            assert len(event_type) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])