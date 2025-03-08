from pyrogram import Client, filters
import requests
from config import API_ID, API_HASH, BOT_TOKEN, DICTIONARY_API
from database import save_word, get_history

bot = Client("DictionaryBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me a word, and I'll define it for you.")

@bot.on_message(filters.text)
async def define_word(client, message):
    word = message.text.lower()
    response = requests.get(f"{DICTIONARY_API}{word}")

    if response.status_code == 200:
        data = response.json()
        meaning = data[0]['meanings'][0]['definitions'][0]['definition']
        await message.reply(f"**{word.capitalize()}**: {meaning}")
        save_word(message.from_user.id, word, meaning)
    else:
        await message.reply("Word not found!")

@bot.on_message(filters.command("history"))
async def history(client, message):
    words = get_history(message.from_user.id)
    history_text = "\n".join([f"{w['word']}: {w['meaning']}" for w in words])
    await message.reply(history_text if history_text else "No history found.")

bot.run()
