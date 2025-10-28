#!/usr/bin/env python3
"""
Deployment-optimized server for Dr. Kishan Bhalani Medical Documentation Services
Minimal, reliable server specifically designed for deployment platforms
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
from datetime import datetime

# Create the main app
app = FastAPI(
    title="Dr. Kishan Bhalani - Medical Documentation API",
    description="Medical documentation services for veterans",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Service(BaseModel):
    id: str
    slug: str
    title: str
    shortDescription: str
    fullDescription: str
    price: str
    duration: str
    features: List[str]
    icon: str
    category: str

class BlogPost(BaseModel):
    id: str
    slug: str
    title: str
    excerpt: str
    content: str
    author: str
    publishedAt: str
    category: str
    readTime: str
    tags: List[str]

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service: str
    message: str

# Mock data
MOCK_SERVICES = [
    {
        "id": "1",
        "slug": "nexus-rebuttal-letters",
        "title": "Nexus & Rebuttal Letters",
        "shortDescription": "Comprehensive medical opinions for claims and appeals",
        "fullDescription": "Professional nexus and rebuttal letters combining initial claim support with appeal expertise. Our comprehensive service covers both nexus opinion letters for establishing service connection and rebuttal letters to counter VA denials, providing complete medical documentation support throughout your claim lifecycle.",
        "price": "₹4,999",
        "duration": "7-10 business days",
        "features": [
            "Nexus opinion letters for service connection",
            "Rebuttal letters for VA denials",
            "Direct, secondary, and aggravation analysis",
            "Clear medical rationale and evidence review",
            "Professional formatting for VA submission"
        ],
        "icon": "FileText",
        "category": "documentation"
    },
    {
        "id": "2",
        "slug": "public-dbqs",
        "title": "Public DBQs",
        "shortDescription": "Standardized disability questionnaires",
        "fullDescription": "Comprehensive Disability Benefits Questionnaires (DBQs) completed by qualified medical professionals. These standardized forms help establish the severity and service connection of your medical conditions, providing the VA with detailed medical evidence in their preferred format.",
        "price": "₹3,999",
        "duration": "5-7 business days",
        "features": [
            "VA-standardized DBQ forms",
            "Condition-specific questionnaires",
            "Medical professional completion",
            "Evidence-based assessments",
            "Ready for VA submission"
        ],
        "icon": "ClipboardList",
        "category": "assessment"
    },
    {
        "id": "3",
        "slug": "aid-attendance",
        "title": "Aid & Attendance (21-2680)",
        "shortDescription": "Enhanced pension benefits documentation",
        "fullDescription": "Specialized medical evaluations for Aid & Attendance benefits, helping veterans and surviving spouses qualify for enhanced pension payments. Our comprehensive assessment covers activities of daily living, mobility limitations, and care requirements.",
        "price": "₹5,999",
        "duration": "7-10 business days",
        "features": [
            "Form 21-2680 completion",
            "Activities of daily living assessment",
            "Mobility and care requirement evaluation",
            "Physician examination and documentation",
            "Enhanced pension qualification support"
        ],
        "icon": "Heart",
        "category": "benefits"
    },
    {
        "id": "4",
        "slug": "cp-coaching",
        "title": "C&P Coaching",
        "shortDescription": "Examination preparation and guidance",
        "fullDescription": "Expert preparation for your Compensation & Pension (C&P) examination. Our coaching service helps you understand what to expect, how to effectively communicate your symptoms, and ensures you're fully prepared to present your case during the examination.",
        "price": "₹2,499",
        "duration": "Same day service",
        "features": [
            "Pre-examination consultation",
            "Symptom presentation guidance",
            "Question preparation and practice",
            "Examination process walkthrough",
            "Post-examination follow-up advice"
        ],
        "icon": "Users",
        "category": "coaching"
    },
    {
        "id": "5",
        "slug": "expert-consultation",
        "title": "One-on-One Consultation with Expert",
        "shortDescription": "Personal consultation with Dr. Kishan Bhalani",
        "fullDescription": "Direct, personal consultation with Dr. Kishan Bhalani via video call or phone. Get expert guidance on your specific case, comprehensive claim review, medical condition assessment, and personalized recommendations for your VA disability claim strategy.",
        "price": "₹3,499",
        "duration": "1-hour consultation scheduled within 3-5 days",
        "features": [
            "Personal consultation with Dr. Kishan Bhalani",
            "Comprehensive claim review and analysis",
            "Medical condition assessment and guidance",
            "Personalized claim strategy recommendations",
            "Real-time Q&A and expert advice"
        ],
        "icon": "Video",
        "category": "consultation"
    },
    {
        "id": "6",
        "slug": "record-review",
        "title": "Record Review",
        "shortDescription": "Professional medical record analysis",
        "fullDescription": "Comprehensive review and analysis of your medical records by qualified professionals. We identify key evidence, gaps in documentation, and provide strategic recommendations to strengthen your VA disability claim.",
        "price": "₹2,999",
        "duration": "5-7 business days",
        "features": [
            "Complete medical record analysis",
            "Evidence identification and organization",
            "Documentation gap analysis",
            "Timeline development",
            "Strategic recommendations report"
        ],
        "icon": "Search",
        "category": "analysis"
    },
    {
        "id": "7",
        "slug": "1151-claim",
        "title": "1151 Claim (VA Medical Malpractice)",
        "shortDescription": "Specialized VA negligence claims",
        "fullDescription": "Expert assistance with VA Form 1151 claims for medical malpractice or negligence by VA healthcare providers. Our specialized service helps establish VA fault and secure compensation for additional disabilities caused by VA medical care.",
        "price": "₹7,999",
        "duration": "10-14 business days",
        "features": [
            "VA Form 1151 preparation and filing",
            "Medical malpractice case analysis",
            "Expert medical opinion on VA negligence",
            "Causation establishment documentation",
            "Comprehensive legal and medical support"
        ],
        "icon": "Shield",
        "category": "specialized"
    }
]

MOCK_BLOG_POSTS = [
    {
        "id": "1",
        "slug": "nexus-rebuttal-letters-guide",
        "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
        "excerpt": "Understanding the critical role of nexus and rebuttal letters in securing your VA disability benefits and winning appeals.",
        "content": "Nexus and rebuttal letters are powerful medical documents that can make or break your VA disability claim...",
        "author": "Dr. Kishan Bhalani",
        "publishedAt": "2024-01-15T10:00:00Z",
        "category": "VA Claims",
        "readTime": "6 min read",
        "tags": ["nexus letters", "rebuttal letters", "VA claims", "medical evidence"]
    },
    {
        "id": "2",
        "slug": "cp-exam-preparation-tips",
        "title": "How to Prepare for Your C&P Examination: Expert Tips",
        "excerpt": "Essential preparation strategies for your Compensation & Pension examination to maximize your disability rating.",
        "content": "The C&P examination is a crucial step in your VA disability claim process...",
        "author": "Dr. Kishan Bhalani",
        "publishedAt": "2024-01-10T14:30:00Z",
        "category": "Examinations",
        "readTime": "8 min read",
        "tags": ["C&P exam", "preparation", "disability rating", "VA process"]
    }
]

# Root endpoints
@app.get("/")
async def root():
    return {
        "message": "Dr. Kishan Bhalani Medical Documentation Services API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "api_health": "/api/health",
            "services": "/api/services",
            "blog": "/api/blog"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Dr. Kishan Bhalani Medical Documentation API"
    }

# API endpoints
@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "services_available": len(MOCK_SERVICES),
        "blog_posts_available": len(MOCK_BLOG_POSTS)
    }

@app.get("/api/services", response_model=List[Service])
async def get_services():
    return MOCK_SERVICES

@app.get("/api/services/{slug}", response_model=Service)
async def get_service_by_slug(slug: str):
    service = next((s for s in MOCK_SERVICES if s["slug"] == slug), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/api/blog", response_model=List[BlogPost])
async def get_blog_posts(
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(20, le=100)
):
    posts = MOCK_BLOG_POSTS.copy()
    
    if category:
        posts = [p for p in posts if p["category"] == category]
    
    if q:
        posts = [p for p in posts if q.lower() in p["title"].lower() or q.lower() in p["excerpt"].lower()]
    
    return posts[:limit]

@app.get("/api/blog/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    post = next((p for p in MOCK_BLOG_POSTS if p["slug"] == slug), None)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@app.post("/api/contact")
async def create_contact(contact_data: ContactCreate):
    # In a real implementation, this would save to database
    return {
        "id": str(uuid.uuid4()),
        "message": "Contact form submitted successfully",
        "status": "received"
    }

# Export for deployment platforms
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)