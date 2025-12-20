from insta_bot_selenium import InstaBotSelenium
import config
import traceback

def print_banner():
    print("\n" + "="*70)
    print(" " * 15 + "INSTAGRAM BOT - INTERACTIVE MODE")
    print("="*70)

def print_current_settings(bot):
    print("\n" + "="*70)
    print("CURRENT SETTINGS:")
    print("="*70)
    print(f"Min Followers:        {bot.min_followers:,}")
    print(f"Max Followers:        {bot.max_followers:,}")
    print(f"Tech Keywords Only:   {'Yes' if bot.tech_only else 'No'}")
    print(f"Check Bio:            {'Yes' if bot.check_bio else 'No'}")
    print(f"Check Username:       {'Yes' if bot.check_username else 'No'}")
    print(f"Skip Private:         {'Yes' if bot.skip_private else 'No'}")
    print(f"Follow Delay:         {bot.min_delay}-{bot.max_delay} seconds")
    print(f"Max Per Hashtag:      {bot.max_follows_per_hashtag}")
    print("="*70 + "\n")

def adjust_settings(bot):
    print("\n" + "="*70)
    print("ADJUST SETTINGS:")
    print("="*70)
    print("1. Change follower range")
    print("2. Toggle tech-only filter")
    print("3. Change delays")
    print("4. Change max follows per hashtag")
    print("5. Toggle filters (bio/username/private)")
    print("6. Back to main menu")
    print("="*70)
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '1':
        try:
            min_f = input(f"Min followers [{bot.min_followers}]: ").strip()
            max_f = input(f"Max followers [{bot.max_followers}]: ").strip()
            
            if min_f:
                bot.min_followers = int(min_f)
            if max_f:
                bot.max_followers = int(max_f)
            
            print(f"\n[+] Updated: {bot.min_followers:,} - {bot.max_followers:,} followers")
        except:
            print("\n[!] Invalid input")
    
    elif choice == '2':
        bot.tech_only = not bot.tech_only
        print(f"\n[+] Tech-only filter: {'ON' if bot.tech_only else 'OFF'}")
    
    elif choice == '3':
        try:
            min_d = input(f"Min delay [{bot.min_delay}s]: ").strip()
            max_d = input(f"Max delay [{bot.max_delay}s]: ").strip()
            
            if min_d:
                bot.min_delay = int(min_d)
            if max_d:
                bot.max_delay = int(max_d)
            
            print(f"\n[+] Updated delays: {bot.min_delay}-{bot.max_delay} seconds")
        except:
            print("\n[!] Invalid input")
    
    elif choice == '4':
        try:
            max_f = input(f"Max per hashtag [{bot.max_follows_per_hashtag}]: ").strip()
            if max_f:
                bot.max_follows_per_hashtag = int(max_f)
            print(f"\n[+] Updated: {bot.max_follows_per_hashtag} max per hashtag")
        except:
            print("\n[!] Invalid input")
    
    elif choice == '5':
        print("\nCurrent filters:")
        print(f"1. Check Bio: {bot.check_bio}")
        print(f"2. Check Username: {bot.check_username}")
        print(f"3. Skip Private: {bot.skip_private}")
        
        toggle = input("\nToggle which? (1-3): ").strip()
        if toggle == '1':
            bot.check_bio = not bot.check_bio
            print(f"[+] Check Bio: {bot.check_bio}")
        elif toggle == '2':
            bot.check_username = not bot.check_username
            print(f"[+] Check Username: {bot.check_username}")
        elif toggle == '3':
            bot.skip_private = not bot.skip_private
            print(f"[+] Skip Private: {bot.skip_private}")

def search_custom_hashtag(bot):
    print("\n" + "="*70)
    print("SEARCH BY CUSTOM HASHTAG")
    print("="*70)
    
    hashtag = input("Enter hashtag (without #): ").strip()
    if not hashtag:
        print("[!] No hashtag entered")
        return
    
    max_follows = input(f"Max follows [{bot.max_follows_per_hashtag}]: ").strip()
    if max_follows:
        try:
            max_follows = int(max_follows)
        except:
            max_follows = bot.max_follows_per_hashtag
    else:
        max_follows = bot.max_follows_per_hashtag
    
    print(f"\n[+] Searching #{hashtag} (max {max_follows} follows)")
    print("[+] Press Ctrl+C to stop at any time\n")
    
    try:
        bot.search_and_follow(hashtag, max_follows=max_follows)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

def search_predefined_hashtags(bot):
    print("\n" + "="*70)
    print("PREDEFINED HASHTAG CATEGORIES")
    print("="*70)
    
    categories = list(config.HASHTAGS.keys())
    for i, cat in enumerate(categories, 1):
        tags = config.HASHTAGS[cat]
        print(f"{i}. {cat.upper()}: {', '.join(['#'+t for t in tags[:3]])}...")
    
    print("="*70)
    
    choice = input(f"\nSelect category (1-{len(categories)}): ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(categories):
            category = categories[idx]
            hashtags = config.HASHTAGS[category]
            
            print(f"\n[+] Selected: {category.upper()}")
            print(f"[+] Hashtags: {', '.join(['#'+t for t in hashtags])}")
            
            max_per = input(f"\nMax follows per hashtag [{bot.max_follows_per_hashtag}]: ").strip()
            if max_per:
                try:
                    max_per = int(max_per)
                except:
                    max_per = bot.max_follows_per_hashtag
            else:
                max_per = bot.max_follows_per_hashtag
            
            print(f"\n[+] Will process {len(hashtags)} hashtags, {max_per} follows each")
            confirm = input("Continue? (y/n): ").strip().lower()
            
            if confirm == 'y':
                for i, hashtag in enumerate(hashtags, 1):
                    print(f"\n{'='*70}")
                    print(f"[{i}/{len(hashtags)}] Processing #{hashtag}")
                    print('='*70)
                    
                    try:
                        bot.search_and_follow(hashtag, max_follows=max_per)
                    except KeyboardInterrupt:
                        print("\n[!] Stopped by user")
                        break
                    except Exception as e:
                        print(f"[!] Error: {str(e)}")
                    
                    if i < len(hashtags):
                        cont = input("\nContinue to next hashtag? (y/n): ").strip().lower()
                        if cont != 'y':
                            break
                
                print("\n[+] All hashtags processed!")
        else:
            print("[!] Invalid choice")
    except:
        print("[!] Invalid input")

def follow_specific_users(bot):
    print("\n" + "="*70)
    print("FOLLOW SPECIFIC USERS")
    print("="*70)
    
    print("Enter usernames (comma-separated):")
    print("Example: user1, user2, user3")
    
    usernames = input("\nUsernames: ").strip()
    if not usernames:
        print("[!] No usernames entered")
        return
    
    user_list = [u.strip().replace('@', '') for u in usernames.split(',')]
    
    print(f"\n[+] Will attempt to follow {len(user_list)} users:")
    for u in user_list:
        print(f"  - {u}")
    
    confirm = input("\nContinue? (y/n): ").strip().lower()
    
    if confirm == 'y':
        for username in user_list:
            try:
                print(f"\n[>] Processing: {username}")
                if bot.follow_user(username):
                    print(f"[+] Followed: {username}")
                else:
                    print(f"[-] Skipped: {username}")
                
                import time
                import random
                time.sleep(random.uniform(bot.min_delay, bot.max_delay))
            except KeyboardInterrupt:
                print("\n[!] Stopped by user")
                break
            except Exception as e:
                print(f"[!] Error: {str(e)}")

def main_menu(bot):
    while True:
        print_current_settings(bot)
        
        print("="*70)
        print("MAIN MENU")
        print("="*70)
        print("1. Search by custom hashtag")
        print("2. Search predefined hashtag categories")
        print("3. Follow specific users")
        print("4. Check follow-backs")
        print("5. Adjust settings")
        print("6. Show statistics")
        print("7. Exit")
        print("="*70)
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            search_custom_hashtag(bot)
        
        elif choice == '2':
            search_predefined_hashtags(bot)
        
        elif choice == '3':
            follow_specific_users(bot)
        
        elif choice == '4':
            print("\n[+] Checking follow-backs...")
            try:
                bot.check_follow_backs()
            except Exception as e:
                print(f"[!] Error: {str(e)}")
        
        elif choice == '5':
            adjust_settings(bot)
        
        elif choice == '6':
            bot.display_stats()
        
        elif choice == '7':
            print("\n[+] Exiting...")
            break
        
        else:
            print("\n[!] Invalid choice")

def main():
    print_banner()
    
    print("[+] Initializing bot...")
    
    try:
        bot = InstaBotSelenium(
            config.INSTAGRAM_USERNAME,
            config.INSTAGRAM_PASSWORD,
            headless=config.BOT_SETTINGS['headless']
        )
        
        # Apply all settings from config
        bot.min_followers = config.FILTER_SETTINGS['min_followers']
        bot.max_followers = config.FILTER_SETTINGS['max_followers']
        bot.tech_only = config.FILTER_SETTINGS['tech_only']
        bot.check_bio = config.FILTER_SETTINGS['check_bio']
        bot.check_username = config.FILTER_SETTINGS['check_username']
        bot.skip_private = config.FILTER_SETTINGS['skip_private']
        bot.min_delay = config.BOT_SETTINGS['min_delay']
        bot.max_delay = config.BOT_SETTINGS['max_delay']
        bot.max_follows_per_hashtag = config.BOT_SETTINGS['max_follows_per_hashtag']
        bot.tech_keywords = config.TECH_KEYWORDS
        
        print("[+] Bot initialized!")
        
        # Login
        print("[+] Logging in...")
        if not bot.login():
            print("[!] Login failed. Exiting...")
            bot.close()
            return
        
        print("[+] Login successful!\n")
        
        # Main menu loop
        main_menu(bot)
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    
    except Exception as e:
        print(f"\n[!] ERROR: {str(e)}")
        traceback.print_exc()
    
    finally:
        print("\n" + "="*70)
        print("FINAL STATISTICS")
        print("="*70)
        bot.display_stats()
        
        print("\n[+] Closing browser...")
        bot.close()
        
        print("\n[+] Done! Check followed_users.json for details")
        print("="*70 + "\n")

if __name__ == "__main__":
    main()