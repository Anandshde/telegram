#!/usr/bin/env python3
"""
Single-User Telegram Games Bot
============================

A fun Telegram bot featuring Keno and Crash games with fake money.
Created for educational and entertainment purposes.

Author: Assistant
Version: 1.0
"""

import logging
import random
import os
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Try to import config, fall back to defaults if not available
try:
    from config import *
except ImportError:
    # Default configuration if config.py is not available
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    STARTING_BALANCE = 1000
    MIN_BET = 10
    MAX_BET = 500
    KENO_PAYOUTS = {0: 0, 1: 0, 2: 1, 3: 2, 4: 3, 5: 5, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10}

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Game states for conversation handlers
KENO_PICK_NUMBERS, KENO_SET_BET, CRASH_SET_BET, CRASH_CASHOUT = range(4)

class GameBot:
    """Main bot class handling all game logic and user interactions"""
    
    def __init__(self):
        # User data storage (in-memory for single user)
        self.user_balance = STARTING_BALANCE  # Starting balance from config
        self.current_game_data = {}  # Store current game session data
        
    def get_balance(self) -> int:
        """Get current user balance"""
        return self.user_balance
    
    def update_balance(self, amount: int) -> None:
        """Update user balance by amount (positive for win, negative for loss)"""
        self.user_balance += amount
        if self.user_balance < 0:
            self.user_balance = 0
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command - show welcome message and main menu"""
        user = update.effective_user
        
        welcome_text = f"""
🎮 **Welcome to the Casino Games Bot!** 🎮

Hello {user.first_name}! 

This bot offers exciting casino-style games with fake money for fun and learning.

💰 Your current balance: **{self.get_balance()} credits**

🎲 **Available Games:**
• **Keno** - Pick numbers and see how many match!
• **Crash** - Cash out before the multiplier crashes!

Choose a game below or use these commands:
• /balance - Check your balance
• /keno - Play Keno
• /crash - Play Crash
• /help - Show this menu again

Good luck and have fun! 🍀
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔢 Play Keno", callback_data="start_keno"),
                InlineKeyboardButton("🚀 Play Crash", callback_data="start_crash")
            ],
            [
                InlineKeyboardButton("💰 Check Balance", callback_data="check_balance"),
                InlineKeyboardButton("ℹ️ Help", callback_data="show_help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /balance command"""
        balance_text = f"💰 **Your Current Balance**\n\n{self.get_balance()} credits"
        
        keyboard = [
            [
                InlineKeyboardButton("🔢 Play Keno", callback_data="start_keno"),
                InlineKeyboardButton("🚀 Play Crash", callback_data="start_crash")
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(balance_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = """
🎮 **Casino Games Bot Help** 🎮

**🔢 Keno Game:**
• Pick 1-10 numbers from 1-20
• Bot draws 10 random numbers
• Win based on how many of your numbers match
• Higher matches = bigger payouts!

**🚀 Crash Game:**
• Set your bet amount
• Watch the multiplier rise from 1.00x
• Cash out before it crashes!
• The longer you wait, the higher the multiplier, but higher the risk

**💰 Payouts:**
• Keno: 0 hits = lose bet, 1-2 hits = break even, 3+ hits = profit
• Crash: Your bet × cashout multiplier

**Commands:**
• /start - Main menu
• /balance - Check balance  
• /keno - Start Keno game
• /crash - Start Crash game
• /help - Show this help

Have fun and good luck! 🍀
        """
        
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')

    # === KENO GAME IMPLEMENTATION ===
    
    async def start_keno(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start Keno game - ask for bet amount"""
        query = update.callback_query
        if query:
            await query.answer()
        
        # Reset game data
        self.current_game_data = {
            'game': 'keno',
            'selected_numbers': [],
            'bet_amount': 0
        }
        
        keno_text = f"""
🔢 **KENO GAME** 🔢

💰 Your balance: {self.get_balance()} credits

**How to play:**
1. Set your bet amount ({MIN_BET}-{min(MAX_BET, self.get_balance())} credits)
2. Pick 1-10 numbers from 1-20
3. Bot draws 10 random numbers
4. Win based on matches!

**💎 Payout Table:**
• 0-1 matches: Lose bet
• 2 matches: Break even (1x)
• 3 matches: 2x bet
• 4 matches: 3x bet
• 5 matches: 5x bet
• 6+ matches: 10x bet

Please enter your bet amount ({MIN_BET}-{min(MAX_BET, self.get_balance())}):
        """
        
        if query:
            await query.edit_message_text(keno_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(keno_text, parse_mode='Markdown')
        
        return KENO_SET_BET
    
    async def keno_set_bet(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle bet amount input for Keno"""
        try:
            bet_amount = int(update.message.text)
            
            if bet_amount < MIN_BET:
                await update.message.reply_text(f"❌ Minimum bet is {MIN_BET} credits. Please try again:")
                return KENO_SET_BET
            
            if bet_amount > self.get_balance():
                await update.message.reply_text(f"❌ Insufficient balance! You have {self.get_balance()} credits. Please try again:")
                return KENO_SET_BET
            
            if bet_amount > MAX_BET:
                await update.message.reply_text(f"❌ Maximum bet is {MAX_BET} credits. Please try again:")
                return KENO_SET_BET
            
            self.current_game_data['bet_amount'] = bet_amount
            
            # Show number selection interface
            numbers_text = f"""
🔢 **KENO - Pick Your Numbers** 🔢

💰 Bet amount: {bet_amount} credits
🎯 Selected: {len(self.current_game_data['selected_numbers'])}/10 numbers

Pick 1-10 numbers from 1-20. Tap numbers below to select/deselect:
            """
            
            keyboard = []
            for row in range(4):  # 4 rows of 5 numbers each
                button_row = []
                for col in range(5):
                    number = row * 5 + col + 1
                    if number <= 20:
                        # Mark selected numbers with ✅
                        display_text = f"✅{number}" if number in self.current_game_data['selected_numbers'] else str(number)
                        button_row.append(InlineKeyboardButton(display_text, callback_data=f"keno_select_{number}"))
                keyboard.append(button_row)
            
            # Control buttons
            keyboard.append([
                InlineKeyboardButton("🎲 PLAY", callback_data="keno_play"),
                InlineKeyboardButton("🔄 Clear All", callback_data="keno_clear"),
                InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(numbers_text, reply_markup=reply_markup, parse_mode='Markdown')
            
            return KENO_PICK_NUMBERS
            
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number:")
            return KENO_SET_BET
    
    async def keno_number_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle number selection for Keno"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data.startswith("keno_select_"):
            number = int(callback_data.split("_")[2])
            
            if number in self.current_game_data['selected_numbers']:
                # Deselect number
                self.current_game_data['selected_numbers'].remove(number)
            else:
                # Select number (max 10)
                if len(self.current_game_data['selected_numbers']) < 10:
                    self.current_game_data['selected_numbers'].append(number)
                else:
                    await query.answer("Maximum 10 numbers allowed!", show_alert=True)
                    return KENO_PICK_NUMBERS
            
            # Update the keyboard
            numbers_text = f"""
🔢 **KENO - Pick Your Numbers** 🔢

💰 Bet amount: {self.current_game_data['bet_amount']} credits
🎯 Selected: {len(self.current_game_data['selected_numbers'])}/10 numbers

Pick 1-10 numbers from 1-20. Tap numbers below to select/deselect:
            """
            
            keyboard = []
            for row in range(4):
                button_row = []
                for col in range(5):
                    number = row * 5 + col + 1
                    if number <= 20:
                        display_text = f"✅{number}" if number in self.current_game_data['selected_numbers'] else str(number)
                        button_row.append(InlineKeyboardButton(display_text, callback_data=f"keno_select_{number}"))
                keyboard.append(button_row)
            
            keyboard.append([
                InlineKeyboardButton("🎲 PLAY", callback_data="keno_play"),
                InlineKeyboardButton("🔄 Clear All", callback_data="keno_clear"),
                InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(numbers_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif callback_data == "keno_clear":
            self.current_game_data['selected_numbers'] = []
            # Update keyboard with cleared selections
            numbers_text = f"""
🔢 **KENO - Pick Your Numbers** 🔢

💰 Bet amount: {self.current_game_data['bet_amount']} credits
🎯 Selected: 0/10 numbers

Pick 1-10 numbers from 1-20. Tap numbers below to select/deselect:
            """
            
            keyboard = []
            for row in range(4):
                button_row = []
                for col in range(5):
                    number = row * 5 + col + 1
                    if number <= 20:
                        button_row.append(InlineKeyboardButton(str(number), callback_data=f"keno_select_{number}"))
                keyboard.append(button_row)
            
            keyboard.append([
                InlineKeyboardButton("🎲 PLAY", callback_data="keno_play"),
                InlineKeyboardButton("🔄 Clear All", callback_data="keno_clear"),
                InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(numbers_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif callback_data == "keno_play":
            if len(self.current_game_data['selected_numbers']) == 0:
                await query.answer("Please select at least 1 number!", show_alert=True)
                return KENO_PICK_NUMBERS
            
            # Play the game!
            await self.play_keno_round(query)
            return ConversationHandler.END
        
        return KENO_PICK_NUMBERS
    
    async def play_keno_round(self, query) -> None:
        """Execute Keno game round and show results"""
        # Deduct bet from balance
        bet_amount = self.current_game_data['bet_amount']
        self.update_balance(-bet_amount)
        
        # Generate 10 random winning numbers
        winning_numbers = sorted(random.sample(range(1, 21), 10))
        user_numbers = sorted(self.current_game_data['selected_numbers'])
        
        # Calculate matches
        matches = [num for num in user_numbers if num in winning_numbers]
        match_count = len(matches)
        
        # Calculate payout using config
        payout_multiplier = KENO_PAYOUTS.get(match_count, 0)
        
        winnings = bet_amount * payout_multiplier
        net_result = winnings - bet_amount
        
        if winnings > 0:
            self.update_balance(winnings)
        
        # Format results
        user_numbers_str = " ".join([f"**{num}**" if num in matches else str(num) for num in user_numbers])
        winning_numbers_str = " ".join([str(num) for num in winning_numbers])
        matches_str = " ".join([str(num) for num in matches]) if matches else "None"
        
        result_text = f"""
🔢 **KENO RESULTS** 🔢

**Your Numbers:** {user_numbers_str}
**Winning Numbers:** {winning_numbers_str}
**Matches:** {matches_str}

🎯 **Matches:** {match_count}
💰 **Bet:** {bet_amount} credits
🏆 **Winnings:** {winnings} credits
📊 **Net Result:** {"+" if net_result >= 0 else ""}{net_result} credits

💳 **New Balance:** {self.get_balance()} credits

{"🎉 Congratulations!" if net_result > 0 else "😔 Better luck next time!" if net_result < 0 else "🤝 Break even!"}
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔢 Play Again", callback_data="start_keno"),
                InlineKeyboardButton("🚀 Try Crash", callback_data="start_crash")
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')

    # === CRASH GAME IMPLEMENTATION ===
    
    async def start_crash(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start Crash game - ask for bet amount"""
        query = update.callback_query
        if query:
            await query.answer()
        
        # Reset game data
        self.current_game_data = {
            'game': 'crash',
            'bet_amount': 0,
            'target_multiplier': 1.0,
            'actual_multiplier': 0.0
        }
        
        crash_text = f"""
🚀 **CRASH GAME** 🚀

💰 Your balance: {self.get_balance()} credits

**How to play:**
1. Set your bet amount ({MIN_BET}-{min(MAX_BET, self.get_balance())} credits)
2. Choose your cash-out multiplier (1.1x - 10.0x)
3. Bot generates a random crash point
4. If you cash out before the crash, you win!

**Example:**
• Bet: 100 credits
• Cash out at: 2.5x
• If crash happens at 3.0x → Win 250 credits!
• If crash happens at 2.0x → Lose 100 credits!

Please enter your bet amount ({MIN_BET}-{min(MAX_BET, self.get_balance())}):
        """
        
        if query:
            await query.edit_message_text(crash_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(crash_text, parse_mode='Markdown')
        
        return CRASH_SET_BET
    
    async def crash_set_bet(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle bet amount input for Crash"""
        try:
            bet_amount = int(update.message.text)
            
            if bet_amount < MIN_BET:
                await update.message.reply_text(f"❌ Minimum bet is {MIN_BET} credits. Please try again:")
                return CRASH_SET_BET
            
            if bet_amount > self.get_balance():
                await update.message.reply_text(f"❌ Insufficient balance! You have {self.get_balance()} credits. Please try again:")
                return CRASH_SET_BET
            
            if bet_amount > MAX_BET:
                await update.message.reply_text(f"❌ Maximum bet is {MAX_BET} credits. Please try again:")
                return CRASH_SET_BET
            
            self.current_game_data['bet_amount'] = bet_amount
            
            # Show cashout selection interface
            cashout_text = f"""
🚀 **CRASH - Choose Cash-Out Point** 🚀

💰 Bet amount: {bet_amount} credits
🎯 Current selection: {self.current_game_data['target_multiplier']:.1f}x

Choose your cash-out multiplier. Higher multipliers = higher risk & reward!

**Potential Winnings:** {int(bet_amount * self.current_game_data['target_multiplier'])} credits
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("1.1x", callback_data="crash_mult_1.1"),
                    InlineKeyboardButton("1.5x", callback_data="crash_mult_1.5"),
                    InlineKeyboardButton("2.0x", callback_data="crash_mult_2.0"),
                    InlineKeyboardButton("2.5x", callback_data="crash_mult_2.5")
                ],
                [
                    InlineKeyboardButton("3.0x", callback_data="crash_mult_3.0"),
                    InlineKeyboardButton("4.0x", callback_data="crash_mult_4.0"),
                    InlineKeyboardButton("5.0x", callback_data="crash_mult_5.0"),
                    InlineKeyboardButton("7.5x", callback_data="crash_mult_7.5")
                ],
                [
                    InlineKeyboardButton("10.0x", callback_data="crash_mult_10.0")
                ],
                [
                    InlineKeyboardButton("🚀 LAUNCH", callback_data="crash_play"),
                    InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(cashout_text, reply_markup=reply_markup, parse_mode='Markdown')
            
            return CRASH_CASHOUT
            
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number:")
            return CRASH_SET_BET
    
    async def crash_multiplier_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle multiplier selection for Crash"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data.startswith("crash_mult_"):
            multiplier = float(callback_data.split("_")[2])
            self.current_game_data['target_multiplier'] = multiplier
            
            # Update the display
            bet_amount = self.current_game_data['bet_amount']
            cashout_text = f"""
🚀 **CRASH - Choose Cash-Out Point** 🚀

💰 Bet amount: {bet_amount} credits
🎯 Current selection: {multiplier:.1f}x

Choose your cash-out multiplier. Higher multipliers = higher risk & reward!

**Potential Winnings:** {int(bet_amount * multiplier)} credits
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅1.1x" if multiplier == 1.1 else "1.1x", callback_data="crash_mult_1.1"),
                    InlineKeyboardButton("✅1.5x" if multiplier == 1.5 else "1.5x", callback_data="crash_mult_1.5"),
                    InlineKeyboardButton("✅2.0x" if multiplier == 2.0 else "2.0x", callback_data="crash_mult_2.0"),
                    InlineKeyboardButton("✅2.5x" if multiplier == 2.5 else "2.5x", callback_data="crash_mult_2.5")
                ],
                [
                    InlineKeyboardButton("✅3.0x" if multiplier == 3.0 else "3.0x", callback_data="crash_mult_3.0"),
                    InlineKeyboardButton("✅4.0x" if multiplier == 4.0 else "4.0x", callback_data="crash_mult_4.0"),
                    InlineKeyboardButton("✅5.0x" if multiplier == 5.0 else "5.0x", callback_data="crash_mult_5.0"),
                    InlineKeyboardButton("✅7.5x" if multiplier == 7.5 else "7.5x", callback_data="crash_mult_7.5")
                ],
                [
                    InlineKeyboardButton("✅10.0x" if multiplier == 10.0 else "10.0x", callback_data="crash_mult_10.0")
                ],
                [
                    InlineKeyboardButton("🚀 LAUNCH", callback_data="crash_play"),
                    InlineKeyboardButton("❌ Cancel", callback_data="main_menu")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(cashout_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif callback_data == "crash_play":
            # Play the game!
            await self.play_crash_round(query)
            return ConversationHandler.END
        
        return CRASH_CASHOUT
    
    async def play_crash_round(self, query) -> None:
        """Execute Crash game round and show results"""
        # Deduct bet from balance
        bet_amount = self.current_game_data['bet_amount']
        target_multiplier = self.current_game_data['target_multiplier']
        self.update_balance(-bet_amount)
        
        # Generate random crash point (weighted towards lower values for realistic casino odds)
        # Higher multipliers should be less likely
        crash_point = self.generate_crash_multiplier()
        self.current_game_data['actual_multiplier'] = crash_point
        
        # Determine win/loss
        won = target_multiplier <= crash_point
        
        if won:
            winnings = int(bet_amount * target_multiplier)
            self.update_balance(winnings)
            net_result = winnings - bet_amount
        else:
            winnings = 0
            net_result = -bet_amount
        
        # Format results with some dramatic flair
        if won:
            result_emoji = "🎉"
            result_message = "SUCCESS!"
            result_description = f"Cashed out safely at {target_multiplier:.1f}x!"
        else:
            result_emoji = "💥"
            result_message = "CRASHED!"
            result_description = f"Crashed at {crash_point:.2f}x before your {target_multiplier:.1f}x target!"
        
        result_text = f"""
🚀 **CRASH RESULTS** 🚀

{result_emoji} **{result_message}** {result_emoji}

**Your Target:** {target_multiplier:.1f}x
**Crash Point:** {crash_point:.2f}x
{result_description}

💰 **Bet:** {bet_amount} credits
🏆 **Winnings:** {winnings} credits  
📊 **Net Result:** {"+" if net_result >= 0 else ""}{net_result} credits

💳 **New Balance:** {self.get_balance()} credits

{"🎉 Congratulations!" if won else "😔 Better luck next time!"}
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🚀 Play Again", callback_data="start_crash"),
                InlineKeyboardButton("🔢 Try Keno", callback_data="start_keno")
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def generate_crash_multiplier(self) -> float:
        """Generate realistic crash multiplier with weighted probabilities"""
        # Weighted random generation to simulate real crash game probabilities
        rand = random.random()
        
        if rand < 0.33:  # 33% chance of crash between 1.0-2.0x
            return round(random.uniform(1.0, 2.0), 2)
        elif rand < 0.65:  # 32% chance of crash between 2.0-4.0x  
            return round(random.uniform(2.0, 4.0), 2)
        elif rand < 0.85:  # 20% chance of crash between 4.0-7.0x
            return round(random.uniform(4.0, 7.0), 2)
        elif rand < 0.95:  # 10% chance of crash between 7.0-15.0x
            return round(random.uniform(7.0, 15.0), 2)
        else:  # 5% chance of crash above 15.0x (rare!)
            return round(random.uniform(15.0, 50.0), 2)

    # === GENERAL HANDLERS ===
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle general button presses"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "main_menu":
            await self.show_main_menu(query)
        elif query.data == "check_balance":
            await self.show_balance(query)
        elif query.data == "show_help":
            await self.show_help(query)
        elif query.data == "start_keno":
            await self.start_keno(update, context)
        elif query.data == "start_crash":
            await self.start_crash(update, context)
    
    async def show_main_menu(self, query) -> None:
        """Show main menu"""
        menu_text = f"""
🎮 **Casino Games Bot** 🎮

💰 Your balance: **{self.get_balance()} credits**

Choose a game or check your stats:
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔢 Play Keno", callback_data="start_keno"),
                InlineKeyboardButton("🚀 Play Crash", callback_data="start_crash")
            ],
            [
                InlineKeyboardButton("💰 Check Balance", callback_data="check_balance"),
                InlineKeyboardButton("ℹ️ Help", callback_data="show_help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_balance(self, query) -> None:
        """Show balance via callback"""
        balance_text = f"💰 **Your Current Balance**\n\n{self.get_balance()} credits"
        
        keyboard = [
            [
                InlineKeyboardButton("🔢 Play Keno", callback_data="start_keno"),
                InlineKeyboardButton("🚀 Play Crash", callback_data="start_crash")
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(balance_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_help(self, query) -> None:
        """Show help via callback"""
        help_text = """
🎮 **Casino Games Bot Help** 🎮

**🔢 Keno Game:**
• Pick 1-10 numbers from 1-20
• Bot draws 10 random numbers  
• Win based on how many of your numbers match
• Higher matches = bigger payouts!

**🚀 Crash Game:**
• Set your bet amount
• Choose your cash-out multiplier
• Bot generates random crash point
• Win if you cash out before the crash!

**💰 Payouts:**
• Keno: 0-1 hits = lose, 2 hits = break even, 3+ hits = profit
• Crash: Your bet × cashout multiplier

**Commands:**
• /start - Main menu
• /balance - Check balance
• /keno - Start Keno game  
• /crash - Start Crash game
• /help - Show this help

Have fun and good luck! 🍀
        """
        
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle conversation cancellation"""
        await update.message.reply_text("❌ Game cancelled. Use /start to play again!")
        return ConversationHandler.END
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")


def main() -> None:
    """Main function to run the bot"""
    # Check if bot token is set
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set your bot token!")
        print("Options:")
        print("1. Set environment variable: export TELEGRAM_BOT_TOKEN='your_token'")
        print("2. Edit BOT_TOKEN in config.py")
        print("3. Edit BOT_TOKEN directly in this file")
        print("\nGet your token from @BotFather on Telegram")
        return
    
    # Create bot instance
    bot = GameBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("balance", bot.balance_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    
    # Keno conversation handler
    keno_handler = ConversationHandler(
        entry_points=[
            CommandHandler("keno", bot.start_keno),
            CallbackQueryHandler(bot.start_keno, pattern="^start_keno$")
        ],
        states={
            KENO_SET_BET: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.keno_set_bet)],
            KENO_PICK_NUMBERS: [CallbackQueryHandler(bot.keno_number_selection)]
        },
        fallbacks=[CommandHandler("cancel", bot.cancel_handler)]
    )
    
    # Crash conversation handler
    crash_handler = ConversationHandler(
        entry_points=[
            CommandHandler("crash", bot.start_crash),
            CallbackQueryHandler(bot.start_crash, pattern="^start_crash$")
        ],
        states={
            CRASH_SET_BET: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.crash_set_bet)],
            CRASH_CASHOUT: [CallbackQueryHandler(bot.crash_multiplier_selection)]
        },
        fallbacks=[CommandHandler("cancel", bot.cancel_handler)]
    )
    
    # Add conversation handlers
    application.add_handler(keno_handler)
    application.add_handler(crash_handler)
    
    # Add general callback handler (must be after conversation handlers)
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    print("🚀 Starting Telegram Games Bot...")
    print("Press Ctrl+C to stop the bot")
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()