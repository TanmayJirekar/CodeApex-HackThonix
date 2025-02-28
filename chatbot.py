import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def chat_with_ai(user_message):
    """Interacts with AI for code-related queries."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are an expert programming assistant."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return [{"user": user_message, "bot": response.json()["choices"][0]["message"]["content"]}]
    else:
        return [{"user": user_message, "bot": f"Error: {response.status_code}, {response.text}"}]
