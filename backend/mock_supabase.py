"""
Mock Supabase Client for Testing Dr. Kishan Bhalani Medical Documentation Services
This provides a fake Supabase interface for development without a real database
"""

class MockSupabaseResponse:
    def __init__(self, data):
        self.data = data

class MockSupabaseQuery:
    def __init__(self, table_name, mock_data):
        self.table_name = table_name
        self.mock_data = mock_data
        self.filters = {}
        self.limit_count = None
        self.order_by = None
    
    def select(self, columns='*'):
        return self
    
    def eq(self, column, value):
        self.filters[column] = value
        return self
    
    def or_(self, condition):
        # Simple search implementation
        if 'ilike' in condition:
            self.filters['search'] = condition
        return self
    
    def limit(self, count):
        self.limit_count = count
        return self
    
    def order(self, column, desc=False):
        self.order_by = (column, desc)
        return self
    
    def execute(self):
        data = self.mock_data.copy()
        
        # Apply filters
        for key, value in self.filters.items():
            if key == 'search':
                # Simple search implementation
                search_term = value.split('%')[1] if '%' in value else value
                data = [item for item in data if 
                       search_term.lower() in item.get('title', '').lower() or 
                       search_term.lower() in item.get('excerpt', '').lower()]
            else:
                data = [item for item in data if item.get(key) == value]
        
        # Apply limit
        if self.limit_count:
            data = data[:self.limit_count]
        
        return MockSupabaseResponse(data)
    
    def insert(self, data):
        if isinstance(data, list):
            return MockSupabaseResponse(data)
        return MockSupabaseResponse([data])
    
    def update(self, data):
        return MockSupabaseResponse([data])
    
    def delete(self):
        return self
    
    def neq(self, column, value):
        return self

class MockSupabaseClient:
    def __init__(self):
        # Mock services data
        self.services_data = [
            {
                "id": "1",
                "slug": "nexus-rebuttal-letters",
                "title": "Nexus & Rebuttal Letters",
                "shortDescription": "Comprehensive medical opinions for claims and appeals",
                "fullDescription": "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions, or challenge unfavorable VA decisions. Our expert medical opinions provide the crucial evidence needed for both initial claims and appeals processes.",
                "features": ["Nexus opinion letters", "Rebuttal to VA denials", "Direct/secondary/aggravation analysis", "Clear medical rationale", "Rush service: +$500 USD (36-48 hours)"],
                "basePriceInUSD": 1499,
                "duration": "7-10 business days",
                "category": "nexus-letter",
                "icon": "file-text",
                "faqs": [
                    {"question": "What's the difference between nexus and rebuttal letters?", "answer": "Nexus letters establish the connection between military service and a condition for initial claims. Rebuttal letters challenge VA decisions by providing contrary medical evidence and opinions."},
                    {"question": "Can you help with both initial claims and appeals?", "answer": "Yes, we provide nexus letters for initial claims and rebuttal letters to challenge unfavorable VA decisions in appeals."}
                ]
            },
            {
                "id": "2",
                "slug": "public-dbqs",
                "title": "DBQs",
                "shortDescription": "Standardized disability questionnaires for VA claims",
                "fullDescription": "Disability Benefits Questionnaires (DBQs) are standardized medical examination forms used by the VA to evaluate disability claims. Our licensed physicians complete these forms based on current VA guidelines and your medical condition.",
                "features": ["Latest public VA DBQs", "Objective findings", "Functional impact", "Rush service: +$50 USD (36-48 hours)"],
                "basePriceInUSD": 249,
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
                "fullDescription": "Aid and Attendance is a benefit available to veterans and surviving spouses who require the regular assistance of another person. We provide comprehensive physician evaluations to support your A&A benefit claim.",
                "features": ["Physician evaluation", "ADL documentation", "When clinically indicated", "Rush service: +$500 USD (36-48 hours)"],
                "basePriceInUSD": 1999,
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
                "basePriceInUSD": 29,
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
                "fullDescription": "Schedule a comprehensive one-on-one consultation with Dr. Kishan Bhalani to review your VA claim, discuss your medical conditions, and receive personalized guidance on strengthening your case. This direct consultation provides expert insights tailored to your specific situation.",
                "features": ["Personal consultation with Dr. Bhalani", "Comprehensive claim review", "Medical condition assessment", "Personalized recommendations"],
                "basePriceInUSD": 249,
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
                "basePriceInUSD": 99,
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
                "fullDescription": "Specialized medical documentation for 38 U.S.C. § 1151 claims when veterans are injured or their conditions worsen due to VA medical care. Our expert analysis helps establish negligence and causation for these complex claims requiring higher burden of proof.",
                "features": ["VA treatment record analysis", "Medical negligence assessment", "Causation nexus opinions", "Standard of care evaluation"],
                "basePriceInUSD": 1999,
                "duration": "10-14 business days",
                "category": "malpractice",
                "icon": "alert-triangle",
                "faqs": [
                    {"question": "What is a 1151 claim?", "answer": "A 1151 claim is filed when a veteran believes they were injured or their condition worsened due to VA medical care negligence, surgical errors, medication mistakes, or other treatment-related harm."},
                    {"question": "How is this different from a regular VA claim?", "answer": "1151 claims require proving VA negligence and deviation from medical standards, not just service connection. They have a higher burden of proof but can provide compensation even for non-service-connected conditions."}
                ]
            }
        ]
        
        self.blog_data = [
            {
                "id": "1",
                "slug": "nexus-and-rebuttal-letters-explained",
                "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
                "excerpt": "Understanding the difference between nexus and rebuttal letters and when you need each for your VA claim.",
                "contentHTML": "<h2>Understanding Nexus and Rebuttal Letters</h2><p>Both nexus and rebuttal letters are crucial medical documents in the VA claims process, but they serve different purposes at different stages of your claim.</p>",
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
    
    def table(self, table_name):
        if table_name == 'services':
            return MockSupabaseQuery(table_name, self.services_data)
        elif table_name == 'blog_posts':
            return MockSupabaseQuery(table_name, self.blog_data)
        elif table_name == 'contacts':
            return MockSupabaseQuery(table_name, [])
        else:
            return MockSupabaseQuery(table_name, [])
    
    def rpc(self, function_name, params=None):
        return MockSupabaseResponse([])

def create_client(url, key):
    """Mock create_client function that works with demo URLs"""
    if 'demo-project' in url or 'placeholder' in url:
        print("🎭 Using mock Supabase client for testing")
        return MockSupabaseClient()
    else:
        # Try to use real Supabase
        from supabase import create_client as real_create_client
        return real_create_client(url, key)