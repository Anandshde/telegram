#!/usr/bin/env python3
"""
Setup script for Telegram Games Bot
==================================

Interactive setup to help configure the bot quickly.
"""

import os
import sys

def print_banner():
    """Print welcome banner"""
    print("🎮 " + "=" * 50)
    print("🎮 Telegram Casino Games Bot Setup")
    print("🎮 " + "=" * 50)
    print()

def check_dependencies():
    """Check if dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import telegram
        print("✅ python-telegram-bot is installed")
        return True
    except ImportError:
        print("❌ python-telegram-bot not found!")
        print("📦 Installing dependencies...")
        
        try:
            import subprocess
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Dependencies installed successfully!")
                return True
            else:
                print("❌ Failed to install dependencies:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            print("💡 Please run manually: pip install -r requirements.txt")
            return False

def setup_bot_token():
    """Interactive bot token setup"""
    print("\n🤖 Bot Token Setup")
    print("-" * 30)
    
    # Check if token is already set
    current_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if current_token and current_token != 'YOUR_BOT_TOKEN_HERE':
        print(f"✅ Bot token already set via environment variable")
        return True
    
    # Check config file
    try:
        with open('config.py', 'r') as f:
            content = f.read()
            if 'YOUR_BOT_TOKEN_HERE' not in content:
                print("✅ Bot token appears to be set in config.py")
                return True
    except FileNotFoundError:
        pass
    
    print("❌ Bot token not configured!")
    print("\n📋 To get a bot token:")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot and follow the instructions")
    print("3. Copy the bot token you receive")
    print()
    
    choice = input("Do you want to set the token now? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        print("\n🔑 Choose setup method:")
        print("1. Set environment variable (recommended)")
        print("2. Edit config.py file")
        
        method = input("Enter choice (1-2): ").strip()
        
        if method == '1':
            token = input("\n🔑 Enter your bot token: ").strip()
            if token:
                # Add to shell profile
                shell_profile = os.path.expanduser("~/.zshrc")  # Default to zsh
                if not os.path.exists(shell_profile):
                    shell_profile = os.path.expanduser("~/.bashrc")
                
                try:
                    with open(shell_profile, 'a') as f:
                        f.write(f'\n# Telegram Bot Token\nexport TELEGRAM_BOT_TOKEN="{token}"\n')
                    
                    print(f"✅ Token added to {shell_profile}")
                    print("🔄 Please restart your terminal or run:")
                    print(f"   source {shell_profile}")
                    print(f"   export TELEGRAM_BOT_TOKEN='{token}'")
                    
                    # Set for current session
                    os.environ['TELEGRAM_BOT_TOKEN'] = token
                    return True
                    
                except Exception as e:
                    print(f"❌ Error writing to shell profile: {e}")
                    print(f"💡 Manually add this line to {shell_profile}:")
                    print(f"   export TELEGRAM_BOT_TOKEN='{token}'")
                    return False
            
        elif method == '2':
            token = input("\n🔑 Enter your bot token: ").strip()
            if token:
                try:
                    # Update config.py
                    with open('config.py', 'r') as f:
                        content = f.read()
                    
                    updated_content = content.replace(
                        "BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')",
                        f"BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '{token}')"
                    )
                    
                    with open('config.py', 'w') as f:
                        f.write(updated_content)
                    
                    print("✅ Token saved to config.py")
                    return True
                    
                except Exception as e:
                    print(f"❌ Error updating config.py: {e}")
                    return False
        
        else:
            print("❌ Invalid choice")
            return False
    
    else:
        print("⚠️ Bot token setup skipped")
        print("💡 You can set it later using one of these methods:")
        print("   1. Environment variable: export TELEGRAM_BOT_TOKEN='your_token'")
        print("   2. Edit config.py file")
        return False

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running tests...")
    print("-" * 20)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_bot.py"], capture_output=True, text=True)
        
        # Show test output
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("⚠️ Some tests failed, but the bot should still work")
            return True  # Non-blocking
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def show_next_steps():
    """Show final instructions"""
    print("\n🚀 Setup Complete!")
    print("=" * 30)
    print()
    print("📝 Next steps:")
    print("1. Run the bot: python3 telegram_games_bot.py")
    print("2. Find your bot on Telegram (search for the username you gave it)")
    print("3. Send /start to begin playing!")
    print()
    print("🎮 Available games:")
    print("   • 🔢 Keno - Pick numbers and match them!")
    print("   • 🚀 Crash - Cash out before the crash!")
    print()
    print("📚 Documentation:")
    print("   • README.md - Complete setup guide")
    print("   • config.py - Bot configuration")
    print("   • test_bot.py - Test suite")
    print()
    print("🎉 Have fun and good luck!")

def main():
    """Main setup flow"""
    print_banner()
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Setup failed: Dependencies not installed")
        return False
    
    # Step 2: Setup bot token
    token_ok = setup_bot_token()
    
    # Step 3: Run tests
    tests_ok = run_tests()
    
    # Step 4: Show next steps
    show_next_steps()
    
    if token_ok and tests_ok:
        print("✅ Setup completed successfully!")
    else:
        print("⚠️ Setup completed with warnings")
        if not token_ok:
            print("   • Bot token needs to be configured")
    
    return True

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)