# 🚀 Deploy MHLABA to Netlify

This guide will walk you through deploying MHLABA web interface to Netlify.

## Prerequisites

- A Netlify account (free at https://netlify.com)
- Node.js 18+ installed locally (for testing)
- Git installed (optional, for CI/CD deploy)

## Method 1: Drag and Drop (Easiest) ⭐

### Step 1: Build the Project

```bash
# Navigate to web directory
cd mhlaba-web

# Install dependencies
npm install

# Build for production
npm run build
```

### Step 2: Deploy to Netlify

1. Go to https://app.netlify.com/drop
2. Drag and drop the `mhlaba-web/dist` folder onto the page
3. Wait a few seconds for deployment
4. Your site is live! 🎉

## Method 2: Git-based Deployment (Recommended for Updates)

### Step 1: Create a Git Repository

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Create GitHub repository (via web or CLI)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/mhlaba.git
git push -u origin main
```

### Step 2: Connect to Netlify

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Select **GitHub** (or your Git provider)
4. Find and select your `mhlaba` repository
5. Configure build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
   - **Base directory**: `mhlaba-web` (if not in root)
6. Click **"Deploy site"**

Netlify will automatically build and deploy your site. Future pushes to your repository will trigger automatic redeploys!

## Method 3: Netlify CLI

### Step 1: Install Netlify CLI

```bash
npm install -g netlify-cli
```

### Step 2: Login

```bash
netlify login
```

### Step 3: Initialize and Deploy

```bash
cd mhlaba-web

# Initialize (first time only)
netlify init

# Build and deploy
npm run build
netlify deploy --prod --dir=dist
```

## 🌍 Custom Domain (Optional)

1. In Netlify dashboard, go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `mhlaba.yourdomain.com`)
4. Follow DNS configuration instructions

## 🔒 Environment Variables (Optional)

If you need to set environment variables:

1. In Netlify dashboard, go to **Site settings** → **Environment variables**
2. Click **"Add variable"**
3. Add your variables

Note: For this app, API keys are stored in the browser's localStorage, not in environment variables.

## 🔄 Continuous Deployment

With Git-based deployment, every push to your main branch automatically redeploys your site!

To disable auto-deploy:
1. Go to **Site settings** → **Build & deploy**
2. Scroll to **Build settings**
3. Toggle **"Auto publish"**

## 📊 Monitoring

View deployment logs:
1. Go to your site dashboard
2. Click **"Deploys"** tab
3. Click on any deploy to see detailed logs

## 🛠️ Troubleshooting

### Build Fails

**Error: "npm not found"**
- Set NODE_VERSION environment variable to 18 in Netlify settings

**Error: "Module not found"**
- Make sure `node_modules` is in `.gitignore`
- Netlify will run `npm install` automatically

### Site Shows 404

- Check that `netlify.toml` redirects are correct
- Verify `publish` directory in `netlify.toml` matches your build output

### API Calls Fail

This is expected! The browser makes direct API calls to OpenAI/Anthropic:
- API keys are stored in browser localStorage
- No backend server needed
- CORS is handled by the AI providers

## 📱 Post-Deployment

### First Time Setup

1. Visit your deployed site
2. Click the **Settings** (gear) icon
3. Enter your OpenAI or Anthropic API key
4. Start chatting!

### Share Your Site

Your friends can use your deployed MHLABA:
- They'll need their own API key
- All data stays in their browser
- No accounts or sign-ups required!

---

## 🎉 Success!

Your MHLABA AI assistant is now live on the internet!

**Next steps:**
- Customize the theme in `App.css`
- Add your own logo
- Share with friends

---

Need help? Check the [Netlify Docs](https://docs.netlify.com/) or open an issue!
