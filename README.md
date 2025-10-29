# Military Disability Nexus - Medical Documentation Services

A modern, full-stack web application for veteran medical documentation services including nexus letters, DBQs, and consultation services.

## 🚀 Tech Stack

- **Frontend**: React 19 + React Router + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) + Supabase Python Client
- **Database**: Supabase (PostgreSQL)
- **State Management**: React Hooks
- **Form Handling**: React Hook Form + Zod validation
- **UI Components**: Shadcn UI with Radix UI primitives
- **Notifications**: Sonner (toast notifications)

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py           # FastAPI application with API routes
│   ├── seed_data.py        # Database seeding script
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/         # Shadcn UI components
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   └── Layout.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Services.js
│   │   │   ├── ServiceDetail.js
│   │   │   ├── Blog.js
│   │   │   ├── BlogPost.js
│   │   │   ├── About.js
│   │   │   └── Contact.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── .env                # Frontend environment variables
└── README.md
```

## 🎯 Features Implemented

### Core Pages
- **Home**: Hero section, services preview, trust badges, how it works, blog previews, CTA sections
- **Services**: Grid view of all 6 services with pricing and features
- **Service Detail**: Individual service pages with detailed info, FAQs (using Shadcn Accordion)
- **Blog**: List view with search and category filtering
- **Blog Post**: Individual article pages with formatted content
- **About**: Mission, values, credentials, approach, team info
- **Contact**: Contact form with validation and success state

### HIPAA Compliance Features
- **Data Encryption**: AES-256 encryption for all PHI data at rest
- **Audit Logging**: Comprehensive audit trail for all PHI access and modifications
- **Access Controls**: Role-based access control with minimum necessary principle
- **Security Headers**: HIPAA-compliant HTTP security headers
- **Rate Limiting**: Protection against brute force and DoS attacks
- **Data Retention**: Automated data retention and secure disposal
- **Breach Response**: Incident reporting and management system
- **Compliance Monitoring**: Real-time compliance dashboard and reporting

### Services Offered (7 Total)
1. Nexus Letters - $1,500
2. DBQs - $250
3. Aid & Attendance (21-2680) - $2,000
4. C&P Coaching - $29
5. Telehealth Consultation - $250
6. Record Review - $100 (unlimited pages)
7. 1151 Claim (VA Medical Malpractice) - $2,000

### Backend API Endpoints
- `GET /api/services` - List all services
- `GET /api/services/:slug` - Get single service
- `GET /api/blog?category=&q=&limit=` - List blog posts with filters
- `GET /api/blog/:slug` - Get single blog post
- `POST /api/contact` - Submit contact form (HIPAA-compliant with PHI encryption)

### HIPAA Compliance Endpoints
- `GET /api/hipaa/audit-logs` - Retrieve HIPAA audit logs (admin only)
- `GET /api/hipaa/compliance-summary` - Get compliance dashboard data (admin only)
- `POST /api/hipaa/execute-data-retention` - Execute scheduled data deletions (admin only)
- `POST /api/hipaa/report-breach` - Report HIPAA breach incidents (admin only)
- `GET /api/health` - System health and compliance status

### Design Features
- Modern, professional healthcare aesthetic
- Teal/emerald color scheme (avoiding dark gradients)
- Space Grotesk + Manrope typography
- Smooth animations and transitions
- Responsive design (mobile, tablet, desktop)
- Glass-morphism effects
- Hover states and micro-interactions
- Accessible components (Shadcn UI)

## 🛠 Local Development

### Prerequisites
- Supabase project with database setup
- Node.js 18+ and Yarn
- Python 3.11+

### Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to the SQL Editor in your Supabase dashboard
3. Run the SQL schema from `backend/supabase_schema.sql`
4. Get your project URL and anon key from Settings > API
5. Update your `.env` file with these credentials

### Backend Setup

```bash
cd /app/backend

# Install dependencies
pip install -r requirements.txt

# Set up Supabase database schemas
# 1. Run supabase_schema.sql in your Supabase SQL editor
# 2. Run hipaa_schema.sql in your Supabase SQL editor

# Seed the database
python seed_data.py

# Run HIPAA compliance tests
python test_hipaa_compliance.py

# Start backend (managed by supervisor)
sudo supervisorctl restart backend
```

### Frontend Setup

```bash
cd /app/frontend

# Install dependencies
yarn install

# Start development server (managed by supervisor)
sudo supervisorctl restart frontend
```

### Check Services Status

```bash
sudo supervisorctl status
```

## 🌐 Environment Variables

### Backend (.env)
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
HIPAA_ENCRYPTION_KEY=your-strong-encryption-key-change-in-production
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,yourdomain.com
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=https://va-services-hub.preview.emergentagent.com
WDS_SOCKET_PORT=443
```

## 📊 Database Schema (Supabase/PostgreSQL)

### Services Table
```sql
CREATE TABLE services (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    shortDescription TEXT NOT NULL,
    fullDescription TEXT NOT NULL,
    features JSONB NOT NULL DEFAULT '[]',
    basePriceInUSD INTEGER NOT NULL,
    duration TEXT NOT NULL,
    category TEXT NOT NULL,
    icon TEXT NOT NULL,
    faqs JSONB NOT NULL DEFAULT '[]'
);
```

### Blog Posts Table
```sql
CREATE TABLE blog_posts (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    contentHTML TEXT NOT NULL,
    category TEXT NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]',
    authorName TEXT NOT NULL,
    publishedAt TEXT NOT NULL,
    readTime TEXT NOT NULL
);
```

### Contacts Table
```sql
CREATE TABLE contacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    createdAt TEXT NOT NULL
);
```

## 🧪 Testing

### Test Backend API
```bash
# Get all services
curl https://va-services-hub.preview.emergentagent.com/api/services

# Get specific service
curl https://va-services-hub.preview.emergentagent.com/api/services/nexus-letters

# Submit contact form
curl -X POST https://va-services-hub.preview.emergentagent.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Inquiry",
    "message": "This is a test message"
  }'
```

### Check Logs
```bash
# Backend logs
tail -f /var/log/supervisor/backend.*.log

# Frontend logs  
tail -f /var/log/supervisor/frontend.*.log
```

## 📦 Export to GitHub

This project is ready to be exported to GitHub:

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "feat: Initial MVP with all core features"

# Add remote
git remote add origin <your-github-repo-url>

# Push
git push -u origin main
```

## 🔄 Future Enhancements (Not in MVP)

Features intentionally left out of MVP that can be added later:

1. **Full Booking Funnel** (6-step wizard with date/time selection, file uploads, payment processing)
2. **Admin Dashboard** (read-only stats, appointments management, contacts CRM)
3. **User Authentication** (JWT-based login/signup)
4. **Real Payment Integration** (Stripe or similar)
5. **File Upload System** (AWS S3 or Cloudinary)
6. **Email Notifications** (SendGrid or similar)
7. **Appointment Scheduling** (calendar integration)
8. **Search Functionality** (full-text search)
9. **SEO Optimization** (meta tags, sitemap, schema markup)
10. **Analytics** (Google Analytics, custom events)

## 🎨 Design Guidelines

- **Typography**: Space Grotesk (headings), Manrope (body)
- **Colors**: 
  - Primary: Teal 600 (#0d9488)
  - Secondary: Emerald 600 (#059669)
  - Background: Slate 50 (#f8fafc)
  - Text: Slate 900 (#0f172a)
- **Spacing**: Generous padding (2-3x normal)
- **Components**: All interactive elements have hover states
- **Accessibility**: WCAG 2.1 AA compliant (via Shadcn)

## 📝 Notes

- All prices are in USD (US Dollars) with $ symbol
- Production data from Supabase database
- Contact form submissions are stored in Supabase
- No authentication required for MVP
- All API routes use `/api` prefix for proper routing
- Services are running on supervisor (auto-restart enabled)

## 🤝 Support

For questions or issues, please check the logs or contact support.

---

**Military Disability Nexus - Professional Medical Documentation Services**
