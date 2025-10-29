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
import uuid
from datetime import datetime

# Create the main app
app = FastAPI(
    title="Military Disability Nexus - Medical Documentation API",
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
        "title": "Nexus Letters",
        "shortDescription": "Professional nexus letters for service connection",
        "fullDescription": "Professional nexus letters for establishing service connection of your medical conditions to military service. Our comprehensive service provides detailed medical opinions linking your current disabilities to your military service, supporting your VA disability claims with expert medical documentation.",
        "price": "$1,500",
        "duration": "7-10 business days",
        "features": [
            "Professional nexus opinion letters",
            "Up to 4 claims per letter",
            "Direct, secondary, and aggravation analysis",
            "Clear medical rationale and evidence review",
            "Professional formatting for VA submission",
            "Rush service: +$500 USD (36-48 hours)"
        ],
        "icon": "FileText",
        "category": "documentation"
    },
    {
        "id": "2",
        "slug": "public-dbqs",
        "title": "DBQs",
        "shortDescription": "Standardized disability questionnaires",
        "fullDescription": "Comprehensive Disability Benefits Questionnaires (DBQs) completed by qualified medical professionals. These standardized forms help establish the severity and service connection of your medical conditions, providing the VA with detailed medical evidence in their preferred format.",
        "price": "$250",
        "duration": "5-7 business days",
        "features": [
            "VA-standardized DBQ forms",
            "Condition-specific questionnaires",
            "Medical professional completion",
            "Evidence-based assessments",
            "Ready for VA submission",
            "Rush service: +$50 USD (36-48 hours)"
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
        "price": "$2,000",
        "duration": "7-10 business days",
        "features": [
            "Form 21-2680 completion",
            "Activities of daily living assessment",
            "Mobility and care requirement evaluation",
            "Physician examination and documentation",
            "Enhanced pension qualification support",
            "Rush service: +$500 USD (36-48 hours)"
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
        "price": "$29",
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
        "title": "Telehealth Consultation",
        "shortDescription": "Virtual consultation with medical expert",
        "fullDescription": "Professional telehealth consultation with our medical expert via secure video call. Get expert medical guidance on your specific case, comprehensive claim review, medical condition assessment, and personalized recommendations for your VA disability claim strategy.",
        "price": "$250",
        "duration": "1-hour consultation scheduled within 3-5 days",
        "features": [
            "Personal consultation with medical expert",
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
        "shortDescription": "Professional medical record analysis (unlimited pages)",
        "fullDescription": "Comprehensive review and analysis of your medical records by qualified professionals with no page limit. We identify key evidence, gaps in documentation, and provide strategic recommendations to strengthen your VA disability claim.",
        "price": "$100",
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
        "price": "$2,000",
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
        "author": "Military Disability Nexus",
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
        "author": "Military Disability Nexus",
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
        "message": "Military Disability Nexus Medical Documentation Services API",
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
        "service": "Military Disability Nexus Medical Documentation API"
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