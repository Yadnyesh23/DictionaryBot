from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["dictionary_bot"]
history_col = db["search_history"]

def save_word(user_id, word, meaning):
    history_col.insert_one({"user_id": user_id, "word": word, "meaning": meaning})

def get_history(user_id):
    return history_col.find({"user_id": user_id})
