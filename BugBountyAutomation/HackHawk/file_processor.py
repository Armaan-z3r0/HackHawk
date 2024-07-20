import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import run_command ,logger ,c , i
from server_info import fetch_server_info, fetch_server_info_concurrently

def process_file(file_path, dict_path, dict_name):
    try:
        logger.info(f"{c} Successfully started processing for {dict_name}")

        # # Read root file content
        # with open(file_path, "r") as file:
        #     root_file_content = file.read().splitlines()

        # # Perform cURL commands
        # for url in root_file_content:
        #     run_command(
        #         f"curl --head {url} --user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' > {dict_path}/ServerHeaders.txt",
        #         f"SUCCESS: cURL done for {dict_name}",
        #         f"Error during cURL for {url}"
        #     )

        # # Perform subfinder, dnsx, and anew operations
        # run_command(
        #     f"subfinder -dL {file_path} -silent | dnsx -silent | anew -q '{dict_path}/resolveddomains.txt'",
        #     f"SUCCESS: subfinder and dnsx done for {dict_name}",
        #     f"Error during subfinder/dnsx for {dict_name}"
        # )

        # # Perform httpx operation
        # run_command(
        #     f"httpx -l '{dict_path}/resolveddomains.txt' -t 75 -silent | anew '{dict_path}/webservers.txt'",
        #     f"SUCCESS: httpx done for {dict_name}",
        #     f"Error during httpx for {dict_name}"
        # )

        # # Perform smap operation
        # run_command(
        #     f"smap -iL '{dict_path}/resolveddomains.txt' > {dict_path}/openports.txt",
        #     f"SUCCESS: smap done for {dict_name}",
        #     f"Error during smap for {dict_name}"
        # )

        # # Perform WAF operation
        # run_command(
        #     f"nuclei -list {dict_path}/root.txt -t /home/avis/Desktop/BugBountyAutomation/NucleiTemplates/waf-detect.yaml -silent | anew '{dict_path}/waf-detect.txt'",
        #     f"SUCCESS: nuclei waf-detection done for {dict_name}",
        #     f"Error during nuclei WAF detection for {dict_name}"
        # )

        # Read webservers file content
        

        with open(f"{dict_path}/webservers.txt", "r") as file2:
            webservers_file_content = file2.read().splitlines()

        Webinfo_dict = {}
        server_info = {}

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(fetch_server_info, url): url for url in webservers_file_content}
            for future in as_completed(futures):
                url, result = future.result()
                Webinfo_dict[url] = result

        server_info = fetch_server_info_concurrently(Webinfo_dict)
        decent_server_info = {}
        server_name_pattern = re.compile(r'\b([a-zA-Z0-9\-\.]+)\b')
        for url, html in server_info.items():
            matches = server_name_pattern.findall(html)
            for match in matches:
                if "server" in match.lower() or "srv" in match.lower():
                    decent_server_info[url] = match
                else:
                    if url not in decent_server_info:
                        decent_server_info[url] = 0        
        for url, info in decent_server_info.items():
            print(f"{url}: {info}")

    except Exception as e:
        logger.error(f"{i} Unexpected error for {file_path}: {e}")
