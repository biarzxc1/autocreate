import os
import sys
import re
import requests
import bs4
import time
import random
import json
import string
from bs4 import BeautifulSoup
from datetime import datetime

# --- Configuration & Assets ---
logo = '[1;37m\n █████  ██   ██  █████  ███████ ██   ██ \n██   ██ ██  ██  ██   ██ ██      ██   ██ \n███████ █████   ███████ ███████ ███████ \n██   ██ ██  ██  ██   ██      ██ ██   ██ \n██   ██ ██   ██ ██   ██ ███████ ██   ██ \n[1;37m——————————————————————————————————————————————————[1;37m\n OWNER     [1;31m:[1;37m MR [1;31mx[1;37m AKASH\n STATUS    [1;31m:[1;37m [1;32mFREE[1;37m\n VERSION   [1;31m:[1;37m 0.0.2 [1;37m\n[1;37m——————————————————————————————————————————————————[1;37m'

# Reconstructed device list from your snippet
infinix = [
    '7060', '8076D', 'F98', 'G636', 'GT 10 Pro', 'Hot', 'Hot 1', 'Hot 10', 'Hot 10 Play', 
    'Hot 10i', 'Hot 10s', 'Hot 10s NFC', 'Hot 10T', 'Hot 11', 'Hot 11 (2020)', 'Hot 11S', 
    'Hot 12', 'Hot 12 Play', 'Hot 12 Play NFC', 'Hot 12 Pro', 'Hot 12i', 'Hot 2', 'Hot 20', 
    'Hot 20 5G', 'Hot 20 Play', 'Hot 20i', 'Hot 20S', 'Hot 3', 'Hot 3 Pro', 'Hot 30', 
    'Hot 30 Play', 'Hot 30i', 'Hot 4', 'Hot 4 Lite', 'Hot 4 Pro', 'Hot 5', 'Hot 5 Lite', 
    'Hot 6', 'Hot 6 Pro', 'Hot 6X', 'Hot 7', 'Hot 7 Pro', 'Hot 8', 'Hot 9', 'Hot 9 Play', 
    'Hot 9 Pro', 'Hot Note', 'Hot S', 'Hot S3'
]

# Reconstructed name list (variable 'boy')
boy = [
    'Shanto Hasan', 'Arif Hossain', 'Rajib Ahmed', 'Shakib Al Hasan', 'Tanvir Rahman', 
    'Rifat Chowdhury', 'Samir Khan', 'Naimul Islam', 'Sohel Rana', 'Farhan Ahmed', 
    'Suman Das', 'Rubel Hossain', 'Anik Miah', 'Shahin Alam', 'Rony Sarker', 
    'Tareq Ahmed', 'Sadiq Hasan', 'Rashedul Islam', 'Jamil Hossain', 'Saifur Rahman', 
    'Asif Ali', 'Shuvo Roy', 'Nizam Uddin', 'Muntasir Khan', 'Hasan Mahmud', 
    'Abir Chowdhury', 'Fahim Hasan', 'Rayan Sardar', 'Shadman Islam', 'Imran Ali', 
    'Billal Hossain', 'Nasim Uddin', 'Shamsul Islam', 'Anwar Hossain', 'Emon Sarker', 
    'Sadiq Rahman', 'Rifat Hasan', 'Shafiqul Islam', 'Nayan Ahmed', 'Jahid Hasan', 
    'Kadir Miah', 'Kamal Hossain', 'Rony Ahmed', 'Mizanur Rahman', 'Arman Sheikh', 
    'Samiul Islam', 'Shajedul Islam', 'Rubaiyat Hossain', 'Babu Miah', 'Akash Ahmed', 
    'Jashim Uddin'
]

ok = []
cp = []

# --- Helper Functions ---

def clear():
    os.system('clear')
    print(logo)

def convert(cok):
    __for = 'datr=' + cok.get('datr', '') + ';' + ('sb=' + cok.get('sb', '')) + ';' + ('fr=' + cok.get('fr', '')) + ';' + ('c_user=' + cok.get('c_user', '')) + ';' + ('xs=' + cok.get('xs', ''))
    return __for

def inbox(session):
    time.sleep(1)
    ses = requests.Session()
    __ = str(time.time()).replace('.', '')[:13]
    try:
        # Using the same API endpoint logic you provided
        data = ses.get(f'https://10minutemail.net/address.api.php?sessionid={session}&_={str(__)}').json()
        if len(data['mail_list']) >= 1:
            for mail in data['mail_list']:
                subject = mail['subject']
                # Look for the FB code pattern
                if 'FB-' in subject or 'Facebook' in subject:
                    code = subject.replace('FB-', '').replace('is your Facebook confirmation code', '').strip()
                    # Extract just the numbers if there's extra text
                    code = re.search(r'\d{5,6}', code).group(0)
                    return code
    except Exception as e:
        return None
    return None

# --- Main Class ---

class create:
    def __init__(self):
        self.loop = 0
        self.gender = []

    def start(self):
        clear()
        print('[1] Facebook account auto create')
        gen = input('select: ')
        print('-----------------------------------------------')
        if gen in ['1', '01']:
            self.gender.append('boy')
        else:
            self.gender.append('boy')
        
        print('LIMIT = 1000-10000-100000')
        try:
            lim = int(input('limit: '))
        except ValueError:
            lim = 10
            
        clear()
        
        # Generating UA dynamically based on fixed list
        ua_model = random.choice(infinix)
        ua = f'Mozilla/5.0 (Linux; Android 7.0; {ua_model} Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' + str(random.randrange(80, 105)) + '.0.' + str(random.randrange(1000, 5000)) + '.' + str(random.randrange(100, 399)) + ' Mobile Safari/537.36'

        headers = {
            'authority': 'www.fbsbx.com', 
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
            'accept-language': 'en-US,en;q=0.9', 
            'referer': 'https://m.facebook.com/', 
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"', 
            'sec-ch-ua-mobile': '?1', 
            'sec-ch-ua-platform': '"Android"', 
            'sec-fetch-dest': 'iframe', 
            'sec-fetch-mode': 'navigate', 
            'sec-fetch-site': 'cross-site', 
            'upgrade-insecure-requests': '1', 
            'user-agent': ua, 
            'viewport-width': '980'
        }
        
        headers1 = {
            'authority': 'www.fbsbx.com', 
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
            'accept-language': 'en-US,en;q=0.9', 
            'referer': 'https://m.facebook.com/', 
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"', 
            'sec-ch-ua-mobile': '?1', 
            'sec-ch-ua-platform': '"Android"', 
            'sec-fetch-dest': 'iframe', 
            'sec-fetch-mode': 'navigate', 
            'sec-fetch-site': 'cross-site', 
            'upgrade-insecure-requests': '1', 
            'user-agent': ua
        }

        for x in range(lim):
            self.loop += 1
            sys.stdout.write(f'\r\r[1;37m[AKASH-AUTO] {self.loop}|[1;32m{str(len(ok))}[1;37m|[1;31m{str(len(cp))} ')
            sys.stdout.flush()
            
            if 'boy' in self.gender:
                name = random.choice(boy).split(' ')
                sex = '2'
            
            try:
                # 1. Get Temporary Email
                ses = requests.Session()
                buildses = ''.join((random.SystemRandom().choice('qwertyuiopasdfghjklzxcvbnm0987654321') for i in range(26)))
                
                try:
                    create_mail = ses.get(f'https://10minutemail.net/address.api.php?new=1&sessionid={buildses}&_={int(datetime.now().timestamp() * 1000)}').json()
                    mail_obj = {'mail': create_mail['permalink']['mail'], 'session': create_mail['session_id']}
                    email = mail_obj['mail']
                    session_id = mail_obj['session']
                except (KeyError, IndexError, json.JSONDecodeError):
                    continue

                passw = random.choice(['arx123', 'arx###', 'arx@@@', 'arxarx123', 'arx@#21', '876876', '009988', '778899', '506070', 'arxarx', '57273200', '57575753', 'P@ssw0rd', 'iloveyou'])
                
                # 2. Get Registration Form
                self.ses = requests.Session()
                a = self.ses.get('https://m.facebook.com/reg?_fb_noscript', headers=headers)
                
                try:
                    logger_id_match = re.search('name="logger_id" value="(.*?)"', str(a.text))
                    loger = logger_id_match.group(1) if logger_id_match else ""
                except:
                    loger = ""

                ref = BeautifulSoup(a.text, 'html.parser').find('form', {'action': True, 'id': 'mobile-reg-form', 'method': 'post'})
                if not ref:
                    continue

                self.data = {}
                bl = ['lsd', 'jazoest', 'cpp', 'reg_instance', 'submission_request']
                bz = ['reg_impression_id', 'ns']
                
                # Extract hidden inputs
                for v in ref('input'):
                    if v.get('name') in bl or v.get('name') in bz:
                        self.data.update({v.get('name'): v.get('value')})
                
                # Add User Data
                self.data.update({
                    'helper': '',
                    'zero_header_af_client': '',
                    'app_id': '103',
                    'logger_id': loger,
                    'field_names[0]': 'firstname',
                    'firstname': name[0],
                    'lastname': name[1] if len(name) > 1 else 'Khan',
                    'field_names[1]': 'birthday_wrapper',
                    'birthday_day': str(random.randint(1, 28)),
                    'birthday_month': str(random.randint(1, 12)),
                    'birthday_year': str(random.randint(1995, 2005)),
                    'sex': sex,
                    'preferred_pronoun': '',
                    'custom_gender': '',
                    'reg_passwd__': passw,
                    'submit': 'Sign Up'
                })

                # 3. Post Registration
                url_post = 'https://m.facebook.com' + ref['action']
                gett = self.ses.post(url_post, headers=headers1, data=self.data)
                
                # 4. Handle Save Device / Checkpoint
                getts = self.ses.get('https://m.facebook.com/login/save-device/?login_source=account_creation&logger_id=' + loger + '&app_id=103', headers=headers1)
                
                if 'checkpoint' in getts.url or 'checkpoint' in gett.url:
                    cp.append(email + '|' + passw)
                
                data1 = {}
                dbl = ['fb_dtsg', 'jazoest', 'flow', 'next', 'nux_source']
                
                # Try to find confirmation form
                forms = BeautifulSoup(getts.text, 'html.parser').find_all('form', {'method': 'post'})
                for x in forms:
                    if '/login/device-based/update-nonce/' in str(x.get('action')):
                        for v in x('input'):
                            if v.get('name') not in dbl:
                                data1.update({v.get('name'): v.get('value')})
                        
                        data1.update({'submit': 'OK'})
                        po = self.ses.post('https://m.facebook.com' + x.get('action'), headers=headers1, data=data1)
                        
                        # 5. Confirmation Code Logic
                        for y in BeautifulSoup(po.text, 'html.parser').find_all('form', {'method': 'post'}):
                            if 'confirmation_event_location=cliff' in str(y.get('action')):
                                data2 = {}
                                for v in y('input'):
                                    if v.get('name') not in dbl:
                                        data2.update({v.get('name'): v.get('value')})
                                
                                # Wait and fetch code
                                code = None
                                # Try a few times to get the code
                                for _ in range(5):
                                    code = inbox(session_id)
                                    if code:
                                        break
                                    time.sleep(3)

                                if code:
                                    data2.update({'c': code, 'submit': 'Confirm'})
                                    rex = self.ses.post('https://m.facebook.com' + y.get('action'), headers=headers1, data=data2)
                                    
                                    if 'checkpoint' in rex.url:
                                        cp.append(email + '|' + passw)
                                    else:
                                        coki = ';'.join(['%s=%s' % (key, value) for key, value in self.ses.cookies.get_dict().items()])
                                        cok_dict = self.ses.cookies.get_dict()
                                        if 'c_user' in cok_dict:
                                            print(f'\r[1;32m[OK] {cok_dict["c_user"]} | {passw}[0;97m')
                                            print(f'\r[1;32m=[🍪]={coki}')
                                            ok.append(email + '|' + passw)
                                            # Save to file
                                            with open('/sdcard/AKASH-OK.txt', 'a') as f:
                                                f.write(f'{email}|{passw}|{coki}\n')
                                else:
                                    # Failed to get code
                                    pass
            
            except requests.exceptions.ConnectionError:
                time.sleep(2)
            except Exception as e:
                # print(e) # Debugging only
                pass

if __name__ == '__main__':
    create().start()
