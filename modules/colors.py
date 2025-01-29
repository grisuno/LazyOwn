import random
from bs4 import BeautifulSoup
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
INVERT = "\033[7m"
BLINK = "\033[5m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"
COLOR_256 = "\033[38;5;{}m"
BG_COLOR_256 = "\033[48;5;{}m"
TRUE_COLOR = "\033[38;2;{};{};{}m"
BG_TRUE_COLOR = "\033[48;2;{};{};{}m"
def retModel():
    """
    gemma2-9b-it	Google	8,192	-	-	
    llama-3.3-70b-versatile	Meta	128k	32,768	-	
    llama-3.1-8b-instant	Meta	128k	8,192	-	
    gemma2-9b-it	Meta	8,192	-	-	
    llama3-70b-8192	Meta	8,192	-	-	
    llama3-8b-8192	Meta	8,192	-	-	
    mixtral-8x7b-32768	Mistral	32,768
    """
    models = [
        {
            "1": "llama-3.3-70b-versatile",
            "2": "llama-3.1-8b-instant",
            "3": "llama3-70b-8192",
            "4": "llama3-8b-8192",
            "5": "mixtral-8x7b-32768"
        }
    ]
    nrand = random.randint(1, 5)

    model_dict = models[0]
    model_key = str(nrand)
    model = model_dict[model_key]

    return model

def delete_lines(content, to_delete):
    for line in to_delete:
        content = content.replace(line, '')
    return content

def no_html(content):
    soup = BeautifulSoup(content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    content = soup.get_text()
    content = ' '.join(content.split())
    return content