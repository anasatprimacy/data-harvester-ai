# Production Deployment Guide

## Environment Setup for Production

### 1. Environment Variables Setup

1. **Copy the template file:**
   ```bash
   cp env.template .env
   ```

2. **Fill in your actual API keys in `.env`:**
   - Firecrawl API key
   - Google Places API key
   - Google Search API key and Engine ID
   - Any other required API keys

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install python-dotenv for environment variable management
pip install python-dotenv
```

### 3. Production Deployment Options

#### Option A: Direct Server Deployment
```bash
# Set environment variables
export $(cat .env | xargs)

# Run the application
python main.py
```

#### Option B: Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  data-harvester:
    build: .
    env_file:
      - .env
    volumes:
      - ./output:/app/output
      - ./logs:/app/logs
```

#### Option C: Cloud Deployment (AWS/Google Cloud/Azure)

1. **Use environment variable management:**
   - AWS: Parameter Store or Secrets Manager
   - Google Cloud: Secret Manager
   - Azure: Key Vault

2. **Set environment variables in your deployment:**
   ```bash
   # Example for AWS ECS
   aws ecs create-service --cli-input-json file://config.json
   ```

### 4. Security Best Practices

1. **Never commit `.env` files to version control**
2. **Use different API keys for development and production**
3. **Rotate API keys regularly**
4. **Monitor API usage and costs**
5. **Use IP restrictions where possible**

### 5. Environment-Specific Configurations

#### Development (.env.dev)
```
DEBUG=True
LOG_LEVEL=DEBUG
RATE_LIMIT_DELAY=1
```

#### Production (.env.prod)
```
DEBUG=False
LOG_LEVEL=INFO
RATE_LIMIT_DELAY=3
MAX_RETRIES=5
```

### 6. Monitoring and Logging

1. **Set up structured logging**
2. **Monitor API rate limits**
3. **Track scraping success rates**
4. **Set up alerts for failures**

### 7. Running in Production

```bash
# Load environment variables
source .env

# Run with proper logging
python main.py >> logs/production.log 2>&1 &

# Or use process manager like systemd or supervisor
```

### 8. API Key Management Services

Consider using:
- **AWS Secrets Manager**
- **Google Secret Manager**
- **HashiCorp Vault**
- **Docker Secrets** (for Docker deployments)

### 9. Backup and Recovery

1. **Backup your `.env` file securely**
2. **Document API key sources and renewal process**
3. **Have a plan for API key compromise**

### 10. Testing Production Setup

```bash
# Test configuration loading
python -c "from config.env_config import config; print(config.validate_required_keys())"

# Test API connections
python test_api_connections.py
```
