# Deployment Guide

Churn Insight & Intervention Portal deployment instructions for various environments.

## 🖥️ Local Development

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Navigate to http://localhost:8501
```

### Development Mode with Auto-Reload
```bash
streamlit run app.py --logger.level=debug
```

---

## 🐳 Docker Deployment

### Build and Run Locally
```bash
# Build the Docker image
docker build -t churn-portal:latest .

# Run the container
docker run -p 8501:8501 churn-portal:latest

# Or use docker-compose
docker-compose up
```

### Docker Compose Options
```bash
# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended for Quick Setup)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy via Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

### AWS ECS Deployment

1. **Push image to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
   
   docker tag churn-portal:latest <account>.dkr.ecr.us-east-1.amazonaws.com/churn-portal:latest
   
   docker push <account>.dkr.ecr.us-east-1.amazonaws.com/churn-portal:latest
   ```

2. **Create ECS Task Definition**
   ```json
   {
     "family": "churn-portal",
     "containerDefinitions": [
       {
         "name": "churn-portal",
         "image": "<account>.dkr.ecr.us-east-1.amazonaws.com/churn-portal:latest",
         "portMappings": [
           {
             "containerPort": 8501,
             "hostPort": 8501,
             "protocol": "tcp"
           }
         ]
       }
     ]
   }
   ```

3. **Create ECS Service**
   - Use Fargate launch type
   - Assign security groups allowing port 8501
   - Configure auto-scaling

### Google Cloud Run Deployment

```bash
# Authenticate
gcloud auth login

# Build and push
gcloud run deploy churn-portal \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501

# Set environment variables
gcloud run services update churn-portal \
  --region us-central1 \
  --set-env-vars "PYTHONUNBUFFERED=1"
```

### Heroku Deployment

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

2. **Create runtime.txt**
   ```
   python-3.11.0
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create churn-portal
   git push heroku main
   heroku open
   ```

### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry <registry-name> --image churn-portal:latest .

# Create container instance
az container create \
  --resource-group <group-name> \
  --name churn-portal \
  --image <registry-name>.azurecr.io/churn-portal:latest \
  --ports 8501 \
  --cpu 1 \
  --memory 1
```

---

## 🔐 Production Hardening

### Environment Variables

Create `.env` file:
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-here
LOG_LEVEL=info
CACHE_TTL=3600
MAX_UPLOAD_SIZE=100
```

Load in `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
```

### Authentication & Authorization

Add Streamlit Authenticator:
```bash
pip install streamlit-authenticator
```

```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials={...},
    cookie_name='churn_portal_auth',
    key='your_secret_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login()

if not authentication_status:
    st.error("Authentication required")
    st.stop()
```

### HTTPS & Reverse Proxy

**Nginx Configuration:**
```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 443 ssl http2;
    server_name churn-portal.company.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://streamlit;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Rate Limiting

In `config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
enableXsrfProtection = true
```

### Data Security

```python
# Mask sensitive data in display
def mask_customer_id(customer_id):
    return f"{customer_id[:4]}...{customer_id[-4:]}"

# Encrypt sensitive columns
from cryptography.fernet import Fernet
cipher = Fernet(key)
encrypted = cipher.encrypt(sensitive_data.encode())
```

---

## 📊 Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Loaded {len(df)} customer records")
```

### Health Check Endpoint

Create `health.py`:
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })
```

### Performance Monitoring

Monitor these metrics:
- **Load Time**: Time to render full dashboard
- **Query Latency**: Database query response times
- **Cache Hit Rate**: Percentage of cached vs. fresh data
- **Error Rate**: Failed requests / total requests
- **User Sessions**: Active concurrent users

---

## 🚀 CI/CD Pipeline

### GitHub Actions Example

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t churn-portal:latest .
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REPO
          docker tag churn-portal:latest $ECR_REPO/churn-portal:latest
          docker push $ECR_REPO/churn-portal:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster prod --service churn-portal \
            --force-new-deployment
```

---

## 📋 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Dependencies pinned in `requirements.txt`
- [ ] Environment variables configured
- [ ] Database connections tested
- [ ] Authentication enabled
- [ ] HTTPS/TLS configured
- [ ] Rate limiting active
- [ ] Logging configured
- [ ] Health checks implemented
- [ ] Backup strategy in place
- [ ] Disaster recovery plan documented
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## 🔄 Rollback Procedures

### Docker Container Rollback
```bash
# Tag previous working version
docker tag churn-portal:latest churn-portal:previous

# Revert to previous
docker run -p 8501:8501 churn-portal:previous
```

### ECS Rollback
```bash
# Get previous task definition
aws ecs describe-task-definition --task-definition churn-portal:1

# Update service with previous version
aws ecs update-service --cluster prod --service churn-portal \
  --task-definition churn-portal:1
```

---

## 📞 Support & Troubleshooting

**Port Already in Use**
```bash
# Find process using port 8501
lsof -i :8501
# Kill process
kill -9 <PID>
```

**Out of Memory**
- Increase container memory allocation
- Reduce dataset size or implement pagination
- Enable data caching with longer TTL

**Connection Timeout**
- Check database connectivity
- Verify firewall rules
- Check proxy/load balancer configuration

For additional support, contact the DevOps team.
