# Instagram Follow Bot

An intelligent Instagram bot that follows users and tracks follow-back statistics with built-in safety features to avoid detection.

## Features

### ✅ **Smart Filtering:**
1. **Follower Count Filter:** Only follows accounts with 100-10,000 followers (configurable) - these have the highest follow-back rates
2. **Tech Content Detection:** Analyzes bio, username, and recent posts for tech/coding keywords
3. **Private Account Skip:** Automatically skips private accounts

### ✅ **Auto Unfollow:**
- Waits 7 days (configurable) before unfollowing
- Only unfollows users who didn't follow back
- Keeps users who followed back forever

### ✅ **GUI Application:**
- Easy-to-use interface
- Real-time activity log
- Visual statistics
- One-click operations
- Settings adjustment

### ✅ **Enhanced Tracking:**
- Tracks why each user was followed
- Shows days until unfollow eligible
- Detailed follow-back reports

<img width="1915" height="1020" alt="image" src="https://github.com/user-attachments/assets/e1a75c00-9982-4b97-bb1a-7d6f491817a1" />


## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
