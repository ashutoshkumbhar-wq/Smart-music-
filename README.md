# 🎵 Smart Music - AI-Powered Music Experience Platform

A cutting-edge web application that combines music streaming, gesture recognition, and AI-powered music recommendations to create an immersive and personalized music experience. Control your Spotify with hand gestures and enjoy intelligent music automation.

## 🎯 **Latest Updates (v2.0)**
- ✅ **Full Spotify Integration** - Complete OAuth 2.0 authentication
- ✅ **8 Trained Gestures** - Hand gesture recognition for music control
- ✅ **Real-time Control** - Live gesture detection with Spotify actions
- ✅ **Unified Interface** - Touch gestures + camera gestures combined
- ✅ **Production Ready** - Comprehensive error handling and debugging

## ✨ Features

### 🎧 **Core Music Features**
- **Music Streaming Interface** - Modern, responsive music player with full controls
- **Playlist Management** - Add and manage custom playlists
- **Music Categories** - Browse through various music genres (Bollywood, LOFI, Classical, Remix, Pop, Electronic)
- **Latest Releases** - Discover new music with curated recommendations
- **Featured Artists** - Explore and follow your favorite musicians
- **Search Functionality** - Powerful search with real-time results

### 🎭 **AI-Powered Features**
- **Gesture Recognition** - Control music playback with 8 trained hand gestures
- **Touch Gestures** - Swipe, tap, and double-tap controls as backup
- **Smart Recommendations** - AI-driven music suggestions based on your preferences
- **DJ Automation** - Automated music queuing and playlist management
- **Real-time Feedback** - Visual feedback for gesture detection and Spotify actions

### 🔐 **Integration & Connectivity**
- **Spotify Integration** - Full Spotify API integration with OAuth authentication
- **Profile Management** - Personalized user profiles with music preferences
- **Cross-Platform** - Responsive design that works on all devices
- **Real-time Control** - Live gesture recognition and music control

### 🎨 **Visual Experience**
- **Dynamic Backgrounds** - Animated particle systems and visual effects
- **Modern UI/UX** - Clean, intuitive interface with smooth animations
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Interactive Elements** - Hover effects, transitions, and micro-interactions

## 🏗️ Project Structure

```
smart-musicoff/
├── frontend/                    # Frontend web application
│   ├── index.html              # Main dashboard with gesture controls
│   ├── gesture-test-simple.html # Simple gesture testing interface
│   ├── gesture-test.html       # Advanced gesture testing interface
│   ├── camera.html             # Original gesture recognition interface
│   ├── profile.html            # Spotify connection & DJ controls
│   ├── script.js               # Main application logic
│   ├── camera.js               # Gesture recognition logic
│   ├── profile.js              # Profile management logic
│   ├── spotify.js              # Spotify API integration
│   ├── unified-gesture-controller.js # Unified gesture system
│   ├── style.css               # Main stylesheet
│   ├── camera.css              # Camera interface styles
│   ├── profile.css             # Profile page styles
│   ├── Cards/                  # Music category browsing
│   │   ├── Page/              # Genre selection pages
│   │   └── artist/            # Artist discovery pages
│   └── profile img/            # User profile images
├── backend/                     # Flask backend API
│   ├── app.py                  # Main Flask application with MediaPipe
│   ├── app_simple.py           # Simplified backend (no MediaPipe dependency)
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (create this)
│   ├── env.template            # Environment variables template
│   └── README.md               # Backend documentation
├── Gesture final/              # Machine Learning models
│   ├── gesture_model.pkl       # Trained gesture recognition model
│   ├── scaler.pkl              # Feature scaling model
│   ├── collect_gestures.py     # Data collection script
│   └── train_model_strong.py   # Model training script
├── Models/                      # DJ and music logic
│   └── Models/                 # DJ automation modules
├── spotify-backend/            # Node.js Spotify backend (alternative)
├── setup_spotify.py            # Spotify credentials setup script
├── start_backend.py            # Backend startup script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (Python 3.11 recommended for best compatibility)
- **Modern web browser** with camera access
- **Spotify account** (for full functionality)
- **Internet connection**

### Step 1: Clone the Repository
```bash
git clone https://github.com/sid003j/smart-music.git
cd smart-music
```

### Step 2: Set Up Spotify Credentials

#### Option A: Use the Setup Script (Recommended)
```bash
python setup_spotify.py
```
Choose option 1 to create .env template, then option 2 to add your credentials.

#### Option B: Manual Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app or use existing one
3. Copy Client ID and Client Secret
4. Add redirect URI: `http://127.0.0.1:5500/frontend/profile.html`
5. Create `backend/.env` file with your credentials

### Step 3: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Start the Backend
```bash
# From project root
python start_backend.py
```
The backend will start on `http://localhost:5000`

### Step 5: Start the Frontend
In a **new terminal window**:
```bash
# From project root
python -m http.server 5500
```

### Step 6: Access the Application
- **Main App**: `http://127.0.0.1:5500/frontend/index.html`
- **Spotify Connect**: `http://127.0.0.1:5500/frontend/profile.html`
- **Gesture Recognition**: `http://127.0.0.1:5500/frontend/camera.html`

## 🔧 Detailed Setup Instructions

### Environment Variables (.env file)

Create a `backend/.env` file with the following content:

```env
# Smart Music Backend Environment Variables

# Flask Settings
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# Spotify API Credentials (REQUIRED)
SPOTIPY_CLIENT_ID=your_spotify_client_id_here
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:5500/frontend/profile.html

# Gesture Recognition Settings
GESTURE_CONFIDENCE_THRESHOLD=0.3
GESTURE_STABLE_FRAMES=5
GESTURE_ACTION_COOLDOWN=1.0

# DJ Settings
DJ_DEFAULT_BATCH_SIZE=150
DJ_STRICT_PRIMARY=1

# Model Paths (relative to backend directory)
GESTURE_MODEL_PATH=../Gesture final/gesture_model.pkl
GESTURE_SCALER_PATH=../Gesture final/scaler.pkl

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5000,http://127.0.0.1:5000,http://localhost:5500,http://127.0.0.1:5500
```

### Spotify Developer Portal Setup

1. **Go to Spotify Developer Dashboard**
   - Visit: https://developer.spotify.com/dashboard
   - Log in with your Spotify account

2. **Create a New App**
   - Click "Create App"
   - Fill in app details:
     - **App name**: Smart Music (or any name you prefer)
     - **App description**: AI-powered music experience platform
     - **Website**: `http://127.0.0.1:5500`
     - **Redirect URI**: `http://127.0.0.1:5500/frontend/profile.html`
     - **API/SDKs**: Web API

3. **Get Your Credentials**
   - Go to your app settings
   - Copy the **Client ID**
   - Copy the **Client Secret**
   - Add these to your `.env` file

4. **Important Notes**
   - Keep your Client Secret secure
   - The redirect URI must match exactly
   - You need a Spotify Premium account for playback control

### Running the Application

#### Backend (Flask API)
```bash
# Option 1: Use startup script (recommended)
python start_backend.py

# Option 2: Direct Flask run
cd backend
python app.py

# Option 3: Flask development server
cd backend
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000
```

#### Frontend (Static Web Server)
```bash
# Option 1: Python HTTP server
python -m http.server 5500

# Option 2: Node.js serve (if you have Node.js)
npx serve -s . -l 5500

# Option 3: Any other static file server
# Just serve the frontend directory on port 5500
```

## 🎭 Gesture Recognition System

### **8 Trained Gestures**
The system recognizes 8 specific hand gestures trained with your custom model:

**Right Hand (Playback Control):**
- `play_right` → Play music
- `pause_right` → Pause music  
- `next_right` → Next track
- `previous_right` → Previous track

**Left Hand (Utility Control):**
- `volume_up_left` → Increase volume (+10%)
- `volume_down_left` → Decrease volume (-10%)
- `like_left` → Like/save current track
- `skip30_left` → Skip 30 seconds forward

**Touch Gestures (Backup):**
- **Swipe Left** → Previous track
- **Swipe Right** → Next track
- **Swipe Up** → Play/Pause toggle
- **Swipe Down** → Volume down
- **Tap** → Play/Pause toggle
- **Double Tap** → Next track

### **How to Use Gesture Recognition**

#### **Option 1: Simple Test Interface (Recommended)**
1. Open `http://127.0.0.1:5500/gesture-test-simple.html`
2. Allow camera permissions when prompted
3. Click the camera button to start video feed
4. Toggle "Gesture Recognition" to ON
5. Make your trained hand gestures
6. Watch real-time detection and Spotify actions

#### **Option 2: Main Application**
1. Open `http://127.0.0.1:5500/`
2. Enable camera gestures via toggle
3. Make gestures while music is playing
4. Enjoy seamless Spotify control

#### **Option 3: Advanced Interface**
1. Open `http://127.0.0.1:5500/gesture-test.html`
2. Full camera interface with debugging
3. Real-time confidence monitoring
4. Advanced gesture testing features

### Gesture Recognition Settings
- **Confidence Threshold**: 0.3 (30%) - adjustable in `.env`
- **Stable Frames**: 5 frames required for stable detection
- **Action Cooldown**: 1 second between actions
- **Detection Frequency**: Every 500ms

## 🎧 DJ System

### Features
- **Automated Music Queuing**: Queue up to 500 tracks automatically
- **Genre-based Selection**: Choose from Remix, LOFI, or Mashup
- **Artist Filtering**: Select specific artists or random selection
- **Batch Processing**: Configurable track batch sizes
- **Real-time Status**: Live session monitoring

### How to Use DJ System
1. Open `http://127.0.0.1:5500/frontend/profile.html`
2. Connect to Spotify (if not already connected)
3. Look for the "🎵 DJ Controls" section
4. Configure your session:
   - **Mode**: Random or Artist-based
   - **Genre**: Remix, LOFI, or Mashup
   - **Artists**: Comma-separated list (for artist mode)
   - **Batch Size**: Number of tracks to queue (10-500)
5. Click "Start DJ Session"
6. Keep Spotify app open and playing music

### DJ Session Modes
- **Random Mode**: Generates random tracks based on genre tags
- **Artist Mode**: Generates tracks from specific artists
- **Genre Options**: Remix, LOFI, Mashup
- **Batch Sizes**: 10-500 tracks per session

## 📡 API Endpoints

### Base URL
```
http://localhost:5000
```

### Available Endpoints

#### Health Check
```
GET /api/health
```
Returns server health status and loaded modules.

#### Gesture Recognition
```
POST /api/gesture/predict
```
Predicts gesture from base64-encoded image data.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "gesture": "play_right",
  "confidence": 0.95,
  "probabilities": [0.01, 0.95, 0.04],
  "threshold": 0.3
}
```

#### DJ Session Control
```
POST /api/spotify/dj/start
```
Starts a DJ session with specified parameters.

**Request Body:**
```json
{
  "mode": "random",
  "genre": "Remix",
  "artists": [],
  "batch_size": 150,
  "strict_primary": true
}
```

**Response:**
```json
{
  "ok": true,
  "mode": "random",
  "genre": "Remix",
  "batch": 150,
  "hint": "Random · Remix",
  "started": 1,
  "queued": 149
}
```

#### Configuration
```
GET /api/config
```
Returns current configuration settings.

#### Gesture Classes
```
GET /api/gesture/classes
```
Returns available gesture classes and confidence threshold.

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SPOTIPY_CLIENT_ID` | Required | Spotify Client ID |
| `SPOTIPY_CLIENT_SECRET` | Required | Spotify Client Secret |
| `SPOTIPY_REDIRECT_URI` | `http://127.0.0.1:5500/frontend/profile.html` | Spotify redirect URI |
| `GESTURE_CONFIDENCE_THRESHOLD` | `0.3` | Minimum confidence for gesture recognition |
| `GESTURE_STABLE_FRAMES` | `5` | Frames required for stable gesture detection |
| `GESTURE_ACTION_COOLDOWN` | `1.0` | Cooldown between gesture actions (seconds) |
| `DJ_DEFAULT_BATCH_SIZE` | `150` | Default number of tracks to queue |
| `DJ_STRICT_PRIMARY` | `1` | Only use primary artist for filtering |
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `5000` | Server port |

### CORS Configuration
The backend is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5000`
- `http://127.0.0.1:5000`
- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `null` (for local file testing)

## 🛠️ Troubleshooting

### Common Issues

#### 1. Backend Won't Start
**Error**: `ModuleNotFoundError` or dependency issues
**Solution**:
```bash
# Check Python version
python --version

# Install dependencies one by one
pip install flask flask-cors python-dotenv
pip install opencv-python mediapipe numpy Pillow
pip install scikit-learn joblib spotipy requests

# Or use the startup script
python start_backend.py
```

#### 2. Spotify Connection Fails
**Error**: OAuth authentication failed
**Solution**:
1. Check `.env` file exists and has correct credentials
2. Verify redirect URI matches exactly: `http://127.0.0.1:5500/frontend/profile.html`
3. Ensure Spotify app is open and playing music
4. Check Spotify Developer Dashboard settings

#### 3. Gesture Recognition Not Working
**Error**: Camera not accessible or models not loading
**Solution**:
1. Allow camera permissions in browser
2. Check that `gesture_model.pkl` and `scaler.pkl` exist in `Gesture final/` directory
3. Verify backend is running on port 5000
4. Check browser console for errors

#### 4. CORS Errors
**Error**: `Access to fetch at 'http://localhost:5000' has been blocked`
**Solution**:
1. Ensure backend is running on port 5000
2. Ensure frontend is served on port 5500
3. Check CORS configuration in backend
4. Clear browser cache and cookies

#### 5. DJ Sessions Failing
**Error**: "No active Spotify device" or "DJ Session failed"
**Solution**:
1. Ensure Spotify is running and playing music
2. Check Spotify Premium subscription
3. Verify Spotify API credentials
4. Check backend logs for detailed error messages

### Debug Information
- **Backend Logs**: Check console output when running `python start_backend.py`
- **Browser Console**: Press F12 and check Console tab for JavaScript errors
- **Network Tab**: Check if API calls are successful
- **Health Endpoint**: Visit `http://localhost:5000/api/health` for system status

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:5000/api/health

# Get configuration
curl http://localhost:5000/api/config

# Get gesture classes
curl http://localhost:5000/api/gesture/classes
```

### Test Frontend
1. Open `http://127.0.0.1:5500/frontend/index.html`
2. Check for JavaScript errors in browser console
3. Test camera functionality
4. Test Spotify connection
5. Test DJ controls

## 📱 Browser Support

- **Chrome** 80+ (Recommended)
- **Firefox** 75+
- **Safari** 13+
- **Edge** 80+

## 🔮 Future Enhancements

### Planned Features
- **Voice Commands** - Speech-to-text integration
- **Emotion Detection** - Mood-based music selection
- **Advanced Gestures** - Complex hand movement recognition
- **Mobile App** - Native mobile application
- **Social Features** - Share playlists and sessions
- **Offline Mode** - Download music for offline listening

### Technical Improvements
- **Model Retraining** - Enhanced gesture recognition accuracy
- **Performance Optimization** - Faster response times
- **Scalability** - Support for multiple concurrent users
- **Cloud Deployment** - Production-ready hosting solution

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Guidelines
- Follow existing code style and structure
- Test on multiple devices and browsers
- Ensure accessibility standards are met
- Document new features and changes
- Add tests for new functionality

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Spotify** for their comprehensive Web API
- **MediaPipe** for hand landmark detection
- **scikit-learn** for machine learning framework
- **Flask** for web framework
- **Inter Font Family** for beautiful typography

## 📞 Support

For support, questions, or feedback:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the API documentation
- Contact the development team

---

**Made with ❤️ for music lovers everywhere**

*Smart Music - Where Technology Meets Musical Passion*

---

## 🎯 Success Indicators

You'll know everything is working when you see:
- ✅ Backend shows "Smart Music Backend API" at `/api/health`
- ✅ Frontend loads without CORS errors
- ✅ Spotify shows "Connected to Spotify (backend)"
- ✅ Camera starts and gesture recognition works
- ✅ DJ controls appear and can start sessions

**🎵 Your Smart Music system should now work perfectly! 🎵**