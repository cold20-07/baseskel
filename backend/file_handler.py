"""
HIPAA-Compliant File Upload Handler for Dr. Kishan Bhalani Medical Documentation Services

This module handles secure file uploads, storage, and management with HIPAA compliance.
"""

import os
import uuid
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import secrets
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
    magic = None
from PIL import Image
import io
import logging

from fastapi import UploadFile, HTTPException, Request
from pydantic import BaseModel
from supabase import Client

from hipaa_compliance import (
    HIPAAAuditLogger, HIPAAValidator, encryption, 
    AuditEventType, AuditLog
)

# Configure logging
logger = logging.getLogger(__name__)

# File upload configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'},
    'documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf'},
    'medical': {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.dcm'},  # DICOM for medical images
    'archives': {'.zip', '.rar', '.7z'}
}

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)

# PHI-sensitive file types
PHI_SENSITIVE_CATEGORIES = {'medical_record', 'service_record'}


class FileUploadResponse(BaseModel):
    id: str
    original_filename: str
    file_size: int
    mime_type: str
    file_category: str
    upload_status: str
    is_phi: bool
    created_at: str


class FileMetadata(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    pages: Optional[int] = None
    author: Optional[str] = None
    title: Optional[str] = None


class HIPAAFileHandler:
    """HIPAA-compliant file upload and management handler"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.audit_logger = HIPAAAuditLogger(supabase_client)
        self.validator = HIPAAValidator()
        
        # Create upload directories
        for category in ['medical_record', 'service_record', 'photo', 'document', 'other']:
            (UPLOAD_DIRECTORY / category).mkdir(exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> Dict[str, Any]:
        """Validate uploaded file for security and compliance"""
        
        # Check file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        allowed_exts = set()
        for category_exts in ALLOWED_EXTENSIONS.values():
            allowed_exts.update(category_exts)
        
        if file_ext not in allowed_exts:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed"
            )
        
        # Detect MIME type
        file_content = file.file.read(1024)  # Read first 1KB for MIME detection
        file.file.seek(0)  # Reset file pointer
        
        if HAS_MAGIC and magic:
            try:
                detected_mime = magic.from_buffer(file_content, mime=True)
            except:
                detected_mime = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        else:
            detected_mime = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
        
        # Validate MIME type matches extension
        expected_mimes = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        
        if file_ext in expected_mimes and not detected_mime.startswith(expected_mimes[file_ext].split('/')[0]):
            raise HTTPException(
                status_code=400,
                detail="File content doesn't match file extension"
            )
        
        return {
            'extension': file_ext,
            'mime_type': detected_mime,
            'size': file.size
        }
    
    def categorize_file(self, filename: str, mime_type: str) -> str:
        """Automatically categorize file based on name and type"""
        filename_lower = filename.lower()
        
        # Medical records keywords
        medical_keywords = ['medical', 'record', 'diagnosis', 'treatment', 'prescription', 'lab', 'xray', 'mri', 'ct']
        if any(keyword in filename_lower for keyword in medical_keywords):
            return 'medical_record'
        
        # Service records keywords
        service_keywords = ['service', 'military', 'dd214', 'discharge', 'veteran']
        if any(keyword in filename_lower for keyword in service_keywords):
            return 'service_record'
        
        # Image files
        if mime_type.startswith('image/'):
            return 'photo'
        
        # Document files
        if mime_type in ['application/pdf', 'application/msword', 'text/plain']:
            return 'document'
        
        return 'other'
    
    def extract_metadata(self, file_path: Path, mime_type: str) -> FileMetadata:
        """Extract metadata from uploaded file"""
        metadata = FileMetadata()
        
        try:
            if mime_type.startswith('image/'):
                with Image.open(file_path) as img:
                    metadata.width = img.width
                    metadata.height = img.height
                    
                    # Extract EXIF data if available
                    if hasattr(img, '_getexif') and img._getexif():
                        exif = img._getexif()
                        if exif and 270 in exif:  # Image description
                            metadata.title = exif[270]
            
            # For PDFs, could extract page count, author, etc.
            # This would require additional libraries like PyPDF2
            
        except Exception as e:
            logger.warning(f"Failed to extract metadata from {file_path}: {e}")
        
        return metadata
    
    def generate_secure_filename(self, original_filename: str, file_category: str) -> str:
        """Generate secure filename for storage"""
        file_ext = Path(original_filename).suffix.lower()
        secure_name = f"{uuid.uuid4().hex}{file_ext}"
        return f"{file_category}/{secure_name}"
    
    async def upload_file(
        self, 
        file: UploadFile, 
        request: Request,
        contact_id: Optional[str] = None,
        file_category: Optional[str] = None,
        upload_source: str = 'direct_upload'
    ) -> FileUploadResponse:
        """Upload and store file with HIPAA compliance"""
        
        try:
            # Validate file
            validation_result = self.validate_file(file)
            
            # Auto-categorize if not provided
            if not file_category:
                file_category = self.categorize_file(file.filename, validation_result['mime_type'])
            
            # Check if file contains PHI
            is_phi = file_category in PHI_SENSITIVE_CATEGORIES
            
            # Generate secure filename and path
            stored_filename = self.generate_secure_filename(file.filename, file_category)
            file_path = UPLOAD_DIRECTORY / stored_filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save file to disk
            content = await file.read()
            
            # Encrypt file if it contains PHI
            if is_phi:
                encrypted_content = encryption.encrypt_phi(content.decode('latin1') if isinstance(content, bytes) else content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(encrypted_content)
            else:
                with open(file_path, 'wb') as f:
                    f.write(content)
            
            # Extract metadata
            metadata = self.extract_metadata(file_path, validation_result['mime_type'])
            
            # Create database record
            file_record = {
                'id': str(uuid.uuid4()),
                'original_filename': file.filename,
                'stored_filename': stored_filename,
                'file_path': str(file_path),
                'file_size': len(content),
                'mime_type': validation_result['mime_type'],
                'file_category': file_category,
                'upload_source': upload_source,
                'contact_id': contact_id,
                'is_phi': is_phi,
                'uploaded_by_ip': request.client.host,
                'uploaded_by_user_agent': request.headers.get('user-agent', ''),
                'upload_status': 'uploaded',
                'metadata': metadata.model_dump(),
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            # Insert into database
            response = self.supabase.table('file_uploads').insert(file_record).execute()
            
            # Log file upload for HIPAA compliance
            audit_log = AuditLog(
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=AuditEventType.PHI_CREATE if is_phi else AuditEventType.SYSTEM_ACCESS,
                ip_address=request.client.host,
                user_agent=request.headers.get('user-agent', ''),
                resource_type='file_upload',
                resource_id=file_record['id'],
                action=f'Uploaded file: {file.filename}',
                outcome='SUCCESS',
                phi_involved=is_phi,
                details={
                    'file_category': file_category,
                    'file_size': len(content),
                    'mime_type': validation_result['mime_type']
                }
            )
            self.audit_logger.log_event(audit_log)
            
            return FileUploadResponse(
                id=file_record['id'],
                original_filename=file.filename,
                file_size=len(content),
                mime_type=validation_result['mime_type'],
                file_category=file_category,
                upload_status='uploaded',
                is_phi=is_phi,
                created_at=file_record['created_at']
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            
            # Log failed upload
            audit_log = AuditLog(
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=AuditEventType.SYSTEM_ACCESS,
                ip_address=request.client.host,
                user_agent=request.headers.get('user-agent', ''),
                resource_type='file_upload',
                action=f'Failed to upload file: {file.filename}',
                outcome='FAILURE',
                phi_involved=False,
                details={'error': str(e)}
            )
            self.audit_logger.log_event(audit_log)
            
            raise HTTPException(status_code=500, detail="File upload failed")
    
    async def get_file(self, file_id: str, request: Request) -> Dict[str, Any]:
        """Retrieve file information"""
        try:
            response = self.supabase.table('file_uploads').select('*').eq('id', file_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="File not found")
            
            file_record = response.data[0]
            
            # Log file access
            self.supabase.rpc('log_file_access', {
                'p_file_id': file_id,
                'p_access_type': 'view',
                'p_user_ip': request.client.host,
                'p_user_agent': request.headers.get('user-agent', '')
            }).execute()
            
            return file_record
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve file {file_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve file")
    
    async def download_file(self, file_id: str, request: Request) -> tuple[bytes, str, str]:
        """Download file content"""
        try:
            file_record = await self.get_file(file_id, request)
            file_path = Path(file_record['file_path'])
            
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found on disk")
            
            # Read file content
            if file_record['is_phi']:
                # Decrypt PHI file
                with open(file_path, 'r', encoding='utf-8') as f:
                    encrypted_content = f.read()
                content = encryption.decrypt_phi(encrypted_content).encode('latin1')
            else:
                with open(file_path, 'rb') as f:
                    content = f.read()
            
            # Log download
            self.supabase.rpc('log_file_access', {
                'p_file_id': file_id,
                'p_access_type': 'download',
                'p_user_ip': request.client.host,
                'p_user_agent': request.headers.get('user-agent', '')
            }).execute()
            
            return content, file_record['original_filename'], file_record['mime_type']
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to download file {file_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to download file")
    
    async def delete_file(self, file_id: str, request: Request) -> bool:
        """Securely delete file"""
        try:
            file_record = await self.get_file(file_id, request)
            file_path = Path(file_record['file_path'])
            
            # Mark as deleted in database
            self.supabase.table('file_uploads').update({
                'upload_status': 'deleted',
                'deleted_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', file_id).execute()
            
            # Securely delete file from disk
            if file_path.exists():
                # Overwrite file with random data for secure deletion
                file_size = file_path.stat().st_size
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(file_size))
                file_path.unlink()
            
            # Log deletion
            audit_log = AuditLog(
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=AuditEventType.PHI_DELETE if file_record['is_phi'] else AuditEventType.SYSTEM_ACCESS,
                ip_address=request.client.host,
                user_agent=request.headers.get('user-agent', ''),
                resource_type='file_upload',
                resource_id=file_id,
                action=f'Deleted file: {file_record["original_filename"]}',
                outcome='SUCCESS',
                phi_involved=file_record['is_phi']
            )
            self.audit_logger.log_event(audit_log)
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete file {file_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete file")
    
    async def list_files(
        self, 
        contact_id: Optional[str] = None,
        file_category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List uploaded files with filters"""
        try:
            query = self.supabase.table('file_uploads').select('*')
            
            if contact_id:
                query = query.eq('contact_id', contact_id)
            
            if file_category:
                query = query.eq('file_category', file_category)
            
            query = query.neq('upload_status', 'deleted')
            query = query.order('created_at', desc=True).limit(limit)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise HTTPException(status_code=500, detail="Failed to list files")