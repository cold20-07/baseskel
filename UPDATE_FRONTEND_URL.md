# Update Frontend URL After Railway Deployment

## Step 1: Get Your Railway URL
After Railway deployment completes, copy your app URL (e.g., `https://your-app.up.railway.app`)

## Step 2: Update Frontend Files

### Update `frontend/.env`:
```
REACT_APP_BACKEND_URL=https://your-app.up.railway.app
```

### Update `frontend/.env.production`:
```
REACT_APP_BACKEND_URL=https://your-app.up.railway.app
```

## Step 3: Test Your Railway Backend

Test these endpoints with your Railway URL:
- Health: `https://your-app.up.railway.app/api/health`
- Services: `https://your-app.up.railway.app/api/services`
- Blog: `https://your-app.up.railway.app/api/blog`

## Step 4: Commit and Deploy

```bash
git add .
git commit -m "Update frontend to use Railway backend URL"
git push origin main
```

This will trigger a new Netlify deployment with the correct backend URL.

## Troubleshooting

**If Railway deployment fails:**
- Check Railway logs for specific error messages
- Verify environment variables are set correctly
- Ensure Supabase database is accessible

**If frontend can't connect:**
- Verify CORS_ORIGINS includes your Netlify domain
- Check that Railway app is running (not sleeping)
- Test Railway endpoints directly in browser