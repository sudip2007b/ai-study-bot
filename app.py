import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)


def call_groq(system_message: str, user_message: str) -> str:
    """Call Groq chat completion API and return the model reply text."""
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                "temperature": 0.4,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq error:", e)
        return (
            "Sorry, I couldn't talk to the AI. "
            "Check your API key, internet connection, and try again."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    question = (data.get("message") or "").strip()
    extra = (data.get("extra") or "").strip()

    if not question:
        return jsonify({"reply": "Please type a question first 😊"}), 400

    prompt = question
    if extra:
        prompt = f"{question}\n\nExtra context/notes from the student:\n{extra}"

    system_message = (
        "You are a friendly AI study buddy for college students. "
        "Explain concepts step by step with simple examples, and keep answers "
        "concise but clear."
    )

    reply = call_groq(system_message, prompt)
    return jsonify({"reply": reply})


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json() or {}
    notes = (data.get("notes") or "").strip()

    if not notes:
        return jsonify({"reply": "Paste some notes to summarize first 😄"}), 400

    system_message = (
        "You are an expert at summarizing lecture notes for exams. "
        "Keep all important definitions, formulas and keywords."
    )
    user_message = (
        "Summarize these notes for a student.\n\n"
        "Output format:\n"
        "1. A very short title\n"
        "2. 5–10 bullet points with key ideas\n"
        "3. One short revision paragraph at the end.\n\n"
        f"Notes:\n{notes}"
    )

    reply = call_groq(system_message, user_message)
    return jsonify({"reply": reply})


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json() or {}
    notes = (data.get("notes") or "").strip()

    if not notes:
        return jsonify({"reply": "Paste notes or a topic to generate a quiz 😊"}), 400

    system_message = (
        "You are an exam coach. You make short quizzes to help students self-test."
    )
    user_message = (
        "Make a 5-question quiz (MCQ if possible) from these notes or topic. "
        "After each question, show the correct answer on the next line starting "
        "with 'Answer:'. Use simple language.\n\n"
        f"Notes/topic:\n{notes}"
    )

    reply = call_groq(system_message, user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)

