# Instagram Bot Configuration

# Your Instagram credentials
INSTAGRAM_USERNAME = "israrahmedpk444@gmail.com"
INSTAGRAM_PASSWORD = "Ahmed@999"
# Target accounts whose followers you want to follow
TARGET_ACCOUNTS = [
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
    'min_delay': 90,           # Minimum delay between follows (seconds)
    'max_delay': 180,           # Maximum delay between follows (seconds)
    'hourly_limit': 5,        # Max follows per hour
    'daily_limit': 30,        # Max follows per day
    'days_before_unfollow': 14, # Days to wait before unfollowing non-followers
    'max_follows_per_account': 5
}