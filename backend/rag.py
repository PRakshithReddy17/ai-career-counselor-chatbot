import json

def load_data():
    with open("backend/data/careers.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

def search(query):
    query = query.lower()

    for career in data:
        if query in career["title"].lower():
            return career["description"]

    return "General career advice: Focus on your interests, build skills, and stay consistent."