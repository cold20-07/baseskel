#!/usr/bin/env python3
"""
Simplified server for Railway deployment without optional dependencies
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client, Client
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import uvicorn

# Load environment variables
load_dotenv()

# Supabase connection
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

supabase: Client = create_client(supabase_url, supabase_key)

# Create FastAPI app
app = FastAPI(
    title="VA Services API",
    description="Medical Documentation Services API",
    version="1.0.0"
)

# CORS middleware
cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# API router
api_router = APIRouter(prefix="/api")

# Models
class Service(BaseModel):
    id: str
    slug: str
    title: str
    shortDescription: str
    fullDescription: str
    features: List[str]
    basePriceInUSD: int
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

# Routes
@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@api_router.get("/services", response_model=List[Service])
async def get_services():
    try:
        response = supabase.table('services').select('*').execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch services: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Failed to fetch service: {str(e)}")

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
            query = query.or_(f'title.ilike.%{q}%,excerpt.ilike.%{q}%')
        
        query = query.limit(limit)
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blog posts: {str(e)}")

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
        raise HTTPException(status_code=500, detail=f"Failed to fetch blog post: {str(e)}")

@api_router.post("/contact", response_model=Contact)
async def create_contact(contact_data: ContactCreate):
    try:
        contact_obj = Contact(
            id=str(uuid.uuid4()),
            **contact_data.model_dump(),
            createdAt=datetime.now(timezone.utc).isoformat()
        )
        
        response = supabase.table('contacts').insert(contact_obj.model_dump()).execute()
        return contact_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contact: {str(e)}")

# Include router
app.include_router(api_router)

# Root health check
@app.get("/")
async def root():
    return {"message": "VA Services API", "status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)