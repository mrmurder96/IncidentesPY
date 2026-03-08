import json

def load_user_data():
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
            return user_data
    except FileNotFoundError:
        return {}
def save_user_data(user_data):
                with open("user_data.json", "w") as f:
                        json.dump(user_data, f)