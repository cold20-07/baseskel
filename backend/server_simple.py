"""
Simplified FastAPI server for Dr. Kishan Bhalani Medical Documentation Services
This version works without external database connections for testing
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main app
app = FastAPI(
    title="Dr. Kishan Bhalani - Medical Documentation API",
    description="HIPAA-compliant API for veteran medical documentation services",
    version="1.0.0"
)



# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = (datetime.now() - start_time).total_seconds()
    
    # Log the request
    if response.status_code >= 400:
        logger.warning(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"({process_time:.3f}s) - Client: {request.client.host}"
        )
    else:
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"({process_time:.3f}s)"
        )
    
    return response

# CORS middleware
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Enums for service functionality
class ServiceStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"

class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Models
class Service(BaseModel):
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

class ServiceOrder(BaseModel):
    id: str
    service_id: str
    service_title: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    order_details: Dict[str, Any]
    status: OrderStatus
    total_amount: int
    created_at: str
    estimated_completion: str
    notes: Optional[str] = None

class ServiceOrderCreate(BaseModel):
    service_id: str
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,15}$')
    order_details: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = Field(None, max_length=1000)

class Appointment(BaseModel):
    id: str
    service_id: str
    service_title: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    appointment_date: str
    appointment_time: str
    duration_minutes: int
    status: AppointmentStatus
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    created_at: str

class AppointmentCreate(BaseModel):
    service_id: str
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,15}$')
    preferred_date: str = Field(..., description="YYYY-MM-DD format")
    preferred_time: str = Field(..., description="HH:MM format")
    notes: Optional[str] = Field(None, max_length=500)

class ServiceAvailability(BaseModel):
    service_id: str
    service_title: str
    status: ServiceStatus
    next_available_date: Optional[str] = None
    estimated_turnaround: str
    current_queue_length: int

class BlogPost(BaseModel):
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
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str
    status: str = "new"
    createdAt: str

# Mock data
MOCK_SERVICES = [
    {
        "id": "1",
        "slug": "nexus-rebuttal-letters",
        "title": "Nexus & Rebuttal Letters",
        "shortDescription": "Comprehensive medical opinions for claims and appeals",
        "fullDescription": "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions, or challenge unfavorable VA decisions. Our expert medical opinions provide the crucial evidence needed for both initial claims and appeals processes.",
        "features": [
            "Nexus opinion letters",
            "Rebuttal to VA denials",
            "Direct/secondary/aggravation analysis",
            "Clear medical rationale"
        ],
        "basePriceInINR": 4999,
        "duration": "7-10 business days",
        "category": "nexus-letter",
        "icon": "file-text",
        "faqs": [
            {
                "question": "What's the difference between nexus and rebuttal letters?",
                "answer": "Nexus letters establish the connection between military service and a condition for initial claims. Rebuttal letters challenge VA decisions by providing contrary medical evidence and opinions."
            },
            {
                "question": "Can you help with both initial claims and appeals?",
                "answer": "Yes, we provide nexus letters for initial claims and rebuttal letters to challenge unfavorable VA decisions in appeals."
            }
        ]
    },
    {
        "id": "2",
        "slug": "public-dbqs",
        "title": "Public DBQs",
        "shortDescription": "Standardized disability questionnaires for VA claims",
        "fullDescription": "Disability Benefits Questionnaires (DBQs) are standardized medical examination forms used by the VA to evaluate disability claims. Our licensed physicians complete these forms based on current VA guidelines and your medical condition.",
        "features": [
            "Latest public VA DBQs",
            "Objective findings",
            "Functional impact"
        ],
        "basePriceInINR": 3999,
        "duration": "5-7 business days",
        "category": "dbq",
        "icon": "clipboard",
        "faqs": [
            {
                "question": "Do you complete VA DBQs?",
                "answer": "Yes, we complete public DBQs that are currently accepted by the VA for various conditions."
            }
        ]
    },
    {
        "id": "3",
        "slug": "aid-attendance",
        "title": "Aid & Attendance (21-2680)",
        "shortDescription": "Enhanced pension benefits for veterans needing assistance",
        "fullDescription": "Aid and Attendance is a benefit available to veterans and surviving spouses who require the regular assistance of another person. We provide comprehensive physician evaluations to support your A&A benefit claim.",
        "features": [
            "Physician evaluation",
            "ADL documentation",
            "When clinically indicated"
        ],
        "basePriceInINR": 5999,
        "duration": "10-14 business days",
        "category": "aid-attendance",
        "icon": "heart-pulse",
        "faqs": [
            {
                "question": "Can you help with Aid & Attendance?",
                "answer": "Yes, we provide complete physician evaluations and documentation for VA Form 21-2680."
            }
        ]
    },
    {
        "id": "4",
        "slug": "cp-coaching",
        "title": "C&P Coaching",
        "shortDescription": "Preparation for compensation and pension examinations",
        "fullDescription": "Prepare for your C&P exam with expert coaching. We help you understand what to expect, how to accurately report your symptoms, and provide tips to ensure your disabilities are properly documented.",
        "features": [
            "What to expect",
            "Accurate symptom reporting",
            "Logbooks & lay tips"
        ],
        "basePriceInINR": 2499,
        "duration": "Same day or next business day",
        "category": "coaching",
        "icon": "users",
        "faqs": [
            {
                "question": "What is C&P coaching?",
                "answer": "C&P coaching prepares you for your Compensation and Pension exam, helping you understand the process and communicate your condition effectively."
            }
        ]
    },
    {
        "id": "5",
        "slug": "expert-consultation",
        "title": "One-on-One Consultation with Expert",
        "shortDescription": "Personal consultation to review your claim with medical expert",
        "fullDescription": "Schedule a comprehensive one-on-one consultation with Dr. Kishan Bhalani to review your VA claim, discuss your medical conditions, and receive personalized guidance on strengthening your case. This direct consultation provides expert insights tailored to your specific situation.",
        "features": [
            "Personal consultation with Dr. Bhalani",
            "Comprehensive claim review",
            "Medical condition assessment",
            "Personalized recommendations"
        ],
        "basePriceInINR": 3499,
        "duration": "1-hour consultation scheduled within 3-5 days",
        "category": "consultation",
        "icon": "users",
        "faqs": [
            {
                "question": "How does the consultation work?",
                "answer": "You'll have a scheduled one-on-one video or phone consultation with Dr. Kishan Bhalani to discuss your claim, medical conditions, and receive personalized guidance."
            }
        ]
    },
    {
        "id": "6",
        "slug": "record-review",
        "title": "Record Review",
        "shortDescription": "Professional analysis of your medical documentation",
        "fullDescription": "Our medical professionals review your service and medical records to identify conditions eligible for VA compensation, build a comprehensive timeline, and prepare targeted questions for your providers.",
        "features": [
            "Service/med records synthesis",
            "Timeline build",
            "Provider question set"
        ],
        "basePriceInINR": 2999,
        "duration": "5-7 business days",
        "category": "review",
        "icon": "file-search",
        "faqs": [
            {
                "question": "What records should I provide?",
                "answer": "Please provide your service treatment records, VA medical records, and any private medical records related to your conditions."
            }
        ]
    },
    {
        "id": "7",
        "slug": "1151-claim",
        "title": "1151 Claim (VA Medical Malpractice)",
        "shortDescription": "Expert medical opinions for VA medical negligence claims",
        "fullDescription": "Specialized medical documentation for 38 U.S.C. § 1151 claims when veterans are injured or their conditions worsen due to VA medical care. Our expert analysis helps establish negligence and causation for these complex claims requiring higher burden of proof.",
        "features": [
            "VA treatment record analysis",
            "Medical negligence assessment",
            "Causation nexus opinions",
            "Standard of care evaluation"
        ],
        "basePriceInINR": 7999,
        "duration": "10-14 business days",
        "category": "malpractice",
        "icon": "alert-triangle",
        "faqs": [
            {
                "question": "What is a 1151 claim?",
                "answer": "A 1151 claim is filed when a veteran believes they were injured or their condition worsened due to VA medical care negligence, surgical errors, medication mistakes, or other treatment-related harm."
            },
            {
                "question": "How is this different from a regular VA claim?",
                "answer": "1151 claims require proving VA negligence and deviation from medical standards, not just service connection. They have a higher burden of proof but can provide compensation even for non-service-connected conditions."
            }
        ]
    }
]

MOCK_BLOG_POSTS = [
    {
        "id": "1",
        "slug": "nexus-and-rebuttal-letters-explained",
        "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
        "excerpt": "Understanding the difference between nexus and rebuttal letters and when you need each for your VA claim.",
        "contentHTML": "<h2>Understanding Nexus and Rebuttal Letters</h2><p>Both nexus and rebuttal letters are crucial medical documents in the VA claims process, but they serve different purposes at different stages of your claim.</p><h3>Nexus Letters: Building Your Initial Case</h3><p>A nexus letter establishes the connection between your military service and your current medical condition.</p>",
        "category": "nexus-letters",
        "tags": ["nexus", "rebuttal", "medical opinion", "appeals"],
        "authorName": "Dr. Kishan Bhalani",
        "publishedAt": "SEPT 2025",
        "readTime": "6 min read"
    },
    {
        "id": "2",
        "slug": "understanding-1151-claims",
        "title": "Understanding 1151 Claims: When VA Medical Care Goes Wrong",
        "excerpt": "Learn about 38 U.S.C. § 1151 claims for compensation when VA medical treatment causes injury or worsens your condition.",
        "contentHTML": "<h2>What is a 1151 Claim?</h2><p>A 1151 claim, filed under 38 U.S.C. § 1151, allows veterans to seek compensation when they are injured or their condition is worsened due to VA medical care, treatment, or hospitalization.</p>",
        "category": "1151-claims",
        "tags": ["1151 claim", "VA malpractice", "medical negligence"],
        "authorName": "Dr. Kishan Bhalani",
        "publishedAt": "OCT 2025",
        "readTime": "8 min read"
    }
]

# In-memory storage for orders and appointments (in production, use a database)
MOCK_ORDERS = []
MOCK_APPOINTMENTS = []

# Custom exception handler for 404 errors (defined after mock data)
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    path = request.url.path
    if "/api/services/" in path:
        service_slug = path.split("/api/services/")[-1]
        available_services = [s["slug"] for s in MOCK_SERVICES]
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Service '{service_slug}' not found",
                "available_services": available_services,
                "suggestion": "Check the available service slugs listed above"
            }
        )
    elif "/api/blog/" in path:
        blog_slug = path.split("/api/blog/")[-1]
        available_blogs = [b["slug"] for b in MOCK_BLOG_POSTS]
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Blog post '{blog_slug}' not found",
                "available_blogs": available_blogs,
                "suggestion": "Check the available blog post slugs listed above"
            }
        )
    else:
        return JSONResponse(
            status_code=404,
            content={"detail": "Resource not found"}
        )

# Service availability data
SERVICE_AVAILABILITY = {
    "nexus-rebuttal-letters": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-05",
        "estimated_turnaround": "7-10 business days",
        "current_queue_length": 3
    },
    "public-dbqs": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-03",
        "estimated_turnaround": "5-7 business days",
        "current_queue_length": 2
    },
    "aid-attendance": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-10",
        "estimated_turnaround": "10-14 business days",
        "current_queue_length": 1
    },
    "cp-coaching": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-10-29",
        "estimated_turnaround": "Same day or next business day",
        "current_queue_length": 0
    },
    "expert-consultation": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-01",
        "estimated_turnaround": "3-5 days",
        "current_queue_length": 4
    },
    "record-review": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-02",
        "estimated_turnaround": "5-7 business days",
        "current_queue_length": 2
    },
    "1151-claim": {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-12",
        "estimated_turnaround": "10-14 business days",
        "current_queue_length": 1
    }
}

# Routes
@api_router.get("/")
async def root():
    return {
        "message": "Dr. Kishan Bhalani Medical Documentation API",
        "version": "1.0.0",
        "endpoints": {
            "services": "/api/services",
            "blog": "/api/blog",
            "contact": "/api/contact",
            "health": "/api/health",
            "resources": "/api/resources"
        }
    }

@api_router.get("/resources")
async def get_available_resources():
    """Get all available services, blog posts, and functionality"""
    return {
        "services": {
            "count": len(MOCK_SERVICES),
            "available": [{"slug": s["slug"], "title": s["title"]} for s in MOCK_SERVICES]
        },
        "blog_posts": {
            "count": len(MOCK_BLOG_POSTS),
            "available": [{"slug": b["slug"], "title": b["title"]} for b in MOCK_BLOG_POSTS]
        },
        "functionality": {
            "service_ordering": {
                "check_availability": "/api/services/{slug}/availability",
                "create_order": "POST /api/services/{slug}/order",
                "view_orders": "/api/services/{slug}/orders",
                "order_details": "/api/orders/{order_id}"
            },
            "appointments": {
                "schedule": "POST /api/services/{slug}/appointment",
                "view_appointments": "/api/services/{slug}/appointments",
                "appointment_details": "/api/appointments/{appointment_id}",
                "supported_services": ["expert-consultation", "cp-coaching"]
            },
            "service_specific": {
                "nexus_templates": "/api/services/nexus-rebuttal-letters/templates",
                "available_dbqs": "/api/services/public-dbqs/available",
                "cp_preparation": "/api/services/cp-coaching/preparation-guide"
            }
        },
        "usage": {
            "service_detail": "/api/services/{slug}",
            "blog_detail": "/api/blog/{slug}"
        }
    }

@api_router.get("/services", response_model=List[Service])
async def get_services():
    return MOCK_SERVICES

@api_router.get("/services/{slug}", response_model=Service)
async def get_service_by_slug(slug: str):
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        logger.warning(f"Service not found: {slug}")
        available_services = [s["slug"] for s in MOCK_SERVICES]
        raise HTTPException(
            status_code=404, 
            detail={
                "message": f"Service '{slug}' not found",
                "available_services": available_services,
                "total_services": len(MOCK_SERVICES)
            }
        )
    logger.info(f"Service accessed: {slug}")
    return service

@api_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(20, le=100)
):
    posts = MOCK_BLOG_POSTS
    
    if category:
        posts = [p for p in posts if p["category"] == category]
    
    if q:
        posts = [p for p in posts if q.lower() in p["title"].lower() or q.lower() in p["excerpt"].lower()]
    
    return posts[:limit]

@api_router.get("/blog/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    post = next((p for p in MOCK_BLOG_POSTS if p["slug"] == slug), None)
    if not post:
        logger.warning(f"Blog post not found: {slug}")
        available_blogs = [b["slug"] for b in MOCK_BLOG_POSTS]
        raise HTTPException(
            status_code=404, 
            detail={
                "message": f"Blog post '{slug}' not found",
                "available_blogs": available_blogs,
                "total_posts": len(MOCK_BLOG_POSTS)
            }
        )
    logger.info(f"Blog post accessed: {slug}")
    return post

@api_router.post("/contact", response_model=Contact)
async def create_contact(contact_data: ContactCreate, request: Request):
    contact_obj = Contact(
        id=str(uuid.uuid4()),
        **contact_data.model_dump(),
        createdAt=datetime.now(timezone.utc).isoformat()
    )
    
    # In a real implementation, this would save to database
    print(f"Contact form submitted: {contact_obj.name} - {contact_obj.subject}")
    
    return contact_obj

# Service functionality endpoints
@api_router.get("/services/{slug}/availability")
async def get_service_availability(slug: str):
    """Get availability information for a specific service"""
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    availability = SERVICE_AVAILABILITY.get(slug, {
        "status": ServiceStatus.AVAILABLE,
        "next_available_date": "2025-11-01",
        "estimated_turnaround": "5-7 business days",
        "current_queue_length": 0
    })
    
    return ServiceAvailability(
        service_id=service["id"],
        service_title=service["title"],
        **availability
    )

@api_router.post("/services/{slug}/order", response_model=ServiceOrder)
async def create_service_order(slug: str, order_data: ServiceOrderCreate):
    """Create a new service order"""
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Calculate estimated completion date
    from datetime import timedelta
    completion_date = datetime.now() + timedelta(days=10)  # Default 10 days
    
    order = ServiceOrder(
        id=str(uuid.uuid4()),
        service_id=service["id"],
        service_title=service["title"],
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        customer_phone=order_data.customer_phone,
        order_details=order_data.order_details,
        status=OrderStatus.PENDING,
        total_amount=service["basePriceInINR"],
        created_at=datetime.now(timezone.utc).isoformat(),
        estimated_completion=completion_date.isoformat(),
        notes=order_data.notes
    )
    
    MOCK_ORDERS.append(order.model_dump())
    logger.info(f"New order created: {order.id} for service {service['title']}")
    
    return order

@api_router.get("/services/{slug}/orders", response_model=List[ServiceOrder])
async def get_service_orders(slug: str, customer_email: Optional[str] = Query(None)):
    """Get orders for a specific service"""
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    orders = [o for o in MOCK_ORDERS if o["service_id"] == service["id"]]
    
    if customer_email:
        orders = [o for o in orders if o["customer_email"] == customer_email]
    
    return [ServiceOrder(**order) for order in orders]

@api_router.get("/orders/{order_id}", response_model=ServiceOrder)
async def get_order_details(order_id: str):
    """Get details of a specific order"""
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return ServiceOrder(**order)

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: OrderStatus):
    """Update order status (admin function)"""
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order["status"] = status
    logger.info(f"Order {order_id} status updated to {status}")
    
    return {"message": "Order status updated successfully", "new_status": status}

# Appointment functionality for consultation services
@api_router.post("/services/{slug}/appointment", response_model=Appointment)
async def schedule_appointment(slug: str, appointment_data: AppointmentCreate):
    """Schedule an appointment for consultation services"""
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if service supports appointments
    consultation_services = ["expert-consultation", "cp-coaching"]
    if slug not in consultation_services:
        raise HTTPException(
            status_code=400, 
            detail=f"Service '{service['title']}' does not support appointment scheduling"
        )
    
    appointment = Appointment(
        id=str(uuid.uuid4()),
        service_id=service["id"],
        service_title=service["title"],
        customer_name=appointment_data.customer_name,
        customer_email=appointment_data.customer_email,
        customer_phone=appointment_data.customer_phone,
        appointment_date=appointment_data.preferred_date,
        appointment_time=appointment_data.preferred_time,
        duration_minutes=60,  # Default 1 hour
        status=AppointmentStatus.SCHEDULED,
        meeting_link=f"https://meet.drkishanbhalani.com/room/{str(uuid.uuid4())[:8]}",
        notes=appointment_data.notes,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    
    MOCK_APPOINTMENTS.append(appointment.model_dump())
    logger.info(f"New appointment scheduled: {appointment.id} for {appointment.appointment_date}")
    
    return appointment

@api_router.get("/services/{slug}/appointments", response_model=List[Appointment])
async def get_service_appointments(slug: str, customer_email: Optional[str] = Query(None)):
    """Get appointments for a specific service"""
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    appointments = [a for a in MOCK_APPOINTMENTS if a["service_id"] == service["id"]]
    
    if customer_email:
        appointments = [a for a in appointments if a["customer_email"] == customer_email]
    
    return [Appointment(**appointment) for appointment in appointments]

@api_router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment_details(appointment_id: str):
    """Get details of a specific appointment"""
    appointment = next((a for a in MOCK_APPOINTMENTS if a["id"] == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return Appointment(**appointment)

@api_router.put("/appointments/{appointment_id}/status")
async def update_appointment_status(appointment_id: str, status: AppointmentStatus):
    """Update appointment status"""
    appointment = next((a for a in MOCK_APPOINTMENTS if a["id"] == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment["status"] = status
    logger.info(f"Appointment {appointment_id} status updated to {status}")
    
    return {"message": "Appointment status updated successfully", "new_status": status}

# Service-specific functionality
@api_router.get("/services/nexus-rebuttal-letters/templates")
async def get_nexus_templates():
    """Get available nexus letter templates"""
    return {
        "templates": [
            {
                "id": "direct-nexus",
                "name": "Direct Service Connection",
                "description": "For conditions directly caused by military service",
                "fields": ["condition", "service_events", "medical_evidence"]
            },
            {
                "id": "secondary-nexus",
                "name": "Secondary Service Connection",
                "description": "For conditions caused by service-connected disabilities",
                "fields": ["primary_condition", "secondary_condition", "medical_rationale"]
            },
            {
                "id": "aggravation-nexus",
                "name": "Aggravation Nexus",
                "description": "For pre-existing conditions worsened by service",
                "fields": ["pre_existing_condition", "aggravation_evidence", "timeline"]
            }
        ]
    }

@api_router.get("/services/public-dbqs/available")
async def get_available_dbqs():
    """Get list of available DBQ forms"""
    return {
        "dbq_forms": [
            {"code": "21-0960A-1", "name": "Hearing Loss", "category": "Auditory"},
            {"code": "21-0960A-2", "name": "Tinnitus", "category": "Auditory"},
            {"code": "21-0960B-1", "name": "Hypertension", "category": "Cardiovascular"},
            {"code": "21-0960C-1", "name": "PTSD", "category": "Mental Health"},
            {"code": "21-0960C-2", "name": "Depression", "category": "Mental Health"},
            {"code": "21-0960D-1", "name": "Diabetes", "category": "Endocrine"},
            {"code": "21-0960E-1", "name": "Back Pain", "category": "Musculoskeletal"},
            {"code": "21-0960F-1", "name": "Sleep Apnea", "category": "Respiratory"}
        ]
    }

@api_router.get("/services/cp-coaching/preparation-guide")
async def get_cp_preparation_guide():
    """Get C&P exam preparation guide"""
    return {
        "preparation_tips": [
            "Arrive 15 minutes early",
            "Bring all relevant medical records",
            "Be honest about your symptoms",
            "Describe your worst days",
            "Don't minimize your pain or limitations"
        ],
        "what_to_expect": [
            "Physical examination",
            "Review of medical history",
            "Discussion of symptoms",
            "Functional assessment",
            "Questions about daily activities"
        ],
        "common_mistakes": [
            "Downplaying symptoms",
            "Not mentioning all conditions",
            "Forgetting to bring records",
            "Being unprepared for questions"
        ]
    }

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services_count": len(MOCK_SERVICES),
        "blog_posts_count": len(MOCK_BLOG_POSTS),
        "active_orders": len(MOCK_ORDERS),
        "scheduled_appointments": len(MOCK_APPOINTMENTS)
    }

# Include the router in the main app
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)