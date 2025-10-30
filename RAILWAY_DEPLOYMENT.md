# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

### **Option 1: Deploy from GitHub (Recommended)**

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** with your GitHub account
3. **Click "Deploy from GitHub repo"**
4. **Select this repository**: `cold20-07/baseskel`
5. **Railway will auto-detect** the `railway.json` configuration
6. **Set Environment Variables** in Railway dashboard:
   ```
   SUPABASE_URL=https://cwjsyxxzdwphhlpppxau.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0
   CORS_ORIGINS=*
   HIPAA_ENCRYPTION_KEY=bw7Y9P3w4QJFVJatMqu8+gv8mRlWmlhAB7FHLvR8c8M=
   ENVIRONMENT=production
   ALLOWED_HOSTS=*
   PORT=8000
   ```
7. **Deploy!** Railway will build and deploy automatically

### **Option 2: Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set SUPABASE_URL=https://cwjsyxxzdwphhlpppxau.supabase.co
railway variables set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0
railway variables set CORS_ORIGINS=*
railway variables set HIPAA_ENCRYPTION_KEY=bw7Y9P3w4QJFVJatMqu8+gv8mRlWmlhAB7FHLvR8c8M=
railway variables set ENVIRONMENT=production
railway variables set ALLOWED_HOSTS=*

# Deploy
railway up
```

## After Deployment

1. **Get your Railway URL** (e.g., `https://your-app.up.railway.app`)
2. **Update frontend/.env** with your Railway URL:
   ```
   REACT_APP_BACKEND_URL=https://your-app.up.railway.app
   ```
3. **Commit and push** to update Netlify deployment
4. **Test the endpoints**:
   - Health: `https://your-app.up.railway.app/api/health`
   - Services: `https://your-app.up.railway.app/api/services`

## Railway Features

✅ **Free Tier**: 500 hours/month, $5 credit  
✅ **Auto-deploy**: Deploys on every git push  
✅ **Custom domains**: Add your own domain  
✅ **Environment variables**: Secure config management  
✅ **Logs & monitoring**: Built-in observability  
✅ **Scaling**: Automatic scaling based on traffic  

## Troubleshooting

**Build fails?**
- Check that `backend/requirements.txt` exists
- Verify Python version compatibility

**Health check fails?**
- Ensure `/api/health` endpoint returns 200
- Check environment variables are set correctly

**CORS errors?**
- Set `CORS_ORIGINS=*` for testing
- Use specific domains for production

**Database connection fails?**
- Verify Supabase URL and key are correct
- Check that database tables exist and are seeded