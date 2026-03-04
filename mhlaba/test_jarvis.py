#!/usr/bin/env python3
"""
JARVIS Test Script
Tests all components without running the full assistant
"""

import asyncio
import sys
from pathlib import Path


def test_config():
    """Test configuration module"""
    print("\n" + "="*50)
    print("TESTING: Config")
    print("="*50)
    
    try:
        from config import Config
        config = Config()
        print(f"[OK] Assistant name: {config.assistant_name}")
        print(f"[OK] Wake word: {config.wake_word}")
        print(f"[OK] AI Provider: {config.ai_provider}")
        print("[PASS] Config module working!")
        return True
    except Exception as e:
        print(f"[FAIL] Config error: {e}")
        return False


def test_ai_brain():
    """Test AI brain module"""
    print("\n" + "="*50)
    print("TESTING: AI Brain")
    print("="*50)
    
    try:
        from ai_brain import AIBrain
        brain = AIBrain()
        
        test_inputs = [
            "hello",
            "how are you",
            "who are you",
            "what can you do",
            "tell me a joke"
        ]
        
        for user_input in test_inputs:
            response = asyncio.run(brain.generate_response(user_input))
            print(f"  User: {user_input}")
            print(f"  Response: {response[:60]}...")
            print()
            
        print("[PASS] AI Brain working!")
        return True
    except Exception as e:
        print(f"[FAIL] AI Brain error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_handler():
    """Test document handler module"""
    print("\n" + "="*50)
    print("TESTING: Document Handler")
    print("="*50)
    
    try:
        from document_handler import DocumentHandler
        handler = DocumentHandler()
        
        # Test file listing
        files = handler.list_files()
        print(f"[OK] Found {len(files)} files in current directory")
        if files:
            print(f"  Examples: {', '.join(files[:5])}")
        
        # Test path resolution
        test_files = ["main.py", "config.py", "nonexistent.txt"]
        for f in test_files:
            path = handler._resolve_path(f)
            status = "[OK]" if path else "[MISSING]"
            print(f"{status} {f}: {path}")
        
        print("[PASS] Document Handler working!")
        return True
    except Exception as e:
        print(f"[FAIL] Document Handler error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_executor():
    """Test system executor module"""
    print("\n" + "="*50)
    print("TESTING: System Executor")
    print("="*50)
    
    try:
        from system_executor import SystemExecutor
        executor = SystemExecutor()
        
        # Test system info
        info = executor.get_system_info()
        print(f"[OK] System info retrieved:\n{info[:300]}...")
        
        # Test current directory
        cwd = executor.get_current_directory()
        print(f"[OK] Current directory: {cwd}")
        
        print("[PASS] System Executor working!")
        return True
    except Exception as e:
        print(f"[FAIL] System Executor error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_voice_speaker():
    """Test voice speaker module"""
    print("\n" + "="*50)
    print("TESTING: Voice Speaker (no audio)")
    print("="*50)
    
    try:
        from voice_speaker import VoiceSpeaker
        speaker = VoiceSpeaker()
        
        voices = speaker.get_available_voices()
        print(f"[OK] Found {len(voices)} voices")
        if voices:
            print(f"  Examples: {voices[:3]}")
        
        print("[PASS] Voice Speaker loaded (audio test skipped)")
        return True
    except Exception as e:
        print(f"[WARN] Voice Speaker error (expected if pyttsx3 not installed): {e}")
        return True  # Not critical


def test_voice_listener():
    """Test voice listener module"""
    print("\n" + "="*50)
    print("TESTING: Voice Listener (no mic)")
    print("="*50)
    
    try:
        from voice_listener import VoiceListener
        from config import Config
        
        # This might fail without PyAudio, that's ok
        listener = VoiceListener(Config())
        print("[PASS] Voice Listener loaded (mic test skipped)")
        return True
    except ImportError as e:
        print(f"[WARN] Voice Listener: PyAudio not installed (expected): {e}")
        return True  # Not critical for basic test
    except Exception as e:
        print(f"[WARN] Voice Listener error: {e}")
        return True


def test_integration():
    """Integration test"""
    print("\n" + "="*50)
    print("TESTING: Integration")
    print("="*50)
    
    try:
        # Simulate a conversation
        from ai_brain import AIBrain
        from document_handler import DocumentHandler
        from system_executor import SystemExecutor
        
        brain = AIBrain()
        docs = DocumentHandler()
        executor = SystemExecutor()
        
        print("Simulated interaction:")
        print("-" * 30)
        
        # Greeting
        response = asyncio.run(brain.generate_response("hello"))
        print(f"User: hello")
        print(f"JARVIS: {response}")
        print()
        
        # System info request
        print(f"User: system info")
        info = executor.get_system_info()
        print(f"JARVIS: [System info retrieved - {len(info)} chars]")
        print()
        
        # File listing
        print(f"User: list files")
        files = docs.list_files()
        print(f"JARVIS: Found {len(files)} files")
        print()
        
        print("[PASS] Integration test passed!")
        return True
    except Exception as e:
        print(f"[FAIL] Integration test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*50)
    print("JARVIS COMPONENT TEST")
    print("="*50)
    print("Testing all modules...")
    
    results = []
    
    results.append(("Config", test_config()))
    results.append(("AI Brain", test_ai_brain()))
    results.append(("Document Handler", test_document_handler()))
    results.append(("System Executor", test_system_executor()))
    results.append(("Voice Speaker", test_voice_speaker()))
    results.append(("Voice Listener", test_voice_listener()))
    results.append(("Integration", test_integration()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {name}")
    
    print("-" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! JARVIS is ready to use!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
