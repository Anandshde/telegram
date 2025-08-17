#!/usr/bin/env python3
"""
Quick start script for Telegram Games Bot
=========================================

Simplified script to start the bot with helpful error messages.
"""

import os
import sys

def check_token():
    """Check if bot token is configured"""
    # Check environment variable
    env_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if env_token and env_token != 'YOUR_BOT_TOKEN_HERE':
        return True, 'environment variable'
    
    # Check config file
    try:
        from config import BOT_TOKEN
        if BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE':
            return True, 'config.py'
    except ImportError:
        pass
    
    return False, 'not set'

def main():
    """Main function"""
    print("🚀 Starting Telegram Casino Games Bot...")
    print("-" * 40)
    
    # Check if bot token is set
    token_set, token_source = check_token()
    
    if not token_set:
        print("❌ ERROR: Bot token not configured!")
        print()
        print("🔧 Quick Setup Options:")
        print("1. Set environment variable:")
        print("   export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        print()
        print("2. Edit config.py and set your token there")
        print()
        print("3. Run the setup script:")
        print("   python3 setup.py")
        print()
        print("📋 Get your bot token from @BotFather on Telegram:")
        print("   1. Search for @BotFather")
        print("   2. Send /newbot")
        print("   3. Follow the instructions")
        print("   4. Copy the token you receive")
        return False
    
    print(f"✅ Bot token found in {token_source}")
    
    # Check dependencies
    try:
        import telegram
        print("✅ Dependencies installed")
    except ImportError:
        print("❌ python-telegram-bot not installed!")
        print("📦 Install with: pip3 install -r requirements.txt")
        return False
    
    # Start the bot
    try:
        print("🎮 Loading bot...")
        from telegram_games_bot import main as run_bot
        print("✅ Bot loaded successfully")
        print()
        print("🎯 Bot is now running!")
        print("   • Find your bot on Telegram")
        print("   • Send /start to begin")
        print("   • Press Ctrl+C to stop")
        print()
        print("-" * 40)
        
        # Run the bot
        run_bot()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your bot token is correct")
        print("2. Make sure you have internet connection")
        print("3. Run test_bot.py to diagnose issues")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)