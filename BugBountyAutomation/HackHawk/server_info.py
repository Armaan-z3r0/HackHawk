import requests
from bs4 import BeautifulSoup, Comment
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import i , c , logger 
    
# Used make a dirtonary contening url and its source code
def fetch_html_content(url, timeout=5):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
        logger.info(f"{c} : source code grabbed for {url}")
        return {url : response.text}
    except requests.RequestException as e:
        logger.error(f"{i} : failed to grab the source code for {url}")
        return {url : "X"}
    
def process_url(url, data, timeout=10):
    try:
        html = data.get(url, '')  # Extract HTML content
        server_info = []

        # Make the request to get server information
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
        if 'Server' in response.headers:
            server_info.append(response.headers['Server'])

        # Define potential server names
        server_names = ['Apache', 'Tomcat', 'Mysql', 'Glassfish']
        # Strip the HTML content
        striped = html.strip()
        # Determine the content type (HTML, XML, or empty)
        page_content = ''
        html_tags = ['<html>', '<head>', '<body>']
        if striped.startswith('<?xml'):
            page_content = 'XML'
        else:
            for tag in html_tags:
                if tag in html:
                    page_content = 'HTML'
                    break
        if not page_content:
            page_content = 'Empty Webpage' if not html else 'Unknown'

        # Process HTML and XML content differently
        if page_content == 'HTML':
            soup = BeautifulSoup(html, 'html.parser')
            meta_tags = soup.find_all('meta')
            h3_tags = soup.find_all('h3')
            b_tags = soup.find_all('b')

            matching_param = []
            server_names_lower = [sevname.lower() for sevname in server_names]

            # Check meta tags
            for info in meta_tags:
                info_str = str(info).lower()
                if any(word in info_str for word in server_names_lower):
                    matching_param.append(info_str)

            # Check b tags
            for info in b_tags:
                if info.string:
                    info_str = info.string.lower()
                    if any(word in info_str for word in server_names_lower):
                        matching_param.append(info_str)

            # Check h3 tags
            for info in h3_tags:
                if info.string:
                    info_str = info.string.lower()
                    if any(word in info_str for word in server_names_lower):
                        matching_param.append(info_str)

            server_info.extend(matching_param)

        elif page_content == 'XML':
            server_info.append("XML Page")

        elif page_content == 'Empty Webpage':
            server_info.append("Empty Webpage")

        else:
            server_info.append("Unknown Data Available")

        return url, server_info

    except Exception as e:
        logger.critical(f"Error occurred for {url} : {e}")
        return url, ["Error"]

def get_server_version(web_info_dict, timeout=10):
    server_versions = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_url, url, html, timeout) for url, html in web_info_dict.items()] 
        for future in as_completed(futures):
            url, result = future.result()
            server_versions[url] = result
    return server_versions  
