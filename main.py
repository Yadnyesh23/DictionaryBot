import os
import requests
from pyrogram import Client, filters
from dotenv import load_dotenv
from database import save_word, get_history

# Load environment variables
load_dotenv()

# Telegram Bot Credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Oxford Dictionary API Credentials
OXFORD_APP_ID = os.getenv("OXFORD_APP_ID")
OXFORD_APP_KEY = os.getenv("OXFORD_APP_KEY")
OXFORD_API_BASE = os.getenv("OXFORD_API_BASE")

# Initialize Bot
bot = Client("DictionaryBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_definition(word):
    """Fetch definition from Oxford Dictionary API."""
    url = f"{OXFORD_API_BASE}{word.lower()}"
    headers = {
        "app_id": OXFORD_APP_ID,
        "app_key": OXFORD_APP_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        meanings = data.get("results", [])[0].get("lexicalEntries", [])
        
        if meanings:
            definitions = [entry["entries"][0]["senses"][0]["definitions"][0] for entry in meanings if "entries" in entry]
            return "\n".join(definitions[:3])  # Return up to 3 definitions
        else:
            return "No definition found!"
    else:
        return "Word not found in Oxford Dictionary!"

@bot.on_message(filters.text)
async def define_word(client, message):
    word = message.text.lower()
    meaning = get_definition(word)
    
    await message.reply(f"**{word.capitalize()}**:\n{meaning}")
    save_word(message.from_user.id, word, meaning)  # Save to database

bot.run()
