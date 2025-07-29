import streamlit as st
import os
from utils import summarizer

# Set Streamlit page configuration
st.set_page_config(page_title='📄 PDF Summarizer', layout="wide")

# Inject custom CSS with background image and sidebar color
st.markdown("""
    <style>
        /* Background image */
        .stApp {
            background-image: url("https://www.google.com/imgres?q=pdf%20summarizer%20bg%20picture&imgurl=https%3A%2F%2Fpng.pngtree.com%2Fthumb_back%2Ffh260%2Fbackground%2F20190221%2Fourmid%2Fpngtree-business-business-office-end-of-year-summary-image_17824.jpg&imgrefurl=https%3A%2F%2Fpngtree.com%2Ffree-backgrounds-photos%2Fsummary&docid=PIG6UGdSKanJKM&tbnid=OKOUEz1GAD2QyM&vet=12ahUKEwjL-8u3luKOAxW0h_0HHQNUBZgQM3oECHoQAA..i&w=714&h=260&hcb=2&ved=2ahUKEwjL-8u3luKOAxW0h_0HHQNUBZgQM3oECHoQAA");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }

        /* Main container */
        .main, .block-container, .css-18e3th9 {
            background-color: rgba(255, 240, 245, 0.88);
            padding: 2rem;
            border-radius: 10px;
        }

        /* Sidebar background color */
        section[data-testid="stSidebar"] {
            background-color: #ffe6f0 !important;
        }

        /* Button style */
        .stButton > button {
            background-color: #ec407a;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-weight: bold;
        }

        .stButton > button:hover {
            background-color: #d81b60;
        }

        /* Custom message box */
        .info-box {
            background-color: #e8eaf6;
            color: black;
            padding: 0.75rem 1rem;
            border-left: 5px solid #7986cb;
            border-radius: 6px;
            margin: 10px 0;
            font-weight: 500;
        }

        /* Summary output box */
        .summary-box {
            background-color: #fff0f5;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #f48fb1;
            color: #4a148c;
        }

        /* Tech with Aafia styling */
        .aafia-style {
            font-size: 24px;
            font-weight: bold;
            color: #ad1457;
            text-align: center;
            padding-top: 10px;
            padding-bottom: 10px;
            text-shadow: 1px 1px 2px #ec407a;
        }

        h1, h2, h3, .stMarkdown {
            color: #6a1b9a !important;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    with st.sidebar:
        st.title("📚 PDF Summarizer")
        st.markdown("---")
        st.markdown("This tool lets you upload a PDF and get a summary in seconds using LLMs via OpenRouter API.")
        st.markdown("### 📌 Instructions:")
        st.markdown("1. Upload your PDF\n2. Click on **Generate Summary**\n3. Read your concise summary!")
        st.markdown("---")
        st.markdown("<div class='aafia-style'>✨ Tech with Aafia ✨</div>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>📃 AI-Powered PDF Summarizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Summarize large documents in seconds using LLMs 🔍</p>", unsafe_allow_html=True)

    pdf = st.file_uploader("📎 Upload your PDF Document", type='pdf')

    if st.button("🧠 Generate Summary", use_container_width=True):
        if pdf is not None:
            # ✅ Custom styled success message
            st.markdown(f"<div class='info-box'>✅ PDF '{pdf.name}' uploaded successfully!</div>", unsafe_allow_html=True)

            # Custom spinner-like message
            st.markdown("<div class='info-box'>⏳ Summarizing your document with LLM...</div>", unsafe_allow_html=True)

            with st.spinner("Working..."):
                response = summarizer(pdf)
                summary = response['output_text']

            st.markdown("---")
            st.subheader('Summary of File:')
            st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload a PDF file before clicking the button.")

# Run the app
if __name__ == '__main__':
    main()
