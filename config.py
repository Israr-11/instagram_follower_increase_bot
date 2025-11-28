# Instagram Bot Configuration

# Your Instagram credentials
INSTAGRAM_USERNAME = "your_username_here"
INSTAGRAM_PASSWORD = "your_password_here"

# Target accounts whose followers you want to follow
TARGET_ACCOUNTS = [
    "freecodecamp",
    "python",
    "coding",
    "programming_quotes",
    "webdevelopment"
]

# Specific users to follow
USERS_TO_FOLLOW = []

# Filtering Settings
FILTER_SETTINGS = {
    'min_followers': 100,      # Minimum followers
    'max_followers': 10000,    # Maximum followers (smaller = better follow-back rate)
    'tech_only': True,         # Only follow tech/coding accounts
}

# Bot behavior settings
BOT_SETTINGS = {
    'min_delay': 30,           # Minimum delay between follows (seconds)
    'max_delay': 90,           # Maximum delay between follows (seconds)
    'hourly_limit': 20,        # Max follows per hour
    'daily_limit': 150,        # Max follows per day
    'days_before_unfollow': 7, # Days to wait before unfollowing non-followers
    'max_follows_per_account': 30
}