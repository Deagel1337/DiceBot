import os
from dotenv import load_dotenv
from command_bot import CommandBot


if __name__ == "__main__":
    load_dotenv(verbose=True)        
    BOT_TOKEN = os.getenv("BOT_TOKEN")
   
    client = CommandBot()
    client.run(BOT_TOKEN)