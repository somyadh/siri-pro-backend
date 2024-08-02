import json

def load_chats():
    try:
        with open('chats.json', 'r') as file:
            chats = json.load(file)
    except FileNotFoundError:
        chats = {}
    return chats

def save_chats(chats):
    with open('chats.json', 'w') as file:
        json.dump(chats, file)

def get_chat_history(chat_id):
    chats = load_chats()
    return chats.get(chat_id, '')

def save_chat_history(chat_id, history):
    chats = load_chats()
    chats[chat_id] = history
    save_chats(chats)