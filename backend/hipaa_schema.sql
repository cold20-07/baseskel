-- HIPAA Compliance Database Schema
-- Run this in your Supabase SQL editor after the main schema

-- HIPAA Audit Logs Table
CREATE TABLE IF NOT EXISTS hipaa_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    event_type TEXT NOT NULL,
    user_id TEXT,
    user_email TEXT,
    ip_address INET,
    user_agent TEXT,
    resource_type TEXT,
    resource_id TEXT,
    action TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('SUCCESS', 'FAILURE', 'WARNING')),
    details JSONB,
    phi_involved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- HIPAA Data Retention Table
CREATE TABLE IF NOT EXISTS hipaa_data_retention (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    scheduled_deletion_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- HIPAA Business Associate Agreements Table
CREATE TABLE IF NOT EXISTS hipaa_business_associates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    contact_person TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    baa_signed_date DATE NOT NULL,
    baa_expiry_date DATE NOT NULL,
    baa_document_url TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'terminated')),
    services_provided TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- HIPAA Breach Incidents Table
CREATE TABLE IF NOT EXISTS hipaa_breach_incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_date TIMESTAMP WITH TIME ZONE NOT NULL,
    discovered_date TIMESTAMP WITH TIME ZONE NOT NULL,
    incident_type TEXT NOT NULL,
    description TEXT NOT NULL,
    affected_individuals_count INTEGER DEFAULT 0,
    phi_types_involved TEXT[],
    cause TEXT,
    mitigation_actions TEXT,
    reported_to_hhs BOOLEAN DEFAULT FALSE,
    reported_to_individuals BOOLEAN DEFAULT FALSE,
    status TEXT NOT NULL DEFAULT 'investigating' CHECK (status IN ('investigating', 'contained', 'resolved')),
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- HIPAA User Access Permissions Table
CREATE TABLE IF NOT EXISTS hipaa_user_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'physician', 'staff', 'patient')),
    permissions JSONB NOT NULL DEFAULT '{}',
    granted_by TEXT NOT NULL,
    granted_date TIMESTAMP WITH TIME ZONE NOT NULL,
    expiry_date TIMESTAMP WITH TIME ZONE,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'revoked')),
    last_access TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- HIPAA Training Records Table
CREATE TABLE IF NOT EXISTS hipaa_training_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    training_type TEXT NOT NULL,
    training_date DATE NOT NULL,
    completion_status TEXT NOT NULL CHECK (completion_status IN ('completed', 'in_progress', 'failed')),
    score INTEGER,
    certificate_url TEXT,
    expiry_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance and compliance reporting
CREATE INDEX IF NOT EXISTS idx_hipaa_audit_logs_timestamp ON hipaa_audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_hipaa_audit_logs_event_type ON hipaa_audit_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_hipaa_audit_logs_user_email ON hipaa_audit_logs(user_email);
CREATE INDEX IF NOT EXISTS idx_hipaa_audit_logs_phi_involved ON hipaa_audit_logs(phi_involved);
CREATE INDEX IF NOT EXISTS idx_hipaa_audit_logs_ip_address ON hipaa_audit_logs(ip_address);

CREATE INDEX IF NOT EXISTS idx_hipaa_data_retention_deletion_date ON hipaa_data_retention(scheduled_deletion_date);
CREATE INDEX IF NOT EXISTS idx_hipaa_data_retention_status ON hipaa_data_retention(status);

CREATE INDEX IF NOT EXISTS idx_hipaa_breach_incidents_date ON hipaa_breach_incidents(incident_date);
CREATE INDEX IF NOT EXISTS idx_hipaa_breach_incidents_severity ON hipaa_breach_incidents(severity);

CREATE INDEX IF NOT EXISTS idx_hipaa_user_permissions_user_email ON hipaa_user_permissions(user_email);
CREATE INDEX IF NOT EXISTS idx_hipaa_user_permissions_role ON hipaa_user_permissions(role);
CREATE INDEX IF NOT EXISTS idx_hipaa_user_permissions_status ON hipaa_user_permissions(status);

-- Enable Row Level Security for HIPAA tables
ALTER TABLE hipaa_audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_data_retention ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_business_associates ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_breach_incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_user_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE hipaa_training_records ENABLE ROW LEVEL SECURITY;

-- Create policies for HIPAA tables (admin access only)
CREATE POLICY "Admin only access to audit logs" ON hipaa_audit_logs
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Admin only access to data retention" ON hipaa_data_retention
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Admin only access to business associates" ON hipaa_business_associates
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Admin only access to breach incidents" ON hipaa_breach_incidents
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Admin only access to user permissions" ON hipaa_user_permissions
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Admin only access to training records" ON hipaa_training_records
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_hipaa_business_associates_updated_at BEFORE UPDATE ON hipaa_business_associates FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_hipaa_breach_incidents_updated_at BEFORE UPDATE ON hipaa_breach_incidents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_hipaa_user_permissions_updated_at BEFORE UPDATE ON hipaa_user_permissions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_hipaa_training_records_updated_at BEFORE UPDATE ON hipaa_training_records FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a view for compliance reporting
CREATE OR REPLACE VIEW hipaa_compliance_summary AS
SELECT 
    'audit_logs' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE phi_involved = true) as phi_access_events,
    COUNT(*) FILTER (WHERE outcome = 'FAILURE') as failed_events,
    MAX(timestamp) as last_event
FROM hipaa_audit_logs
UNION ALL
SELECT 
    'data_retention' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE status = 'scheduled') as scheduled_deletions,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_deletions,
    MAX(created_at) as last_event
FROM hipaa_data_retention
UNION ALL
SELECT 
    'breach_incidents' as table_name,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE severity IN ('high', 'critical')) as high_severity_incidents,
    COUNT(*) FILTER (WHERE status != 'resolved') as open_incidents,
    MAX(incident_date) as last_event
FROM hipaa_breach_incidents;