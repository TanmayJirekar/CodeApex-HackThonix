import streamlit as st
import pytesseract
import requests
import os
from PIL import Image

# Set Tesseract path (Update for Windows users if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Securely retrieve Groq API Key (Replace with your API key if not using env variable)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # ✅ Corrected API endpoint

# Function to extract text from an image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to send extracted code to Groq AI for suggestions
def get_groq_suggestions(code):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",  # ✅ Correct Groq model
        "messages": [
            {"role": "system", "content": "You are an expert programmer. Analyze the following code and suggest improvements for efficiency and readability."},
            {"role": "user", "content": f"Code:\n\n{code}"}
        ],
        "max_tokens": 500
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit UI
st.title("Code Snippet Extractor & Groq AI Analyzer")
st.write("Upload an image containing a code snippet, extract the code, and get AI-based improvement suggestions.")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    extracted_code = extract_text_from_image(image)

    if extracted_code.strip():
        st.subheader("Extracted Code:")
        st.code(extracted_code, language="python")

        # Save extracted code to a file
        with open("extracted_code.txt", "w", encoding="utf-8") as f:
            f.write(extracted_code)

        st.success("Code extracted and saved!")

        # Send code to Groq AI and display suggestions
        if st.button("Get AI Suggestions"):
            with st.spinner("Analyzing code..."):
                suggestions = get_groq_suggestions(extracted_code)
            st.subheader("AI Suggestions for Improvement:")
            st.write(suggestions)

    else:
        st.error("No code detected. Please upload a clear image.")
