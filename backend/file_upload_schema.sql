-- File Upload Schema for Dr. Kishan Bhalani Medical Documentation Services
-- Run this in your Supabase SQL editor after the main schemas

-- File Uploads Table
CREATE TABLE IF NOT EXISTS file_uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type TEXT NOT NULL,
    file_category TEXT NOT NULL CHECK (file_category IN ('medical_record', 'service_record', 'photo', 'document', 'other')),
    upload_source TEXT NOT NULL CHECK (upload_source IN ('contact_form', 'service_request', 'direct_upload')),
    contact_id TEXT, -- Reference to contacts table
    service_request_id TEXT, -- For future service requests
    is_phi BOOLEAN DEFAULT FALSE,
    encryption_key_id TEXT, -- For encrypted files
    upload_status TEXT NOT NULL DEFAULT 'uploaded' CHECK (upload_status IN ('uploading', 'uploaded', 'processed', 'error', 'deleted')),
    uploaded_by_ip INET,
    uploaded_by_user_agent TEXT,
    virus_scan_status TEXT DEFAULT 'pending' CHECK (virus_scan_status IN ('pending', 'clean', 'infected', 'error')),
    virus_scan_result JSONB,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- File Access Log Table (for HIPAA compliance)
CREATE TABLE IF NOT EXISTS file_access_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID NOT NULL REFERENCES file_uploads(id) ON DELETE CASCADE,
    access_type TEXT NOT NULL CHECK (access_type IN ('view', 'download', 'delete', 'share')),
    accessed_by_ip INET,
    accessed_by_user_agent TEXT,
    user_id TEXT, -- For authenticated users
    user_email TEXT,
    access_granted BOOLEAN DEFAULT TRUE,
    access_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- File Sharing Table (for secure file sharing)
CREATE TABLE IF NOT EXISTS file_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID NOT NULL REFERENCES file_uploads(id) ON DELETE CASCADE,
    share_token TEXT UNIQUE NOT NULL,
    share_type TEXT NOT NULL CHECK (share_type IN ('public', 'password_protected', 'time_limited')),
    password_hash TEXT, -- For password-protected shares
    expires_at TIMESTAMP WITH TIME ZONE,
    max_downloads INTEGER DEFAULT 1,
    download_count INTEGER DEFAULT 0,
    created_by_ip INET,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_file_uploads_contact_id ON file_uploads(contact_id);
CREATE INDEX IF NOT EXISTS idx_file_uploads_category ON file_uploads(file_category);
CREATE INDEX IF NOT EXISTS idx_file_uploads_status ON file_uploads(upload_status);
CREATE INDEX IF NOT EXISTS idx_file_uploads_created_at ON file_uploads(created_at);
CREATE INDEX IF NOT EXISTS idx_file_uploads_is_phi ON file_uploads(is_phi);

CREATE INDEX IF NOT EXISTS idx_file_access_logs_file_id ON file_access_logs(file_id);
CREATE INDEX IF NOT EXISTS idx_file_access_logs_created_at ON file_access_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_file_shares_token ON file_shares(share_token);
CREATE INDEX IF NOT EXISTS idx_file_shares_file_id ON file_shares(file_id);
CREATE INDEX IF NOT EXISTS idx_file_shares_expires_at ON file_shares(expires_at);

-- Enable Row Level Security
ALTER TABLE file_uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_access_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_shares ENABLE ROW LEVEL SECURITY;

-- Create policies for file access
CREATE POLICY "Allow public upload of files" ON file_uploads
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow admin access to all files" ON file_uploads
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Allow admin access to file logs" ON file_access_logs
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

CREATE POLICY "Allow admin access to file shares" ON file_shares
    FOR ALL USING (auth.jwt() ->> 'role' = 'admin');

-- Function to update updated_at timestamp
CREATE TRIGGER update_file_uploads_updated_at BEFORE UPDATE ON file_uploads FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_file_shares_updated_at BEFORE UPDATE ON file_shares FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean up expired shares
CREATE OR REPLACE FUNCTION cleanup_expired_shares()
RETURNS void AS $$
BEGIN
    UPDATE file_shares 
    SET is_active = FALSE 
    WHERE expires_at < NOW() AND is_active = TRUE;
END;
$$ LANGUAGE plpgsql;

-- Function to log file access
CREATE OR REPLACE FUNCTION log_file_access(
    p_file_id UUID,
    p_access_type TEXT,
    p_user_ip INET DEFAULT NULL,
    p_user_agent TEXT DEFAULT NULL,
    p_user_email TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    log_id UUID;
BEGIN
    INSERT INTO file_access_logs (
        file_id, access_type, accessed_by_ip, 
        accessed_by_user_agent, user_email
    ) VALUES (
        p_file_id, p_access_type, p_user_ip, 
        p_user_agent, p_user_email
    ) RETURNING id INTO log_id;
    
    RETURN log_id;
END;
$$ LANGUAGE plpgsql;