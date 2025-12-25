"""
Facebook Auto Registration - Using Steel API directly
======================================================

SETUP:
    pip install requests

USAGE:
    python fb_auto.py your_email@gmail.com
"""

import requests
import random
import sys
import time
from datetime import datetime

# =============================================
# 👇👇👇 PUT YOUR STEEL API KEY HERE 👇👇👇
# =============================================

STEEL_API_KEY = "ste-h9rofstUq2bjiCKCBNZTwKiAHZbD6hHvTJoS851Mxo78Nis447DesAUwQnDPEWyw5HLwVN6hwEKnELHNN0CIT19INHcNQVr0ygF"

# =============================================
# Get your free key at: https://steel.dev
# =============================================


# Steel API base URL
STEEL_API_URL = "https://api.steel.dev/v1"

# Name lists
MALE_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Joseph", 
    "Daniel", "Matthew", "Chris", "Ryan", "Kevin", "Justin", "Brandon", 
    "Tyler", "Kyle", "Nathan", "Adam", "Dylan", "Ethan", "Noah", "Mason"
]

FEMALE_NAMES = [
    "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte", "Emily", 
    "Jessica", "Sarah", "Ashley", "Amanda", "Stephanie", "Nicole", "Jennifer", 
    "Elizabeth", "Michelle", "Samantha", "Lauren", "Rachel", "Victoria"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
    "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", 
    "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White"
]


def generate_data(email):
    """Generate random registration data."""
    gender = random.choice(["male", "female"])
    
    if gender == "male":
        first_name = random.choice(MALE_NAMES)
    else:
        first_name = random.choice(FEMALE_NAMES)
    
    last_name = random.choice(LAST_NAMES)
    
    year = datetime.now().year - random.randint(18, 35)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$"
    password = ''.join(random.choices(chars, k=12))
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "month": month,
        "day": day,
        "year": year,
        "gender": gender
    }


def create_session(api_key):
    """Create a Steel browser session."""
    headers = {
        "Steel-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "useProxy": True,
        "solveCaptcha": True
    }
    
    response = requests.post(
        f"{STEEL_API_URL}/sessions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create session: {response.status_code} - {response.text}")


def release_session(api_key, session_id):
    """Release a Steel browser session."""
    headers = {
        "Steel-Api-Key": api_key
    }
    
    requests.delete(
        f"{STEEL_API_URL}/sessions/{session_id}",
        headers=headers
    )


def scrape_page(api_key, session_id, url):
    """Navigate to a URL using Steel scrape endpoint."""
    headers = {
        "Steel-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "sessionId": session_id,
        "waitFor": 3000
    }
    
    response = requests.post(
        f"{STEEL_API_URL}/scrape",
        headers=headers,
        json=payload
    )
    
    return response.json() if response.status_code == 200 else None


def run_registration(email):
    """Run Facebook registration."""
    
    # Check API key
    if STEEL_API_KEY == "your-steel-api-key-here":
        print("\n" + "=" * 55)
        print("  ❌ ERROR: STEEL API KEY NOT SET!")
        print("=" * 55)
        print("\n  1. Open fb_auto.py")
        print("\n  2. Find line 20:")
        print('     STEEL_API_KEY = "your-steel-api-key-here"')
        print("\n  3. Replace with your key:")
        print('     STEEL_API_KEY = "sk-steel-xxxxxxxxxxxxx"')
        print("\n  4. Get FREE key at: https://steel.dev")
        print("=" * 55)
        return
    
    # Generate data
    print("\n🎲 Generating random data...\n")
    data = generate_data(email)
    
    print("+" + "-" * 45 + "+")
    print("|" + " GENERATED DATA".center(45) + "|")
    print("+" + "-" * 45 + "+")
    print(f"|  First Name:  {data['first_name']:<29}|")
    print(f"|  Last Name:   {data['last_name']:<29}|")
    print(f"|  Email:       {data['email']:<29}|")
    print(f"|  Password:    {data['password']:<29}|")
    print(f"|  Birthday:    {data['month']}/{data['day']}/{data['year']:<24}|")
    print(f"|  Gender:      {data['gender']:<29}|")
    print("+" + "-" * 45 + "+")
    
    # Create session
    print("\n🚀 Creating Steel browser session...")
    
    try:
        session = create_session(STEEL_API_KEY)
    except Exception as e:
        print(f"\n❌ Failed to create session: {e}")
        return
    
    session_id = session.get("id")
    session_viewer_url = session.get("sessionViewerUrl")
    websocket_url = session.get("websocketUrl")
    
    # Show URLs
    print("\n" + "=" * 65)
    print("  🟢 SESSION CREATED!")
    print("=" * 65)
    print(f"\n  Session ID: {session_id}")
    print("\n  ┌───────────────────────────────────────────────────────────────┐")
    print("  │  👁️  LIVE VIEW URL - OPEN THIS IN YOUR BROWSER:               │")
    print("  └───────────────────────────────────────────────────────────────┘")
    print(f"\n  {session_viewer_url}")
    print(f"\n  WebSocket URL:")
    print(f"  {websocket_url}")
    print("\n" + "=" * 65)
    
    # JavaScript to fill the form
    js_fill_form = f'''
    (function() {{
        // Fill first name
        var fn = document.querySelector('input[name="firstname"]');
        if (fn) {{ fn.value = "{data['first_name']}"; fn.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        
        // Fill last name  
        var ln = document.querySelector('input[name="lastname"]');
        if (ln) {{ ln.value = "{data['last_name']}"; ln.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        
        // Fill email
        var em = document.querySelector('input[name="reg_email__"]');
        if (em) {{ em.value = "{data['email']}"; em.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        
        // Fill password
        var pw = document.querySelector('input[name="reg_passwd__"]');
        if (pw) {{ pw.value = "{data['password']}"; pw.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        
        // Birthday
        var mo = document.querySelector('select[name="birthday_month"]');
        if (mo) {{ mo.value = "{data['month']}"; mo.dispatchEvent(new Event('change', {{bubbles:true}})); }}
        
        var dy = document.querySelector('select[name="birthday_day"]');
        if (dy) {{ dy.value = "{data['day']}"; dy.dispatchEvent(new Event('change', {{bubbles:true}})); }}
        
        var yr = document.querySelector('select[name="birthday_year"]');
        if (yr) {{ yr.value = "{data['year']}"; yr.dispatchEvent(new Event('change', {{bubbles:true}})); }}
        
        // Gender
        var gv = "{1 if data['gender'] == 'female' else 2}";
        var gn = document.querySelector('input[name="sex"][value="' + gv + '"]');
        if (gn) {{ gn.click(); }}
        
        // Confirm email if exists
        setTimeout(function() {{
            var ce = document.querySelector('input[name="reg_email_confirmation__"]');
            if (ce) {{ ce.value = "{data['email']}"; ce.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        }}, 1000);
        
        return "done";
    }})();
    '''
    
    try:
        # Navigate to Facebook
        print("\n📍 Opening Facebook registration...")
        scrape_page(STEEL_API_KEY, session_id, "https://www.facebook.com/r.php")
        
        print("⏳ Page loading...")
        time.sleep(5)
        
        # Try to execute JS via actions endpoint
        print("✏️  Attempting to fill form...")
        
        headers = {
            "Steel-Api-Key": STEEL_API_KEY,
            "Content-Type": "application/json"
        }
        
        # Use the actions/execute endpoint
        response = requests.post(
            f"{STEEL_API_URL}/sessions/{session_id}/actions/execute",
            headers=headers,
            json={"script": js_fill_form}
        )
        
        if response.status_code == 200:
            print("✅ Form filled successfully!")
        else:
            print(f"⚠️  Auto-fill may not have worked (status: {response.status_code})")
        
    except Exception as e:
        print(f"\n⚠️  Auto-fill error: {e}")
    
    # Show final info
    print("\n" + "=" * 65)
    print("  📋 COPY THIS DATA AND USE IN LIVE VIEW:")
    print("=" * 65)
    print(f"\n  First Name:  {data['first_name']}")
    print(f"  Last Name:   {data['last_name']}")
    print(f"  Email:       {data['email']}")
    print(f"  Password:    {data['password']}")
    print(f"  Birthday:    {data['month']}/{data['day']}/{data['year']}")
    print(f"  Gender:      {data['gender']}")
    print("\n" + "=" * 65)
    print(f"\n  👁️  LIVE VIEW: {session_viewer_url}")
    print("\n  Open the URL above to see the browser and fill/submit the form!")
    print("=" * 65)
    
    # Keep session alive
    print("\n⏳ Session open for 120 seconds. Press Ctrl+C to exit.\n")
    
    try:
        time.sleep(120)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    
    # Cleanup
    print("🧹 Closing session...")
    try:
        release_session(STEEL_API_KEY, session_id)
        print("✅ Done!")
    except:
        pass


def main():
    if len(sys.argv) < 2:
        print("\n" + "=" * 45)
        print("  Facebook Auto Registration")
        print("  Using Steel API (requests only)")
        print("=" * 45)
        print("\n  Usage:")
        print("    python fb_auto.py <email>")
        print("\n  Example:")
        print("    python fb_auto.py john@gmail.com")
        print("=" * 45)
        return
    
    email = sys.argv[1]
    
    print("\n" + "=" * 55)
    print("  🔵 FACEBOOK AUTO REGISTRATION")
    print("  Using Steel API (no SDK needed)")
    print("=" * 55)
    
    run_registration(email)


if __name__ == "__main__":
    main()
