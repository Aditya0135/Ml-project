import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log" # Log file name
LOG_PATH = os.path.join(os.getcwd(), "logs", LOG_FILE) # fog file directory
os.makedirs(LOG_PATH, exist_ok=True) # make directory
LOG_FILE_PATH= os.path.join(LOG_PATH,LOG_FILE) # directory + file name

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    level=logging.INFO,
) 
#print("\nLog file={0}\n Log Path = {1}\n Log File path={2}".format(LOG_FILE,LOG_PATH,LOG_FILE_PATH))

if __name__ == "__main__":
    logging.info("Logging is working successfully")