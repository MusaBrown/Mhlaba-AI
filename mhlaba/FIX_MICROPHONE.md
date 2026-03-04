# Fix Microphone Access for JARVIS

## The Problem
Your microphone works in Windows Settings but Python can't hear you. This is because Windows is blocking CMD/PowerShell from accessing the microphone.

## Solution

### Step 1: Allow Apps to Access Microphone

1. Press `Win + I` to open **Settings**
2. Click **Privacy & Security**
3. Click **Microphone** (under App permissions)
4. Turn ON these settings:
   - ✅ **Microphone access**
   - ✅ **Let apps access your microphone**
   - ✅ **Let desktop apps access your microphone** (IMPORTANT!)

### Step 2: Check Which Microphone Python Uses

1. Right-click the **speaker icon** in your taskbar
2. Click **Sound settings**
3. Under **Input**, check which microphone is selected
4. Make sure it's the same one you tested (your laptop microphone)
5. Click the microphone and test the volume - make sure it's not at 0%

### Step 3: Run CMD as Administrator (Optional)

Sometimes Windows requires admin rights:

1. Press `Win`
2. Type `cmd`
3. Right-click **Command Prompt** → **Run as administrator**
4. Then navigate to JARVIS folder:
   ```cmd
   cd C:\Users\USER1\Desktop\Jarvis\jarvis
   python diagnose.py
   ```

### Step 4: Alternative - Use Text Mode

If voice still doesn't work after all this, use text mode:

```cmd
python demo.py
```

You can type commands instead of speaking. The AI works exactly the same!

---

## Quick Test After Fixing

After changing settings, run:
```cmd
python diagnose.py
```

Press Enter and say "HELLO" loudly. It should now work!

---

## Why This Happened

Windows 10/11 has strict privacy rules. Apps need explicit permission to use the microphone. Since Python runs inside CMD/PowerShell, Windows treats it as a "desktop app" and blocks it by default.

The test in Windows Settings works because that's a built-in Windows app with automatic permissions.
