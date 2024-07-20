import logging
import subprocess
from termcolor import colored
# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
c = colored("[+]", "light_green", attrs=["bold"])
i = colored("[x]", "red", attrs=["bold"])
def run_command(command, success_message, error_message):
    c = colored("[+]", "light_green", attrs=["bold"])
    i = colored("[x]", "red", attrs=["bold"])
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"{c} {success_message}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"{i} {error_message}: {e.stderr.decode().strip()}")
        raise
