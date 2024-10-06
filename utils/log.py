import time

from pyexpat.errors import messages

INFO = "\033[92m"  # GREEN
MAIN = "\033[94m"  # BLUE
WARN = "\033[93m"  # YELLOW
ERROR = "\033[91m"  # RED
RESET = "\033[0m"  # RESET COLOR


def log(module, msg, flush=False, end="\n", level=0):
    message = ""
    if flush:
        message += "\r"
    message += time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if level == 0:
        message += INFO + " [INFO] "
    elif level == 1:
        message += MAIN + " [MAIN] "
    elif level == 2:
        message += WARN + " [WARN] "
    elif level == 3:
        message += ERROR + " [ERROR]"
    message += f" [{module}] "
    message += msg
    message += RESET
    print(message, end=end, flush=flush)
