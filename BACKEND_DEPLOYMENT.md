# Backend Deployment Guide

## 🚀 Backend Deployment Options for Data Harvester

Since your frontend is deployed on Netlify (static hosting), you need to deploy your Python backend separately. Here are the best options:

## Option 1: Railway (Recommended - Easiest)

### Setup Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize Railway project
railway init

# Deploy backend
railway up
```

### Railway Configuration
1. Create `railway.toml`:
```toml
[build]
  builder = "NIXPACKS"

[deploy]
  startCommand = "python backend_api.py"
  restartPolicyType = "ON_FAILURE"
  restartPolicyMaxRetries = 10

[env]
  PYTHON_VERSION = "3.11"
```

2. Set environment variables in Railway dashboard:
   - Copy your `.env` file contents
   - Add all API keys

## Option 2: Render (Free Tier Available)

### Deploy to Render
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create "Web Service"
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend_api.py`
   - **Python Version**: `3.11`

### Render Configuration
Add `render.yaml`:
```yaml
services:
  - type: web
    name: data-harvester-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python backend_api.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

## Option 3: Heroku (Paid)

### Heroku Setup
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Push to Heroku
git subtree push --prefix backend_api.py heroku main
```

## Option 4: DigitalOcean App Platform

### DigitalOcean Setup
1. Create `app.yaml`:
```yaml
name: data-harvester-api
services:
- name: api
  source_dir: /
  github:
    repo: anas-ai-ml/data-harvester-ai
    branch: master
  run_command: python backend_api.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: PYTHON_VERSION
    value: "3.11"
```

## Option 5: AWS Lambda Serverless

### Serverless Function
Create `lambda_function.py`:
```python
import json
from backend_api import app
from mangum import Mangum

handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

Add `serverless.yml`:
```yaml
service: data-harvester-api
provider:
  name: aws
  runtime: python3.11
  region: us-east-1

functions:
  api:
    handler: lambda_function.lambda_handler
    events:
      - httpApi:
          path: /{proxy+}
          method: ANY

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    layer: true
```

## 🔧 Update Netlify Configuration

Once your backend is deployed, update `netlify.toml`:

```toml
# Replace this line with your actual backend URL
[[redirects]]
  from = "/api/*"
  to = "https://your-backend-url.railway.app/api/:splat"  # Update this!
  status = 200
  force = true
```

## 🌐 Update Frontend API Configuration

Update `frontend/src/services/api.ts`:

```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.railway.app'  // Update this!
  : 'http://localhost:8000';
```

## 🎯 Recommended Quick Setup

**For fastest deployment:**

1. **Use Railway** (free tier, easiest)
2. **Deploy backend** (5 minutes)
3. **Update Netlify config** with Railway URL
4. **Redeploy frontend** to pick up new backend URL

## 📋 Environment Variables

Don't forget to set these in your backend deployment:
- FIRECRAWL_API_KEY
- GOOGLE_PLACES_API_KEY
- GOOGLE_SEARCH_API_KEY
- GOOGLE_SEARCH_ENGINE_ID

## 🚀 Testing

After deployment:
```bash
# Test backend
curl https://your-backend-url.railway.app/health

# Test frontend
# Should load and connect to backend
```

Choose the option that best fits your needs and budget!
