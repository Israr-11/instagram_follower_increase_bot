from insta_bot_selenium import InstaBotSelenium
import config

print("="*60)
print("INSTAGRAM BOT - SELENIUM VERSION (ACTUALLY WORKS!)")
print("="*60)

# Initialize bot (headless=False to see browser)
bot = InstaBotSelenium(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD, headless=False)

# Apply settings - INCREASED for better results
bot.min_followers = 500      # At least 500 followers (active accounts)
bot.max_followers = 5000    # Up to 5k followers (better chance of finding matches)
bot.min_delay = 30           # Safer delays
bot.max_delay = 60

print(f"\nSettings:")
print(f"  - Min Followers: {bot.min_followers}")
print(f"  - Max Followers: {bot.max_followers}")
print(f"  - Delays: {bot.min_delay}-{bot.max_delay} seconds")

# Login
if not bot.login():
    print("\nLogin failed. Exiting...")
    bot.close()
    exit()

print("\n[+] Login successful!")
print("\n" + "="*60)
print("CHOOSE AN OPTION:")
print("="*60)
print("1. Search by hashtag (e.g., #webdevelopment, #python)")
print("2. Follow specific users (you must edit the code first)")
print("3. Exit")
print("="*60)

choice = input("\nEnter choice (1, 2, or 3): ").strip()

try:
    if choice == "1":
        # Search hashtags
        print("\n[+] Starting hashtag search mode...")
        print("[+] Will search: #webdevelopment, #python, #coding, #programming")
        print("[+] Will follow 3 users from each hashtag")
        print()
        
        confirm = input("Continue? (y/n): ").strip().lower()
        
        if confirm == 'y':
            # Use smaller/more specific hashtags for better results
            hashtags = ["100daysofcode", "learntocode", "codingnewbie", "frontend"]
            
            print(f"[+] Using hashtags: {', '.join(['#' + h for h in hashtags])}")
            print(f"[+] These have more small/medium accounts")
            print()
            
            for hashtag in hashtags:
                print(f"\n{'='*60}")
                print(f"Processing #{hashtag}")
                print('='*60)
                
                bot.search_and_follow(hashtag, max_follows=3)  # Start with 3 per hashtag
                
                print("\n[+] Completed this hashtag!")
                cont = input("Continue to next hashtag? (y/n): ").strip().lower()
                if cont != 'y':
                    print("[!] Stopping...")
                    break
            
            print("\n[+] All hashtags processed!")
        else:
            print("[!] Cancelled by user")
    
    elif choice == "2":
        # Follow specific users
        users_to_follow = [
            # Add real usernames here!
            # Example: "techwithtim", "cs_dojo", "python_hub"
        ]
        
        if len(users_to_follow) == 0:
            print("\n[!] ERROR: No users specified!")
            print("[!] Edit test_bot.py and add usernames to 'users_to_follow' list")
            print("[!] Example: users_to_follow = ['techaccount1', 'devblog2']")
        else:
            print(f"\n[+] Following {len(users_to_follow)} specific users...")
            
            followed = 0
            for username in users_to_follow:
                if bot.follow_user(username):
                    followed += 1
                    bot.human_delay()
            
            print(f"\n[+] Followed {followed}/{len(users_to_follow)} users")
    
    elif choice == "3":
        print("\n[!] Exiting without following anyone...")
    
    else:
        print(f"\n[!] Invalid choice: {choice}")
        print("[!] Please run again and choose 1, 2, or 3")

except KeyboardInterrupt:
    print("\n\n[!] Stopped by user (Ctrl+C)")

except Exception as e:
    print(f"\n[x] ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    print("\n" + "="*60)
    print("FINAL STATS")
    print("="*60)
    bot.display_stats()
    
    print("\n[+] Closing browser...")
    bot.close()
    
    print("\n[+] Done! Check followed_users.json for details")