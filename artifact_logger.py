# logger_config.py
import logging
import hashlib
import os
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def get_color_from_string(s):
    hash_value = hashlib.md5(s.encode()).hexdigest()
    r = int(hash_value[:2], 16)
    g = int(hash_value[2:4], 16)
    b = int(hash_value[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__(fmt)

    def format(self, record):
        color = get_color_from_string(record.name)
        reset = "\033[0m"
        bold = "\033[1m"
        message = super().format(record)
        if record.levelno >= logging.ERROR:
            message = f"{bold}{message}{reset}"
        return f"{color}{message}{reset}"

def setup_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        formatter = ColoredFormatter('%(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger