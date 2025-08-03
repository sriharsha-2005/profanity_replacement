# 🔧 502 Bad Gateway - Troubleshooting Guide

## 🚨 Problem
You're getting a 502 Bad Gateway error when trying to access your deployed app on Render.

## 🔍 Root Causes & Solutions

### 1. **Configuration Conflict (Most Likely)**
**Problem**: Your `render.yaml` was overriding the custom `gunicorn.conf.py` settings.

**Solution**: ✅ **FIXED** - Updated `render.yaml` to use the custom config:
```yaml
startCommand: gunicorn -c gunicorn.conf.py run:app
```

### 2. **Memory Issues**
**Problem**: AI models (Whisper + Edge TTS) consume too much memory.

**Solutions**:
- ✅ Single worker configuration
- ✅ Memory optimization in code
- ✅ Garbage collection calls
- ✅ 300-second timeout

### 3. **Import Errors**
**Problem**: Python modules not importing correctly.

**Solution**: Run the test script:
```bash
python test_app.py
```

### 4. **FFmpeg Missing**
**Problem**: FFmpeg not installed in the deployment environment.

**Solution**: ✅ **FIXED** - `build.sh` installs FFmpeg:
```bash
apt-get install -y ffmpeg
```

## 🚀 **Immediate Steps to Fix**

### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Fix 502 error: use custom gunicorn config and add health endpoint"
git push
```

### Step 2: Monitor Deployment
1. Go to your Render dashboard
2. Check the build logs for any errors
3. Look for these success indicators:
   - ✅ "Build completed successfully"
   - ✅ "Service is live"

### Step 3: Test the Health Endpoint
Once deployed, test: `https://your-app.onrender.com/health`

Expected response:
```json
{"status": "healthy", "message": "Server is running"}
```

## 🔍 **Debugging Steps**

### 1. Check Render Logs
In your Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. Look for error messages

### 2. Common Error Messages & Solutions

**"ModuleNotFoundError"**:
- Check if all dependencies are in `requirements.txt`
- Ensure Python version is correct (3.9.16)

**"FFmpeg not found"**:
- Verify `build.sh` is executable
- Check if FFmpeg installation succeeded

**"Worker timeout"**:
- Already fixed with 300-second timeout
- Single worker configuration

**"Memory exceeded"**:
- Already optimized with garbage collection
- Single worker prevents conflicts

### 3. Test Locally First
```bash
# Test the app locally
python test_app.py

# Test Gunicorn locally
python test_gunicorn.py
```

## 🛠️ **Alternative Solutions**

### If Still Getting 502:

1. **Simplify the Start Command**:
   ```yaml
   startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 run:app
   ```

2. **Add Environment Variables**:
   ```yaml
   envVars:
     - key: GUNICORN_TIMEOUT
       value: "300"
     - key: GUNICORN_WORKERS
       value: "1"
   ```

3. **Use a Different Python Version**:
   ```yaml
   envVars:
     - key: PYTHON_VERSION
       value: 3.8.16
   ```

## 📊 **Monitoring Your App**

### Health Check Endpoints
- `/` - Main page
- `/health` - Health status

### Expected Behavior
- ✅ App starts within 2-3 minutes
- ✅ Health endpoint returns 200 OK
- ✅ Main page loads without errors
- ✅ No timeout errors in logs

## 🚨 **Emergency Fixes**

### If Nothing Works:

1. **Restart the Service**:
   - Go to Render dashboard
   - Click "Manual Deploy"
   - Select "Clear build cache & deploy"

2. **Check Resource Limits**:
   - Render free tier has limitations
   - Consider upgrading if needed

3. **Simplify the App**:
   - Temporarily remove AI processing
   - Test with basic Flask app first

## 📞 **Getting Help**

### Check These First:
1. ✅ Render build logs
2. ✅ Application logs
3. ✅ Health endpoint response
4. ✅ Local testing results

### If Still Stuck:
1. Share the exact error from Render logs
2. Test the health endpoint URL
3. Check if the build completed successfully

## 🎯 **Success Indicators**

Your app is working correctly when:
- ✅ Build completes without errors
- ✅ Service shows "Live" status
- ✅ `/health` returns `{"status": "healthy"}`
- ✅ Main page loads in browser
- ✅ No 502 errors

---

**Next Steps**: Commit the changes and redeploy. The 502 error should be resolved! 