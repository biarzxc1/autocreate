import asyncio
import aiohttp
import re
from rich.console import Console
import sys
import os

# 1. SETUP & CONFIGURATION
os.system('clear')
console = Console()

config = {
    'cookies': '',
    'post': ''
}

# Global counter for high-speed tracking
total_processed = 0
target_share_count = 0

def banner():
    console.print(
        """[bold cyan]
   SPEED SHARE   
  NO DELAY MODE  
[/bold cyan]"""
    )

# 2. INPUTS
banner()
config['cookies'] = input("\033[0mCOOKIE : \033[92m")
config['post'] = input("\033[0mPOST LINK : \033[92m")
try:
    target_share_count = int(input("\033[0mSHARE COUNT : \033[92m"))
except ValueError:
    target_share_count = 0

if not config['post'].startswith('https://'):
    console.print("[bold red]Invalid post link[/bold red]"); sys.exit()
elif not target_share_count:
    console.print("[bold red]Invalid count[/bold red]"); sys.exit()

os.system("clear")
banner()

# 3. OPTIMIZED HEADERS & DATA
# These headers are static (defined once) to save processing time
base_headers = {
    'authority': 'b-graph.facebook.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'connection': 'keep-alive',  # Crucial for speed
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.facebook.com',
    'referer': 'https://www.facebook.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

class Share:
    async def get_token(self, session):
        """
        Fetches the access token. 
        """
        token_headers = base_headers.copy()
        token_headers.update({
            'authority': 'business.facebook.com',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'cookie': config['cookies']
        })

        try:
            async with session.get('https://business.facebook.com/content_management', headers=token_headers) as response:
                data = await response.text()
                access_token = 'EAAG' + re.search('EAAG(.*?)","', data).group(1)
                return access_token
        except (AttributeError, Exception):
            console.print("[bold red]Failed to get access token. Cookie invalid or expired.[/bold red]")
            sys.exit()

    async def share(self, session, token):
        global total_processed
        
        # Prepare headers specifically for the share request
        share_headers = base_headers.copy()
        share_headers.update({
            'host': 'b-graph.facebook.com',
            'cookie': config['cookies']
        })

        # Pre-format the URL to avoid doing it inside the loop every time
        url = f'https://b-graph.facebook.com/me/feed?link=https://mbasic.facebook.com/{config["post"]}&published=0&access_token={token}'

        while True:
            # High-speed check: stop if we reached the target
            if total_processed >= target_share_count:
                break

            try:
                # The actual request
                async with session.post(url, headers=share_headers) as response:
                    data = await response.json()
                    
                    if 'id' in data:
                        total_processed += 1
                        # Minimal logging to reduce console lag
                        console.print(f"[bold green]SHARES: {total_processed}/{target_share_count}")
                    else:
                        # If blocked, kill the process immediately
                        console.print(f"[bold red]BLOCKED RESPONSE: {data}[/bold red]")
                        total_processed = target_share_count + 1 # Force stop all threads
                        break
            except Exception as e:
                # Ignore connection errors to keep speed up, just retry
                pass

async def main():
    # TCPConnector(limit=None) allows unlimited simultaneous connections
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
        share_bot = Share()
        token = await share_bot.get_token(session)
        
        console.print(f"[bold yellow]Token Retrieved. Launching 100 threads...[/bold yellow]")
        
        # Create 100 concurrent tasks for maximum speed
        tasks = [asyncio.create_task(share_bot.share(session, token)) for _ in range(100)]
        
        await asyncio.gather(*tasks)
        console.print(f"[bold cyan]Finished. Total shares: {total_processed}[/bold cyan]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
