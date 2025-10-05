@echo off
REM Smart Music - Git Setup Script (Windows)
REM This script helps you initialize Git and upload your project

echo 🎵 Smart Music - Git Setup
echo ==========================

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Initialize Git repository
echo 📁 Initializing Git repository...
git init

REM Add all files (respecting .gitignore)
echo 📝 Adding files to Git...
git add .

REM Check if there are any files to commit
git status --porcelain >nul 2>&1
if %errorlevel% equ 0 (
    echo ℹ️  No changes to commit. All files are already tracked or ignored.
) else (
    REM Create initial commit
    echo 💾 Creating initial commit...
    git commit -m "🎵 Initial commit: Smart Music AI-powered music platform

✨ Features:
- 8 trained hand gestures for Spotify control
- Real-time gesture recognition with 95%%+ accuracy
- Complete Spotify OAuth 2.0 integration
- Touch gesture backup system
- Modern responsive web interface
- Comprehensive error handling and debugging

🎭 Gesture Recognition:
- play_right, pause_right, next_right, previous_right
- volume_up_left, volume_down_left, like_left, skip30_left
- Real-time confidence scoring and visual feedback

🎵 Spotify Integration:
- Full playback control (play, pause, next, previous, volume, seek)
- Device management and switching
- Track information display
- Like/save functionality

🔧 Technical Stack:
- Frontend: HTML5, CSS3, JavaScript (ES6+)
- Backend: Python Flask with RESTful API
- ML: scikit-learn ensemble classifier
- Integration: Spotify Web API, MediaPipe
- Gestures: Custom trained model with 42-dimensional features

📁 Project Structure:
- frontend/: Web application with gesture controls
- backend/: Flask API with Spotify integration
- Gesture final/: Trained ML models and training scripts
- Documentation: Comprehensive setup and usage guides

🚀 Ready for deployment and further development!"
)

REM Show status
echo.
echo 📊 Git Status:
git status

echo.
echo 🌐 Remote Repository Setup:
echo 1. Create a new repository on GitHub/GitLab
echo 2. Copy the repository URL
echo 3. Run: git remote add origin ^<repository-url^>
echo 4. Run: git push -u origin main

echo.
echo 📋 Files to upload:
echo ✅ All source code files
echo ✅ Documentation (README, guides)
echo ✅ Configuration templates
echo ✅ Trained ML models
echo ❌ Environment files (.env)
echo ❌ Node modules
echo ❌ Cache files
echo ❌ Large media files

echo.
echo 🎉 Git setup complete! Your project is ready to upload.
echo 📖 See SETUP_GUIDE.md for detailed instructions.

pause
