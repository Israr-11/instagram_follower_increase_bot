from insta_bot import InstaBot
import config

print("="*60)
print("INSTAGRAM BOT - CONSOLE TEST MODE")
print("="*60)

# Initialize bot
bot = InstaBot(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)

# Apply settings
bot.min_followers = config.FILTER_SETTINGS['min_followers']
bot.max_followers = config.FILTER_SETTINGS['max_followers']
bot.days_before_unfollow = config.BOT_SETTINGS['days_before_unfollow']

print(f"\nSettings:")
print(f"  - Min Followers: {bot.min_followers}")
print(f"  - Max Followers: {bot.max_followers}")
print(f"  - Tech Keywords: {len(bot.tech_keywords)} keywords loaded")

# Login
if not bot.login():
    print("\nLogin failed. Exiting...")
    exit()

print("\nLogin successful!")
print("\nStarting to follow users...")
print(f"Target Accounts: {config.TARGET_ACCOUNTS}")
print()

# Try following from FIRST target account only (for testing)
target = config.TARGET_ACCOUNTS[0]
print(f"\n>>> Testing with: {target}")
print(f">>> Will try to follow max {config.BOT_SETTINGS['max_follows_per_account']} users")
print()

bot.follow_followers_of(target, max_follows=5)  # Start with just 5 for testing

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
bot.display_stats()