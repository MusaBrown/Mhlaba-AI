#!/usr/bin/env python3
"""
Quick Microphone Test for JARVIS
Tests if your microphone is working properly
"""

import speech_recognition as sr


def test_microphone():
    print("="*50)
    print("MICROPHONE TEST")
    print("="*50)
    print()
    
    # List microphones
    print("Available microphones:")
    mics = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mics):
        print(f"  {i}: {mic}")
    print()
    
    # Use default microphone
    print("Testing default microphone...")
    print("Please say something clearly after 'Listening...' appears")
    print()
    
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Calibrating for ambient noise... (stay quiet)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"Energy threshold set to: {recognizer.energy_threshold}")
        print()
        
        print("Listening... SAY SOMETHING NOW!")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Audio captured! Processing...")
            
            # Try Google
            try:
                text = recognizer.recognize_google(audio)
                print(f"\n>>> GOOGLE HEARD: '{text}' <<<")
                print("\nSUCCESS! Your microphone is working!")
                return True
            except sr.UnknownValueError:
                print("Google could not understand the audio")
            except sr.RequestError as e:
                print(f"Google error: {e}")
                
            # Try Sphinx offline
            try:
                text = recognizer.recognize_sphinx(audio)
                print(f"\n>>> SPHINX HEARD: '{text}' <<<")
                print("\nSUCCESS! Your microphone is working (offline mode)!")
                return True
            except Exception as e:
                print(f"Sphinx error: {e}")
                
        except sr.WaitTimeoutError:
            print("\nTIMEOUT: No speech detected within 10 seconds")
            print("Possible issues:")
            print("  - Microphone is muted")
            print("  - Wrong microphone selected")
            print("  - Microphone volume too low")
        except Exception as e:
            print(f"Error: {e}")
            
    print("\nMICROPHONE TEST FAILED")
    print("\nTroubleshooting:")
    print("1. Check Windows Settings > Privacy > Microphone")
    print("   - Allow apps to access your microphone: ON")
    print("   - Allow desktop apps: ON")
    print("2. Check your microphone is not muted")
    print("3. Try setting default microphone in Sound settings")
    return False


if __name__ == "__main__":
    success = test_microphone()
    input("\nPress Enter to exit...")
