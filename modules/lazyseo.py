import sys
import requests
import os
from colors import *
from bs4 import BeautifulSoup

def analyze_seo(url):
    print(f"URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    print(f"Title: {title}")
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
    print(f"JavaScript Files: {js_files if js_files else 'No JavaScript files found'}")
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
    # Filtrar enlaces externos
    valid_external_links = [link for link in external_links if link and link not in ['#', 'javascript:void(0)', '/', '']]

    # Lanzar el script para cada enlace válido
    for link in valid_external_links:
        new_url = url + "/" + link
        os.system(f"python3 modules/lazyseo.py {new_url}")

if __name__ == "__main__":
    BANNER = f"""{RED}[⚠] Starting 👽 LazyOwn ☠ 530 ☠ [;,;] {RESET}"""
    print(BANNER)
    website_url = sys.argv[1] if len(sys.argv) > 1 else input("   [?] Enter the URL of the website to analyze (including http/https): ")
    analyze_seo(website_url)
