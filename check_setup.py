#!/usr/bin/env python3
"""
Test script to verify the LINE BOT setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_env():
    required_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET', 'GROQ_API_KEY']
    missing = []

    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your_{var.lower().replace("_", "_")}_here':
            missing.append(var)

    if missing:
        print("❌ Missing or placeholder environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment.")
        print("Get LINE credentials from https://developers.line.biz/")
        print("Get Groq API key from https://console.groq.com/keys")
        return False

    print("✅ Environment variables are set.")
    return True

def check_openclaw():
    # Since we use --local mode, just check if openclaw command exists
    import subprocess
    try:
        result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ OpenClaw CLI is available.")
            return True
        else:
            print(f"❌ OpenClaw CLI not working: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error checking OpenClaw: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Checking LINE BOT + OpenClaw setup...\n")

    env_ok = check_env()
    openclaw_ok = check_openclaw()

    if env_ok and openclaw_ok:
        print("\n🎉 Setup looks good! You can now run: python main.py")
        print("Remember to set your webhook URL in LINE Developers Console to your app's /callback endpoint.")
    else:
        print("\n⚠️  Please fix the issues above before running the bot.")