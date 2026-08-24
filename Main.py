#!/data/data/com.termux/files/usr/bin/python
import os
import sys
import time
import random
from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, BadCredentials, TwoFactorRequired, ClientError

# Colors for terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    clear_screen()
    print(f"""{PURPLE}
    ╔══════════════════════════════════════╗
    ║                                      ║
    ║   ☠️  𝐍𝐀𝐒𝐈𝐈𝐑 𝐀𝐋𝐈𝐈 𝐊𝐈𝐈𝐍𝐆  ☠️      ║
    ║      Instagram Edition               ║
    ║                                      ║
    ╚══════════════════════════════════════╝
    {END}""")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{END}")
    print(f"{YELLOW}💬 Instagram Message Sender Tool 💬{END}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{END}\n")

def load_messages(file_path):
    """Read messages from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()]
        return messages
    except FileNotFoundError:
        print(f"{RED}❌ File not found: {file_path}{END}")
        print(f"{YELLOW}💡 Tip: 'messages.txt' file banao apne messages ke saath{END}")
        return []
    except Exception as e:
        print(f"{RED}❌ Error reading file: {e}{END}")
        return []

def instagram_login():
    """Instagram login function with proper error handling"""
    print(f"\n{BOLD}{PURPLE}📱 INSTAGRAM LOGIN{END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    
    username = input(f"{CYAN}👤 Instagram Username: {END}").strip()
    password = input(f"{CYAN}🔑 Instagram Password: {END}").strip()
    
    if not username or not password:
        print(f"{RED}❌ Username/Password required!{END}")
        return None
    
    print(f"\n{YELLOW}⏳ Connecting to Instagram...{END}")
    
    try:
        # Create client with proper settings
        cl = Client()
        
        # Set delay to avoid rate limiting
        cl.delay_range = [2, 5]
        
        # Try to login
        cl.login(username, password)
        
        # Verify login
        if cl.user_id:
            print(f"{GREEN}✅ Login Successful!{END}")
            print(f"{GREEN}👤 Logged in as: @{username}{END}")
            return cl
        else:
            print(f"{RED}❌ Login failed - user_id not found{END}")
            return None
            
    except BadCredentials:
        print(f"{RED}❌ Invalid username or password!{END}")
        return None
    except TwoFactorRequired:
        print(f"{YELLOW}⚠️ Two-Factor Authentication (2FA) required.{END}")
        print(f"{YELLOW}💡 Solution: Disable 2FA temporarily OR use APP password{END}")
        print(f"{YELLOW}   Instagram > Settings > Security > Two-Factor Authentication{END}")
        return None
    except LoginRequired:
        print(f"{RED}❌ Login required but failed!{END}")
        return None
    except ClientError as e:
        print(f"{RED}❌ Instagram error: {e}{END}")
        return None
    except Exception as e:
        print(f"{RED}❌ Unexpected error: {e}{END}")
        return None

def get_user_id(cl, username):
    """Get user ID from username"""
    try:
        user_id = cl.user_id_from_username(username)
        return user_id
    except Exception as e:
        print(f"{RED}❌ Could not find user @{username}{END}")
        return None

def send_messages(cl, user_id, username, prefix, messages, delay):
    """Send messages to a user"""
    total = len(messages)
    success = 0
    failed = 0
    
    print(f"\n{BOLD}{GREEN}🚀 Sending Messages Started!{END}")
    print(f"{BLUE}📝 Total Messages: {total}{END}")
    print(f"{BLUE}👤 Target: @{username}{END}")
    print(f"{BLUE}⏰ Delay: {delay} seconds{END}\n")
    
    for idx, msg in enumerate(messages, 1):
        # Add prefix if provided
        full_message = f"{prefix} {msg}" if prefix else msg
        
        try:
            # Send message
            cl.direct_send(full_message, users=[user_id])
            success += 1
            print(f"{GREEN}✅ [{idx}/{total}] Sent: {full_message[:50]}{END}")
        except Exception as e:
            failed += 1
            print(f"{RED}❌ [{idx}/{total}] Failed: {str(e)[:50]}{END}")
            print(f"{YELLOW}   Trying next message...{END}")
        
        # Progress bar
        percent = (idx / total) * 100
        bar_length = 30
        filled = int(bar_length * idx // total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"{YELLOW}   [{bar}] {percent:.0f}%{END}")
        
        # Wait for next message (except after last message)
        if idx < total:
            time.sleep(delay)
    
    # Summary
    print(f"\n{BOLD}{CYAN}═══════════════════════════════════{END}")
    print(f"{GREEN}✅ Task Completed!{END}")
    print(f"{GREEN}📊 Total: {total}{END}")
    print(f"{GREEN}✅ Success: {success}{END}")
    print(f"{RED}❌ Failed: {failed}{END}")
    print(f"{CYAN}═══════════════════════════════════{END}")

def main():
    print_banner()
    
    # Step 1: Login
    cl = instagram_login()
    if not cl:
        print(f"\n{RED}❌ Login failed. Exiting...{END}")
        sys.exit(1)
    
    # Step 2: Target username
    print(f"\n{BOLD}{PURPLE}🎯 TARGET USERNAME{END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    target_username = input(f"{CYAN}👤 Target Instagram Username: {END}").strip()
    
    if not target_username:
        print(f"{RED}❌ Target username required!{END}")
        sys.exit(1)
    
    # Step 3: Get user ID
    target_user_id = send_user_id(cl, target_username)
    if not target_user_id:
        print(f"{RED}❌ Could not find target user{END}")
        sys.exit(1)
    else:
        print(f"{GREEN}✅ User found! ID: {target_user_id}{END}")
    
    # Step 4: Message prefix
    print(f"\n{BOLD}{PURPLE}📝 MESSAGE PREFIX (HATER NAME){END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    prefix = input(f"{CYAN}Prefix (Enter to skip): {END}").strip()
    
    # Step 5: Load messages
    print(f"\n{BOLD}{PURPLE}📄 MESSAGES FILE{END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    file_path = input(f"{CYAN}📁 File path (default: messages.txt): {END}").strip()
    
    if not file_path:
        file_path = "messages.txt"
    
    messages = load_messages(file_path)
    if not messages:
        print(f"{RED}❌ No messages found!{END}")
        print(f"{YELLOW}💡 Create messages.txt with one message per line{END}")
        sys.exit(1)
    
    print(f"{GREEN}✅ Loaded {len(messages)} messages{END}")
    
    # Step 6: Delay
    print(f"\n{BOLD}{PURPLE}⏰ SPEED SETTINGS{END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    while True:
        try:
            delay_input = input(f"{CYAN}⏰ Delay between messages (seconds, min 3): {END}").strip()
            delay = float(delay_input) if delay_input else 5
            if delay >= 3:
                break
            else:
                print(f"{RED}❌ Delay should be at least 3 seconds{END}")
        except ValueError:
            print(f"{RED}❌ Please enter a valid number{END}")
    
    # Step 7: Multiple users option
    print(f"\n{BOLD}{PURPLE}⚙️ MORE OPTIONS{END}")
    print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
    multiple = input(f"{CYAN}Send to multiple usernames? (y/n): {END}").lower().strip()
    
    target_users = [target_username]
    if multiple == 'y':
        print(f"{CYAN}Enter usernames (comma separated): {END}")
        usernames_input = input().strip()
        additional_users = [u.strip() for u in usernames_input.split(',') if u.strip()]
        target_users.extend(additional_users)
    
    # Step 8: Send messages
    for user in target_users:
        print(f"\n{BOLD}{PURPLE}🎯 Sending to: @{user}{END}")
        print(f"{YELLOW}━━━━━━━━━━━━━━━━━{END}")
        
        # Get user ID for each user
        user_id = send_user_id(cl, user)
        if not user_id:
            print(f"{RED}❌ Could not find user @{user}{END}")
            continue
        
        send_messages(cl, user_id, user, prefix, messages, delay)
        
        # Wait between users
        if user != target_users[-1]:
            print(f"\n{YELLOW}⏳ Moving to next user in 3s...{END}")
            time.sleep(3)
    
    print(f"\n{BOLD}{GREEN}✅ All done! Thank you for using!{END}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{END}")
    print(f"{PURPLE}Made by @nasir_ali_king{END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}❌ Stopped by user{END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}❌ Unexpected error: {e}{END}")
        sys.exit(1)
