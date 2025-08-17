#!/usr/bin/env python3
"""
Test script for Telegram Games Bot
=================================

Simple test to verify bot configuration and basic functionality.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError:
        print("❌ python-telegram-bot not found! Run: pip install -r requirements.txt")
        return False
    
    try:
        from telegram_games_bot import GameBot
        print("✅ GameBot class imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import GameBot: {e}")
        return False
    
    return True

def test_config():
    """Test bot configuration"""
    print("\n🔧 Testing configuration...")
    
    try:
        # Test config import
        try:
            from config import BOT_TOKEN, STARTING_BALANCE, MIN_BET, MAX_BET
            print("✅ Config file loaded successfully")
            config_source = "config.py"
        except ImportError:
            # Fallback to environment variable
            BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
            STARTING_BALANCE = 1000
            MIN_BET = 10
            MAX_BET = 500
            print("⚠️ Config file not found, using defaults")
            config_source = "defaults"
        
        # Check token
        if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("❌ Bot token not set!")
            print("   Set TELEGRAM_BOT_TOKEN environment variable or edit config.py")
            token_status = "❌ NOT SET"
        else:
            print("✅ Bot token is configured")
            token_status = "✅ SET"
        
        # Check configuration values
        print(f"\n📊 Configuration Summary:")
        print(f"   Config Source: {config_source}")
        print(f"   Bot Token: {token_status}")
        print(f"   Starting Balance: {STARTING_BALANCE} credits")
        print(f"   Betting Range: {MIN_BET}-{MAX_BET} credits")
        
        return BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE'
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_game_logic():
    """Test basic game logic"""
    print("\n🎮 Testing game logic...")
    
    try:
        from telegram_games_bot import GameBot
        
        # Create bot instance
        bot = GameBot()
        
        # Test balance operations
        initial_balance = bot.get_balance()
        print(f"✅ Initial balance: {initial_balance} credits")
        
        # Test balance update
        bot.update_balance(100)
        new_balance = bot.get_balance()
        if new_balance == initial_balance + 100:
            print("✅ Balance update works correctly")
        else:
            print("❌ Balance update failed")
            return False
        
        # Test negative balance protection
        bot.update_balance(-10000)  # Try to go negative
        if bot.get_balance() >= 0:
            print("✅ Negative balance protection works")
        else:
            print("❌ Negative balance protection failed")
            return False
        
        # Test crash multiplier generation
        bot.update_balance(1000)  # Reset balance
        multiplier = bot.generate_crash_multiplier()
        if 1.0 <= multiplier <= 50.0:
            print(f"✅ Crash multiplier generation works: {multiplier:.2f}x")
        else:
            print(f"❌ Invalid crash multiplier: {multiplier}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Game logic test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "telegram_games_bot.py",
        "requirements.txt", 
        "README.md"
    ]
    
    optional_files = [
        "config.py"
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing!")
            all_good = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} exists (optional)")
        else:
            print(f"⚠️ {file} not found (optional)")
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 Telegram Games Bot Test Suite")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Game Logic", test_game_logic),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your bot is ready to run.")
        print("💡 Next steps:")
        print("   1. Set your bot token (see README.md)")
        print("   2. Run: python telegram_games_bot.py")
        print("   3. Find your bot on Telegram and send /start")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)