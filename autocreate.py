"""
Facebook Auto Registration with Steel SDK
==========================================

SETUP:
    pip install steel-sdk playwright
    playwright install chromium

USAGE:
    python fb_auto.py your_email@gmail.com
"""

import asyncio
import random
import sys
from datetime import datetime

# =============================================
# PUT YOUR STEEL API KEY HERE 👇
# =============================================
STEEL_API_KEY = "ste-h9rofstUq2bjiCKCBNZTwKiAHZbD6hHvTJoS851Mxo78Nis447DesAUwQnDPEWyw5HLwVN6hwEKnELHNN0CIT19INHcNQVr0ygF"
# =============================================
# Get your key at: https://steel.dev
# =============================================


# Name lists
MALE_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Joseph", "Daniel", "Matthew", "Chris", "Ryan", "Kevin", "Justin", "Brandon", "Tyler", "Kyle", "Nathan", "Adam", "Dylan", "Ethan", "Noah", "Mason", "Logan", "Lucas", "Jack"]

FEMALE_NAMES = ["Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte", "Emily", "Jessica", "Sarah", "Ashley", "Amanda", "Stephanie", "Nicole", "Jennifer", "Elizabeth", "Michelle", "Samantha", "Lauren", "Rachel", "Katherine", "Victoria", "Hannah", "Natalie", "Grace", "Lily"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Clark", "Lewis", "Young", "Walker"]


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
    
    # Random password
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


async def run_facebook_registration(email):
    """Main function to fill Facebook registration."""
    
    # Check API key
    if STEEL_API_KEY == "your-steel-api-key-here":
        print("\n❌ ERROR: You need to set your Steel API key!")
        print("\n   Open this file and find this line:")
        print('   STEEL_API_KEY = "your-steel-api-key-here"')
        print("\n   Replace it with your actual key from https://steel.dev")
        return
    
    # Import Steel and Playwright
    try:
        from steel import Steel
        from playwright.async_api import async_playwright
    except ImportError:
        print("\n❌ Missing packages! Run these commands:")
        print("   pip install steel-sdk playwright")
        print("   playwright install chromium")
        return
    
    # Generate random data
    print("\n🎲 Generating random data...")
    data = generate_data(email)
    
    print("\n" + "=" * 50)
    print("        GENERATED DATA")
    print("=" * 50)
    print(f"  First Name:  {data['first_name']}")
    print(f"  Last Name:   {data['last_name']}")
    print(f"  Email:       {data['email']}")
    print(f"  Password:    {data['password']}")
    print(f"  Birthday:    {data['month']}/{data['day']}/{data['year']}")
    print(f"  Gender:      {data['gender']}")
    print("=" * 50)
    
    # Create Steel session
    print("\n🚀 Creating browser session...")
    
    try:
        client = Steel(steel_api_key=STEEL_API_KEY)
        session = client.sessions.create(
            use_proxy=True,
            solve_captcha=True
        )
    except Exception as e:
        print(f"\n❌ Failed to create session: {e}")
        print("\n   Check your API key is correct")
        return
    
    # Print session URLs
    print("\n" + "=" * 50)
    print("        SESSION INFO")
    print("=" * 50)
    print(f"  Session ID: {session.id}")
    print(f"\n  👁️  LIVE VIEW URL (watch the browser):")
    print(f"  {session.session_viewer_url}")
    print(f"\n  🔗 WebSocket URL:")
    print(f"  {session.websocket_url}")
    print("=" * 50)
    
    print("\n📺 Open the LIVE VIEW URL above to watch!")
    print("   Waiting 5 seconds for you to open it...\n")
    await asyncio.sleep(5)
    
    try:
        async with async_playwright() as p:
            # Connect to Steel browser
            print("🔗 Connecting to browser...")
            browser = await p.chromium.connect_over_cdp(
                f"wss://connect.steel.dev?apiKey={STEEL_API_KEY}&sessionId={session.id}"
            )
            
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            
            # Go to Facebook registration page
            print("📍 Opening Facebook registration page...")
            await page.goto("https://www.facebook.com/r.php", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(2)
            
            # Fill the form
            print("✏️  Filling form...")
            
            # First name
            print(f"   → First name: {data['first_name']}")
            await page.locator('input[name="firstname"]').fill(data['first_name'])
            await asyncio.sleep(0.5)
            
            # Last name
            print(f"   → Last name: {data['last_name']}")
            await page.locator('input[name="lastname"]').fill(data['last_name'])
            await asyncio.sleep(0.5)
            
            # Email
            print(f"   → Email: {data['email']}")
            await page.locator('input[name="reg_email__"]').fill(data['email'])
            await asyncio.sleep(0.5)
            
            # Re-enter email (if exists)
            try:
                email_confirm = page.locator('input[name="reg_email_confirmation__"]')
                if await email_confirm.count() > 0:
                    print(f"   → Confirm email: {data['email']}")
                    await email_confirm.fill(data['email'])
                    await asyncio.sleep(0.5)
            except:
                pass
            
            # Password
            print(f"   → Password: {data['password']}")
            await page.locator('input[name="reg_passwd__"]').fill(data['password'])
            await asyncio.sleep(0.5)
            
            # Birthday
            print(f"   → Birthday: {data['month']}/{data['day']}/{data['year']}")
            await page.locator('select[name="birthday_month"]').select_option(str(data['month']))
            await asyncio.sleep(0.3)
            await page.locator('select[name="birthday_day"]').select_option(str(data['day']))
            await asyncio.sleep(0.3)
            await page.locator('select[name="birthday_year"]').select_option(str(data['year']))
            await asyncio.sleep(0.5)
            
            # Gender
            print(f"   → Gender: {data['gender']}")
            if data['gender'] == "female":
                await page.locator('input[name="sex"][value="1"]').click()
            else:
                await page.locator('input[name="sex"][value="2"]').click()
            await asyncio.sleep(0.5)
            
            # Done!
            print("\n✅ Form filled successfully!")
            print("\n" + "=" * 50)
            print("   WATCH THE LIVE VIEW TO SEE THE RESULT")
            print("   You can submit the form manually there")
            print("=" * 50)
            print(f"\n👁️  {session.session_viewer_url}")
            
            # Keep browser open for 60 seconds
            print("\n⏳ Browser stays open for 60 seconds...")
            print("   Press Ctrl+C to close earlier\n")
            
            try:
                await asyncio.sleep(60)
            except:
                pass
            
            await browser.close()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        print("\n🧹 Closing session...")
        try:
            client.sessions.release(session.id)
            print("✅ Done!")
        except:
            pass


def main():
    # Check for email argument
    if len(sys.argv) < 2:
        print("\n❌ Please provide your email!")
        print("\nUsage:")
        print("   python fb_auto.py your_email@gmail.com")
        print("\nExample:")
        print("   python fb_auto.py john@example.com")
        return
    
    email = sys.argv[1]
    
    print("\n" + "=" * 50)
    print("   FACEBOOK AUTO REGISTRATION")
    print("   Using Steel SDK")
    print("=" * 50)
    
    # Run the registration
    asyncio.run(run_facebook_registration(email))


if __name__ == "__main__":
    main()
