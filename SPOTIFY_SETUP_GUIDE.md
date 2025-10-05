# Smart Music - Spotify Integration & Gesture Controls Setup Guide

This guide will help you set up Spotify OAuth 2.0 authentication and configure gesture controls for your Smart Music application.

## 🎵 Spotify Setup

### 1. Create a Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - **App Name**: `Smart Music Controller`
   - **App Description**: `Gesture-controlled music player with Spotify integration`
   - **Website**: `http://localhost:5000` (or your domain)
   - **Redirect URI**: `http://localhost:5000/callback`
5. Click "Save"

### 2. Get Your Credentials

After creating the app, you'll see:
- **Client ID**: Copy this value
- **Client Secret**: Click "Show Client Secret" and copy this value

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory with your Spotify credentials:

```env
# Spotify API Credentials
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback

# Optional: Additional Spotify Settings
SPOTIFY_SCOPES=user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-modify
SPOTIFY_CACHE_PATH=.cache-dj-session

# Flask Settings
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# Gesture Recognition Settings
GESTURE_CONFIDENCE_THRESHOLD=0.3
GESTURE_STABLE_FRAMES=5
GESTURE_ACTION_COOLDOWN=1.0

# DJ Settings
DJ_DEFAULT_BATCH_SIZE=150
DJ_STRICT_PRIMARY=1

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000,http://127.0.0.1:5000,http://localhost:5500,http://127.0.0.1:5500,null
```

### 4. Update Redirect URIs in Spotify Dashboard

Make sure to add these redirect URIs in your Spotify app settings:
- `http://localhost:5000/callback`
- `http://127.0.0.1:5000/callback`
- `http://localhost:5500/frontend/profile.html` (for frontend-only auth)

## 🎭 Gesture Controls Setup

### Touch/Mouse Gestures (Hammer.js)

The application automatically includes Hammer.js for touch and mouse gesture recognition. No additional setup is required.

**Supported Gestures:**
- **Swipe Left** → Previous Track
- **Swipe Right** → Next Track  
- **Swipe Up** → Play/Pause Toggle
- **Swipe Down** → Volume Down
- **Tap** → Play/Pause Toggle
- **Double Tap** → Next Track

### Camera-Based Hand Gestures (Optional)

For camera-based gesture recognition, you need to:

1. **Enable Camera Access**: The browser will prompt for camera permission
2. **Ensure Backend is Running**: Camera gestures require the Python backend with gesture models
3. **Toggle Camera Mode**: Use the camera button in the UI to enable/disable

**Supported Hand Gestures:**
- **Fist** → Pause
- **Open Palm** → Play
- **Thumbs Up** → Next Track
- **Thumbs Down** → Previous Track
- **Peace Sign** → Volume Up

## 🚀 Running the Application

### 1. Start the Backend Server

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

### 2. Start the Frontend

You can serve the frontend using any static file server:

**Option A: Python HTTP Server**
```bash
cd frontend
python -m http.server 5500
```

**Option B: Live Server (VS Code)**
- Install Live Server extension
- Right-click on `index.html` → "Open with Live Server"

**Option C: Node.js http-server**
```bash
npm install -g http-server
cd frontend
http-server -p 5500
```

### 3. Access the Application

Open your browser and go to:
- Main App: `http://localhost:5500`
- Profile/Spotify Setup: `http://localhost:5500/profile.html`

## 🔧 Configuration Options

### Gesture Sensitivity

You can adjust gesture sensitivity by modifying these values in the frontend:

```javascript
window.gestureController = new GestureController({
  backendUrl: 'http://localhost:5000',
  enableTouchGestures: true,
  enableCameraGestures: false,
  gestureThreshold: 0.3,    // Lower = more sensitive
  cooldownMs: 1000          // Minimum time between gestures
});
```

### Backend Gesture Settings

Modify these in your `.env` file:

```env
GESTURE_CONFIDENCE_THRESHOLD=0.3  # 0.1-1.0, lower = more sensitive
GESTURE_STABLE_FRAMES=5           # Frames needed for stable detection
GESTURE_ACTION_COOLDOWN=1.0       # Seconds between actions
```

## 🎯 Usage Instructions

### 1. Connect to Spotify

1. Open the application in your browser
2. Click on the profile icon or go to `/profile.html`
3. Click "Connect with Spotify"
4. Authorize the application in the Spotify popup
5. You'll be redirected back with a success message

### 2. Enable Gesture Controls

**Touch/Mouse Gestures:**
1. Click the "Gestures" button in the bottom-right corner
2. The button will turn green when enabled
3. Use swipe gestures on any part of the screen

**Camera Gestures:**
1. Click the "Camera" button in the bottom-right corner
2. Allow camera access when prompted
3. A small camera preview will appear
4. Make hand gestures in front of the camera

### 3. Control Music

Once connected to Spotify and with gestures enabled:

- **Play Music**: Start playing music on any Spotify device (desktop app, mobile app, web player)
- **Control with Gestures**: Use the supported gestures to control playback
- **Manual Controls**: Use the control buttons in the Spotify status panel
- **View Current Track**: The current track info will be displayed automatically

## 🔍 Troubleshooting

### Common Issues

**1. "Not authenticated" Error**
- Make sure you've completed the Spotify OAuth flow
- Check that your Client ID and Secret are correct in `.env`
- Verify the redirect URI matches exactly

**2. "No active Spotify device" Error**
- Make sure Spotify is open and playing on any device
- Try playing a song first, then use the controls

**3. Gestures Not Working**
- Check browser console for errors
- Ensure Hammer.js is loaded (check Network tab)
- Try refreshing the page

**4. Camera Gestures Not Working**
- Allow camera permissions in your browser
- Make sure the backend is running
- Check that gesture models are loaded (check backend logs)

**5. CORS Errors**
- Make sure the backend is running on the correct port
- Check that CORS origins include your frontend URL
- Try accessing via `localhost` instead of `127.0.0.1`

### Debug Mode

Enable debug logging by opening browser console (F12) and looking for:
- `🎭 Gesture Controller initialized`
- `🎵 Spotify authenticated`
- `✅ Gesture action executed`

## 📱 Mobile Support

The application is fully responsive and supports:
- Touch gestures on mobile devices
- Camera gestures using mobile cameras
- Responsive UI that adapts to screen size

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Use environment variables in production
- Consider using HTTPS for production deployments
- Regularly rotate your Spotify Client Secret

## 🆘 Support

If you encounter issues:

1. Check the browser console for JavaScript errors
2. Check the backend logs for Python errors
3. Verify all environment variables are set correctly
4. Ensure all required dependencies are installed
5. Try the troubleshooting steps above

## 📋 Dependencies

### Backend Dependencies
- Flask
- Flask-CORS
- spotipy
- mediapipe
- opencv-python
- scikit-learn
- numpy
- pillow

### Frontend Dependencies
- Hammer.js (loaded via CDN)
- Font Awesome (loaded via CDN)

All dependencies are automatically loaded from CDNs, so no additional installation is required for the frontend.
