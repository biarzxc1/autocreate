import os
import sys
import requests
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- COLORS ---
red = "\033[1;31m"
green = "\033[1;32m"
blue = "\033[1;34m"
yellow = "\033[1;33m"
white = "\033[1;37m"
reset = "\033[0m"

# --- HELPER FUNCTIONS ---

def clear_screen():
    os.system('clear')

def banner():
    print(f"""{blue}
    ██████╗ ███████╗    ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██╔════╝    ██╔══██╗██╔════╝██║   ██║
    ██████╔╝█████╗      ██║  ██║█████╗  ██║   ██║
    ██╔══██╗██╔══╝      ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║███████╗    ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚══════╝  ╚═══╝  
    {yellow}      MULTI-TOOL: REACTOR & TOKEN GETTER
    {blue}───────────────────────────────────────────────────────────────{reset}""")

def W_ueragnt():
    """Generates a random User-Agent."""
    versions = ["10.0", "11.0", "12.0", "13.0", "14.0", "15.0"]
    models = ["SM-G991B", "SM-A528B", "Pixel 6", "iPhone 13", "Xiaomi 11T"]
    return f"Mozilla/5.0 (Linux; Android {random.choice(versions)}; {random.choice(models)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"

# --- TOKEN GETTER LOGIC (Cookie -> EAAG) ---

def convert_cookie_to_token(cookie):
    """
    Exchanges a Facebook Cookie for an EAAG (Business) Access Token.
    """
    try:
        # 1. Get the User ID from the cookie (c_user)
        try:
            c_user = re.search(r'c_user=(\d+)', cookie).group(1)
        except AttributeError:
            return None, "Invalid Cookie: Missing c_user"

        # 2. Prepare headers for Business Manager
        headers = {
            'User-Agent': W_ueragnt(),
            'Cookie': cookie,
            'Host': 'business.facebook.com',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0'
        }

        # 3. Request the Business Manager page
        # We target a specific endpoint that usually exposes the token in the source
        url = "https://business.facebook.com/content_management"
        response = requests.get(url, headers=headers)
        
        # 4. Extract Token using Regex
        # EAAG tokens usually start with EAAG and are enclosed in quotes
        token_match = re.search(r'(EAAG\w+)', response.text)
        
        if token_match:
            eaag_token = token_match.group(1)
            return eaag_token, "Success"
        else:
            # Try alternative extraction if the first one fails
            token_match_alt = re.search(r'["\']access_token["\']\s*:\s*["\'](EAAG\w+)["\']', response.text)
            if token_match_alt:
                return token_match_alt.group(1), "Success"
            else:
                return None, "Failed to extract EAAG token. Cookie might be dead or checkpointed."

    except Exception as e:
        return None, str(e)

def token_getter_menu():
    """Menu for converting cookies to tokens."""
    clear_screen()
    banner()
    print(f"    {yellow}PASTE YOUR COOKIES BELOW (One per line).")
    print(f"    {white}Format: c_user=...; xs=...; sb=...;")
    print(f"    {white}Type {red}'DONE'{white} on a new line when finished.{reset}")
    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")

    cookies = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            if line.strip():
                cookies.append(line.strip())
        except EOFError:
            break
            
    if not cookies:
        print(f"{red}No cookies entered.{reset}")
        return

    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")
    print(f"{yellow}    Converting {len(cookies)} cookies to tokens...{reset}\n")
    
    success_tokens = []
    
    for cookie in cookies:
        token, msg = convert_cookie_to_token(cookie)
        if token:
            print(f"    {green}[SUCCESS] {white}Token Generated!")
            print(f"    {yellow}{token[:30]}...{reset}") # Show partial token
            success_tokens.append(token)
            
            # Save to file immediately
            with open('/sdcard/boostphere/generated_tokens.txt', 'a') as f:
                f.write(token + '\n')
        else:
            print(f"    {red}[FAILED] {msg}{reset}")

    print(f"\n    {blue}───────────────────────────────────────────────────────────────{reset}")
    print(f"    {green}Conversion Complete!")
    print(f"    {green}Tokens saved to: /sdcard/boostphere/generated_tokens.txt")
    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")
    input(f"\n{yellow}Press Enter to return to main menu...{reset}")

# --- REACTOR LOGIC ---

def react_comment(token, uid_url, reaction_type):
    """Send a reaction using the provided access token."""
    try:
        # Handle format: email|token OR uid|token OR just token
        if "|" in token:
            access_token = token.split('|')[1]
            uid_display = token.split('|')[0]
        else:
            access_token = token
            uid_display = "Token..."

        url = f'https://graph.facebook.com/v18.0/{uid_url}/reactions'
        params = {'access_token': access_token, 'type': reaction_type}
        headers_ = {'User-Agent': W_ueragnt()}

        response = requests.post(url, params=params, headers=headers_)
        return uid_display, response.status_code, response.text
        
    except Exception as e:
        return "Error", None, str(e)

def reactor_menu():
    """Main execution logic for the reactor."""
    clear_screen()
    banner()

    # 1. Get Tokens via Paste
    print(f"    {yellow}PASTE YOUR TOKENS BELOW.")
    print(f"    {white}Type {red}'DONE'{white} on a new line when finished.{reset}")
    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")
    
    tokens = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            if line.strip(): 
                tokens.append(line.strip())
        except EOFError:
            break

    if not tokens:
        print(f"{red}No tokens entered.{reset}")
        return

    # 2. Get Target Info
    print(f"    {green}FORMAT {yellow}: {red}https://www.facebook.com/.../posts/12345/?mibextid=...")
    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")
    post_id = input(f"   {green}POST ID: ")
    print(f"    {blue}───────────────────────────────────────────────────────────────{reset}")
    comment_id = input(f"   {green}COMMENT ID: ")
    uid_url = f"{post_id}_{comment_id}"

    # 3. Choose Reaction
    print(f"""    {yellow}Choose the reaction type:
     {blue}[1] {green}LIKE   {blue}[2] {green}LOVE
     {blue}[3] {green}WOW    {blue}[4] {green}SAD
     {blue}[5] {green}ANGRY  {blue}[6] {green}HAHA
    {blue}───────────────────────────────────────────────────────────────{reset}""")
    try:
        choice = int(input(f"     {green}Choose: "))
        reaction_map = {1:"LIKE", 2:"LOVE", 3:"WOW", 4:"SAD", 5:"ANGRY", 6:"HAHA"}
        reaction_type = reaction_map.get(choice)
        if not reaction_type: return
    except: return

    # 4. Quantity
    try:
        num = int(input(f"     {yellow}Amount (Max {len(tokens)}): "))
        active_tokens = tokens[:min(num, len(tokens))]
    except: return

    # 5. Threading
    print(f"\n{yellow}    Starting...{reset}\n")
    success_count = 0
    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_token = {executor.submit(react_comment, t, uid_url, reaction_type): t for t in active_tokens}
        for future in as_completed(future_to_token):
            uid, status, _ = future.result()
            if status == 200:
                success_count += 1
                print(f"     {red}[REACTOR] {yellow}{uid} {blue}──> {green}SUCCESS {reaction_type}")
            else:
                print(f"     {red}[REACTOR] {yellow}{uid} {blue}──> {red}FAILED")
    
    print(f"\n    {green}Completed: {success_count}/{len(active_tokens)} Success")
    input(f"\n{yellow}Press Enter to return...{reset}")

# --- MAIN MENU ---

def main_menu():
    # Ensure directory exists for saving tokens
    if not os.path.exists("/sdcard/boostphere/"):
        try: os.makedirs("/sdcard/boostphere/")
        except: pass

    while True:
        clear_screen()
        banner()
        print(f"""
     {blue}[1] {green}START REACTOR (Direct Input)
     {blue}[2] {green}COOKIE TO TOKEN (Get EAAG)
     {red}[0] {red}EXIT
    {blue}───────────────────────────────────────────────────────────────{reset}""")
        
        choice = input(f"    {green}Choose: ")
        
        if choice == '1':
            reactor_menu()
        elif choice == '2':
            token_getter_menu()
        elif choice == '0':
            sys.exit()
        else:
            print(f"{red}Invalid Choice{reset}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
