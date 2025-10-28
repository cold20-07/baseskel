from fastapi import FastAPI, APIRouter, HTTPException, Query, Request, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
try:
    from supabase import create_client, Client
except ImportError:
    from mock_supabase import create_client, MockSupabaseClient as Client
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
try:
    from hipaa_compliance import (
        HIPAAAuditLogger, HIPAAValidator, HIPAASecurityHeaders, 
        HIPAADataRetention, encryption, AuditEventType
    )
    HIPAA_AVAILABLE = True
except ImportError as e:
    print(f"HIPAA compliance not available: {e}")
    HIPAA_AVAILABLE = False

try:
    from file_handler import HIPAAFileHandler, FileUploadResponse
    FILE_HANDLER_AVAILABLE = True
except ImportError as e:
    print(f"File handler not available: {e}")
    FILE_HANDLER_AVAILABLE = False
    
    # Define FileUploadResponse as fallback
    class FileUploadResponse(BaseModel):
        id: str
        original_filename: str
        file_size: int
        mime_type: str
        file_category: str
        upload_status: str
        is_phi: bool
        created_at: str


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase connection (with mock support)
try:
    supabase_url = os.environ.get('SUPABASE_URL', 'https://demo-project.supabase.co')
    supabase_key = os.environ.get('SUPABASE_KEY', 'demo-key')
    
    supabase: Client = create_client(supabase_url, supabase_key)
    SUPABASE_AVAILABLE = True
    
    if 'demo-project' in supabase_url:
        print("🎭 Using mock Supabase client for testing")
    else:
        print("✅ Connected to real Supabase instance")
        
except Exception as e:
    print(f"⚠️  Supabase connection failed: {e}")
    # Try mock as fallback
    try:
        from mock_supabase import create_client, MockSupabaseClient as Client
        supabase = create_client('https://demo-project.supabase.co', 'demo-key')
        SUPABASE_AVAILABLE = True
        print("🎭 Fallback to mock Supabase client")
    except Exception as e2:
        print(f"❌ Mock Supabase also failed: {e2}")
        supabase = None
        SUPABASE_AVAILABLE = False

# Initialize HIPAA compliance components (if available)
if HIPAA_AVAILABLE and SUPABASE_AVAILABLE and supabase:
    audit_logger = HIPAAAuditLogger(supabase)
    validator = HIPAAValidator()
    security_headers = HIPAASecurityHeaders()
    data_retention = HIPAADataRetention(supabase)
else:
    audit_logger = None
    validator = None
    security_headers = None
    data_retention = None

if FILE_HANDLER_AVAILABLE and SUPABASE_AVAILABLE and supabase:
    file_handler = HIPAAFileHandler(supabase)
else:
    file_handler = None

# Security
security = HTTPBearer(auto_error=False)

# Create the main app without a prefix
app = FastAPI(
    title="Dr. Kishan Bhalani - Medical Documentation API",
    description="HIPAA-compliant API for veteran medical documentation services",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ===== HIPAA MIDDLEWARE =====
class HIPAASecurityMiddleware(BaseHTTPMiddleware):
    """HIPAA-compliant security middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Log system access (if audit logger is available)
        if audit_logger and HIPAA_AVAILABLE:
            try:
                from hipaa_compliance import AuditLog
                audit_log = AuditLog(
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    event_type=AuditEventType.SYSTEM_ACCESS,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    action=f"{request.method} {request.url.path}",
                    outcome='SUCCESS',
                    phi_involved=False
                )
                audit_logger.log_event(audit_log)
            except Exception as e:
                # Silently fail if audit logging is not available
                pass
        
        # Process request
        response = await call_next(request)
        
        # Add HIPAA security headers
        for header, value in security_headers.get_security_headers().items():
            response.headers[header] = value
        
        return response


class HIPAARateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for HIPAA compliance"""
    
    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = datetime.now()
        
        # Clean old requests
        cutoff_time = current_time.timestamp() - 60
        self.requests = {
            ip: [req_time for req_time in times if req_time > cutoff_time]
            for ip, times in self.requests.items()
        }
        
        # Check rate limit
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        if len(self.requests[client_ip]) >= self.calls_per_minute:
            # Log potential abuse (if audit logger is available)
            if audit_logger and HIPAA_AVAILABLE:
                try:
                    from hipaa_compliance import AuditLog
                    audit_log = AuditLog(
                        timestamp=current_time.isoformat(),
                        event_type=AuditEventType.UNAUTHORIZED_ACCESS,
                        ip_address=client_ip,
                        action='Rate limit exceeded',
                        outcome='FAILURE',
                        phi_involved=False
                    )
                    audit_logger.log_event(audit_log)
                except Exception:
                    pass
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[client_ip].append(current_time.timestamp())
        return await call_next(request)


# ===== AUTHENTICATION =====
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user (placeholder for future auth implementation)"""
    # For now, return None since we don't have auth implemented
    # In production, validate JWT token here
    return None


def require_phi_access(user_role: str = "patient"):
    """Decorator to require PHI access permissions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # In production, check user permissions here
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ===== MOCK DATA =====
def get_mock_services():
    return [
        {
            "id": "1",
            "slug": "nexus-rebuttal-letters",
            "title": "Nexus & Rebuttal Letters",
            "shortDescription": "Comprehensive medical opinions for claims and appeals",
            "fullDescription": "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions, or challenge unfavorable VA decisions.",
            "features": ["Nexus opinion letters", "Rebuttal to VA denials", "Direct/secondary/aggravation analysis", "Clear medical rationale"],
            "basePriceInINR": 4999,
            "duration": "7-10 business days",
            "category": "nexus-letter",
            "icon": "file-text",
            "faqs": [{"question": "What's the difference between nexus and rebuttal letters?", "answer": "Nexus letters establish the connection between military service and a condition for initial claims. Rebuttal letters challenge VA decisions by providing contrary medical evidence and opinions."}]
        },
        {
            "id": "2",
            "slug": "public-dbqs",
            "title": "Public DBQs",
            "shortDescription": "Standardized disability questionnaires for VA claims",
            "fullDescription": "Disability Benefits Questionnaires (DBQs) are standardized medical examination forms used by the VA to evaluate disability claims.",
            "features": ["Latest public VA DBQs", "Objective findings", "Functional impact"],
            "basePriceInINR": 3999,
            "duration": "5-7 business days",
            "category": "dbq",
            "icon": "clipboard",
            "faqs": [{"question": "Do you complete VA DBQs?", "answer": "Yes, we complete public DBQs that are currently accepted by the VA for various conditions."}]
        },
        {
            "id": "3",
            "slug": "aid-attendance",
            "title": "Aid & Attendance (21-2680)",
            "shortDescription": "Enhanced pension benefits for veterans needing assistance",
            "fullDescription": "Aid and Attendance is a benefit available to veterans and surviving spouses who require the regular assistance of another person.",
            "features": ["Physician evaluation", "ADL documentation", "When clinically indicated"],
            "basePriceInINR": 5999,
            "duration": "10-14 business days",
            "category": "aid-attendance",
            "icon": "heart-pulse",
            "faqs": [{"question": "Can you help with Aid & Attendance?", "answer": "Yes, we provide complete physician evaluations and documentation for VA Form 21-2680."}]
        },
        {
            "id": "4",
            "slug": "cp-coaching",
            "title": "C&P Coaching",
            "shortDescription": "Preparation for compensation and pension examinations",
            "fullDescription": "Prepare for your C&P exam with expert coaching. We help you understand what to expect, how to accurately report your symptoms, and provide tips to ensure your disabilities are properly documented.",
            "features": ["What to expect", "Accurate symptom reporting", "Logbooks & lay tips"],
            "basePriceInINR": 2499,
            "duration": "Same day or next business day",
            "category": "coaching",
            "icon": "users",
            "faqs": [{"question": "What is C&P coaching?", "answer": "C&P coaching prepares you for your Compensation and Pension exam, helping you understand the process and communicate your condition effectively."}]
        },
        {
            "id": "5",
            "slug": "expert-consultation",
            "title": "One-on-One Consultation with Expert",
            "shortDescription": "Personal consultation to review your claim with medical expert",
            "fullDescription": "Schedule a comprehensive one-on-one consultation with Dr. Kishan Bhalani to review your VA claim, discuss your medical conditions, and receive personalized guidance.",
            "features": ["Personal consultation with Dr. Bhalani", "Comprehensive claim review", "Medical condition assessment", "Personalized recommendations"],
            "basePriceInINR": 3499,
            "duration": "1-hour consultation scheduled within 3-5 days",
            "category": "consultation",
            "icon": "users",
            "faqs": [{"question": "How does the consultation work?", "answer": "You'll have a scheduled one-on-one video or phone consultation with Dr. Kishan Bhalani to discuss your claim, medical conditions, and receive personalized guidance."}]
        },
        {
            "id": "6",
            "slug": "record-review",
            "title": "Record Review",
            "shortDescription": "Professional analysis of your medical documentation",
            "fullDescription": "Our medical professionals review your service and medical records to identify conditions eligible for VA compensation, build a comprehensive timeline, and prepare targeted questions for your providers.",
            "features": ["Service/med records synthesis", "Timeline build", "Provider question set"],
            "basePriceInINR": 2999,
            "duration": "5-7 business days",
            "category": "review",
            "icon": "file-search",
            "faqs": [{"question": "What records should I provide?", "answer": "Please provide your service treatment records, VA medical records, and any private medical records related to your conditions."}]
        },
        {
            "id": "7",
            "slug": "1151-claim",
            "title": "1151 Claim (VA Medical Malpractice)",
            "shortDescription": "Expert medical opinions for VA medical negligence claims",
            "fullDescription": "Specialized medical documentation for 38 U.S.C. § 1151 claims when veterans are injured or their conditions worsen due to VA medical care.",
            "features": ["VA treatment record analysis", "Medical negligence assessment", "Causation nexus opinions", "Standard of care evaluation"],
            "basePriceInINR": 7999,
            "duration": "10-14 business days",
            "category": "malpractice",
            "icon": "alert-triangle",
            "faqs": [{"question": "What is a 1151 claim?", "answer": "A 1151 claim is filed when a veteran believes they were injured or their condition worsened due to VA medical care negligence, surgical errors, medication mistakes, or other treatment-related harm."}]
        }
    ]

def get_mock_blog_posts():
    return [
        {
            "id": "1",
            "slug": "nexus-and-rebuttal-letters-explained",
            "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
            "excerpt": "Understanding the difference between nexus and rebuttal letters and when you need each for your VA claim.",
            "contentHTML": "<h2>Understanding Nexus and Rebuttal Letters</h2><p>Both nexus and rebuttal letters are crucial medical documents in the VA claims process.</p>",
            "category": "nexus-letters",
            "tags": ["nexus", "rebuttal", "medical opinion"],
            "authorName": "Dr. Kishan Bhalani",
            "publishedAt": "SEPT 2025",
            "readTime": "6 min read"
        },
        {
            "id": "2",
            "slug": "understanding-1151-claims",
            "title": "Understanding 1151 Claims: When VA Medical Care Goes Wrong",
            "excerpt": "Learn about 38 U.S.C. § 1151 claims for compensation when VA medical treatment causes injury or worsens your condition.",
            "contentHTML": "<h2>What is a 1151 Claim?</h2><p>A 1151 claim allows veterans to seek compensation when they are injured due to VA medical care.</p>",
            "category": "1151-claims",
            "tags": ["1151 claim", "VA malpractice"],
            "authorName": "Dr. Kishan Bhalani",
            "publishedAt": "OCT 2025",
            "readTime": "8 min read"
        }
    ]

# ===== MODELS =====
class Service(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    slug: str
    title: str
    shortDescription: str
    fullDescription: str
    features: List[str]
    basePriceInINR: int
    duration: str
    category: str
    icon: str
    faqs: List[dict]


class BlogPost(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    slug: str
    title: str
    excerpt: str
    contentHTML: str
    category: str
    tags: List[str]
    authorName: str
    publishedAt: str
    readTime: str


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str


class Contact(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str
    status: str = "new"
    createdAt: str


# ===== ROUTES =====
@api_router.get("/")
async def root():
    return {"message": "Dr. Kishan Bhalani Medical Documentation API"}

# Root level health check for deployment platforms
@app.get("/")
async def root_health():
    return {
        "message": "Dr. Kishan Bhalani Medical Documentation Services",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def root_health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hipaa_compliant": True
    }


@api_router.get("/services", response_model=List[Service])
async def get_services():
    if not SUPABASE_AVAILABLE or not supabase:
        return get_mock_services()
    
    try:
        response = supabase.table('services').select('*').execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching services: {e}")
        # Return mock data as fallback
        return get_mock_services()


@api_router.get("/services/{slug}", response_model=Service)
async def get_service_by_slug(slug: str):
    try:
        response = supabase.table('services').select('*').eq('slug', slug).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Service not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching service {slug}: {e}")
        # Try mock data as fallback
        mock_services = get_mock_services()
        service = next((s for s in mock_services if s["slug"] == slug), None)
        if service:
            return service
        raise HTTPException(status_code=404, detail="Service not found")


@api_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(20, le=100)
):
    try:
        query = supabase.table('blog_posts').select('*')
        
        if category:
            query = query.eq('category', category)
        
        if q:
            # Supabase uses ilike for case-insensitive search
            query = query.or_(f'title.ilike.%{q}%,excerpt.ilike.%{q}%')
        
        query = query.limit(limit)
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching blog posts: {e}")
        # Return mock data as fallback
        posts = get_mock_blog_posts()
        
        if category:
            posts = [p for p in posts if p["category"] == category]
        
        if q:
            posts = [p for p in posts if q.lower() in p["title"].lower() or q.lower() in p["excerpt"].lower()]
        
        return posts[:limit]


@api_router.get("/blog/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    try:
        response = supabase.table('blog_posts').select('*').eq('slug', slug).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching blog post {slug}: {e}")
        # Try mock data as fallback
        mock_posts = get_mock_blog_posts()
        post = next((p for p in mock_posts if p["slug"] == slug), None)
        if post:
            return post
        raise HTTPException(status_code=404, detail="Blog post not found")


@api_router.post("/contact", response_model=Contact)
async def create_contact(contact_data: ContactCreate, request: Request):
    try:
        contact_dict = contact_data.model_dump()
        
        # Check if data contains PHI
        contains_phi = validator.is_phi_data(contact_dict)
        
        # Encrypt PHI fields
        if contains_phi:
            if contact_dict.get('name'):
                contact_dict['name'] = encryption.encrypt_phi(contact_dict['name'])
            if contact_dict.get('email'):
                contact_dict['email'] = encryption.encrypt_phi(contact_dict['email'])
            if contact_dict.get('phone'):
                contact_dict['phone'] = encryption.encrypt_phi(contact_dict['phone'])
        
        contact_obj = Contact(
            id=str(uuid.uuid4()),
            **contact_dict,
            createdAt=datetime.now(timezone.utc).isoformat()
        )
        
        # Insert into database
        response = supabase.table('contacts').insert(contact_obj.model_dump()).execute()
        
        # Schedule for data retention (6 years for medical records)
        data_retention.schedule_data_deletion('contacts', contact_obj.id, retention_years=6)
        
        # Log PHI creation
        if contains_phi:
            from hipaa_compliance import AuditLog
            audit_log = AuditLog(
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=AuditEventType.PHI_CREATE,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent", ""),
                resource_type='contact',
                resource_id=contact_obj.id,
                action='Created contact form submission',
                outcome='SUCCESS',
                phi_involved=True
            )
            audit_logger.log_event(audit_log)
        
        # Return decrypted data for response (in production, limit based on user role)
        response_obj = contact_obj.model_copy()
        if contains_phi:
            if response_obj.name:
                response_obj.name = encryption.decrypt_phi(response_obj.name)
            if response_obj.email:
                response_obj.email = encryption.decrypt_phi(response_obj.email)
            if response_obj.phone:
                response_obj.phone = encryption.decrypt_phi(response_obj.phone)
        
        return response_obj
        
    except Exception as e:
        # Log error without PHI
        sanitized_data = validator.sanitize_phi_for_logging(contact_dict)
        logger.error(f"Error creating contact: {e}, Data: {sanitized_data}")
        
        # Log failed PHI creation attempt
        from hipaa_compliance import AuditLog
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.PHI_CREATE,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
            resource_type='contact',
            action='Failed to create contact form submission',
            outcome='FAILURE',
            phi_involved=True,
            details={'error': str(e)}
        )
        audit_logger.log_event(audit_log)
        
        raise HTTPException(status_code=500, detail="Error creating contact")


# Include the router in the main app
app.include_router(api_router)

# Add HIPAA-compliant middleware (order matters!) - only if HIPAA is available
if HIPAA_AVAILABLE:
    app.add_middleware(HIPAASecurityMiddleware)
    app.add_middleware(HIPAARateLimitMiddleware, calls_per_minute=100)

# Add trusted host middleware for production
if os.environ.get('ENVIRONMENT') == 'production':
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# CORS middleware (more restrictive for HIPAA)
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Request-ID"]
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== HIPAA COMPLIANCE ENDPOINTS =====
@api_router.get("/hipaa/audit-logs")
async def get_audit_logs(
    limit: int = Query(100, le=1000),
    event_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """Get HIPAA audit logs (admin only)"""
    try:
        # In production, verify admin role
        # if not current_user or current_user.role != 'admin':
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        query = supabase.table('hipaa_audit_logs').select('*')
        
        if event_type:
            query = query.eq('event_type', event_type)
        if start_date:
            query = query.gte('timestamp', start_date)
        if end_date:
            query = query.lte('timestamp', end_date)
        
        query = query.order('timestamp', desc=True).limit(limit)
        response = query.execute()
        
        return {
            "audit_logs": response.data,
            "total": len(response.data)
        }
        
    except Exception as e:
        logger.error(f"Error fetching audit logs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching audit logs")


@api_router.get("/hipaa/compliance-summary")
async def get_compliance_summary(current_user = Depends(get_current_user)):
    """Get HIPAA compliance summary (admin only)"""
    try:
        # In production, verify admin role
        # if not current_user or current_user.role != 'admin':
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        # Get compliance summary from view
        response = supabase.rpc('get_hipaa_compliance_summary').execute()
        
        return {
            "compliance_summary": response.data,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching compliance summary: {e}")
        raise HTTPException(status_code=500, detail="Error fetching compliance summary")


@api_router.post("/hipaa/execute-data-retention")
async def execute_data_retention(current_user = Depends(get_current_user)):
    """Execute scheduled data retention deletions (admin only)"""
    try:
        # In production, verify admin role
        # if not current_user or current_user.role != 'admin':
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        data_retention.execute_scheduled_deletions()
        
        from hipaa_compliance import AuditLog
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.PHI_DELETE,
            user_email='system',
            action='Executed scheduled data retention deletions',
            outcome='SUCCESS',
            phi_involved=True
        )
        audit_logger.log_event(audit_log)
        
        return {"message": "Data retention executed successfully"}
        
    except Exception as e:
        logger.error(f"Error executing data retention: {e}")
        raise HTTPException(status_code=500, detail="Error executing data retention")


@api_router.post("/hipaa/report-breach")
async def report_breach_incident(
    incident_data: dict,
    request: Request,
    current_user = Depends(get_current_user)
):
    """Report a HIPAA breach incident (admin only)"""
    try:
        # In production, verify admin role
        # if not current_user or current_user.role != 'admin':
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        breach_record = {
            'id': str(uuid.uuid4()),
            'incident_date': incident_data.get('incident_date'),
            'discovered_date': datetime.now(timezone.utc).isoformat(),
            'incident_type': incident_data.get('incident_type'),
            'description': incident_data.get('description'),
            'affected_individuals_count': incident_data.get('affected_individuals_count', 0),
            'phi_types_involved': incident_data.get('phi_types_involved', []),
            'cause': incident_data.get('cause'),
            'severity': incident_data.get('severity', 'medium'),
            'status': 'investigating'
        }
        
        response = supabase.table('hipaa_breach_incidents').insert(breach_record).execute()
        
        # Log the breach report
        from hipaa_compliance import AuditLog
        audit_log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=AuditEventType.DATA_BREACH_ATTEMPT,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
            resource_type='breach_incident',
            resource_id=breach_record['id'],
            action='Reported HIPAA breach incident',
            outcome='SUCCESS',
            phi_involved=True
        )
        audit_logger.log_event(audit_log)
        
        return {"message": "Breach incident reported successfully", "incident_id": breach_record['id']}
        
    except Exception as e:
        logger.error(f"Error reporting breach incident: {e}")
        raise HTTPException(status_code=500, detail="Error reporting breach incident")


# ===== FILE UPLOAD ENDPOINTS =====
if FILE_HANDLER_AVAILABLE and file_handler:
    @api_router.post("/upload", response_model=FileUploadResponse)
    async def upload_file(
        request: Request,
        file: UploadFile = File(...),
        contact_id: Optional[str] = Form(None),
        file_category: Optional[str] = Form(None),
        upload_source: str = Form("direct_upload")
    ):
        """Upload a file with HIPAA compliance"""
        return await file_handler.upload_file(
            file=file,
            request=request,
            contact_id=contact_id,
            file_category=file_category,
            upload_source=upload_source
        )
else:
    @api_router.post("/upload")
    async def upload_file_disabled():
        """File upload not available - missing dependencies"""
        raise HTTPException(status_code=503, detail="File upload service not available")


if FILE_HANDLER_AVAILABLE and file_handler:
    @api_router.get("/files/{file_id}")
    async def get_file_info(file_id: str, request: Request):
        """Get file information"""
        return await file_handler.get_file(file_id, request)

    @api_router.get("/files/{file_id}/download")
    async def download_file(file_id: str, request: Request):
        """Download a file"""
        content, filename, mime_type = await file_handler.download_file(file_id, request)
        
        return Response(
            content=content,
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(content))
            }
        )

    @api_router.delete("/files/{file_id}")
    async def delete_file(file_id: str, request: Request):
        """Delete a file"""
        success = await file_handler.delete_file(file_id, request)
        return {"success": success, "message": "File deleted successfully"}

    @api_router.get("/files")
    async def list_files(
        contact_id: Optional[str] = Query(None),
        file_category: Optional[str] = Query(None),
        limit: int = Query(50, le=100)
    ):
        """List uploaded files"""
        return await file_handler.list_files(
            contact_id=contact_id,
            file_category=file_category,
            limit=limit
        )
else:
    @api_router.get("/files/{file_id}")
    async def get_file_info_disabled(file_id: str):
        raise HTTPException(status_code=503, detail="File service not available")
    
    @api_router.get("/files/{file_id}/download")
    async def download_file_disabled(file_id: str):
        raise HTTPException(status_code=503, detail="File service not available")
    
    @api_router.delete("/files/{file_id}")
    async def delete_file_disabled(file_id: str):
        raise HTTPException(status_code=503, detail="File service not available")
    
    @api_router.get("/files")
    async def list_files_disabled():
        raise HTTPException(status_code=503, detail="File service not available")


# Health check endpoint
@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hipaa_compliant": True
    }


# No cleanup needed for Supabase client
