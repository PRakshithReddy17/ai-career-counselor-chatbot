import json
import os

def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "data", "careers.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

def search(query):
    query = query.lower()

    for career in data:
        if query in career["title"].lower():
            return career["description"]

    return "Focus on your interests, build skills, and stay consistent in your career path."