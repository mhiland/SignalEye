import os
import logging
import sys

LOG_DIR = os.path.join('/', 'var', 'log', 'wifi_monitor')
LOG_FILE = os.path.join(LOG_DIR, 'wifi_monitor.log')
LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
ENABLE_FILE_LOGGING = not os.environ.get('UNIT_TESTING', False)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if ENABLE_FILE_LOGGING:
    os.makedirs(LOG_DIR, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_formatter = logging.Formatter(LOG_FORMAT)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def print_last_log_lines():
    try:
        print(f"\n{'Logs':<30}")
        print('=' * 100)
        num_lines = 5
        with open(LOG_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print("".join(lines[-num_lines:]))
    except FileNotFoundError:
        print(f"Log file {LOG_FILE} not found")
    except Exception as e:
        print(f"Error reading log file: {e}")
