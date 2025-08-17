#!/usr/bin/env python3
"""
Configuration file for Telegram Games Bot
========================================

Store your bot token and other settings here.
"""

import os

# === BOT CONFIGURATION ===

# Your Telegram Bot Token from @BotFather
# You can set this as an environment variable or directly here
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8289657118:AAE_lSBm_FZwDn11GzSE-plVbsLW2uPER0E')

# === GAME SETTINGS ===

# Starting balance for new users (fake credits)
STARTING_BALANCE = 1000

# Betting limits
MIN_BET = 10
MAX_BET = 500

# Keno settings
KENO_TOTAL_NUMBERS = 20  # Numbers 1-20
KENO_DRAWN_NUMBERS = 10  # Bot draws 10 numbers
KENO_MAX_PICKS = 10      # Player can pick up to 10 numbers

# Keno payout multipliers based on matches
KENO_PAYOUTS = {
    0: 0,   # 0 matches: lose bet
    1: 0,   # 1 match: lose bet  
    2: 1,   # 2 matches: break even (1x)
    3: 2,   # 3 matches: 2x bet
    4: 3,   # 4 matches: 3x bet
    5: 5,   # 5 matches: 5x bet
    6: 10,  # 6+ matches: 10x bet
    7: 10,
    8: 10,
    9: 10,
    10: 10
}

# Crash game settings
CRASH_MIN_MULTIPLIER = 1.1
CRASH_MAX_MULTIPLIER = 10.0

# === LOGGING SETTINGS ===

# Enable/disable logging
ENABLE_LOGGING = True

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "INFO"

# === DEVELOPMENT SETTINGS ===

# Set to True for development/testing
DEBUG_MODE = False

# Print additional debug information
VERBOSE_OUTPUT = True

# === VALIDATION ===

def validate_config():
    """Validate configuration settings"""
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        raise ValueError("Please set your bot token in config.py or as TELEGRAM_BOT_TOKEN environment variable")
    
    if MIN_BET >= MAX_BET:
        raise ValueError("MIN_BET must be less than MAX_BET")
    
    if STARTING_BALANCE < MIN_BET:
        raise ValueError("STARTING_BALANCE must be at least MIN_BET")
    
    print("✅ Configuration validated successfully!")
    return True

if __name__ == '__main__':
    # Test configuration when run directly
    try:
        validate_config()
        print(f"Bot Token: {'Set' if BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE' else 'NOT SET'}")
        print(f"Starting Balance: {STARTING_BALANCE} credits")
        print(f"Betting Range: {MIN_BET}-{MAX_BET} credits")
        print(f"Debug Mode: {DEBUG_MODE}")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")