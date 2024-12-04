import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key at startup
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("Please ensure OPENROUTER_API_KEY is set in your .env file")
    st.stop()

# Initialize OpenAI client with OpenRouter
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": "https://openrouter.ai/",  # Required for OpenRouter
        }
    )
except Exception as e:
    st.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

# App Title
st.title("Content Transformer")

# Default prompt template
default_prompt = """You are an expert Thai technology journalist with extensive knowledge across crypto sector. Your task is to transform the provided content according to these specifications:

Content Transformation Goals:
1. REWRITE the content completely while keeping the core information
2. Use different sentence structures; vary between simple, compound, and complex sentences
3. Reorganise paragraphs and information flow when possible while maintaining logical flow and keeping key points, all facts, statistics, and key information accurate
4. Use synonyms and alternative expressions 
5. Keep the same number of sections, paragraphs, lists, and similar paragraph lengths but transform EVERY sentence.
6. Voice and Style is Semi-Professional

Language-Specific Requirements:
- Output must be in Thai language
- Use natural Thai expressions rather than direct translations
- Maintain Thai grammar language structure
- Use English names for entities like people, city names, organisations, platform names
- Use English for cryptocurrency names. For example, use 'Bitcoin' instead of 'บิทคอยน์', 'Ethereum' instead of 'อีเธอเรียม', 'Solana' instead of 'โซลาน่า', etc.
- Integrate these keywords naturally: {keywords}

Original Content:
{content}
"""

# Initialize session states
if 'prompt_template' not in st.session_state:
    st.session_state.prompt_template = default_prompt

# Prompt Template Editor (collapsed by default)
with st.expander("✏️ Edit Prompt Template", expanded=False):
    prompt_template = st.text_area(
        "Prompt Template",
        value=st.session_state.prompt_template,
        height=400
    )

# Keywords Input
st.subheader("Enter Keywords (one per line)")
keywords = st.text_area(
    "Keywords",
    height=100,
    help="Enter one keyword per line. These will be integrated naturally into the transformed content."
)

# Content Input
st.subheader("Paste Content to Transform")
content = st.text_area(
    "Content",
    height=300,
    help="Paste the content you want to transform here."
)

def get_transformed_content(prompt):
    """Get transformed content from OpenAI"""
    if not client:
        st.error("OpenAI client is not properly initialized")
        return None
        
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-2024-11-20",  
            messages=[
                {"role": "system", "content": "You are an expert Thai technology journalist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        # Debug information (hidden by default)
        with st.expander("Debug Information", expanded=False):
            st.write("Debug - Response:", response)
        
        # Safely access response content
        try:
            if response and response.choices:
                return response.choices[0].message.content
            else:
                st.error("No valid response content received")
                return None
        except AttributeError as ae:
            st.error(f"Error accessing response content: {str(ae)}")
            return None
            
    except Exception as e:
        st.error(f"Error during transformation: {str(e)}")
        if hasattr(e, 'response'):
            st.error(f"API Response: {e.response}")
        return None

# Transform Button
if st.button("✨ Transform Content"):
    if not content:
        st.warning("Please paste some content to transform.")
    else:
        try:
            # Prepare keywords
            keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]
            keywords_formatted = ", ".join(keyword_list)
            
            # Show the final prompt for debugging (hidden by default)
            final_prompt = prompt_template.format(
                keywords=keywords_formatted,
                content=content
            )
            
            with st.expander("Debug - Final Prompt", expanded=False):
                st.text(final_prompt)
            
            # Show progress
            with st.spinner("Transforming content..."):
                transformed_content = get_transformed_content(final_prompt)
                
            if transformed_content:
                # Display content in HTML format
                def format_content_to_html(content):
                    # Split content into lines
                    lines = content.split('\n')
                    html_parts = []
                    in_list = False
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Clean up the line content (remove ** and ---)
                        def clean_content(text):
                            # Remove ** markers
                            text = text.replace('**', '')
                            # Remove single - or multiple --- if they're not bullet points
                            if not text.startswith(('- ', '* ')):
                                text = text.replace('-', '')
                            text = text.strip()
                            return text
                            
                        # Handle headings
                        if line.startswith('### '):
                            html_parts.append(f'<h3>{clean_content(line[4:])}</h3>')
                        elif line.startswith('## '):
                            html_parts.append(f'<h2>{clean_content(line[3:])}</h2>')
                        elif line.startswith('# '):
                            html_parts.append(f'<h1>{clean_content(line[2:])}</h1>')
                        # Handle numbered lists
                        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                            if not in_list:
                                html_parts.append('<ol>')
                                in_list = True
                            content = line[line.find(" ")+1:]
                            html_parts.append(f'<li>{clean_content(content)}</li>')
                        # Handle bullet points
                        elif line.startswith(('- ', '* ')):
                            if not in_list:
                                html_parts.append('<ul>')
                                in_list = True
                            html_parts.append(f'<li>{clean_content(line[2:])}</li>')
                        else:
                            if in_list:
                                html_parts.append('</ol>' if html_parts[-2].startswith('<ol') else '</ul>')
                                in_list = False
                            html_parts.append(f'<p>{clean_content(line)}</p>')
                    
                    if in_list:
                        html_parts.append('</ol>' if html_parts[-2].startswith('<ol') else '</ul>')
                    
                    return '\n'.join(html_parts)
                
                formatted_html = format_content_to_html(transformed_content)
                html_content = f"""
                    <div style="background-color: white; padding: 20px; border-radius: 5px; border: 1px solid #ddd; line-height: 1.6;">
                        <style>
                            h1 {{ font-size: 24px; margin-bottom: 20px; color: #333; }}
                            h2 {{ font-size: 20px; margin: 20px 0 15px; color: #444; }}
                            h3 {{ font-size: 18px; margin: 15px 0 10px; color: #555; }}
                            p {{ margin: 10px 0; color: #666; }}
                            ul, ol {{ margin: 10px 0; padding-left: 25px; }}
                            li {{ margin: 5px 0; color: #666; }}
                        </style>
                        {formatted_html}
                    </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error processing content: {str(e)}")
