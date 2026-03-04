# 🚀 Deploy MHLABA with Ollama Backend

This guide explains how to deploy the **complete MHLABA system** with:
- **Backend**: Ollama API server (mhlaba-api)
- **Frontend**: React web app (mhlaba-web)

## 📋 Overview

```
┌─────────────────┐      HTTP API      ┌─────────────────┐
│  mhlaba-web     │  ◄──────────────►  │  mhlaba-api     │
│  (Frontend)     │                    │  (Backend)      │
│  Netlify        │                    │  Render/Docker  │
└─────────────────┘                    └─────────────────┘
```

## Step 1: Deploy the Backend (Ollama API)

### Option A: Render.com (Easiest) ⭐

**Note**: Render free tier has limitations. For Ollama, you may need a paid plan or use Docker on a VPS.

1. **Fork this repo** to your GitHub account

2. **Create Ollama Web Service on Render:**
   - Go to https://dashboard.render.com
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repo
   - **Name**: `mhlaba-ollama`
   - **Environment**: Docker
   - **Dockerfile Path**: `mhlaba-api/Dockerfile`
   - **Plan**: Standard or higher (needs 2GB+ RAM for Ollama)

3. **Add Environment Variables:**
   - `DEFAULT_MODEL`: `llama3.2`

4. **Deploy**

5. **Pull a model** (one-time):
   ```bash
   curl -X POST https://your-render-url.onrender.com/api/pull \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.2"}'
   ```

### Option B: Railway.app

1. Go to https://railway.app
2. Create new project → Deploy from GitHub repo
3. Select `mhlaba-api` directory
4. Deploy

### Option C: Docker on VPS (Most Control)

1. **Get a VPS** (DigitalOcean, AWS, Hetzner, etc.)
   - Minimum: 2 vCPU, 4GB RAM, 20GB SSD

2. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

3. **Clone and deploy:**
   ```bash
   git clone https://github.com/MusaBrown/Mhlaba-AI.git
   cd Mhlaba-AI/mhlaba-api
   
   # Pull and start
   docker-compose up -d
   
   # Pull a model
   docker exec mhlaba-ollama ollama pull llama3.2
   ```

4. **Your API is at**: `http://your-vps-ip:3001`

### Option D: Local Machine (Testing)

1. **Install Ollama:** https://ollama.com/download

2. **Pull a model:**
   ```bash
   ollama pull llama3.2
   ```

3. **Run Ollama server:**
   ```bash
   ollama serve
   ```

4. **Run API:**
   ```bash
   cd mhlaba-api
   npm install
   npm start
   ```

5. **API is at**: `http://localhost:3001`

---

## Step 2: Update Frontend Config

1. **Edit `mhlaba-web/src/config.js`:**

   ```javascript
   // Replace with your deployed API URL
   export const API_URL = 'https://mhlaba-api.onrender.com';
   // or
   export const API_URL = 'http://your-vps-ip:3001';
   ```

2. **Update CORS in `mhlaba-api/src/index.js`:**

   ```javascript
   const corsOptions = {
     origin: [
       'http://localhost:3000',
       // Add your Netlify domain after deploying frontend:
       'https://mhlaba-ai-xxx.netlify.app',
     ],
     // ...
   };
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update API URL"
   git push origin main
   ```

---

## Step 3: Deploy Frontend to Netlify

### One-Click Deploy

1. Go to https://app.netlify.com
2. **Add new site** → **Import an existing project**
3. Select `MusaBrown/Mhlaba-AI`
4. **Build settings:**
   - **Base directory**: `mhlaba-web`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. **Deploy**

### Environment Variable (Optional)

In Netlify dashboard:
- Go to **Site settings** → **Environment variables**
- Add: `REACT_APP_API_URL` = `https://your-api-url.com`
- Update `config.js` to use this variable

---

## 🔗 Testing Your Deployment

### Test API
```bash
curl https://your-api-url.com/api/health
# Should return: {"status":"ok","ollama":"connected"}
```

### Test Chat
```bash
curl -X POST https://your-api-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

---

## 💰 Cost Estimates

| Service | Plan | Cost/Month |
|---------|------|-----------|
| **Netlify** (Frontend) | Free | $0 |
| **Render** (Backend) | Standard | $25+ |
| **Railway** (Backend) | Starter | $5+ |
| **VPS** (Hetzner/DigitalOcean) | 4GB RAM | $6-12 |

**Cheapest option**: VPS (Hetzner CX21 - €5.35/month)

---

## 🛠️ Recommended Models

Install on your Ollama server:

```bash
# Small & fast (default)
ollama pull llama3.2

# Better quality
ollama pull llama3.1:8b

# Best quality (needs more RAM)
ollama pull llama3.1:70b

# Code-focused
ollama pull codellama:7b
```

Update `DEFAULT_MODEL` in your API environment variables.

---

## 🔄 Updating After Deployment

### Update Backend
```bash
# Pull changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Update Frontend
Just push to GitHub → Netlify auto-redeploys!

---

## 🐛 Troubleshooting

### "CORS error"
Add your Netlify domain to `corsOptions.origin` in `mhlaba-api/src/index.js`

### "Model not found"
SSH into your server and pull the model:
```bash
docker exec mhlaba-ollama ollama pull llama3.2
```

### "Out of memory"
- Use a smaller model (llama3.2 instead of llama3.1:70b)
- Upgrade your server RAM
- Or use a quantized model (q4_0, q5_0)

---

## 📞 Support

Issues? Check:
1. API health: `/api/health`
2. Ollama logs: `docker logs mhlaba-ollama`
3. API logs: `docker logs mhlaba-api`
