import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set Streamlit page configuration
st.set_page_config(page_title="Bill OCR Extractor", page_icon="🧾")

# Define a function to extract details using Google Gemini's API (gemini-1.5-flash)
def get_gemini_response(input_text, image_file):
    try:
        # Load and process the image
        image = Image.open(image_file)

        # Prepare the image and input prompt for the model
        model = genai.GenerativeModel('gemini-1.5-flash')  # Use gemini-1.5-flash model
        prompt = "Extract customer details, product details, and total amount from this bill."

        # Generate content with input text, image, and prompt
        response = model.generate_content([input_text, image, prompt])

        # Extract and return the response text
        return response.text

    except Exception as e:
        return f"Error processing the image: {str(e)}"

# Streamlit app layout
st.title("OCR Bill Extractor 🧾")
st.write("Upload an image of a bill to extract details like customer info, product list, and total amount.")

# Image upload feature
uploaded_file = st.file_uploader("Upload a bill image", type=["jpg", "png", "jpeg", "pdf"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Bill', use_column_width=True)

    # Input box for additional text if needed
    input_text = st.text_input("Optional: Provide additional input text", value="")

    # Button to trigger extraction
    if st.button("Extract Details"):
        with st.spinner("Extracting details..."):
            result = get_gemini_response(input_text, uploaded_file)
            st.write(result)

# Footer
st.write("Powered by Google Gemini and Streamlit.")
