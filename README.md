# 🎮 Telegram Casino Games Bot

A fun, single-user Telegram bot featuring **Keno** and **Crash** games with fake money for educational and entertainment purposes.

## 🎯 Features

### 🎲 Games Available

- **🔢 Keno**: Pick 1-10 numbers from 1-20, bot draws 10 random numbers, win based on matches
- **🚀 Crash**: Choose a cash-out multiplier, try to cash out before the randomly generated crash point

### 💰 Game Features

- Starting balance: **1,000 fake credits**
- Betting range: **10-500 credits**
- Real-time balance updates
- Interactive inline keyboards
- Detailed game results and statistics

### 🎮 Available Commands

- `/start` - Welcome message and main menu
- `/balance` - Check your current fake balance
- `/keno` - Start a Keno game
- `/crash` - Start a Crash game
- `/help` - Show help and game rules

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Telegram account
- Basic knowledge of creating Telegram bots

### 1. Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Save the **bot token** you receive

### 2. Download and Setup

```bash
# Clone or download the files
cd telegram-games-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Your Bot

**Option A: Edit the main file directly**

```python
# In telegram_games_bot.py, line 1077, replace:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
# with your actual token:
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
```

**Option B: Use environment variable (recommended)**

```bash
export TELEGRAM_BOT_TOKEN="your_actual_bot_token"
python telegram_games_bot.py
```

**Option C: Use config file**

```python
# Edit config.py and set your token there
BOT_TOKEN = "your_actual_bot_token"
```

### 4. Run the Bot

**Option A: Quick Start (Recommended)**

```bash
python3 run_bot.py
```

**Option B: Interactive Setup**

```bash
python3 setup.py
```

**Option C: Direct Start**

```bash
python3 telegram_games_bot.py
```

You should see:

```
🚀 Starting Telegram Games Bot...
Press Ctrl+C to stop the bot
```

### 5. Start Playing!

1. Find your bot on Telegram (search for the username you gave it)
2. Send `/start` to begin
3. Enjoy the games!

## 🎲 How to Play

### 🔢 Keno Game

1. **Set your bet** (10-500 credits)
2. **Pick numbers** (1-10 numbers from 1-20)
3. **Bot draws 10 random numbers**
4. **Win based on matches:**
   - 0-1 matches: Lose your bet
   - 2 matches: Break even (1x)
   - 3 matches: 2x your bet
   - 4 matches: 3x your bet
   - 5 matches: 5x your bet
   - 6+ matches: 10x your bet

### 🚀 Crash Game

1. **Set your bet** (10-500 credits)
2. **Choose cash-out point** (1.1x to 10.0x)
3. **Bot generates random crash point**
4. **Results:**
   - If crash > your target: **WIN** (bet × your multiplier)
   - If crash < your target: **LOSE** your bet

**Example**: Bet 100 credits, choose 2.5x cash-out

- Crash at 3.0x → Win 250 credits! 🎉
- Crash at 2.0x → Lose 100 credits 😔

## 📁 Project Structure

```
telegram-games-bot/
├── telegram_games_bot.py  # Main bot file with all game logic
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── setup.py              # Interactive setup script
├── run_bot.py            # Quick start script
├── test_bot.py           # Test suite
└── README.md            # This file
```

## 🛠️ Customization

### Modify Game Settings

Edit these values in `telegram_games_bot.py` or `config.py`:

```python
# Starting balance
self.user_balance = 1000  # Change starting credits

# Betting limits
MIN_BET = 10              # Minimum bet
MAX_BET = 500             # Maximum bet

# Keno payouts (in play_keno_round function)
# Modify the payout_multiplier logic

# Crash probabilities (in generate_crash_multiplier function)
# Adjust the probability ranges
```

### Add New Features

The code is well-commented and modular. You can easily add:

- New games
- Database storage (SQLite, PostgreSQL)
- Multi-user support
- Leaderboards
- Daily bonuses
- More betting options

## 🌐 Deployment Options

### Local Development

```bash
python telegram_games_bot.py
```

### Free Cloud Hosting

#### Option 1: Replit

1. Go to [replit.com](https://replit.com)
2. Create a new Python repl
3. Upload your files
4. Add your bot token as a secret: `TELEGRAM_BOT_TOKEN`
5. Run the bot

#### Option 2: Render.com

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set environment variable: `TELEGRAM_BOT_TOKEN`
5. Deploy

#### Option 3: Railway

1. Go to [railway.app](https://railway.app)
2. Deploy from GitHub
3. Add environment variable
4. Deploy

### Production Tips

- Use environment variables for sensitive data
- Add proper error handling
- Implement logging
- Consider using a database for persistence
- Add rate limiting for multi-user scenarios

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**

- Check if bot token is correct
- Ensure bot is not already running elsewhere
- Verify network connection

**"YOUR_BOT_TOKEN_HERE" error:**

```bash
❌ ERROR: Please set your bot token in the BOT_TOKEN variable!
```

**Solution**: Replace the placeholder with your actual bot token.

**Import errors:**

```bash
ModuleNotFoundError: No module named 'telegram'
```

**Solution**: Install dependencies: `pip install -r requirements.txt`

**Bot stops unexpectedly:**

- Check Python version (3.8+ required)
- Check for syntax errors
- Review error logs

### Debug Mode

Enable verbose logging by setting:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Technical Details

### Dependencies

- **python-telegram-bot**: Modern Telegram bot framework
- **Python 3.8+**: Core language support

### Architecture

- **Single-user design**: One user, one balance
- **In-memory storage**: No database required
- **Conversation handlers**: Manage game states
- **Inline keyboards**: Interactive buttons
- **Error handling**: Graceful error recovery

### Security Notes

- **Fake money only**: No real gambling
- **Single user**: Not designed for production multi-user
- **Local storage**: Balance resets on restart
- **Educational purpose**: Learn bot development

## 🤝 Contributing

This is a learning project! Feel free to:

- Add new games
- Improve the UI
- Add database support
- Enhance security
- Create multi-user version

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with Telegram's Terms of Service.

## 🎯 Next Steps

### Potential Enhancements

1. **Database Integration**: Add SQLite/PostgreSQL for persistent storage
2. **Multi-user Support**: Handle multiple users with separate balances
3. **More Games**: Blackjack, Roulette, Slots
4. **Statistics**: Track win/loss ratios, favorite games
5. **Daily Bonuses**: Login rewards, achievements
6. **Admin Features**: Manage user balances, view statistics

### Learning Opportunities

- **Database Design**: Learn SQL and database integration
- **API Development**: Build REST APIs for web interfaces
- **Frontend Development**: Create web dashboard
- **DevOps**: Deploy with Docker, CI/CD pipelines
- **Monitoring**: Add logging, metrics, alerts

---

## 🚀 Ready to Play?

1. **Get your bot token** from @BotFather
2. **Set the token** in the code
3. **Run** `python telegram_games_bot.py`
4. **Find your bot** on Telegram
5. **Send** `/start` and enjoy! 🎉

**Good luck and have fun!** 🍀

---

_Made with ❤️ for learning and fun. Remember: This uses fake money only!_
