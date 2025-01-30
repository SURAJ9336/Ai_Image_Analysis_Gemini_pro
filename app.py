import re
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import tempfile
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API key not found! Please add it to the .env file.")
    st.stop()

# Configure the Generative AI API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_response(prompt, image_file_path):
    """
    Function to generate response based on a prompt and an image.

    Parameters:
    - prompt: The text prompt for generating the response.
    - image_file_path: The file path of the image to be used.

    Returns:
    - The generated response text.
    """
    try:
        # Open the image 
        with open(image_file_path, "rb") as f:
            image_bytes = f.read()

        # Encode the image bytes in Base64
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        # Prepare the payload
        payload = [
            prompt,
            {"mime_type": "image/png", "data": encoded_image}
        ]

        # Generate the response
        response = model.generate_content(payload)
        return response.text

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None


def main():
    """
    Main function for running the Streamlit web application.
    """
    # Set the title and display the logo
    st.title("Vertex AI with Gemini Pro Vision")
    st.image("logo.png", width=100)

    # Allow users to upload an image
    img = st.file_uploader("Upload an image")

    # If an image is uploaded
    if img:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        # Define the path to save the uploaded image
        image_path = os.path.join(temp_dir, img.name)

        # Write the uploaded image to the specified path
        with open(image_path, "wb") as f:
            f.write(img.getvalue())

        # Show the uploaded image
        st.image(image_path, caption="Uploaded Image", use_container_width=True)
    else:
        image_path = None  # Ensure the path is defined, even if no image is uploaded

    # Input area for the user's question
    st.header(":violet[Question]")
    question = st.text_area(label="Enter your question")
    submit = st.button("Submit")

    # If a question is entered and submitted
    if image_path and question and submit:
        # Generate a response based on the question and uploaded image
        response = generate_response(question, image_path)
        if response:
            # Display the generated response
            st.header("Answer")
            st.write(response)
        else:
            st.warning("Failed to generate a response. Please try again.")
    elif submit:
        st.warning("Please upload an image and enter a question before submitting.")


# Entry point of the script
if __name__ == "__main__":
    main()

