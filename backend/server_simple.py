"""
Simplified FastAPI server for Dr. Kishan Bhalani Medical Documentation Services
This version works without external database connections for testing
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

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

# Custom exception handler for 404 errors
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
    """Get all available services and blog posts"""
    return {
        "services": {
            "count": len(MOCK_SERVICES),
            "available": [{"slug": s["slug"], "title": s["title"]} for s in MOCK_SERVICES]
        },
        "blog_posts": {
            "count": len(MOCK_BLOG_POSTS),
            "available": [{"slug": b["slug"], "title": b["title"]} for b in MOCK_BLOG_POSTS]
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

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services_count": len(MOCK_SERVICES),
        "blog_posts_count": len(MOCK_BLOG_POSTS)
    }

# Include the router in the main app
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)