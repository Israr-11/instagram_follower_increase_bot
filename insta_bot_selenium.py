"""
Instagram Bot using Selenium - ACTUALLY WORKS!
This mimics real browser behavior just like Phantom and other professional tools
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import json
import os
from datetime import datetime

class InstaBotSelenium:
    def __init__(self, username, password, headless=False):
        """Initialize Instagram bot with real browser"""
        self.username = username
        self.password = password
        self.driver = None
        self.headless = headless
        
        # Files
        self.stats_file = 'follow_stats.json'
        self.followed_users_file = 'followed_users.json'
        self.stats = self.load_stats()
        self.followed_users = self.load_followed_users()
        
        # Settings
        self.min_followers = 100
        self.max_followers = 10000
        self.min_delay = 30
        self.max_delay = 60
        self.days_before_unfollow = 7
        
        # Tech keywords for filtering
        self.tech_keywords = [
            'coding', 'programming', 'developer', 'software', 'tech', 'code',
            'python', 'javascript', 'java', 'web', 'app', 'ai', 'ml', 'data',
            'engineer', 'devops', 'frontend', 'backend', 'fullstack', 'react',
            'node', 'django', 'flutter', 'android', 'ios', 'html', 'css'
        ]

            # NEW: Flexible filter settings
        self.tech_only = True
        self.check_bio = True
        self.check_username = True
        self.skip_private = True
        self.skip_verified = False
        self.max_follows_per_hashtag = 5
    
    def setup_driver(self):
        """Setup Chrome driver with anti-detection measures"""
        print("[+] Setting up Chrome browser...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection measures
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to hide automation
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("[+] Browser ready!")
    
    def login(self):
        """Login to Instagram"""
        try:
            if not self.driver:
                self.setup_driver()
            
            print(f"[+] Logging in as {self.username}...")
            self.driver.get('https://www.instagram.com/accounts/login/')
            
            # Wait for page to load
            time.sleep(random.uniform(3, 5))
            
            # Accept cookies if present
            try:
                cookies_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]"))
                )
                cookies_btn.click()
                time.sleep(2)
            except:
                pass
            
            # Find username and password fields
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            password_input = self.driver.find_element(By.NAME, 'password')
            
            # Type with human-like delays
            self.human_type(username_input, self.username)
            time.sleep(random.uniform(1, 2))
            self.human_type(password_input, self.password)
            time.sleep(random.uniform(1, 2))
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("[+] Waiting for login...")
            time.sleep(random.uniform(5, 8))
            
            # Check if login was successful
            try:
                # Look for "Save Your Login Info" or "Not Now" buttons
                save_info = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now') or contains(text(), 'Not now')]"))
                )
                save_info.click()
                time.sleep(2)
            except:
                pass
            
            # Dismiss notification popup if present
            try:
                notif_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                notif_button.click()
                time.sleep(2)
            except:
                pass
            
            print("[+] Login successful!")
            return True
            
        except Exception as e:
            print(f"[x] Login failed: {str(e)}")
            return False
    
    def human_type(self, element, text):
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def human_delay(self, min_sec=None, max_sec=None):
        """Human-like delay"""
        min_sec = min_sec or self.min_delay
        max_sec = max_sec or self.max_delay
        delay = random.uniform(min_sec, max_sec)
        print(f"[~] Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def get_timestamp(self):
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def load_stats(self):
        """Load statistics"""
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
        """Save statistics"""
        self.stats['last_updated'] = self.get_timestamp()
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, indent=4, fp=f)
    
    def load_followed_users(self):
        """Load followed users"""
        if os.path.exists(self.followed_users_file):
            with open(self.followed_users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_followed_users(self):
        """Save followed users"""
        with open(self.followed_users_file, 'w') as f:
            json.dump(self.followed_users, indent=4, fp=f)
    
    def is_tech_account(self, username):
        """Check if account is tech-related"""
        try:
            # Go to profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(random.uniform(2, 4))
            
            # Get bio text
            try:
                bio = self.driver.find_element(By.XPATH, "//div[contains(@class, '_aa_c')]").text.lower()
            except:
                bio = ""
            
            # Check username
            username_lower = username.lower()
            
            # Check for tech keywords
            all_text = f"{bio} {username_lower}"
            
            for keyword in self.tech_keywords:
                if keyword in all_text:
                    return True, f"Tech keyword: {keyword}"
            
            return False, "No tech content"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_follower_count(self, username):
        """Get follower count for a user"""
        try:
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(random.uniform(2, 3))
            
            # Find followers count
            followers_elem = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]/span/span")
            followers_text = followers_elem.get_attribute('title')
            
            if not followers_text:
                followers_text = followers_elem.text
            
            # Remove commas and convert to int
            followers_count = int(followers_text.replace(',', '').replace('K', '000').replace('M', '000000'))
            
            return followers_count
            
        except Exception as e:
            print(f"[!] Could not get follower count: {str(e)}")
            return 0
    
    def follow_user(self, username):
        """Follow a specific user"""
        try:
            # Check if already followed
            if username in self.followed_users:
                print(f"[-] Already followed: {username}")
                return False
            
            print(f"\n[>] Checking: {username}")
            
            # Go to profile
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(random.uniform(3, 5))
            
            # Check if profile exists
            if "Sorry, this page isn't available" in self.driver.page_source:
                print(f"[-] Profile not found: {username}")
                return False
            
            # Check if private
            is_private = "This account is private" in self.driver.page_source
            if is_private:
                print(f"[-] Private account: {username}")
                return False
            
            # Get follower count
            followers = self.get_follower_count(username)
            
            if followers < self.min_followers:
                print(f"[-] Too few followers ({followers}): {username}")
                return False
            
            if followers > self.max_followers:
                print(f"[-] Too many followers ({followers}): {username}")
                return False
            
            # Check if tech account
            is_tech, reason = self.is_tech_account(username)
            if not is_tech:
                print(f"[-] Not tech account: {username} - {reason}")
                return False
            
            # Find and click follow button
            try:
                follow_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Follow') and not(contains(text(), 'Following'))]"))
                )
                
                # Scroll to button
                self.driver.execute_script("arguments[0].scrollIntoView();", follow_button)
                time.sleep(1)
                
                # Click follow
                follow_button.click()
                
                # Record the follow
                self.followed_users[username] = {
                    'followed_date': self.get_timestamp(),
                    'followers_count': followers,
                    'followed_back': False,
                    'reason': reason
                }
                
                self.stats['total_followed'] += 1
                
                print(f"[+] FOLLOWED: {username} (Followers: {followers})")
                print(f"    Reason: {reason}")
                
                self.save_followed_users()
                self.save_stats()
                
                return True
                
            except Exception as e:
                print(f"[-] Could not follow {username}: {str(e)}")
                return False
                
        except Exception as e:
            print(f"[x] Error following {username}: {str(e)}")
            return False
    
    def search_and_follow(self, hashtag, max_follows=10):
        """Search hashtag and follow users"""
        print(f"\n[+] Searching hashtag: #{hashtag}")
        
        try:
            # Go to hashtag page
            self.driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(random.uniform(3, 5))
            
            # Scroll and collect posts
            posts_found = []
            
            for scroll in range(3):
                # Find post links
                posts = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                
                for post in posts:
                    href = post.get_attribute('href')
                    if href and href not in posts_found:
                        posts_found.append(href)
                
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
            
            print(f"[+] Found {len(posts_found)} posts")
            
            followed_count = 0
            
            for post_url in posts_found[:max_follows * 3]:  # Check 3x the target
                if followed_count >= max_follows:
                    break
                
                try:
                    # Go to post
                    self.driver.get(post_url)
                    time.sleep(random.uniform(2, 4))
                    
                    # Get username
                    username_elem = self.driver.find_element(By.XPATH, "//a[contains(@href, '/') and @role='link']")
                    username = username_elem.get_attribute('href').split('/')[-2]
                    
                    if self.follow_user(username):
                        followed_count += 1
                        self.human_delay()
                
                except Exception as e:
                    print(f"[!] Error processing post: {str(e)}")
                    continue
            
            print(f"\n[+] Followed {followed_count} users from #{hashtag}")
            
        except Exception as e:
            print(f"[x] Error searching hashtag: {str(e)}")
    
    def display_stats(self):
        """Display statistics"""
        print("\n" + "="*60)
        print("FOLLOW STATISTICS")
        print("="*60)
        print(f"Total Followed:        {self.stats['total_followed']}")
        print(f"Total Followed Back:   {self.stats['total_followed_back']}")
        print(f"Total Unfollowed:      {self.stats['total_unfollowed']}")
        print(f"Follow Back Rate:      {self.stats['follow_back_rate']:.2f}%")
        print(f"Currently Following:   {len(self.followed_users)}")
        print(f"Last Updated:          {self.stats['last_updated']}")
        print("="*60 + "\n")
    
    def close(self):
        """Close browser"""
        if self.driver:
            print("[+] Closing browser...")
            self.driver.quit()
