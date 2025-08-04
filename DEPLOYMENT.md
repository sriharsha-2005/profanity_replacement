# 🚀 Deployment Guide for Render

This guide will help you deploy your Video Profanity Replacement app to Render.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub (✅ Done!)
2. **Render Account**: Sign up at https://render.com

## 🎯 Step-by-Step Deployment

### 1. Sign up for Render
- Go to https://render.com
- Sign up with your GitHub account (recommended) or email

### 2. Create a New Web Service
1. **Click "New +"** in your Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository**:
   - Choose "Connect a repository"
   - Select `sriharsha-2005/profanity_replacement`
   - Click "Connect"

### 3. Configure the Service
Fill in these settings:

**Basic Settings:**
- **Name**: `profanity-replacement-app` (or any name you prefer)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT`

**Advanced Settings (Optional):**
- **Auto-Deploy**: ✅ Enabled (recommended)
- **Health Check Path**: `/` (optional)

### 4. Deploy
1. **Click "Create Web Service"**
2. **Wait for the build** (usually 2-5 minutes)
3. **Your app will be live** at the provided URL

## 🔧 Important Notes

### FFmpeg Dependency
⚠️ **Important**: Your app requires FFmpeg for video processing. Render doesn't include FFmpeg by default.

**Solution**: Add a build script to install FFmpeg:

1. **Create a `build.sh` file** in your repository:
```bash
#!/usr/bin/env bash
# Install FFmpeg
apt-get update
apt-get install -y ffmpeg
```

2. **Update your `render.yaml`**:
```yaml
services:
  - type: web
    name: profanity-replacement-app
    env: python
    buildCommand: |
      chmod +x build.sh
      ./build.sh
      pip install -r requirements.txt
    startCommand: gunicorn run:app --bind 0.0.0.0:$PORT
```

### Environment Variables
You can set these in Render dashboard:
- `FLASK_ENV`: `production`
- `PORT`: (auto-set by Render)

## 🌐 Access Your App

Once deployed, your app will be available at:
`https://your-app-name.onrender.com`

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`

2. **FFmpeg Not Found**:
   - Add the build script mentioned above
   - Or use a different deployment platform that supports FFmpeg

3. **App Crashes**:
   - Check the logs in Render dashboard
   - Ensure `gunicorn` is in requirements.txt

### Alternative Platforms

If Render doesn't work due to FFmpeg limitations, consider:

1. **Railway**: https://railway.app
2. **Heroku**: https://heroku.com (requires credit card)
3. **DigitalOcean App Platform**: https://digitalocean.com

## 📞 Support

If you encounter issues:
1. Check the Render logs
2. Verify all files are committed to GitHub
3. Ensure `requirements.txt` includes all dependencies

---

**Your GitHub Repository**: https://github.com/sriharsha-2005/profanity_replacement.git 