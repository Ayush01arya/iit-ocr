import streamlit as st
import easyocr
import re
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'hi'])


# Function for OCR and search functionality
def process_image(image, keyword):
    # Perform OCR on the image
    result = reader.readtext(image, detail=0)
    extracted_text = " ".join(result)

    # Highlight the keyword in the extracted text
    highlight_color = "#87CEEB"  # Soft Sky Blue
    if keyword:
        highlighted_text = re.sub(
            f"({re.escape(keyword)})",
            f"<mark style='background-color: {highlight_color};'>{keyword}</mark>",
            extracted_text,
            flags=re.IGNORECASE
        )
    else:
        highlighted_text = extracted_text

    # Check if the keyword is in the text
    if keyword and keyword.lower() in extracted_text.lower():
        return f"Keyword '{keyword}' found in the text.", highlighted_text
    else:
        return f"Keyword '{keyword}' not found.", highlighted_text


# Streamlit app layout
st.title("OCR and Document Search with Highlighting")
st.write("Upload an image, extract text, and search for keywords with highlighting.")

# Image upload
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Keyword input
keyword = st.text_input("Enter keyword to search")

# Process the image and display results
if image_file is not None:
    # Open the image file
    image = Image.open(image_file)

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Process Image"):
        message, highlighted_text = process_image(image, keyword)
        st.success(message)

        # Display extracted text with highlighting
        st.markdown("### Extracted Text with Highlighting")
        st.markdown(highlighted_text, unsafe_allow_html=True)
