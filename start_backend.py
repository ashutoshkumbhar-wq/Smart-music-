#!/usr/bin/env python3
"""
Smart Music Backend Startup Script
This script sets up and runs the Flask backend server
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'opencv-python', 'mediapipe', 
        'numpy', 'Pillow', 'joblib', 'spotipy', 'requests', 'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_models():
    """Check if gesture models exist"""
    model_path = "Gesture final/gesture_model.pkl"
    scaler_path = "Gesture final/scaler.pkl"
    
    if not os.path.exists(model_path):
        print(f"❌ Gesture model not found: {model_path}")
        return False
    
    if not os.path.exists(scaler_path):
        print(f"❌ Gesture scaler not found: {scaler_path}")
        return False
    
    print("✅ Gesture models found")
    return True

def setup_environment():
    """Load environment variables from backend/.env if present and validate."""
    env_path = Path('backend') / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from {env_path}")
    else:
        print("⚠️ backend/.env not found. Using process environment only.")

    cid = os.environ.get('SPOTIPY_CLIENT_ID')
    csec = os.environ.get('SPOTIPY_CLIENT_SECRET')
    redir = os.environ.get('SPOTIPY_REDIRECT_URI') or 'http://127.0.0.1:5000/callback'
    os.environ['SPOTIPY_REDIRECT_URI'] = redir

    if not cid or not csec:
        print("\n❌ Missing Spotify credentials.")
        print("   Please create backend/.env with:")
        print("   SPOTIPY_CLIENT_ID=your_client_id")
        print("   SPOTIPY_CLIENT_SECRET=your_client_secret")
        print("   SPOTIPY_REDIRECT_URI=http://127.0.0.1:5000/callback")
        # Continue to start so the server can run for non-Spotify features
    else:
        print("✅ Spotify credentials detected (client id + secret)")

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Smart Music Backend Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📱 Frontend can be accessed at: frontend/index.html")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory and start server
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("🎵 Smart Music Backend Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Please run this script from the project root directory")
        print("   Expected structure:")
        print("   smart-music/")
        print("   ├── backend/")
        print("   ├── frontend/")
        print("   └── start_backend.py")
        return
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        if input("Install missing dependencies? (y/n): ").lower() == 'y':
            if not install_dependencies():
                return
        else:
            print("❌ Cannot continue without required dependencies")
            return
    
    # Check models
    if not check_models():
        print("⚠️  Gesture recognition will not work without models")
        print("   You can still use the DJ functionality")
    
    # Setup environment
    setup_environment()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
