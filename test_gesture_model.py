#!/usr/bin/env python3
"""
Test script to verify your gesture model is working correctly
Run this from the project root directory
"""

import os
import sys
import joblib
import numpy as np

# Add the Gesture final directory to path
sys.path.append('Gesture final')

def test_gesture_model():
    """Test the gesture model loading and basic functionality"""
    
    print("🧪 Testing Gesture Model Integration...")
    print("=" * 50)
    
    # Check if model files exist
    model_path = "Gesture final/gesture_model.pkl"
    scaler_path = "Gesture final/scaler.pkl"
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
        
    if not os.path.exists(scaler_path):
        print(f"❌ Scaler file not found: {scaler_path}")
        return False
    
    print(f"✅ Model file found: {model_path}")
    print(f"✅ Scaler file found: {scaler_path}")
    
    try:
        # Load the model and scaler
        print("\n📦 Loading model and scaler...")
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        print("✅ Model loaded successfully")
        print("✅ Scaler loaded successfully")
        
        # Check model properties
        if hasattr(model, 'classes_'):
            classes = list(model.classes_)
            print(f"📊 Model classes: {classes}")
            print(f"📊 Number of classes: {len(classes)}")
        else:
            print("⚠️ Model doesn't have classes_ attribute")
        
        # Test with dummy data (42 features as per your spec)
        print("\n🧪 Testing with dummy data...")
        dummy_features = np.random.rand(1, 42).astype(np.float32)
        print(f"📊 Dummy features shape: {dummy_features.shape}")
        
        # Scale the features
        scaled_features = scaler.transform(dummy_features)
        print(f"📊 Scaled features shape: {scaled_features.shape}")
        
        # Make prediction
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(scaled_features)[0]
            predicted_class = model.classes_[np.argmax(probabilities)]
            confidence = float(np.max(probabilities))
            
            print(f"🎯 Predicted class: {predicted_class}")
            print(f"🎯 Confidence: {confidence:.3f}")
            print(f"🎯 All probabilities: {dict(zip(model.classes_, probabilities))}")
        else:
            prediction = model.predict(scaled_features)[0]
            print(f"🎯 Predicted class: {prediction}")
        
        print("\n✅ Model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_integration():
    """Test if the backend can load the model"""
    
    print("\n🔧 Testing Backend Integration...")
    print("=" * 50)
    
    try:
        # Try to import the backend modules
        sys.path.append('backend')
        from app import gesture_model, gesture_scaler
        
        if gesture_model is None:
            print("❌ Backend failed to load gesture model")
            return False
            
        if gesture_scaler is None:
            print("❌ Backend failed to load gesture scaler")
            return False
        
        print("✅ Backend successfully loaded gesture model")
        print("✅ Backend successfully loaded gesture scaler")
        
        # Test the feature extraction function
        print("\n🧪 Testing feature extraction...")
        
        # Create dummy hand landmarks (simulating MediaPipe output)
        class DummyLandmark:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        class DummyHandLandmarks:
            def __init__(self):
                # Create 21 landmarks (wrist + 20 finger joints)
                self.landmark = []
                for i in range(21):
                    self.landmark.append(DummyLandmark(
                        np.random.rand(), 
                        np.random.rand()
                    ))
        
        dummy_hand = DummyHandLandmarks()
        
        # Test the feature extraction (same as in your maintesting_spotify.py)
        def to_feature_vec(hand_landmarks):
            base_x = hand_landmarks.landmark[0].x
            base_y = hand_landmarks.landmark[0].y
            vec = []
            for lm in hand_landmarks.landmark:
                vec.append(lm.x - base_x)
                vec.append(lm.y - base_y)
            return np.array(vec, dtype=np.float32).reshape(1, -1)  # (1,42)
        
        features = to_feature_vec(dummy_hand)
        print(f"📊 Extracted features shape: {features.shape}")
        
        # Test scaling
        scaled_features = gesture_scaler.transform(features)
        print(f"📊 Scaled features shape: {scaled_features.shape}")
        
        # Test prediction
        if hasattr(gesture_model, 'predict_proba'):
            probabilities = gesture_model.predict_proba(scaled_features)[0]
            predicted_class = gesture_model.classes_[np.argmax(probabilities)]
            confidence = float(np.max(probabilities))
            
            print(f"🎯 Predicted class: {predicted_class}")
            print(f"🎯 Confidence: {confidence:.3f}")
        
        print("✅ Backend integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing backend integration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎵 Smart Music - Gesture Model Test")
    print("=" * 50)
    
    # Test 1: Model loading
    model_ok = test_gesture_model()
    
    # Test 2: Backend integration
    backend_ok = test_backend_integration()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Model Loading: {'✅ PASS' if model_ok else '❌ FAIL'}")
    print(f"   Backend Integration: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    
    if model_ok and backend_ok:
        print("\n🎉 All tests passed! Your gesture model is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Start the backend: cd backend && python app.py")
        print("   2. Start the frontend: cd frontend && python -m http.server 5500")
        print("   3. Open: http://127.0.0.1:5500/gesture-test.html")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
