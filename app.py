import streamlit as st
import pytesseract
import requests
import os
from PIL import Image
from language_detector import detect_language
from execute_code import execute_code
from chatbot import chat_with_ai

# Set Tesseract path (Update if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Groq API Key
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Function to extract text from an image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to send code to Groq AI for suggestions
def get_groq_suggestions(code):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a professional programmer. Analyze this code and suggest improvements."},
            {"role": "user", "content": f"Code:\n\n{code}"}
        ],
        "max_tokens": 500
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error: {response.status_code}, {response.text}"

# Load code history safely (Fix UnicodeDecodeError)
def load_code_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "rb") as history_file:
            return history_file.read().decode("utf-8", errors="ignore")  # Ignore invalid bytes
    return "📭 No code history available."

# Sidebar: Show Code History
st.sidebar.title("📜 Code History")
st.sidebar.text_area("📄 Previous Extracted Code:", load_code_history(), height=300)

# Streamlit UI - Main Section
st.title("🤖 CodeClarity ")
st.write("✨ Upload an image containing a code snippet to extract, analyze, and improve it.")

# Upload Image Section
uploaded_file = st.file_uploader("📤 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼 Uploaded Image", use_column_width=True)

    extracted_code = extract_text_from_image(image)

    if extracted_code.strip():
        st.subheader("📝 Extracted Code:")
        st.code(extracted_code, language="python")

        # Detect programming language
        language = detect_language(extracted_code)
        st.write(f"🖥 **Detected Language:** `{language}`")

        # Save extracted code to history
        with open("history.txt", "a", encoding="utf-8") as history_file:
            history_file.write(f"\n---\n🖥 Language: {language}\n{extracted_code}\n")

        # Get AI suggestions
        if st.button("💡 Get AI Suggestions"):
            with st.spinner("🤖 AI is analyzing your code..."):
                suggestions = get_groq_suggestions(extracted_code)
            st.subheader("🚀 AI Suggestions for Improvement:")
            st.write(suggestions)

        # Execute the extracted code
        if st.button("▶️ Run Code"):
            output = execute_code(extracted_code, language)
            st.subheader("⚡ Execution Output:")
            st.code(output)

        # Open chatbot for discussion
        if st.button("💬 Discuss with AI Chatbot"):
            chat_history = chat_with_ai(extracted_code)
            st.subheader("🤖 Chatbot Conversation:")
            for chat in chat_history:
                st.write(f"**🧑‍💻 You:** {chat['user']}")
                st.write(f"**🤖 AI:** {chat['bot']}")

    else:
        st.error("❌ No code detected. Please upload a clear image.")
