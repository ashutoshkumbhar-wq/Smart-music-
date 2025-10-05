#!/usr/bin/env python3
"""
Simplified backend for Smart Music without MediaPipe dependency
Uses your trained gesture model for image-based gesture recognition
"""

import os
import sys
import base64
import io
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:3000/callback')
    PORT = int(os.getenv('PORT', 3000))

# Load gesture recognition models
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Gesture final", "gesture_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Gesture final", "scaler.pkl")

try:
    gesture_model = joblib.load(MODEL_PATH)
    gesture_scaler = joblib.load(SCALER_PATH)
    print("✅ Gesture models loaded successfully")
    print(f"📊 Model classes: {list(gesture_model.classes_) if hasattr(gesture_model, 'classes_') else 'Unknown'}")
except Exception as e:
    print(f"❌ Error loading gesture models: {e}")
    gesture_model = None
    gesture_scaler = None

# Initialize Spotify
sp = None
if Config.SPOTIPY_CLIENT_ID and Config.SPOTIPY_CLIENT_SECRET:
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=Config.SPOTIPY_CLIENT_ID,
            client_secret=Config.SPOTIPY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIPY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state user-library-modify"
        ))
        print("✅ Spotify initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Spotify: {e}")
        sp = None
else:
    print("⚠️ Spotify credentials not configured")

# CORS headers
@app.after_request
def after_request(response):
    try:
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    except Exception:
        pass
    return response

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "spotify_configured": sp is not None,
        "gesture_models": gesture_model is not None and gesture_scaler is not None
    })

# Spotify authentication status
@app.route('/api/spotify/status', methods=['GET'])
def spotify_status():
    if not sp:
        return jsonify({"authenticated": False, "error": "Spotify not configured"})
    
    try:
        user = sp.current_user()
        return jsonify({
            "authenticated": True,
            "user": {
                "id": user.get('id'),
                "name": user.get('display_name'),
                "email": user.get('email')
            }
        })
    except Exception as e:
        return jsonify({"authenticated": False, "error": str(e)})

# Spotify OAuth callback
@app.route('/callback', methods=['GET'])
def spotify_callback():
    return send_from_directory('../frontend', 'profile.html')

# Get current playback
@app.route('/api/spotify/current', methods=['GET'])
def get_current_track():
    if not sp:
        return jsonify({"ok": False, "error": "Spotify not configured"})
    
    try:
        playback = sp.current_playback()
        if not playback or not playback.get('item'):
            return jsonify({"ok": True, "playing": False})
        
        track = playback['item']
        return jsonify({
            "ok": True,
            "playing": True,
            "track": {
                "name": track.get('name', 'Unknown'),
                "artists": [artist['name'] for artist in track.get('artists', [])],
                "album_art": track.get('album', {}).get('images', [{}])[0].get('url', ''),
                "duration_ms": track.get('duration_ms', 0)
            },
            "playback": {
                "is_playing": playback.get('is_playing', False),
                "progress_ms": playback.get('progress_ms', 0)
            }
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# Get available devices
@app.route('/api/spotify/devices', methods=['GET'])
def get_devices():
    if not sp:
        return jsonify({"ok": False, "error": "Spotify not configured"})
    
    try:
        devices = sp.devices()
        return jsonify({"ok": True, "devices": devices.get('devices', [])})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# Transfer playback to device
@app.route('/api/spotify/transfer', methods=['POST'])
def transfer_playback():
    if not sp:
        return jsonify({"ok": False, "error": "Spotify not configured"})
    
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        if not device_id:
            return jsonify({"ok": False, "error": "device_id required"})
        
        sp.transfer_playback(device_id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# Spotify control actions
@app.route('/api/spotify/control', methods=['POST'])
def spotify_control():
    if not sp:
        return jsonify({"ok": False, "error": "Spotify not configured"})
    
    try:
        data = request.get_json()
        action = data.get('action')
        delta = data.get('delta', 0)
        
        # Get active device
        devices = sp.devices()
        device_list = devices.get('devices', [])
        if not device_list:
            return jsonify({"ok": False, "error": "No devices available"})
        
        active_device = next((d for d in device_list if d.get('is_active')), device_list[0])
        device_id = active_device.get('id')
        
        if action == 'play':
            sp.start_playback(device_id=device_id)
        elif action == 'pause':
            sp.pause_playback(device_id=device_id)
        elif action == 'next':
            sp.next_track(device_id=device_id)
        elif action == 'previous':
            sp.previous_track(device_id=device_id)
        elif action == 'volume':
            cur_v = active_device.get('volume_percent', 50)
            new_v = max(0, min(100, cur_v + delta))
            sp.volume(new_v, device_id=device_id)
        elif action == 'seek':
            pb = sp.current_playback()
            if not pb or not pb.get('item'):
                return jsonify({"ok": False, "error": "No current playback"})
            pos = pb.get('progress_ms', 0)
            dur = pb['item'].get('duration_ms', 0)
            new_pos = min(max(0, pos + delta), max(0, dur - 1000))
            sp.seek_track(new_pos, device_id=device_id)
        elif action == 'like':
            pb = sp.current_playback()
            if not pb or not pb.get('item'):
                return jsonify({"ok": False, "error": "No current playback"})
            track_id = pb['item'].get('id')
            if track_id:
                sp.current_user_saved_tracks_add([track_id])
            else:
                return jsonify({"ok": False, "error": "No track ID"})
        else:
            return jsonify({"ok": False, "error": "Unknown action"})
        
        return jsonify({"ok": True, "action": action})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

# Gesture prediction endpoint (simplified - no MediaPipe)
@app.route('/api/gesture/predict', methods=['POST'])
def predict_gesture():
    if not gesture_model or not gesture_scaler:
        return jsonify({"gesture": "none", "confidence": 0.0, "error": "Gesture models not loaded"})
    
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"gesture": "none", "confidence": 0.0, "error": "No image data"})
        
        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to expected size (you may need to adjust this based on your training data)
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # For now, return a dummy prediction since we don't have MediaPipe
        # In a real implementation, you'd need to extract hand landmarks
        # and convert them to the 42-dimensional feature vector
        
        # This is a placeholder - you'll need to implement proper hand landmark extraction
        # or use a different approach for gesture recognition
        
        return jsonify({
            "gesture": "none",
            "confidence": 0.0,
            "message": "Gesture recognition requires MediaPipe. Please use the main app.py with MediaPipe installed."
        })
        
    except Exception as e:
        return jsonify({"gesture": "none", "confidence": 0.0, "error": str(e)})

# Play specific track
@app.route('/api/spotify/play', methods=['POST'])
def play_track():
    if not sp:
        return jsonify({"ok": False, "error": "Spotify not configured"})
    
    try:
        data = request.get_json()
        track_uri = data.get('track_uri')
        query = data.get('query')
        
        if track_uri:
            sp.start_playback(uris=[track_uri])
        elif query:
            results = sp.search(q=query, type='track', limit=1)
            tracks = results['tracks']['items']
            if tracks:
                sp.start_playback(uris=[tracks[0]['uri']])
            else:
                return jsonify({"ok": False, "error": "Track not found"})
        else:
            return jsonify({"ok": False, "error": "track_uri or query required"})
        
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == '__main__':
    print(f"🚀 Starting Smart Music Backend on port {Config.PORT}")
    print(f"📁 Serving frontend from: {os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
