#!/usr/bin/env python3
"""
Smart Music Spotify Setup Script
This script helps you configure Spotify credentials and create the .env file
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create the .env file with Spotify configuration"""
    env_content = """# Smart Music Backend Environment Variables
# Fill in your Spotify Developer App credentials below

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
"""
    
    env_path = Path('backend') / '.env'
    if env_path.exists():
        print(f"⚠️  .env file already exists at {env_path}")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Keeping existing .env file")
            return
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created .env file at {env_path}")
        print("📝 Please edit this file with your actual Spotify credentials")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    return True

def get_spotify_credentials():
    """Get Spotify credentials from user input"""
    print("\n🎵 Spotify Developer App Setup")
    print("=" * 40)
    print("1. Go to https://developer.spotify.com/dashboard")
    print("2. Create a new app or use existing one")
    print("3. Copy the Client ID and Client Secret")
    print("4. Add this redirect URI to your app:")
    print("   http://127.0.0.1:5500/frontend/profile.html")
    print()
    
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Client Secret are required")
        return None, None
    
    return client_id, client_secret

def update_env_file():
    """Update the .env file with actual credentials"""
    env_path = Path('backend') / '.env'
    if not env_path.exists():
        print("❌ .env file not found. Run setup first.")
        return False
    
    client_id, client_secret = get_spotify_credentials()
    if not client_id or not client_secret:
        return False
    
    try:
        # Read existing content
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace placeholder values
        content = content.replace('your_spotify_client_id_here', client_id)
        content = content.replace('your_spotify_client_secret_here', client_secret)
        
        # Write updated content
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("✅ Updated .env file with your Spotify credentials")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    print("🎵 Smart Music Spotify Setup")
    print("=" * 30)
    
    if not os.path.exists('backend'):
        print("❌ Please run this script from the project root directory")
        return
    
    while True:
        print("\nOptions:")
        print("1. Create .env file template")
        print("2. Update .env file with credentials")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            update_env_file()
        elif choice == '3':
            print("👋 Setup complete!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
