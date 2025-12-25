from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Use your OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

# Crisis keywords for safety
CRISIS_TERMS = ["suicide", "self-harm", "kill myself", "end my life"]
CRISIS_MESSAGE = (
    "It sounds like you are in crisis. "
    "Please contact a trained professional immediately. "
    "In India, you can call the Vandrevala Helpline: 1860 266 2345 or 9152987821."
)

# OpenRouter model
OPENROUTER_MODEL = "meta-llama/Llama-3.3-8b-instruct"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    # Safety check
    if any(term in user_message.lower() for term in CRISIS_TERMS):
        return jsonify({"reply": CRISIS_MESSAGE})

    # OpenRouter API call
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error calling OpenRouter:", e)
        reply = "Sorry, the bot is offline."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
