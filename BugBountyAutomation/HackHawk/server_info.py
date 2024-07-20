import requests
from bs4 import BeautifulSoup, Comment
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_server_info(url, timeout=10):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
        return url, response.text
    except requests.RequestException as e:
        return url, 'X'

def get_server_info(url_dict):
    server_info = {}
    
    for url, html_content in url_dict.items():
        info = {}

        # Check headers for 'Server' information
        try:
            response = requests.get(url)
            if 'Server' in response.headers:
                info['Server_Header'] = response.headers['Server']
        except Exception as e:
            info['Header_Error'] = str(e)

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find server info in meta tags or comments
        meta_tags = soup.find_all('meta')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        # Extract server info from meta tags
        for tag in meta_tags:
            if 'server' in tag.attrs.get('name', '').lower() or 'server' in tag.attrs.get('content', '').lower():
                info['Meta_Tag'] = tag.attrs

        # Extract server info from comments
        for comment in comments:
            if 'server' in comment.lower():
                info['Comment'] = comment

        server_info[url] = info

    return server_info
    
def fetch_server_info_concurrently(url_dict):
    server_info = {}
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(get_server_info, {url: html_content}): url for url, html_content in url_dict.items()}
        for future in as_completed(futures):
            url_info = future.result()
            server_info.update(url_info)
    
    return server_info
