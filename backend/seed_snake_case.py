#!/usr/bin/env python3
"""
Seed database with snake_case column names to match actual database schema
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Services data with snake_case column names
SERVICES_SNAKE_CASE = [
    {
        "id": "1",
        "slug": "nexus-rebuttal-letters",
        "title": "Nexus & Rebuttal Letters",
        "short_description": "Comprehensive medical opinions for claims and appeals",
        "full_description": "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions, or challenge unfavorable VA decisions. Our expert medical opinions provide the crucial evidence needed for both initial claims and appeals processes.",
        "features": [
            "Nexus opinion letters",
            "Rebuttal to VA denials",
            "Direct/secondary/aggravation analysis",
            "Clear medical rationale",
            "Rush service: +$500 USD (36-48 hours)"
        ],
        "base_price_in_usd": 1499,
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
        "title": "DBQs",
        "short_description": "Standardized disability questionnaires for VA claims",
        "full_description": "Disability Benefits Questionnaires (DBQs) are standardized medical examination forms used by the VA to evaluate disability claims. Our licensed physicians complete these forms based on current VA guidelines and your medical condition.",
        "features": [
            "Latest public VA DBQs",
            "Objective findings",
            "Functional impact",
            "Rush service: +$50 USD (36-48 hours)"
        ],
        "base_price_in_usd": 249,
        "duration": "5-7 business days",
        "category": "dbq",
        "icon": "clipboard",
        "faqs": [
            {
                "question": "Do you complete VA DBQs?",
                "answer": "Yes, we complete public DBQs that are currently accepted by the VA for various conditions."
            }
        ]
    }
]

# Blog posts with snake_case column names
BLOG_POSTS_SNAKE_CASE = [
    {
        "id": "1",
        "slug": "nexus-and-rebuttal-letters-explained",
        "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
        "excerpt": "Understanding the difference between nexus and rebuttal letters and when you need each for your VA claim.",
        "content_html": "<h2>Understanding Nexus and Rebuttal Letters</h2><p>Both nexus and rebuttal letters are crucial medical documents in the VA claims process.</p>",
        "category": "nexus-letters",
        "tags": ["nexus", "rebuttal", "medical opinion"],
        "author_name": "Dr. Kishan Bhalani",
        "published_at": "SEPT 2025",
        "read_time": "6 min read"
    }
]

def test_snake_case():
    print("Testing snake_case column names...")
    
    # Test with just one service first
    try:
        print("Inserting test service...")
        result = supabase.table('services').insert(SERVICES_SNAKE_CASE[0]).execute()
        print(f"✅ Service insert successful: {result.data[0]['title']}")
        
        # Clean up
        supabase.table('services').delete().eq('id', '1').execute()
        print("✅ Test service cleaned up")
        
    except Exception as e:
        print(f"❌ Service insert failed: {e}")
    
    # Test with one blog post
    try:
        print("Inserting test blog post...")
        result = supabase.table('blog_posts').insert(BLOG_POSTS_SNAKE_CASE[0]).execute()
        print(f"✅ Blog post insert successful: {result.data[0]['title']}")
        
        # Clean up
        supabase.table('blog_posts').delete().eq('id', '1').execute()
        print("✅ Test blog post cleaned up")
        
    except Exception as e:
        print(f"❌ Blog post insert failed: {e}")

if __name__ == "__main__":
    test_snake_case()