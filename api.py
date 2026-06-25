from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Load cover data once on startup
with open("all_covers.json", "r") as file:
    covers = json.load(file)

# Helper to parse cover date
def parse_cover_date(cover):
    try:
        return datetime.strptime(cover["date"], "%B %d, %Y")
    except Exception:
        return None

@app.route("/cover", methods=["GET"])
def get_cover():
    birthday_str = request.args.get("birthday")
    if not birthday_str:
        return jsonify({"error": "Please provide a birthday like YYYY-MM-DD"}), 400

    try:
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    closest_cover = None
    smallest_diff = None

    for cover in covers:
        cover_date = parse_cover_date(cover)
        if not cover_date:
            continue

        diff = abs((cover_date - birthday).days)
        if smallest_diff is None or diff < smallest_diff:
            smallest_diff = diff
            closest_cover = cover

    if closest_cover:
        return jsonify({
            "title": closest_cover["title"],
            "image_url": closest_cover["image_url"],
            "date": closest_cover["date"],
            "days_difference": smallest_diff
        })
    else:
        return jsonify({"error": "No matching cover found."}), 404

# Run with: python api.py
if __name__ == "__main__":
    app.run(debug=True)

