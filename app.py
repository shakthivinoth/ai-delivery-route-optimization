import os
from flask import Flask, jsonify, render_template, request
import route_optimizer
from chatbot import SafetyChatbot

BASE = os.path.dirname(os.path.abspath(__file__))
POLICY_PATH = os.path.join(BASE, "policy", "safety_policy.txt")

app = Flask(__name__)
bot = SafetyChatbot(POLICY_PATH)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/locations")
def locations():
    return jsonify(route_optimizer.LOCATIONS)


@app.route("/api/optimize", methods=["POST"])
def optimize():
    data = request.get_json(silent=True) or {}
    try:
        speed = float(data.get("speed", route_optimizer.DEFAULT_SPEED))
        result = route_optimizer.optimize(data.get("customers", []), speed,
                                          data.get("warehouse", "Warehouse"))
        return jsonify(result)
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    return jsonify(bot.ask(str(data.get("message", ""))))


@app.route("/api/policy")
def policy():
    sections = {}
    for heading, sentence in bot.entries:
        sections.setdefault(heading, []).append(sentence)
    return jsonify(sections)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
