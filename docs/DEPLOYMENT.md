# Deployment Guide

This guide covers deploying **Chat with PDF** to production environments.

## Deployment Options

| Platform | Difficulty | Cost | Recommended For |
|----------|-----------|------|-----------------|
| **Streamlit Cloud** | Easy | Free/$USD | Getting started, small projects |
| **Docker + AWS/GCP** | Medium | $/month | Scalable, production apps |
| **Docker + DigitalOcean** | Medium | $5-15/month | Cost-effective hosting |
| **Heroku** | Easy | Free-$$$ | Simple deployments |
| **Self-hosted** | Hard | Hardware cost | Maximum control |

---

## Option 1: Streamlit Cloud ⭐ (Easiest)

### Why Choose Streamlit Cloud?
- ✅ Free to deploy and host
- ✅ Auto-scaling, no server management
- ✅ SSL/HTTPS built-in
- ✅ GitHub integration for auto-deploys
- ❌ Cold starts can be slow
- ❌ Limited to Streamlit apps

### Step-by-Step Deployment

#### 1. Push Code to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

Ensure these files are in repo:
- `app_enhanced.py`
- `config.py`
- `requirements.txt`

#### 2. Create Streamlit Cloud Account

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **Deploy an app**
4. Select your repository

#### 3. Configure App Settings

1. Set repo, branch, main file path:
   - **Repository**: `YOUR_ORG/chat_with_pdf`
   - **Branch**: `main`
   - **Main file path**: `app_enhanced.py`

2. Click **Deploy**

#### 4. Add Secrets (API Keys)

1. Click **Settings** (gear icon in menu)
2. Go to **Secrets** tab
3. Add your API key:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   DEFAULT_PROVIDER = "openai"
   ```

4. Save and app will auto-refresh

### Secret File Format

Streamlit uses `.streamlit/secrets.toml`:

```toml
# OpenAI
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-3.5-turbo"

# HuggingFace
HUGGINGFACE_API_KEY = "hf_..."

# Ollama (if using local instance)
OLLAMA_BASE_URL = "http://localhost:11434"
```

Note: This file is git-ignored locally, configured via dashboard in cloud.

### Cost

- **Free Tier**: Up to 3 apps, limited resources
- **Professional**: $5/month per app
- **Advanced**: Enterprise pricing

### Streamlit Cloud Limitations

- Apps sleep after 1 hour of inactivity (premium feature to disable)
- Limited RAM: 2GB
- No persistent storage
- Region-locked to US (unless paid)

### Troubleshooting

**App takes long to load**
- Cold start issue on free tier
- Upgrade to Professional tier
- Optimize app startup code

**"Module not found" error**
- Ensure all imports in `requirements.txt`
- Check spelling matches import statements

**Environment variables not loaded**
- Verify in **Settings → Secrets**
- Restart app after adding secrets
- Use `st.secrets["KEY_NAME"]` to access

---

## Option 2: Docker + AWS/GCP

### Prerequisites
- Docker account (https://hub.docker.com)
- AWS/GCP account with credits
- Command line tools installed

### Step-by-Step

#### 1. Build and Push Docker Image

```bash
# Login to Docker
docker login

# Build image
docker build -t YOUR_USERNAME/chat-pdf:latest .

# Push to Docker Hub
docker push YOUR_USERNAME/chat-pdf:latest
```

#### 2. Deploy to AWS ECS

**Using Fargate (serverless):**

```bash
# Create cluster
aws ecs create-cluster --cluster-name chat-pdf-cluster

# Register task definition
aws ecs register-task-definition \
  --family chat-pdf-task \
  --container-definitions '[
    {
      "name": "chat-pdf",
      "image": "YOUR_USERNAME/chat-pdf:latest",
      "portMappings": [{"containerPort": 8501}],
      "environment": [
        {"name": "OPENAI_API_KEY", "value": "sk-your-key"}
      ]
    }
  ]'

# Create service
aws ecs create-service \
  --cluster chat-pdf-cluster \
  --service-name chat-pdf-service \
  --task-definition chat-pdf-task \
  --desired-count 1 \
  --launch-type FARGATE
```

#### 3. Deploy to Google Cloud Run

```bash
# Login to gcloud
gcloud auth login

# Build with Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/chat-pdf

# Deploy to Cloud Run
gcloud run deploy chat-pdf \
  --image gcr.io/PROJECT_ID/chat-pdf \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-your-key
```

### Costs
- **AWS Fargate**: ~$0.03/hour (24/7) = ~$22/month
- **Google Cloud Run**: Free tier + pay per request

---

## Option 3: DigitalOcean App Platform

### Why Choose?
- ✅ Simplest Docker deployment
- ✅ Cheap: $5-15/month
- ✅ Great documentation
- ✅ GitHub integration

### Deployment

#### 1. Push to GitHub (same as Streamlit)

#### 2. Connect to DigitalOcean

1. Create account: https://www.digitalocean.com
2. Click **Apps** → **Create App**
3. Select your GitHub repository
4. Choose **Dockerfile** deployment
5. Configure environment variables:
   ```
   OPENAI_API_KEY=sk-your-key
   DEFAULT_PROVIDER=openai
   ```

#### 3. Deploy

Click **Deploy** and wait ~2-3 minutes.

Your app will be live at: `https://your-app-name.ondigitalocean.app`

### Costs
- Starter: $5/month ($0.15/hour)
- Basic: $15/month ($0.015/hour)

---

## Option 4: Heroku (Deprecated but still works)

Note: Heroku free tier ended in Nov 2022. Paid options available.

### Setup with Procfile

```bash
# Create Procfile
echo "web: streamlit run app_enhanced.py" > Procfile

# Install Heroku CLI and deploy
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-your-key
git push heroku main
```

---

## Option 5: Self-Hosted (Docker)

### Local Machine

```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-key \
  YOUR_USERNAME/chat-pdf:latest
```

### VPS (Linode, Vultr, etc.)

```bash
# SSH into VPS
ssh root@YOUR_VPS_IP

# Install Docker
curl https://get.docker.com | sh

# Pull and run image
docker pull YOUR_USERNAME/chat-pdf:latest
docker run -d -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-key \
  YOUR_USERNAME/chat-pdf:latest

# Access at: http://YOUR_VPS_IP:8501
```

### Docker Compose (Recommended for VPS)

```bash
# Copy docker-compose.yml to server
scp docker-compose.yml root@YOUR_VPS_IP:/home/

# SSH and deploy
ssh root@YOUR_VPS_IP
cd /home
cp .env.example .env
# Edit .env with API keys
docker-compose up -d

# View logs
docker-compose logs -f chat-pdf
```

---

## Production Best Practices

### Security

✅ **Do:**
- Load secrets from environment variables
- Use HTTPS (AWS/GCP handle this)
- Limit resource allocation (RAM, CPU)
- Keep dependencies updated
- Use minimal Docker image (python:3.10-slim)

❌ **Don't:**
- Hardcode API keys in code
- Commit `.env` file
- Use root user in containers
- Expose unnecessary ports

### Monitoring

```bash
# Check Streamlit Cloud logs
streamlit run app_enhanced.py --logger.level=debug

# Monitor Docker containers
docker stats YOUR_USERNAME/chat-pdf

# Health checks
curl https://your-app.streamlit.app/_stcore/health
```

### Scaling

For high traffic:
1. **Streamlit Cloud**: Upgrade to Professional/Advanced
2. **Docker**: Use load balancer (AWS ALB, NGINX)
3. **Database**: Add persistent storage if needed

### Cost Optimization

| Deployment | Monthly Cost | Daily Users |
|-----------|--------------|-----------|
| Streamlit Cloud | Free-$5 | 1-100 |
| DigitalOcean | $5-15 | 100-1000 |
| AWS Fargate | ~$22 | 1000+ |

---

## Deployment Checklist

- [ ] `.env` file with API keys (not committed)
- [ ] `requirements.txt` up-to-date
- [ ] Tests passing locally (`pytest tests/`)
- [ ] Code linted (`black .`, `flake8 .`)
- [ ] GitHub repo clean (no uncommitted changes)
- [ ] Secrets configured in deployment platform
- [ ] Domain configured (if using custom domain)
- [ ] HTTPS enabled (automatic on most platforms)
- [ ] Monitoring/alerts set up
- [ ] Rollback plan in place

---

## Rollback Plan

If deployment fails:

**Streamlit Cloud:**
```bash
git revert HEAD
git push origin main
# Auto-redeploys with previous version
```

**Docker/VPS:**
```bash
docker pull YOUR_USERNAME/chat-pdf:previous-tag
docker run -d -p 8501:8501 YOUR_USERNAME/chat-pdf:previous-tag
```

---

## Custom Domain Setup

### Streamlit Cloud

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Streamlit dashboard: **Settings → Custom domain**
3. Follow DNS configuration instructions
4. Update domain DNS records (CNAME)

### Docker/VPS

Use NGINX as reverse proxy:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Install Let's Encrypt SSL: `certbot certonly --nginx -d yourdomain.com`

---

## Troubleshooting Deployments

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Add missing package to `requirements.txt` |
| `API key not found` | Add secret/env var in deployment settings |
| `Port already in use` | Change port or kill existing process |
| `Out of memory` | Reduce PDF chunk size or upgrade tier |
| `Cold start too slow` | Use paid tier or optimize imports |

---

For more help, check:
- [Streamlit Documentation](https://docs.streamlit.io/deploy)
- [Docker Documentation](https://docs.docker.com)
- [AWS Documentation](https://docs.aws.amazon.com)

Open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues) for deployment problems!
