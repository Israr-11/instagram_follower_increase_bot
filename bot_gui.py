import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from insta_bot import InstaBot
import config

class InstaBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Follow Bot")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        self.bot = None
        self.is_logged_in = False
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#0078d4', foreground='white', 
                       font=('Segoe UI', 10), padding=10)
        style.configure('TLabel', background='#1e1e1e', foreground='white', 
                       font=('Segoe UI', 10))
        style.configure('TFrame', background='#1e1e1e')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="🤖 Instagram Follow Bot", 
                        font=('Segoe UI', 20, 'bold'), bg='#1e1e1e', fg='#0078d4')
        title.pack(pady=10)
        
        # Login Frame
        login_frame = ttk.Frame(self.root)
        login_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.insert(0, config.INSTAGRAM_USERNAME)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, show='*')
        self.password_entry.insert(0, config.INSTAGRAM_PASSWORD)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.login_btn = ttk.Button(login_frame, text="Login", command=self.login)
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Filter Settings", padding=10)
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(settings_frame, text="Min Followers:").grid(row=0, column=0, sticky='w', pady=5)
        self.min_followers = ttk.Entry(settings_frame, width=15)
        self.min_followers.insert(0, str(config.FILTER_SETTINGS['min_followers']))
        self.min_followers.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Max Followers:").grid(row=0, column=2, sticky='w', pady=5)
        self.max_followers = ttk.Entry(settings_frame, width=15)
        self.max_followers.insert(0, str(config.FILTER_SETTINGS['max_followers']))
        self.max_followers.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="Days Before Unfollow:").grid(row=1, column=0, sticky='w', pady=5)
        self.days_unfollow = ttk.Entry(settings_frame, width=15)
        self.days_unfollow.insert(0, str(config.BOT_SETTINGS['days_before_unfollow']))
        self.days_unfollow.grid(row=1, column=1, padx=10, pady=5)
        
        # Stats Frame
        stats_frame = ttk.LabelFrame(self.root, text="Statistics", padding=10)
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        self.stats_text = tk.Text(stats_frame, height=5, bg='#2d2d2d', fg='white', 
                                 font=('Consolas', 10), relief='flat')
        self.stats_text.pack(fill='x')
        
        # Action Buttons Frame
        actions_frame = ttk.Frame(self.root)
        actions_frame.pack(pady=10, padx=20, fill='x')
        
        btn_config = {'width': 20, 'padding': 10}
        
        self.follow_target_btn = ttk.Button(actions_frame, text="Follow from Targets", 
                                           command=self.follow_from_targets, **btn_config)
        self.follow_target_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.check_followback_btn = ttk.Button(actions_frame, text="Check Follow-backs", 
                                              command=self.check_followbacks, **btn_config)
        self.check_followback_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.unfollow_btn = ttk.Button(actions_frame, text="Unfollow Non-followers", 
                                       command=self.unfollow_non_followers, **btn_config)
        self.unfollow_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.stats_btn = ttk.Button(actions_frame, text="Refresh Stats", 
                                   command=self.update_stats, **btn_config)
        self.stats_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.report_btn = ttk.Button(actions_frame, text="Detailed Report", 
                                    command=self.show_report, **btn_config)
        self.report_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Disable action buttons initially
        self.toggle_action_buttons(False)
        
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding=10)
        log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, bg='#2d2d2d', 
                                                  fg='#00ff00', font=('Consolas', 9), 
                                                  relief='flat')
        self.log_text.pack(fill='both', expand=True)
    
    def toggle_action_buttons(self, state):
        """Enable/disable action buttons"""
        btn_state = 'normal' if state else 'disabled'
        self.follow_target_btn['state'] = btn_state
        self.check_followback_btn['state'] = btn_state
        self.unfollow_btn['state'] = btn_state
        self.stats_btn['state'] = btn_state
        self.report_btn['state'] = btn_state
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def login(self):
        """Login to Instagram"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        def login_thread():
            self.log("Logging in...")
            self.bot = InstaBot(username, password)
            
            # Apply settings
            try:
                self.bot.min_followers = int(self.min_followers.get())
                self.bot.max_followers = int(self.max_followers.get())
                self.bot.days_before_unfollow = int(self.days_unfollow.get())
            except:
                pass
            
            if self.bot.login():
                self.is_logged_in = True
                self.log("✓ Login successful!")
                self.toggle_action_buttons(True)
                self.login_btn['state'] = 'disabled'
                self.update_stats()
            else:
                self.log("✗ Login failed!")
                messagebox.showerror("Error", "Login failed. Check credentials.")
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def update_stats(self):
        """Update statistics display"""
        if not self.bot:
            return
        
        stats = self.bot.stats
        self.stats_text.delete('1.0', tk.END)
        
        stats_str = f"""
Total Followed:       {stats['total_followed']}
Total Followed Back:  {stats['total_followed_back']}
Total Unfollowed:     {stats['total_unfollowed']}
Follow Back Rate:     {stats['follow_back_rate']:.2f}%
Currently Following:  {len(self.bot.followed_users)}
        """
        self.stats_text.insert('1.0', stats_str)
    
    def follow_from_targets(self):
        """Follow followers from target accounts"""
        if not self.is_logged_in:
            messagebox.showerror("Error", "Please login first")
            return
        
        def follow_thread():
            self.log("\n=== Starting Follow Campaign ===")
            for target in config.TARGET_ACCOUNTS:
                self.log(f"\nProcessing: {target}")
                # Redirect bot output to GUI log
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                self.bot.follow_followers_of(target, max_follows=config.BOT_SETTINGS['max_follows_per_account'])
                
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                for line in output.split('\n'):
                    if line.strip():
                        self.log(line)
            
            self.log("\n=== Campaign Complete ===")
            self.update_stats()
        
        threading.Thread(target=follow_thread, daemon=True).start()
    
    def check_followbacks(self):
        """Check for follow-backs"""
        if not self.is_logged_in:
            messagebox.showerror("Error", "Please login first")
            return
        
        def check_thread():
            self.log("\n=== Checking Follow-backs ===")
            self.bot.check_follow_backs()
            self.log("=== Check Complete ===")
            self.update_stats()
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def unfollow_non_followers(self):
        """Unfollow users who didn't follow back"""
        if not self.is_logged_in:
            messagebox.showerror("Error", "Please login first")
            return
        
        confirm = messagebox.askyesno("Confirm", 
                                     "Unfollow users who didn't follow back?")
        if not confirm:
            return
        
        def unfollow_thread():
            self.log("\n=== Starting Unfollow Process ===")
            self.bot.unfollow_non_followers()
            self.log("=== Unfollow Complete ===")
            self.update_stats()
        
        threading.Thread(target=unfollow_thread, daemon=True).start()
    
    def show_report(self):
        """Show detailed report in new window"""
        if not self.is_logged_in:
            messagebox.showerror("Error", "Please login first")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Detailed Report")
        report_window.geometry("600x500")
        report_window.configure(bg='#1e1e1e')
        
        report_text = scrolledtext.ScrolledText(report_window, bg='#2d2d2d', 
                                               fg='white', font=('Consolas', 9))
        report_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Generate report
        from datetime import datetime
        followed_back = []
        not_followed_back = []
        waiting = []
        
        now = datetime.now()
        
        for username, data in self.bot.followed_users.items():
            followed_date = datetime.strptime(data['followed_date'], "%Y-%m-%d %H:%M:%S")
            days_passed = (now - followed_date).days
            
            if data['followed_back']:
                followed_back.append((username, data))
            elif days_passed < self.bot.days_before_unfollow:
                waiting.append((username, data, days_passed))
            else:
                not_followed_back.append((username, data, days_passed))
        
        report = "=" * 60 + "\n"
        report += "DETAILED FOLLOW REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += f"✓ Users who followed back ({len(followed_back)}):\n"
        for user, data in followed_back:
            report += f"  - {user} (Followers: {data['followers_count']})\n"
        
        report += f"\n⏳ Waiting for follow-back ({len(waiting)}):\n"
        for user, data, days in waiting:
            report += f"  - {user} (Day {days}/{self.bot.days_before_unfollow})\n"
        
        report += f"\n⚠ Ready to unfollow ({len(not_followed_back)}):\n"
        for user, data, days in not_followed_back:
            report += f"  - {user} (No follow-back after {days} days)\n"
        
        report_text.insert('1.0', report)

def main():
    root = tk.Tk()
    app = InstaBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()