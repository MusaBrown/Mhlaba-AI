#!/usr/bin/env python3
"""
Better Microphone Test for JARVIS
"""

import speech_recognition as sr
import time


def test_microphone():
    print("="*60)
    print("JARVIS MICROPHONE TEST - v2")
    print("="*60)
    print()
    
    recognizer = sr.Recognizer()
    
    # Adjust settings for better recognition
    recognizer.energy_threshold = 300  # Higher = less sensitive
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0   # Wait 1 sec of silence
    
    with sr.Microphone() as source:
        print("[1] Calibrating for 3 seconds...")
        print("    Please stay QUIET during calibration\n")
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print(f"    Done! Energy threshold: {recognizer.energy_threshold}")
        print()
        
        # Multiple test attempts
        for attempt in range(3):
            print(f"[2] TEST {attempt + 1}/3: Press ENTER then speak clearly...")
            input("    (Press Enter when ready)")
            print()
            
            print("    >> LISTENING... SPEAK NOW <<")
            print("    (Say something like: 'Hello JARVIS' or 'What time is it')")
            print()
            
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                print("    Audio captured! Analyzing...")
                print()
                
                # Try Google
                try:
                    text = recognizer.recognize_google(audio)
                    print("="*60)
                    print(f">>> SUCCESS! JARVIS HEARD: '{text}' <<<")
                    print("="*60)
                    print("\nYour microphone is working perfectly!")
                    print("You can now run: python main.py")
                    return True
                except sr.UnknownValueError:
                    print("    [!] Could not understand audio (try speaking louder/clearer)")
                except sr.RequestError as e:
                    print(f"    [!] Network error: {e}")
                    
            except sr.WaitTimeoutError:
                print("    [!] No speech detected (timeout)")
                
            print()
            
    print("="*60)
    print("TESTS COMPLETED")
    print("="*60)
    print("\nIf JARVIS didn't understand you:")
    print("1. Speak louder and closer to the microphone")
    print("2. Reduce background noise")
    print("3. Check your mic is not muted (Fn + mic key on laptop)")
    print("4. Try using the TEXT mode: python demo.py")
    return False


if __name__ == "__main__":
    test_microphone()
    input("\nPress Enter to exit...")
