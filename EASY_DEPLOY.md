# 🚀 Easy Deploy: API Key on Backend

Deploy MHLABA with **your API key** - users don't enter anything!

## How It Works

```
User → Netlify (Frontend) → Your Backend (has API key) → OpenAI/Anthropic
                              ↑
                         YOUR API KEY (safe on server)
```

**Users never see your API key!**

---

## Step 1: Get an API Key

### Option A: Groq (FREE & Fast!) ⭐ Recommended
1. Go to https://console.groq.com/keys
2. Create free account
3. Copy your API key
4. **Free tier**: 20 requests/minute, 1M tokens/day

### Option B: OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create API key
3. Add billing (pay-as-you-go)

### Option C: Anthropic
1. Go to https://console.anthropic.com/settings/keys
2. Create API key
3. Add billing

---

## Step 2: Deploy Backend (Render.com)

### 2.1 Fork/Use This Repo
Make sure your code is on GitHub: `MusaBrown/Mhlaba-AI`

### 2.2 Create Render Account
1. Go to https://dashboard.render.com
2. Sign up with GitHub

### 2.3 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect `MusaBrown/Mhlaba-AI`
3. Configure:
   - **Name**: `mhlaba-api`
   - **Root Directory**: `mhlaba-api`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Plan**: Free (or paid for better performance)

### 2.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:

**For Groq (Recommended):**
```
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama3-8b-8192
```

**For OpenAI:**
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

**For Anthropic:**
```
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

### 2.5 Deploy
Click **"Create Web Service"**

Wait 2-3 minutes for deployment.

### 2.6 Copy Your API URL
After deployment, you'll get a URL like:
```
https://mhlaba-api.onrender.com
```

Copy this!

---

## Step 3: Update Frontend

### 3.1 Edit Config File
Edit `mhlaba-web/src/config.js`:

```javascript
// Replace with your Render URL
export const API_URL = 'https://mhlaba-api.onrender.com';

// This is ignored now - backend uses its own key
export const DEFAULT_MODEL = 'groq-llama3';
```

### 3.2 Push to GitHub
```bash
git add .
git commit -m "Update API URL"
git push origin main
```

---

## Step 4: Deploy Frontend (Netlify)

### Option A: Git Auto-Deploy
1. Go to https://app.netlify.com
2. **Add new site** → **Import from GitHub**
3. Select `MusaBrown/Mhlaba-AI`
4. Build settings:
   - **Base directory**: `mhlaba-web`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
5. Click **Deploy**

### Option B: Manual Upload
```bash
cd mhlaba-web
npm install
npm run build
```

Then drag `dist` folder to https://app.netlify.com/drop

---

## ✅ Done!

Your site is live! Users can chat without entering any API keys.

**Test it:**
1. Visit your Netlify URL
2. Type a message
3. AI responds using YOUR backend key!

---

## 💰 Cost Estimates

| Provider | Free Tier | Paid Cost |
|----------|-----------|-----------|
| **Groq** | 1M tokens/day | $0.10-0.30/M tokens |
| **OpenAI** | $5 credit (3 months) | $0.50-30/M tokens |
| **Anthropic** | $5 credit | $0.80-75/M tokens |

**Groq is cheapest and fastest!**

---

## 🔒 Security

- ✅ API key stays on YOUR server
- ✅ Users never see the key
- ✅ No one can steal it from frontend code

---

## 🐛 Troubleshooting

### "API Key Missing" Error
- Check environment variables in Render dashboard
- Redeploy after adding variables

### CORS Error
Add your Netlify domain to `mhlaba-api/src/index.js`:
```javascript
origin: [
  'https://mhlaba-ai-xxx.netlify.app',  // Your domain
],
```

### Slow Responses
- Upgrade Render to paid plan ($7/month)
- Or use Groq (faster than OpenAI)

---

## 📞 Need Help?

Check the full guide: [DEPLOY_OLLAMA.md](DEPLOY_OLLAMA.md)
