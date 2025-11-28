import instaloader
import time
import random
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class InstaBot:
    def __init__(self, username, password):
        """Initialize the Instagram bot with credentials"""
        self.username = username
        self.password = password
        self.loader = instaloader.Instaloader(
            quiet=False,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            download_pictures=False,
            download_videos=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            max_connection_attempts=3
        )
        
        self.stats_file = 'follow_stats.json'
        self.followed_users_file = 'followed_users.json'
        self.stats = self.load_stats()
        self.followed_users = self.load_followed_users()
        
        # Rate limiting settings to avoid detection
        self.min_delay = 30
        self.max_delay = 90
        self.hourly_limit = 20
        self.daily_limit = 150
        
        # Filtering settings
        self.min_followers = 100
        self.max_followers = 10000
        self.tech_keywords = [
            'coding', 'programming', 'developer', 'software', 'tech', 'code',
            'python', 'javascript', 'java', 'web', 'app', 'ai', 'ml', 'data',
            'engineer', 'devops', 'frontend', 'backend', 'fullstack', 'react',
            'node', 'django', 'flutter', 'android', 'ios', 'cybersecurity',
            'blockchain', 'cloud', 'aws', 'docker', 'kubernetes', 'api',
            'database', 'sql', 'mongodb', 'git', 'github', 'opensource',
            'linux', 'ubuntu', 'windows', 'macos', 'tutorial', 'learning',
            'computer', 'science', 'algorithm', 'startup', 'technology'
        ]
        
        # Unfollow settings
        self.days_before_unfollow = 7  # Wait 7 days before unfollowing
        
    def login(self):
        """Login to Instagram"""
        try:
            print(f"[{self.get_timestamp()}] Logging in as {self.username}...")
            self.loader.login(self.username, self.password)
            print(f"[{self.get_timestamp()}] ✓ Login successful!")
            return True
        except Exception as e:
            print(f"[{self.get_timestamp()}] ✗ Login failed: {str(e)}")
            return False
    
    def get_timestamp(self):
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def human_delay(self):
        """Add random human-like delay between actions"""
        delay = random.uniform(self.min_delay, self.max_delay)
        print(f"[{self.get_timestamp()}] Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def load_stats(self):
        """Load follow statistics from file"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {
            'total_followed': 0,
            'total_followed_back': 0,
            'total_unfollowed': 0,
            'follow_back_rate': 0.0,
            'last_updated': self.get_timestamp()
        }
    
    def save_stats(self):
        """Save statistics to file"""
        self.stats['last_updated'] = self.get_timestamp()
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, indent=4, fp=f)
    
    def load_followed_users(self):
        """Load list of followed users"""
        if os.path.exists(self.followed_users_file):
            with open(self.followed_users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_followed_users(self):
        """Save followed users list"""
        with open(self.followed_users_file, 'w') as f:
            json.dump(self.followed_users, indent=4, fp=f)
    
    def check_rate_limits(self):
        """Check if we're within safe rate limits"""
        now = datetime.now()
        today = now.date().isoformat()
        current_hour = now.hour
        
        today_count = sum(1 for user_data in self.followed_users.values() 
                         if user_data.get('followed_date', '').startswith(today))
        
        hour_count = sum(1 for user_data in self.followed_users.values()
                        if user_data.get('followed_date', '').startswith(f"{today} {current_hour:02d}:"))
        
        if today_count >= self.daily_limit:
            print(f"[{self.get_timestamp()}] ⚠ Daily limit reached ({self.daily_limit})")
            return False
        
        if hour_count >= self.hourly_limit:
            print(f"[{self.get_timestamp()}] ⚠ Hourly limit reached ({self.hourly_limit})")
            return False
        
        return True
    
    def is_tech_account(self, profile):
        """Check if account posts tech/coding content"""
        try:
            # Check bio for tech keywords
            bio = (profile.biography or '').lower()
            username = profile.username.lower()
            full_name = (profile.full_name or '').lower()
            
            # Check if any tech keyword is in bio, username, or full name
            for keyword in self.tech_keywords:
                if keyword in bio or keyword in username or keyword in full_name:
                    return True, f"Keyword '{keyword}' found in profile"
            
            # Check recent posts for tech-related captions/hashtags
            posts = profile.get_posts()
            tech_post_count = 0
            
            for i, post in enumerate(posts):
                if i >= 5:  # Check only last 5 posts
                    break
                
                caption = (post.caption or '').lower() if post.caption else ''
                
                for keyword in self.tech_keywords:
                    if keyword in caption:
                        tech_post_count += 1
                        break
            
            if tech_post_count >= 2:  # At least 2 out of 5 posts are tech-related
                return True, f"{tech_post_count}/5 recent posts are tech-related"
            
            return False, "No tech content detected"
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] ⚠ Error checking tech content: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def meets_follower_criteria(self, profile):
        """Check if account meets follower count criteria"""
        followers = profile.followers
        
        if followers < self.min_followers:
            return False, f"Too few followers ({followers} < {self.min_followers})"
        
        if followers > self.max_followers:
            return False, f"Too many followers ({followers} > {self.max_followers})"
        
        return True, f"Followers: {followers} (within range)"
    
    def should_follow(self, profile):
        """Determine if we should follow this account based on all criteria"""
        # Check if private
        if profile.is_private:
            return False, "Private account"
        
        # Check if already followed
        if profile.username in self.followed_users:
            return False, "Already followed"
        
        # Check follower count
        meets_followers, follower_msg = self.meets_follower_criteria(profile)
        if not meets_followers:
            return False, follower_msg
        
        # Check if tech account
        is_tech, tech_msg = self.is_tech_account(profile)
        if not is_tech:
            return False, tech_msg
        
        return True, f"✓ Tech account | {follower_msg}"
    
    def follow_user(self, username_to_follow):
        """Follow a specific user"""
        try:
            if not self.check_rate_limits():
                return False
            
            profile = instaloader.Profile.from_username(self.loader.context, username_to_follow)
            
            # Check if we should follow this account
            should_follow, reason = self.should_follow(profile)
            
            if not should_follow:
                print(f"[{self.get_timestamp()}] ⊘ Skipping {username_to_follow}: {reason}")
                return False
            
            # Follow the user
            profile.follow()
            
            # Record the follow
            self.followed_users[username_to_follow] = {
                'followed_date': self.get_timestamp(),
                'followers_count': profile.followers,
                'following_count': profile.followees,
                'followed_back': False,
                'checked_date': None,
                'bio': profile.biography[:100] if profile.biography else '',
                'reason': reason
            }
            
            self.stats['total_followed'] += 1
            
            print(f"[{self.get_timestamp()}] ✓ Followed {username_to_follow}")
            print(f"  → {reason}")
            
            self.save_followed_users()
            self.save_stats()
            
            return True
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] ✗ Error following {username_to_follow}: {str(e)}")
            return False
    
    def check_follow_backs(self):
        """Check which users followed back"""
        print(f"\n[{self.get_timestamp()}] Checking follow-backs...")
        
        try:
            my_profile = instaloader.Profile.from_username(self.loader.context, self.username)
            my_followers = set(follower.username for follower in my_profile.get_followers())
            
            updated_count = 0
            for username, data in self.followed_users.items():
                if not data['followed_back'] and username in my_followers:
                    self.followed_users[username]['followed_back'] = True
                    self.followed_users[username]['checked_date'] = self.get_timestamp()
                    self.stats['total_followed_back'] += 1
                    updated_count += 1
                    print(f"[{self.get_timestamp()}] ✓ {username} followed back!")
            
            if self.stats['total_followed'] > 0:
                self.stats['follow_back_rate'] = (self.stats['total_followed_back'] / self.stats['total_followed']) * 100
            
            self.save_followed_users()
            self.save_stats()
            
            print(f"[{self.get_timestamp()}] Found {updated_count} new follow-backs")
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] ✗ Error checking follow-backs: {str(e)}")
    
    def unfollow_non_followers(self):
        """Unfollow users who didn't follow back after specified days"""
        print(f"\n[{self.get_timestamp()}] Checking for users to unfollow...")
        
        try:
            my_profile = instaloader.Profile.from_username(self.loader.context, self.username)
            my_followers = set(follower.username for follower in my_profile.get_followers())
            
            now = datetime.now()
            unfollowed_count = 0
            
            users_to_unfollow = []
            
            for username, data in self.followed_users.items():
                # Skip if already followed back
                if data['followed_back']:
                    continue
                
                # Check if enough days have passed
                followed_date = datetime.strptime(data['followed_date'], "%Y-%m-%d %H:%M:%S")
                days_passed = (now - followed_date).days
                
                if days_passed >= self.days_before_unfollow:
                    # Double-check they haven't followed back
                    if username not in my_followers:
                        users_to_unfollow.append(username)
            
            print(f"[{self.get_timestamp()}] Found {len(users_to_unfollow)} users to unfollow")
            
            for username in users_to_unfollow:
                try:
                    if not self.check_rate_limits():
                        break
                    
                    profile = instaloader.Profile.from_username(self.loader.context, username)
                    profile.unfollow()
                    
                    # Remove from followed users
                    del self.followed_users[username]
                    self.stats['total_unfollowed'] += 1
                    unfollowed_count += 1
                    
                    print(f"[{self.get_timestamp()}] ✓ Unfollowed {username} (no follow-back)")
                    
                    self.save_followed_users()
                    self.save_stats()
                    
                    # Human-like delay
                    time.sleep(random.uniform(20, 40))
                    
                except Exception as e:
                    print(f"[{self.get_timestamp()}] ✗ Error unfollowing {username}: {str(e)}")
            
            print(f"\n[{self.get_timestamp()}] Unfollowed {unfollowed_count} users")
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] ✗ Error in unfollow process: {str(e)}")
    
    def follow_from_list(self, usernames_list):
        """Follow users from a list"""
        print(f"\n[{self.get_timestamp()}] Starting follow campaign...")
        print(f"Target users: {len(usernames_list)}")
        
        followed_count = 0
        for username in usernames_list:
            if self.follow_user(username):
                followed_count += 1
                self.human_delay()
        
        print(f"\n[{self.get_timestamp()}] Campaign complete. Followed {followed_count} new users.")
        self.display_stats()
    
    def follow_followers_of(self, target_username, max_follows=50):
        """Follow followers of a specific account with filtering"""
        try:
            print(f"\n[{self.get_timestamp()}] Getting followers of {target_username}...")
            
            target_profile = instaloader.Profile.from_username(self.loader.context, target_username)
            followers = target_profile.get_followers()
            
            followed_count = 0
            checked_count = 0
            
            for follower in followers:
                if followed_count >= max_follows:
                    break
                
                if checked_count >= max_follows * 3:  # Check max 3x the target
                    break
                
                checked_count += 1
                
                if self.follow_user(follower.username):
                    followed_count += 1
                    self.human_delay()
            
            print(f"\n[{self.get_timestamp()}] Followed {followed_count}/{checked_count} checked followers of {target_username}")
            self.display_stats()
            
        except Exception as e:
            print(f"[{self.get_timestamp()}] ✗ Error: {str(e)}")
    
    def display_stats(self):
        """Display follow statistics"""
        print("\n" + "="*60)
        print("📊 FOLLOW STATISTICS")
        print("="*60)
        print(f"Total Followed:        {self.stats['total_followed']}")
        print(f"Total Followed Back:   {self.stats['total_followed_back']}")
        print(f"Total Unfollowed:      {self.stats['total_unfollowed']}")
        print(f"Follow Back Rate:      {self.stats['follow_back_rate']:.2f}%")
        print(f"Currently Following:   {len(self.followed_users)}")
        print(f"Last Updated:          {self.stats['last_updated']}")
        print("="*60 + "\n")
    
    def get_detailed_report(self):
        """Get detailed follow-back report"""
        followed_back = []
        not_followed_back = []
        waiting = []
        
        now = datetime.now()
        
        for username, data in self.followed_users.items():
            followed_date = datetime.strptime(data['followed_date'], "%Y-%m-%d %H:%M:%S")
            days_passed = (now - followed_date).days
            
            if data['followed_back']:
                followed_back.append((username, data))
            elif days_passed < self.days_before_unfollow:
                waiting.append((username, data, days_passed))
            else:
                not_followed_back.append((username, data, days_passed))
        
        print("\n" + "="*60)
        print("📋 DETAILED REPORT")
        print("="*60)
        
        print(f"\n✓ Users who followed back ({len(followed_back)}):")
        for user, data in followed_back[:10]:
            print(f"  - {user} (Followers: {data['followers_count']})")
        if len(followed_back) > 10:
            print(f"  ... and {len(followed_back) - 10} more")
        
        print(f"\n⏳ Waiting for follow-back ({len(waiting)}):")
        for user, data, days in waiting[:10]:
            print(f"  - {user} (Day {days}/{self.days_before_unfollow})")
        if len(waiting) > 10:
            print(f"  ... and {len(waiting) - 10} more")
        
        print(f"\n⚠ Ready to unfollow ({len(not_followed_back)}):")
        for user, data, days in not_followed_back[:10]:
            print(f"  - {user} (No follow-back after {days} days)")
        if len(not_followed_back) > 10:
            print(f"  ... and {len(not_followed_back) - 10} more")
        
        print("="*60 + "\n")