# content_transformer_app.py

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import time

# Load environment variables
load_dotenv()

# Check for API keys at startup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("Please ensure OPENROUTER_API_KEY is set in your .env file")
    st.stop()

# Initialize OpenAI client with OpenRouter
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )
except Exception as e:
    st.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

# App Title
st.title("Content Transformer")

# Sidebar for Inputs
st.sidebar.header("Transformation Settings")

# Language Selection
output_language = st.sidebar.selectbox(
    "Select Output Language",
    ("Thai", "English"),
    index=0  # Default to Thai
)

# Content Type and Purpose
content_type = st.sidebar.selectbox(
    "Select Content Type & Purpose",
    (
        "Article - Informational",
        "Article - Commercial",
        "Review - Product Comparison",
        "Review - Single Product",
        "Guide - How-to",
        "Guide - Buying Decision",
        "News"
    ),
)

# Tone and Style
tone_style = st.sidebar.selectbox(
    "Select Tone and Style",
    (
        "Formal (Academic/Professional)",
        "Semi-formal (Business)",
        "Business Casual (Industry Blog)",
        "Casual (General Audience)",
        "Authoritative (Expert Opinion)"
    ),
)

# Content Structure
content_structure = st.sidebar.selectbox(
    "Content Structure",
    (
        "Standard Article",
        "Pros and Cons Format",
        "Step-by-Step Guide",
        "Comparison Table Format",
        "Q&A Format"
    )
)

# Content Length Options
length_option = st.sidebar.radio(
    "Content Length",
    ("Keep Original Length", "Make Shorter (50%)", "Make Longer (150%)", "Custom Length")
)

if length_option == "Custom Length":
    sentences_per_section = st.sidebar.number_input(
        "Number of sentences per section",
        min_value=1,
        max_value=20,
        value=5
    )

# CTA Options (only show if content type is commercial or review)
if any(x in content_type.lower() for x in ['commercial', 'review']):
    cta_type = st.sidebar.selectbox(
        "Call-to-Action Type",
        (
            "None",
            "Soft CTA (Learn More)",
            "Medium CTA (Free Trial/Demo)",
            "Strong CTA (Purchase/Subscribe)"
        )
    )
else:
    cta_type = "None"

# Keywords Input
st.sidebar.subheader("SEO Keywords")
keywords = st.sidebar.text_input("Enter keywords separated by commas")

# Keyword Frequency
keyword_frequency = st.sidebar.number_input(
    "Number of times each keyword should be mentioned",
    min_value=1,
    max_value=10,
    value=2
)

# Content Input Area
st.subheader("Paste Your Content Here")
existing_content = st.text_area(
    "",
    height=300,
)

def generate_prompt(
    content_type,
    tone_style,
    content_structure,
    existing_content,
    output_language,
    length_option,
    cta_type,
    keywords,
    keyword_frequency,
    sentences_per_section=None
):
    prompt = f"Transform this content into {output_language} as a {content_type}. "

    # Content Structure Instructions
    if content_structure == "Pros and Cons Format":
        prompt += "Organize the content into clear Advantages and Disadvantages sections. "
    elif content_structure == "Step-by-Step Guide":
        prompt += "Present the information as numbered steps with clear instructions. "
    elif content_structure == "Comparison Table Format":
        prompt += "Structure the content to highlight key comparison points between options. "
    elif content_structure == "Q&A Format":
        prompt += "Restructure the content into a Q&A format addressing key points. "

    # Tone Instructions
    tone_mapping = {
        "Formal (Academic/Professional)": "Use formal language suitable for professional contexts. Use transliteration where appropriate.",
        "Semi-formal (Business)": "Use clear, professional language that's accessible but maintains authority. Use transliteration where appropriate.",
        "Business (Industry Blog)": "Use relevant industry language that's engaging but professional. Use transliteration where appropriate.",
        "Casual (General Audience)": "Use clear, simple language accessible to general readers. Use transliteration where appropriate.",
        "Authoritative (Expert Opinion)": "Use authoritative language that demonstrates expertise. Use transliteration where appropriate." 
    }
    prompt += f"{tone_mapping[tone_style]}. "

    # Length Instructions
    if length_option == "Make Shorter (50%)":
        prompt += "Reduce the content length by about 50% while maintaining key information. "
    elif length_option == "Make Longer (150%)":
        prompt += "Expand the content by about 50% with relevant details and examples. "
    elif length_option == "Custom Length":
        prompt += f"Structure the content with {sentences_per_section} sentences per section. "

    # CTA Instructions
    if cta_type == "Soft CTA (Learn More)":
        prompt += "End with a gentle suggestion to learn more or explore further. "
    elif cta_type == "Medium CTA (Free Trial/Demo)":
        prompt += "End with an encouragement to try a free trial or demo. "
    elif cta_type == "Strong CTA (Purchase/Subscribe)":
        prompt += "End with a clear call to purchase or subscribe. "

    # Keywords Instructions
    if keywords:
        prompt += f"Ensure the following keywords are mentioned naturally {keyword_frequency} times each: {keywords}. "

    prompt += f"\n\nHere is the content to transform:\n{existing_content}"
    return prompt

def get_transformed_content(prompt):
    try:
        if not client:
            return "Please enter a valid API key in the settings."
            
        response = client.chat.completions.create(
            model="openai/o1-mini-2024-09-12",  # or any other OpenRouter model you prefer
            messages=[
                {"role": "system", "content": "You are a professional content editor and translator specializing in creating well-structured, engaging content."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=3000
        )
        transformed = response.choices[0].message.content.strip()
        return transformed
    except Exception as e:
        st.error(f"Error in transformation: {str(e)}")
        return "An error occurred during transformation. Please check your API key and try again."

# Initialize session state for edited content
if 'edited_content' not in st.session_state:
    st.session_state.edited_content = ""

# Generate Button
if st.button("✨ Generate Transformed Content"):
    if not existing_content.strip():
        st.warning("Please paste the content you want to transform.")
    else:
        with st.spinner("Transforming your content..."):
            prompt = generate_prompt(
                content_type,
                tone_style,
                content_structure,
                existing_content,
                output_language,
                length_option,
                cta_type,
                keywords,
                keyword_frequency,
                sentences_per_section if length_option == "Custom Length" else None
            )
            transformed_content = get_transformed_content(prompt)
            st.session_state.edited_content = transformed_content
            st.subheader("Transformed Content")
            st.text_area("Edit transformed content:", 
                        value=transformed_content,
                        height=400,
                        key="editor")

            # Option to Download Edited Content
            st.download_button(
                label="📥 Download Edited Content",
                data=st.session_state.editor,
                file_name="transformed_content.txt",
                mime="text/plain",
            )
