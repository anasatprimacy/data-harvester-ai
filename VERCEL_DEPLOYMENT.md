# Vercel Deployment Guide

## 🚀 Deploying Data Harvester on Vercel

Vercel can host both your Next.js frontend AND Python backend as serverless functions!

## 📋 Prerequisites

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Install mangum for FastAPI serverless compatibility:
```bash
pip install mangum
```

## 🏗️ Project Structure for Vercel

```
data-harvester-ai/
├── api/
│   └── index.py          # Serverless function entry point
├── frontend/             # Next.js app
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── backend_api.py       # Your FastAPI app
```

## ⚙️ Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

### api/index.py
```python
import sys
from pathlib import Path
from mangum import Mangum
from backend_api import app

# Add root to Python path
sys.path.append(str(Path(__file__).parent))

# Wrap FastAPI for serverless
handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

## 🚀 Deployment Steps

### Step 1: Update requirements.txt
Add mangum to your requirements:
```bash
echo "mangum" >> requirements.txt
```

### Step 2: Deploy to Vercel
```bash
# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? data-harvester-ai
# - Directory? . (root)
# - Override settings? Yes
```

### Step 3: Set Environment Variables
```bash
# Set API keys in Vercel dashboard or CLI
vercel env add FIRECRAWL_API_KEY
vercel env add GOOGLE_PLACES_API_KEY
vercel env add GOOGLE_SEARCH_API_KEY
vercel env add GOOGLE_SEARCH_ENGINE_ID
```

## 🔄 Update Frontend for Vercel

Since both frontend and backend are on Vercel, update `frontend/src/services/api.ts`:

```typescript
// No need for external backend URL - use relative paths
const RAW_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "";

// Vercel handles the routing automatically
const isRelative = true; // Always use relative on Vercel

export const api = axios.create({
  baseURL: "", // Empty for relative paths
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});
```

## 🎯 Benefits of Vercel

### ✅ Advantages:
- **Single platform** for frontend + backend
- **Automatic deployments** from git
- **Free tier** available
- **Global CDN** included
- **Environment variables** management
- **Custom domains** supported

### ⚠️ Limitations:
- **Serverless timeout**: 10-60 seconds max
- **Cold starts**: First request may be slower
- **Memory limits**: 1GB max on free tier
- **No long-running processes** (scraping jobs may timeout)

## 🔧 Alternative: Backend on Railway + Frontend on Vercel

If serverless limitations are an issue:

1. **Frontend on Vercel** (current setup)
2. **Backend on Railway** (long-running processes)
3. **Update Vercel redirects**:
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend.railway.app/api/$1"
    }
  ]
}
```

## 📊 Testing Your Vercel Deployment

```bash
# Test locally
vercel dev

# Test deployed API
curl https://your-app.vercel.app/api/health

# Test frontend
# Open https://your-app.vercel.app
```

## 🎉 Recommended Approach

**For small scraping jobs**: Use Vercel serverless
**For heavy scraping**: Use Railway backend + Vercel frontend

Choose based on your scraping workload size!
