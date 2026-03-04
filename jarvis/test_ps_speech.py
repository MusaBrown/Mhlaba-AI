#!/usr/bin/env python3
"""Test PowerShell speech"""
import subprocess
import sys

text = "Testing speech. Can you hear me?"
safe_text = text.replace('"', '`"')

ps_cmd = f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak("{safe_text}");'

print("Testing PowerShell speech...")
print(f"Command: {ps_cmd[:60]}...")

try:
    result = subprocess.run(
        ['powershell.exe', '-Command', ps_cmd],
        capture_output=True,
        text=True,
        timeout=10
    )
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    print("Done!")
except Exception as e:
    print(f"Error: {e}")

input("\nPress Enter to exit...")
