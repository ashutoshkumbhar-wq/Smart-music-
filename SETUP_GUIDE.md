# 🚀 Smart Music - Complete Setup Guide

## 📋 **Prerequisites**

Before starting, ensure you have:
- **Python 3.8+** (Python 3.11 recommended)
- **Modern web browser** (Chrome, Firefox, Edge)
- **Spotify account** (Premium recommended for full functionality)
- **Camera access** (for gesture recognition)
- **Internet connection**

## 🎯 **Quick Start (5 Minutes)**

### **Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/smart-musicoff.git
cd smart-musicoff
```

### **Step 2: Install Dependencies**
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### **Step 3: Set Up Spotify Credentials**
```bash
# Copy environment template
cp backend/env.template backend/.env

# Edit the .env file with your Spotify credentials
# Get them from: https://developer.spotify.com/dashboard
```

### **Step 4: Start the Application**
```bash
# Terminal 1: Start Backend
cd backend
python app_simple.py

# Terminal 2: Start Frontend
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

### **Step 5: Access the Application**
- **Main App**: `http://127.0.0.1:5500/`
- **Gesture Test**: `http://127.0.0.1:5500/gesture-test-simple.html`
- **Spotify Connect**: `http://127.0.0.1:5500/profile.html`

## 🔧 **Detailed Setup**

### **1. Spotify Developer Setup**

#### **Create Spotify App**
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create App"
3. Fill in details:
   - **App name**: Smart Music
   - **App description**: AI-powered music experience
   - **Website**: `http://127.0.0.1:5500`
   - **Redirect URI**: `http://localhost:3000/callback`
4. Click "Save"

#### **Get Credentials**
1. Click on your app
2. Copy **Client ID**
3. Click "Show Client Secret" and copy it
4. Add to `backend/.env` file

### **2. Environment Configuration**

Create `backend/.env` file:
```env
# Spotify API Credentials
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:3000/callback

# Flask Settings
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=3000

# Gesture Recognition
GESTURE_CONFIDENCE_THRESHOLD=0.3
GESTURE_STABLE_FRAMES=5
GESTURE_ACTION_COOLDOWN=1.0
```

### **3. Backend Options**

#### **Option A: Full Backend (with MediaPipe)**
```bash
cd backend
python app.py
```
- ✅ Full gesture recognition
- ❌ May have MediaPipe DLL issues on Windows

#### **Option B: Simple Backend (recommended)**
```bash
cd backend
python app_simple.py
```
- ✅ No MediaPipe dependency
- ✅ More stable on Windows
- ⚠️ Gesture recognition requires MediaPipe

### **4. Frontend Setup**

#### **Start Frontend Server**
```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

#### **Alternative: Node.js Server**
```bash
cd frontend
npx serve -s . -l 5500
```

## 🎭 **Gesture Recognition Setup**

### **Your Trained Model**
The system includes your pre-trained gesture model:
- `Gesture final/gesture_model.pkl` - Trained model
- `Gesture final/scaler.pkl` - Feature scaler
- **8 Gestures**: play_right, pause_right, next_right, previous_right, volume_up_left, volume_down_left, like_left, skip30_left

### **Testing Gestures**
1. Open `http://127.0.0.1:5500/gesture-test-simple.html`
2. Allow camera permissions
3. Click camera button
4. Toggle "Gesture Recognition" ON
5. Make your trained gestures

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Backend Won't Start**
```bash
# Check Python version
python --version

# Install missing dependencies
pip install flask flask-cors python-dotenv spotipy requests pillow

# Try simple backend
python app_simple.py
```

#### **2. Spotify Connection Fails**
- Check `.env` file has correct credentials
- Verify redirect URI matches exactly
- Ensure Spotify app is open and playing music
- Check Spotify Developer Dashboard settings

#### **3. Camera Not Working**
- Allow camera permissions in browser
- Check if camera is used by another app
- Try different browser (Chrome recommended)
- Check browser console for errors

#### **4. Gestures Not Detected**
- Ensure camera is active
- Check lighting conditions
- Make gestures clearly visible
- Check confidence threshold (default: 0.3)

### **Debug Information**

#### **Backend Health Check**
```bash
curl http://localhost:3000/api/health
```

#### **Browser Console**
- Press F12 to open developer tools
- Check Console tab for errors
- Check Network tab for API calls

#### **Backend Logs**
- Watch terminal output for error messages
- Look for "✅" success indicators
- Check for "❌" error messages

## 📱 **Browser Compatibility**

| Browser | Version | Camera | Gestures | Notes |
|---------|---------|--------|----------|-------|
| Chrome | 80+ | ✅ | ✅ | Recommended |
| Firefox | 75+ | ✅ | ✅ | Good support |
| Edge | 80+ | ✅ | ✅ | Good support |
| Safari | 13+ | ⚠️ | ⚠️ | Limited support |

## 🎯 **Success Indicators**

You'll know everything is working when you see:

### **Backend**
- ✅ "Smart Music Backend API" at `/api/health`
- ✅ "Spotify initialized successfully"
- ✅ "Gesture models loaded successfully"

### **Frontend**
- ✅ No CORS errors in console
- ✅ "Connected to Spotify" message
- ✅ Camera starts without errors
- ✅ Gesture recognition toggle works

### **Spotify Integration**
- ✅ "Connected to Spotify as [Your Name]"
- ✅ Current track information displays
- ✅ Gesture actions control Spotify playback

## 🚀 **Production Deployment**

### **Environment Variables**
```env
# Production settings
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=3000
SECRET_KEY=your-production-secret-key

# Spotify (same as development)
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=https://yourdomain.com/callback
```

### **Deployment Options**
- **Heroku**: Easy deployment with Procfile
- **DigitalOcean**: VPS with Docker
- **AWS**: EC2 with load balancer
- **Vercel**: Frontend deployment

## 📞 **Support**

### **Getting Help**
1. Check this setup guide
2. Review troubleshooting section
3. Check browser console for errors
4. Verify all prerequisites are met

### **Common Solutions**
- **Restart both servers** if issues persist
- **Clear browser cache** and cookies
- **Check firewall settings** for port access
- **Update Python packages** if needed

---

**🎵 Your Smart Music system should now be working perfectly! 🎵**

*Enjoy controlling Spotify with hand gestures!*
