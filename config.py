# Instagram Bot Configuration

# Your Instagram credentials
INSTAGRAM_USERNAME = "israrahmedpk444@gmail.com"
INSTAGRAM_PASSWORD = "Ahmed@999"

# Filtering Settings - FULLY CUSTOMIZABLE
FILTER_SETTINGS = {
    'min_followers': 500,      # Minimum followers
    'max_followers': 50000,    # Maximum followers
    'tech_only': True,         # Only follow tech/coding accounts
    'check_bio': True,         # Check bio for tech keywords
    'check_username': True,    # Check username for tech keywords
    'skip_private': True,      # Skip private accounts
    'skip_verified': False,    # Skip verified accounts
}

# Bot behavior settings
BOT_SETTINGS = {
    'min_delay': 30,           # Minimum delay between follows (seconds)
    'max_delay': 60,           # Maximum delay between follows (seconds)
    'scroll_delay': 2,         # Delay while scrolling
    'typing_delay': 0.1,       # Delay between keypresses
    'max_follows_per_hashtag': 5,  # Max follows per hashtag
    'headless': False,         # Show browser (True = hidden, False = visible)
}

# Hashtags to search - FULLY CUSTOMIZABLE
HASHTAGS = {
    'python': ['python', 'pythonprogramming', 'pythoncode', 'pythondeveloper'],
    'javascript': ['javascript', 'js', 'nodejs', 'reactjs', 'vuejs'],
    'webdev': ['webdevelopment', 'webdev', 'frontend', 'backend', 'fullstack'],
    'general': ['coding', 'programming', '100daysofcode', 'learntocode', 'codingnewbie'],
    'data': ['datascience', 'machinelearning', 'artificialintelligence', 'dataanalysis'],
    'mobile': ['androiddev', 'iosdev', 'flutter', 'reactnative', 'mobiledev'],
}

# Tech keywords for detection (expanded)
TECH_KEYWORDS = [
    'coding', 'programming', 'developer', 'software', 'tech', 'code',
    'python', 'javascript', 'java', 'web', 'app', 'ai', 'ml', 'data',
    'engineer', 'devops', 'frontend', 'backend', 'fullstack', 'react',
    'node', 'django', 'flutter', 'android', 'ios', 'cybersecurity',
    'blockchain', 'cloud', 'aws', 'docker', 'kubernetes', 'api',
    'database', 'sql', 'mongodb', 'git', 'github', 'opensource',
    'linux', 'ubuntu', 'tutorial', 'learning', 'computer', 'science',
    'algorithm', 'startup', 'technology', 'html', 'css', 'php',
    'ruby', 'golang', 'rust', 'typescript', 'vue', 'angular',
]
