import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import run_command ,logger ,c , i
from file_processor import process_file

def find_root_txt_files(base_dir):
    found_files = False  # Flag to track if any files were found

    def perform_recon(root, file):
        nonlocal found_files
        if file == 'root.txt':
            found_files = True
            file_path = os.path.join(root, file)
            dict_path = root

            # Extract the directory name
            dict_name = os.path.basename(root)

            # Perform recon operations
            process_file(file_path, dict_path, dict_name)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for root, _, files in os.walk(base_dir):
            for file in files:
                futures.append(executor.submit(perform_recon, root, file))
        
        for future in as_completed(futures):
            future.result()

    if not found_files:
        # Notify if no 'root.txt' files were found
        notify_message = "No root.txt files found in any subdirectory."
        run_command(
            f"echo '{notify_message}' | notify -silent -provider-config {base_dir}/NotifyConfigFiles/no-roots.yaml",
            f"root.txt not found notification sent",
            f"Error sending root.txt not found notification"
        )
        logger.critical(f"{i} root.txt not found")
