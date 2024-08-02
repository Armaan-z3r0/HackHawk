import os
from utils import run_command ,logger ,c , i
from root_finder import find_root_txt_files

def main():
    base_directory = '/home/pixel/HackHawk/BugBountyAutomation/'  # Replace with your actual base directory path

    try:
        if os.path.isdir(base_directory):
           find_root_txt_files(base_directory)
        else:
            # Handle case where base directory doesn't exist
            notify_message = "NO such directory found"
            run_command(
                f"echo '{notify_message}' | notify -silent -provider-config {base_directory}/NotifyConfigFiles/no-directory.yaml",
                f"Directory not found notification sent",
                f"Error sending directory not found notification"
            )
            logger.error(f"{i} Directory '{base_directory}' does not exist.")
    except Exception as e:
        # Handle other exceptions
        logger.error(f"{i} Exception occurred: {e}")
        run_command(
            f"echo 'An error occurred' | notify -silent -provider-config {base_directory}/NotifyConfigFiles/error.yaml",
            f"General error notification sent",
            f"Error sending general error notification"
        )

if __name__ == "__main__":
    main()

