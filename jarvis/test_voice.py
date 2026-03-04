"""
Quick Voice Test for JARVIS
Run this to test if your microphone is working properly
"""
import speech_recognition as sr
import sys

def test_microphone():
    print("=" * 50)
    print("JARVIS MICROPHONE TEST")
    print("=" * 50)
    print()
    
    # Show available mics
    print("Available microphones:")
    for i, name in enumerate(sr.Microphone.list_microphone_names()[:5]):
        print(f"  [{i}] {name}")
    print()
    
    # Initialize
    r = sr.Recognizer()
    
    # Lower threshold for better sensitivity
    r.energy_threshold = 800
    r.pause_threshold = 1.0
    r.phrase_threshold = 0.3
    
    with sr.Microphone() as source:
        print("Calibrating for background noise...")
        print("Please be quiet for 2 seconds...")
        r.adjust_for_ambient_noise(source, duration=2)
        print(f"Energy threshold set to: {r.energy_threshold}")
        print()
        
        print("=" * 50)
        print("TEST 1: Say something now (listening for 5 seconds)...")
        print("=" * 50)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Audio detected! Processing...")
            
            try:
                text = r.recognize_google(audio)
                print()
                print("✅ SUCCESS! I heard you say:")
                print(f"   \"{text}\"")
                print()
                
                # Wake word test
                if "jarvis" in text.lower():
                    print("🎉 Perfect! You said the wake word 'Jarvis'")
                else:
                    print("💡 Tip: Remember to say 'Jarvis' first, like:")
                    print("   \"Jarvis, what time is it?\"")
                    
                return True
                
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                print("   Try speaking louder or closer to the mic")
                return False
            except sr.RequestError as e:
                print(f"❌ Google Speech error: {e}")
                print("   Check your internet connection")
                return False
                
        except sr.WaitTimeoutError:
            print("❌ No speech detected within 5 seconds")
            print("   Check your microphone is not muted")
            return False

if __name__ == "__main__":
    success = test_microphone()
    print()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
