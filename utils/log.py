import time


class Bcolors:
    NORMAL = "\033[92m"  # GREEN
    PROCESS = "\033[94m"  # BLUE
    WARNING = "\033[93m"  # YELLOW
    ERROR = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


def get_time() -> str:
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return localtime


def normal_log(module, msg):
    message = f"{get_time()} [INFO]    [{module}] {msg}"
    print(Bcolors.NORMAL + message + Bcolors.RESET)


def process_log(module, msg, flush=False, end="\n"):
    message = f"{get_time()} [PROCESS] [{module}] {msg}"
    if flush:
        message = "\r" + message
    print(Bcolors.PROCESS + message + Bcolors.RESET, flush=flush, end=end)


def warning_log(module, msg):
    message = f"{get_time()} [WARNING] [{module}] {msg}"
    print(Bcolors.WARNING + message + Bcolors.RESET)


def error_log(module, msg):
    message = f"{get_time()} [ERROR]   [{module}] {msg}"
    print(Bcolors.ERROR + message + Bcolors.RESET)
