import json
import os

DATA_FILE = "bot_data.json"

# Load existing data or start with empty
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"channels": [], "users": [], "tasks": {}}

# Save current data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Add user/channel/task
def add_user(user_id):
    data = load_data()
    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data(data)

def add_channel(channel_id):
    data = load_data()
    if channel_id not in data["channels"]:
        data["channels"].append(channel_id)
        save_data(data)

def save_task(task_id, task_data):
    data = load_data()
    data["tasks"][task_id] = task_data
    save_data(data)

def get_all_data():
    return load_data()
