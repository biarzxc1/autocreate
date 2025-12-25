"""
Facebook Auto Registration with Steel SDK + Playwright
=======================================================

SETUP (run these commands):
    pip install steel-sdk playwright faker
    python -m playwright install chromium

USAGE:
    python fb_auto.py your_email@gmail.com
"""

import asyncio
import random
import sys
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
    "Tyler", "Kyle", "Nathan", "Adam", "Dylan", "Ethan", "Noah", "Mason", 
    "Logan", "Lucas", "Jack", "Alexander", "Benjamin", "Henry", "Sebastian"
]

FEMALE_NAMES = [
    "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte", "Emily", 
    "Jessica", "Sarah", "Ashley", "Amanda", "Stephanie", "Nicole", "Jennifer", 
    "Elizabeth", "Michelle", "Samantha", "Lauren", "Rachel", "Katherine", 
    "Victoria", "Hannah", "Natalie", "Grace", "Lily", "Chloe", "Zoey"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
    "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", 
    "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", 
    "Harris", "Clark", "Lewis", "Young", "Walker", "Hall", "Allen", "King"
]


def generate_data(email):
    """Generate random registration data."""
    gender = random.choice(["male", "female"])
    
    if gender == "male":
        first_name = random.choice(MALE_NAMES)
    else:
        first_name = random.choice(FEMALE_NAMES)
    
    last_name = random.choice(LAST_NAMES)
    
    # Random birthday (18-35 years old)
    year = datetime.now().year - random.randint(18, 35)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    # Random password (letters + numbers + symbols)
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


async def run_registration(email):
    """Run the Facebook registration automation."""
    
    # Check API key
    if STEEL_API_KEY == "your-steel-api-key-here":
        print("\n" + "=" * 55)
        print("  ❌ ERROR: STEEL API KEY NOT SET!")
        print("=" * 55)
        print("\n  1. Open fb_auto.py in a text editor")
        print("\n  2. Find this line (around line 20):")
        print('     STEEL_API_KEY = "your-steel-api-key-here"')
        print("\n  3. Replace with your actual API key:")
        print('     STEEL_API_KEY = "sk-steel-xxxxxxxxxxxxx"')
        print("\n  4. Get your FREE key at: https://steel.dev")
        print("\n" + "=" * 55)
        return
    
    # Try importing
    try:
        from steel import Steel
        from playwright.async_api import async_playwright
    except ImportError as e:
        print("\n❌ Missing packages!")
        print("\nRun these commands:")
        print("  pip install steel-sdk playwright faker")
        print("  python -m playwright install chromium")
        print(f"\nError: {e}")
        return
    
    # Generate data
    print("\n🎲 Generating random registration data...\n")
    data = generate_data(email)
    
    print("+" + "-" * 48 + "+")
    print("|" + " GENERATED DATA".center(48) + "|")
    print("+" + "-" * 48 + "+")
    print(f"|  First Name:  {data['first_name']:<32}|")
    print(f"|  Last Name:   {data['last_name']:<32}|")
    print(f"|  Email:       {data['email']:<32}|")
    print(f"|  Password:    {data['password']:<32}|")
    print(f"|  Birthday:    {data['month']}/{data['day']}/{data['year']:<27}|")
    print(f"|  Gender:      {data['gender']:<32}|")
    print("+" + "-" * 48 + "+")
    
    # Create Steel client
    print("\n🚀 Creating Steel browser session...")
    
    try:
        client = Steel(steel_api_key=STEEL_API_KEY)
        session = client.sessions.create(
            use_proxy=True,
            solve_captcha=True
        )
    except Exception as e:
        print(f"\n❌ Failed to create Steel session!")
        print(f"   Error: {e}")
        print("\n   Make sure your API key is correct.")
        return
    
    # Show session info
    print("\n" + "=" * 55)
    print("  🟢 STEEL SESSION CREATED!")
    print("=" * 55)
    print(f"\n  Session ID: {session.id}")
    print(f"\n  ╔══════════════════════════════════════════════════╗")
    print(f"  ║  👁️  LIVE VIEW URL - OPEN THIS IN BROWSER:       ║")
    print(f"  ╚══════════════════════════════════════════════════╝")
    print(f"\n  {session.session_viewer_url}")
    print(f"\n  WebSocket: {session.websocket_url}")
    print("\n" + "=" * 55)
    
    print("\n⏳ Open the LIVE VIEW URL above to watch!")
    print("   Starting in 5 seconds...\n")
    await asyncio.sleep(5)
    
    try:
        async with async_playwright() as p:
            # Connect to Steel browser
            print("🔗 Connecting to Steel browser...")
            
            browser = await p.chromium.connect_over_cdp(
                f"wss://connect.steel.dev?apiKey={STEEL_API_KEY}&sessionId={session.id}"
            )
            
            # Get page
            context = browser.contexts[0]
            if context.pages:
                page = context.pages[0]
            else:
                page = await context.new_page()
            
            # Go to Facebook registration
            print("📍 Opening Facebook registration page...")
            await page.goto("https://www.facebook.com/r.php", timeout=60000)
            await asyncio.sleep(3)
            
            # Fill form
            print("\n✏️  Filling registration form...\n")
            
            # First name
            print(f"   [1/6] First name: {data['first_name']}")
            await page.fill('input[name="firstname"]', data['first_name'])
            await asyncio.sleep(0.5)
            
            # Last name
            print(f"   [2/6] Last name: {data['last_name']}")
            await page.fill('input[name="lastname"]', data['last_name'])
            await asyncio.sleep(0.5)
            
            # Email
            print(f"   [3/6] Email: {data['email']}")
            await page.fill('input[name="reg_email__"]', data['email'])
            await asyncio.sleep(1)
            
            # Confirm email if field appears
            try:
                confirm_email = page.locator('input[name="reg_email_confirmation__"]')
                if await confirm_email.is_visible(timeout=2000):
                    print(f"   [3b]  Confirming email...")
                    await confirm_email.fill(data['email'])
                    await asyncio.sleep(0.5)
            except:
                pass
            
            # Password
            print(f"   [4/6] Password: {data['password']}")
            await page.fill('input[name="reg_passwd__"]', data['password'])
            await asyncio.sleep(0.5)
            
            # Birthday
            print(f"   [5/6] Birthday: {data['month']}/{data['day']}/{data['year']}")
            await page.select_option('select[name="birthday_month"]', str(data['month']))
            await asyncio.sleep(0.3)
            await page.select_option('select[name="birthday_day"]', str(data['day']))
            await asyncio.sleep(0.3)
            await page.select_option('select[name="birthday_year"]', str(data['year']))
            await asyncio.sleep(0.5)
            
            # Gender
            print(f"   [6/6] Gender: {data['gender']}")
            if data['gender'] == "female":
                await page.click('input[name="sex"][value="1"]')
            else:
                await page.click('input[name="sex"][value="2"]')
            await asyncio.sleep(0.5)
            
            # Done
            print("\n" + "=" * 55)
            print("  ✅ FORM FILLED SUCCESSFULLY!")
            print("=" * 55)
            print(f"\n  👁️  Watch/submit at: {session.session_viewer_url}")
            print("\n  ⚠️  Form NOT auto-submitted (for safety)")
            print("      Click 'Sign Up' manually in the live view")
            print("\n" + "=" * 55)
            
            # Keep open
            print("\n⏳ Browser open for 60 seconds. Press Ctrl+C to exit.\n")
            await asyncio.sleep(60)
            
            await browser.close()
            
    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🧹 Releasing Steel session...")
        try:
            client.sessions.release(session.id)
            print("✅ Session closed.")
        except:
            pass


def main():
    if len(sys.argv) < 2:
        print("\n" + "=" * 50)
        print("  Facebook Auto Registration")
        print("  Using Steel SDK + Playwright")
        print("=" * 50)
        print("\n  Usage:")
        print("    python fb_auto.py <your_email>")
        print("\n  Example:")
        print("    python fb_auto.py john@gmail.com")
        print("\n" + "=" * 50)
        return
    
    email = sys.argv[1]
    
    print("\n" + "=" * 55)
    print("  🔵 FACEBOOK AUTO REGISTRATION")
    print("  Using Steel SDK + Playwright")
    print("=" * 55)
    
    asyncio.run(run_registration(email))


if __name__ == "__main__":
    main()
