"""
Facebook Auto Registration - Steel SDK Only
============================================

SETUP:
    pip install steel-sdk faker

USAGE:
    python fb_auto.py your_email@gmail.com
"""

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


def run_registration(email):
    """Run Facebook registration using Steel SDK."""
    
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
    
    # Import Steel
    try:
        from steel import Steel
    except ImportError:
        print("\n❌ Steel SDK not installed!")
        print("\nRun: pip install steel-sdk")
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
    
    # Create Steel client and session
    print("\n🚀 Creating Steel browser session...")
    
    try:
        client = Steel(steel_api_key=STEEL_API_KEY)
        session = client.sessions.create(
            use_proxy=True,
            solve_captcha=True
        )
    except Exception as e:
        print(f"\n❌ Failed to create session: {e}")
        return
    
    # Show URLs
    print("\n" + "=" * 60)
    print("  🟢 SESSION CREATED!")
    print("=" * 60)
    print(f"\n  Session ID: {session.id}")
    print("\n  ┌─────────────────────────────────────────────────────────┐")
    print("  │  👁️  LIVE VIEW URL (open in browser to watch):          │")
    print("  └─────────────────────────────────────────────────────────┘")
    print(f"\n  {session.session_viewer_url}")
    print(f"\n  WebSocket URL: {session.websocket_url}")
    print("\n" + "=" * 60)
    
    # Build JavaScript to fill the form
    js_script = f'''
    async function fillForm() {{
        // Wait for page to load
        await new Promise(r => setTimeout(r, 2000));
        
        // Fill first name
        const firstName = document.querySelector('input[name="firstname"]');
        if (firstName) {{
            firstName.value = "{data['first_name']}";
            firstName.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        
        // Fill last name
        const lastName = document.querySelector('input[name="lastname"]');
        if (lastName) {{
            lastName.value = "{data['last_name']}";
            lastName.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        
        // Fill email
        const email = document.querySelector('input[name="reg_email__"]');
        if (email) {{
            email.value = "{data['email']}";
            email.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        
        // Wait and fill confirm email if it appears
        await new Promise(r => setTimeout(r, 1000));
        const emailConfirm = document.querySelector('input[name="reg_email_confirmation__"]');
        if (emailConfirm) {{
            emailConfirm.value = "{data['email']}";
            emailConfirm.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        
        // Fill password
        const password = document.querySelector('input[name="reg_passwd__"]');
        if (password) {{
            password.value = "{data['password']}";
            password.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
        
        // Select birthday month
        const month = document.querySelector('select[name="birthday_month"]');
        if (month) {{
            month.value = "{data['month']}";
            month.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
        
        // Select birthday day
        const day = document.querySelector('select[name="birthday_day"]');
        if (day) {{
            day.value = "{data['day']}";
            day.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
        
        // Select birthday year
        const year = document.querySelector('select[name="birthday_year"]');
        if (year) {{
            year.value = "{data['year']}";
            year.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
        
        // Select gender
        const genderValue = "{1 if data['gender'] == 'female' else 2}";
        const gender = document.querySelector('input[name="sex"][value="' + genderValue + '"]');
        if (gender) {{
            gender.click();
        }}
        
        return "Form filled!";
    }}
    fillForm();
    '''
    
    try:
        # Navigate to Facebook registration
        print("\n📍 Opening Facebook registration page...")
        client.sessions.context.navigate(
            session_id=session.id,
            url="https://www.facebook.com/r.php"
        )
        
        print("⏳ Waiting for page to load...")
        time.sleep(5)
        
        # Execute JavaScript to fill form
        print("✏️  Filling form with generated data...")
        client.sessions.context.execute(
            session_id=session.id,
            script=js_script
        )
        
        print("\n" + "=" * 60)
        print("  ✅ DONE!")
        print("=" * 60)
        print(f"\n  👁️  View result: {session.session_viewer_url}")
        print("\n  ⚠️  Form NOT submitted (for safety)")
        print("      Open the live view and click 'Sign Up' manually")
        print("=" * 60)
        
        # Keep session alive
        print("\n⏳ Session stays open for 60 seconds...")
        print("   Press Ctrl+C to exit\n")
        time.sleep(60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
        # Fallback: just show the data and URL
        print("\n" + "=" * 60)
        print("  ℹ️  MANUAL MODE")
        print("=" * 60)
        print(f"\n  Open this URL in browser:")
        print(f"  {session.session_viewer_url}")
        print(f"\n  Then manually fill in:")
        print(f"    First Name: {data['first_name']}")
        print(f"    Last Name:  {data['last_name']}")
        print(f"    Email:      {data['email']}")
        print(f"    Password:   {data['password']}")
        print(f"    Birthday:   {data['month']}/{data['day']}/{data['year']}")
        print(f"    Gender:     {data['gender']}")
        print("=" * 60)
        
        print("\n⏳ Session open for 120 seconds...")
        time.sleep(120)
        
    finally:
        print("\n🧹 Closing session...")
        try:
            client.sessions.release(session.id)
            print("✅ Done!")
        except:
            pass


def main():
    if len(sys.argv) < 2:
        print("\n" + "=" * 45)
        print("  Facebook Auto Registration")
        print("  Steel SDK Only")
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
    print("  Steel SDK Only (No Playwright)")
    print("=" * 55)
    
    run_registration(email)


if __name__ == "__main__":
    main()
