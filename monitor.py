import os
import json
import time
import hashlib
from urllib.request import urlopen
from urllib.error import URLError

# Terminal colors for alerts
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_page_content(config):
    """Fetches content from a live URL or a local HTML file based on config."""
    if config.get("is_local_file", False):
        if os.path.exists(config["target_url"]):
            with open(config["target_url"], "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"{RED}[ERROR] Local test file not found at: {config['target_url']}{RESET}")
            return None
    else:
        try:
            with urlopen(config["target_url"]) as response:
                return response.read().decode("utf-8")
        except URLError as e:
            print(f"{RED}[ERROR] Failed to reach target URL: {e.reason}{RESET}")
            return None

def calculate_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def check_keywords(content, keywords):
    found_keywords = []
    content_lower = content.lower()
    for kw in keywords:
        if kw.lower() in content_lower:
            found_keywords.append(kw)
    return found_keywords

def main():
    print(f"{GREEN}[INFO] Starting Website Defacement Monitor...{RESET}")
    
    try:
        config = load_config()
    except Exception as e:
        print(f"{RED}[ERROR] Failed to load config.json: {e}{RESET}")
        return

    print(f"{GREEN}[INFO] Target under watch: {config['target_url']}{RESET}")
    
    # Initial baseline fetch
    initial_content = get_page_content(config)
    if not initial_content:
        print(f"{RED}[ERROR] Could not establish a baseline. Exiting.{RESET}")
        return
        
    last_hash = calculate_hash(initial_content)
    print(f"{GREEN}[INFO] Baseline established. Monitoring loop active...{RESET}\n")

    try:
        while True:
            # Reload config every loop in case changes are made
            config = load_config()
            current_content = get_page_content(config)
            
            if current_content:
                # 1. Check for Unauthorized Source Code Changes (Hash Matching)
                current_hash = calculate_hash(current_content)
                if current_hash != last_hash:
                    print(f"{RED}[CRITICAL ALERT] Integrity breach detected! Source code of the website has changed!{RESET}")
                    last_hash = current_hash # Update hash to avoid continuous alert loop
                
                # 2. Check for Malicious Keywords
                triggered_keywords = check_keywords(current_content, config["alert_keywords"])
                if triggered_keywords:
                    print(f"{RED}[CRITICAL ALERT] Defacement signatures found! Indicators: {triggered_keywords}{RESET}")
                
                if not triggered_keywords and current_hash == last_hash:
                    print(f"{GREEN}[OK] {time.strftime('%Y-%m-%d %H:%M:%S')} - Integrity safe. No defacement signatures found.{RESET}")
            
            time.sleep(config["check_interval_seconds"])
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[INFO] Monitor stopped by user.{RESET}")

if __name__ == "__main__":
    main()
