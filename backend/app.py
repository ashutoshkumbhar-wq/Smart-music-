from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import os
import sys
import joblib
import numpy as np
import cv2
import mediapipe as mp
import base64
from PIL import Image
import io
import json
import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Import configuration
try:
    from config import Config
except ImportError:
    print("Warning: config.py not found, using default values")
    class Config:
        GESTURE_CONFIDENCE_THRESHOLD = 0.8
        GESTURE_STABLE_FRAMES = 5
        GESTURE_ACTION_COOLDOWN = 1.0
        DJ_DEFAULT_BATCH_SIZE = 150
        DJ_STRICT_PRIMARY = True

# Add the gesture models path
sys.path.append('../Gesture final')

# Import your existing modules
try:
    sys.path.append('../Models/Models')
    from artists_gig_backfriend import run_once as dj_run_once
    print("✅ DJ module imported successfully")
except ImportError as e:
    print(f"Warning: DJ module not available: {e}")
    dj_run_once = None

app = Flask(__name__)
# Allow frontend origins including local file server and dev ports
_cors_origins = getattr(Config, 'CORS_ORIGINS', [
    'http://localhost:3000', 'http://127.0.0.1:3000',
    'http://localhost:5000', 'http://127.0.0.1:5000',
    'http://localhost:5500', 'http://127.0.0.1:5500',
    'null'
])
CORS(app, resources={r"/*": {"origins": _cors_origins}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    try:
        origin = request.headers.get('Origin')
        if origin and origin in _cors_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Vary'] = 'Origin'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    except Exception:
        pass
    return response

# Load gesture recognition models
MODEL_PATH = getattr(Config, 'GESTURE_MODEL_PATH', "../Gesture final/gesture_model.pkl")
SCALER_PATH = getattr(Config, 'GESTURE_SCALER_PATH', "../Gesture final/scaler.pkl")

try:
    gesture_model = joblib.load(MODEL_PATH)
    gesture_scaler = joblib.load(SCALER_PATH)
    print("✅ Gesture models loaded successfully")
    print(f"📊 Model classes: {list(gesture_model.classes_) if hasattr(gesture_model, 'classes_') else 'Unknown'}")
except Exception as e:
    print(f"❌ Error loading gesture models: {e}")
    gesture_model = None
    gesture_scaler = None

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

@app.route('/')
def index():
    return jsonify({
        "message": "Smart Music Backend API", 
        "status": "running",
        "version": "1.0.0",
        "features": {
            "gesture_recognition": gesture_model is not None,
            "dj_control": dj_run_once is not None,
            "spotify_integration": True
        }
    })

@app.route('/api/gesture/predict', methods=['POST'])
def predict_gesture():
    if not gesture_model or not gesture_scaler:
        return jsonify({"error": "Gesture models not loaded"}), 500
    
    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400
        
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return jsonify({"error": f"Invalid image data: {str(e)}"}), 400
        
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        rgb_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        
        # Debug: Log image dimensions
        print(f"🔍 Image dimensions: {rgb_image.shape}")
        
        results = hands.process(rgb_image)
        
        # Debug: Log hand detection results
        if results.multi_hand_landmarks:
            print(f"✅ Hand detected! Number of hands: {len(results.multi_hand_landmarks)}")
            hand_landmarks = results.multi_hand_landmarks[0]
            print(f"📏 Hand landmarks: {len(hand_landmarks.landmark)} points")
            
            # Debug: Log first few landmark positions
            for i, landmark in enumerate(hand_landmarks.landmark[:5]):
                print(f"   Landmark {i}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}")
        else:
            print("❌ No hand detected in image")
            return jsonify({"gesture": "none", "confidence": 0.0, "message": "No hand detected"})
        
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Use your exact feature extraction method
        def to_feature_vec(hand_landmarks):
            base_x = hand_landmarks.landmark[0].x
            base_y = hand_landmarks.landmark[0].y
            vec = []
            for lm in hand_landmarks.landmark:
                vec.append(lm.x - base_x)
                vec.append(lm.y - base_y)
            return np.array(vec, dtype=np.float32).reshape(1, -1)  # (1,42)
        
        features = to_feature_vec(hand_landmarks)
        
        # Debug: Log feature extraction
        print(f"🔢 Features extracted: {features.shape}")
        print(f"   First 5 features: {features[0][:5]}")
        print(f"   Last 5 features: {features[0][-5:]}")
        
        features_scaled = gesture_scaler.transform(features)
        
        # Debug: Log scaling results
        print(f"⚖️ Features scaled: {features_scaled.shape}")
        print(f"   First 5 scaled: {features_scaled[0][:5]}")
        
        if hasattr(gesture_model, 'predict_proba'):
            probabilities = gesture_model.predict_proba(features_scaled)[0]
            predicted_class = gesture_model.classes_[np.argmax(probabilities)]
            confidence = float(np.max(probabilities))
            
            # Debug: Log all class probabilities
            print(f"🎯 Model prediction results:")
            print(f"   Predicted class: {predicted_class}")
            print(f"   Confidence: {confidence:.3f}")
            print(f"   All probabilities:")
            for i, (cls, prob) in enumerate(zip(gesture_model.classes_, probabilities)):
                print(f"     {cls}: {prob:.3f}")
        else:
            predicted_class = gesture_model.predict(features_scaled)[0]
            confidence = 1.0
        
        threshold = getattr(Config, 'GESTURE_CONFIDENCE_THRESHOLD', 0.3)
        
        # Debug: Log threshold comparison
        print(f"🎚️ Confidence threshold: {threshold}")
        print(f"   Confidence {confidence:.3f} {'>=' if confidence >= threshold else '<'} threshold {threshold}")
        
        if confidence < threshold:
            predicted_class = "none"
            confidence = 0.0
            print(f"   ⚠️ Below threshold, setting to 'none'")
        else:
            print(f"   ✅ Above threshold, keeping prediction: {predicted_class}")
        
        return jsonify({
            "gesture": predicted_class,
            "confidence": confidence,
            "probabilities": probabilities.tolist() if hasattr(gesture_model, 'predict_proba') else None,
            "threshold": threshold
        })
        
    except Exception as e:
        print(f"❌ Gesture prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/spotify/dj/start', methods=['POST'])
def start_dj_session():
    """Start a DJ session with the specified parameters"""
    if not dj_run_once:
        return jsonify({"error": "DJ functionality not available"}), 503
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        mode = data.get('mode', 'random')
        genre = data.get('genre', 'Remix')
        artists = data.get('artists', [])
        batch_size = data.get('batch_size', getattr(Config, 'DJ_DEFAULT_BATCH_SIZE', 150))
        strict_primary = data.get('strict_primary', getattr(Config, 'DJ_STRICT_PRIMARY', True))
        
        # Validate inputs
        if mode not in ['random', 'artist']:
            return jsonify({"error": "Invalid mode. Must be 'random' or 'artist'"}), 400
            
        if genre not in ['Remix', 'LOFI', 'Mashup']:
            return jsonify({"error": "Invalid genre. Must be 'Remix', 'LOFI', or 'Mashup'"}), 400
            
        if mode == 'artist' and not artists:
            return jsonify({"error": "Artists list required for artist mode"}), 400
        
        # Call the DJ function
        result = dj_run_once(
            mode=mode,
            genre=genre,
            artists=artists,
            batch_size=batch_size,
            strict_primary=strict_primary
        )
        
        return jsonify(result)
        
    except Exception as e:
        print(f"DJ session error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": str(datetime.datetime.now()),
        "gesture_models": gesture_model is not None,
        "dj_module": dj_run_once is not None,
        "config": {
            "gesture_confidence_threshold": getattr(Config, 'GESTURE_CONFIDENCE_THRESHOLD', 0.8),
            "dj_batch_size": getattr(Config, 'DJ_DEFAULT_BATCH_SIZE', 150)
        }
    })

@app.route('/api/gesture/classes')
def get_gesture_classes():
    """Get available gesture classes"""
    if not gesture_model:
        return jsonify({"error": "Gesture model not loaded"}), 500
    
    classes = gesture_model.classes_.tolist() if hasattr(gesture_model, 'classes_') else []
    return jsonify({
        "classes": classes,
        "total_classes": len(classes),
        "confidence_threshold": getattr(Config, 'GESTURE_CONFIDENCE_THRESHOLD', 0.8)
    })

@app.route('/api/config')
def get_config():
    """Get current configuration (non-sensitive)"""
    return jsonify({
        "gesture_recognition": {
            "confidence_threshold": getattr(Config, 'GESTURE_CONFIDENCE_THRESHOLD', 0.8),
            "stable_frames": getattr(Config, 'GESTURE_STABLE_FRAMES', 5),
            "action_cooldown": getattr(Config, 'GESTURE_ACTION_COOLDOWN', 1.0)
        },
        "dj": {
            "default_batch_size": getattr(Config, 'DJ_DEFAULT_BATCH_SIZE', 150),
            "strict_primary": getattr(Config, 'DJ_STRICT_PRIMARY', True)
        },
        "server": {
            "host": getattr(Config, 'HOST', '0.0.0.0'),
            "port": getattr(Config, 'PORT', 5000),
            "debug": getattr(Config, 'DEBUG', True)
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ===== Spotify OAuth (server-managed) =====

def _spotify_oauth():
    client_id = getattr(Config, 'SPOTIPY_CLIENT_ID', None)
    client_secret = getattr(Config, 'SPOTIPY_CLIENT_SECRET', None)
    redirect_uri = getattr(Config, 'SPOTIPY_REDIRECT_URI', 'http://localhost:5000/callback')
    scopes = os.environ.get(
        'SPOTIFY_SCOPES',
        'user-modify-playback-state user-read-playback-state user-read-currently-playing user-library-modify'
    )
    cache_path = os.environ.get('SPOTIFY_CACHE_PATH', '.cache-dj-session')
    if not client_id or not client_secret:
        # Return a minimal auth manager which will error on use; endpoints will surface error
        print("⚠️ Spotify credentials not configured")
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
        cache_path=cache_path,
        open_browser=False,
    )

@app.get('/api/spotify/status')
def spotify_status():
    try:
        oauth = _spotify_oauth()
        token_info = oauth.get_cached_token()
        is_authed = bool(token_info)
        status = {"authenticated": is_authed}
        if is_authed:
            sp = spotipy.Spotify(auth=token_info['access_token'])
            try:
                me = sp.current_user()
                status["user"] = {"id": me.get('id'), "name": me.get('display_name') or me.get('id')}
                devices = sp.devices().get('devices', [])
                status["devices"] = [{"id": d.get('id'), "name": d.get('name'), "is_active": d.get('is_active')} for d in devices]
            except Exception:
                pass
        return jsonify(status)
    except Exception as e:
        return jsonify({"authenticated": False, "error": str(e)}), 500

@app.get('/api/spotify/login')
def spotify_login():
    try:
        oauth = _spotify_oauth()
        auth_url = oauth.get_authorize_url()
        return jsonify({"auth_url": auth_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/callback')
def spotify_callback():
    try:
        oauth = _spotify_oauth()
        if not oauth:
            return jsonify({"error": "Spotify OAuth not configured"}), 500
            
        code = request.args.get('code')
        state = request.args.get('state')
        if not code:
            return jsonify({"error": "Missing authorization code"}), 400
            
        token_info = oauth.get_access_token(code)
        # Persisted via cache_path; redirect back to frontend with success
        frontend_url = getattr(Config, 'SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:5500/frontend/profile.html')
        return redirect(f"{frontend_url}?auth=success&expires_in={token_info.get('expires_in', 0)}")
    except Exception as e:
        print(f"Spotify callback error: {e}")
        frontend_url = getattr(Config, 'SPOTIPY_REDIRECT_URI', 'http://127.0.0.1:5500/frontend/profile.html')
        return redirect(f"{frontend_url}?auth=error&message={str(e)}")

@app.post('/api/spotify/play')
def spotify_play_specific():
    """Play a specific track given a Spotify URI or search query."""
    try:
        data = request.get_json(force=True)
        uri = (data or {}).get('uri')
        query = (data or {}).get('query')
        oauth = _spotify_oauth()
        token = oauth.get_cached_token()
        if not token:
            return jsonify({"ok": False, "error": "Not authenticated"}), 401
        sp = spotipy.Spotify(auth=token['access_token'])

        # resolve device
        devices = sp.devices().get('devices', [])
        if not devices:
            return jsonify({"ok": False, "error": "No active Spotify device"}), 400
        device_id = None
        for d in devices:
            if d.get('is_active'):
                device_id = d.get('id'); break
        if not device_id:
            device_id = devices[0].get('id')
            try:
                sp.transfer_playback(device_id=device_id, force_play=True)
            except Exception:
                pass

        target_uri = uri
        if not target_uri and query:
            res = sp.search(q=query, type='track', limit=1)
            items = ((res or {}).get('tracks') or {}).get('items') or []
            if not items:
                return jsonify({"ok": False, "error": "Track not found"}), 404
            target_uri = items[0].get('uri')

        if not target_uri:
            return jsonify({"ok": False, "error": "Provide 'uri' or 'query'"}), 400

        sp.start_playback(device_id=device_id, uris=[target_uri])
        return jsonify({"ok": True, "played": target_uri})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post('/api/spotify/control')
def spotify_control():
    """Generic control endpoint for playback actions from gestures/UI.
    Body: { "action": "play|pause|next|previous|volume|seek", "delta": 10| -10 | 30000 }
    """
    try:
        data = request.get_json(force=True) or {}
        action = (data.get('action') or '').lower()
        delta = int(data.get('delta') or 0)

        oauth = _spotify_oauth()
        token = oauth.get_cached_token()
        if not token:
            return jsonify({"ok": False, "error": "Not authenticated"}), 401
        sp = spotipy.Spotify(auth=token['access_token'])

        devices = sp.devices().get('devices', [])
        if not devices:
            return jsonify({"ok": False, "error": "No active Spotify device"}), 400
        device = next((d for d in devices if d.get('is_active')), devices[0])
        device_id = device.get('id')

        if action == 'play':
            sp.start_playback(device_id=device_id)
        elif action == 'pause':
            sp.pause_playback(device_id=device_id)
        elif action == 'next':
            sp.next_track(device_id=device_id)
        elif action == 'previous':
            sp.previous_track(device_id=device_id)
        elif action == 'volume':
            cur_v = device.get('volume_percent', 50)
            new_v = max(0, min(100, cur_v + (delta if delta else 0)))
            sp.volume(new_v, device_id=device_id)
        elif action == 'seek':
            pb = sp.current_playback()
            if not pb or not pb.get('item'):
                return jsonify({"ok": False, "error": "No current playback"}), 400
            pos = pb.get('progress_ms', 0)
            dur = pb['item'].get('duration_ms', 0)
            new_pos = min(max(0, pos + (delta if delta else 0)), max(0, dur - 1000))
            sp.seek_track(new_pos, device_id=device_id)
        elif action == 'like':
            # Like/save current track
            pb = sp.current_playback()
            if not pb or not pb.get('item'):
                return jsonify({"ok": False, "error": "No current playback"}), 400
            track_id = pb['item'].get('id')
            if track_id:
                sp.current_user_saved_tracks_add([track_id])
            else:
                return jsonify({"ok": False, "error": "No track ID"}), 400
        else:
            return jsonify({"ok": False, "error": "Unknown action"}), 400

        return jsonify({"ok": True, "action": action})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get('/api/spotify/current')
def spotify_current():
    """Get currently playing track information with metadata and progress"""
    try:
        oauth = _spotify_oauth()
        token = oauth.get_cached_token()
        if not token:
            return jsonify({"ok": False, "error": "Not authenticated"}), 401
        
        sp = spotipy.Spotify(auth=token['access_token'])
        playback = sp.current_playback()
        
        if not playback:
            return jsonify({"ok": True, "playing": False, "message": "No active playback"})
        
        track = playback.get('item', {})
        if not track:
            return jsonify({"ok": True, "playing": False, "message": "No track information"})
        
        # Extract track information
        track_info = {
            "id": track.get('id'),
            "name": track.get('name'),
            "artists": [artist.get('name') for artist in track.get('artists', [])],
            "album": track.get('album', {}).get('name'),
            "duration_ms": track.get('duration_ms'),
            "external_urls": track.get('external_urls', {}),
            "preview_url": track.get('preview_url')
        }
        
        # Extract album art
        images = track.get('album', {}).get('images', [])
        if images:
            track_info['album_art'] = images[0].get('url')  # Get largest image
        
        # Extract playback state
        playback_info = {
            "is_playing": playback.get('is_playing', False),
            "progress_ms": playback.get('progress_ms', 0),
            "volume_percent": playback.get('device', {}).get('volume_percent', 0),
            "shuffle_state": playback.get('shuffle_state', False),
            "repeat_state": playback.get('repeat_state', 'off'),
            "device": {
                "id": playback.get('device', {}).get('id'),
                "name": playback.get('device', {}).get('name'),
                "type": playback.get('device', {}).get('type'),
                "is_active": playback.get('device', {}).get('is_active', False)
            }
        }
        
        return jsonify({
            "ok": True,
            "playing": True,
            "track": track_info,
            "playback": playback_info
        })
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get('/api/spotify/devices')
def spotify_devices():
    """Get available Spotify devices"""
    try:
        oauth = _spotify_oauth()
        token = oauth.get_cached_token()
        if not token:
            return jsonify({"ok": False, "error": "Not authenticated"}), 401
        
        sp = spotipy.Spotify(auth=token['access_token'])
        devices = sp.devices().get('devices', [])
        
        return jsonify({
            "ok": True,
            "devices": devices
        })
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.post('/api/spotify/transfer')
def spotify_transfer():
    """Transfer playback to a specific device"""
    try:
        data = request.get_json(force=True) or {}
        device_id = data.get('device_id')
        
        if not device_id:
            return jsonify({"ok": False, "error": "Device ID required"}), 400
        
        oauth = _spotify_oauth()
        token = oauth.get_cached_token()
        if not token:
            return jsonify({"ok": False, "error": "Not authenticated"}), 401
        
        sp = spotipy.Spotify(auth=token['access_token'])
        sp.transfer_playback(device_id=device_id, force_play=True)
        
        return jsonify({"ok": True, "device_id": device_id})
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Print startup information
    print("🎵 Smart Music Backend Starting...")
    print(f"📍 Server will run on {getattr(Config, 'HOST', '0.0.0.0')}:{getattr(Config, 'PORT', 5000)}")
    print(f"🔧 Gesture models: {'✅ Loaded' if gesture_model else '❌ Not loaded'}")
    print(f"🎧 DJ functionality: {'✅ Available' if dj_run_once else '❌ Not available'}")
    print("-" * 50)
    
    app.run(
        debug=getattr(Config, 'DEBUG', True),
        host=getattr(Config, 'HOST', '0.0.0.0'),
        port=getattr(Config, 'PORT', 5000)
    )
