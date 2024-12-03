# content_transformer_app.py

import streamlit as st
from openai import OpenAI  # Ensure this is the correct import based on your OpenAI client
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

# Content Structure Tab
with st.sidebar.expander("📝 Content Structure", expanded=True):
    content_type = st.selectbox(
        "Format Style",
        (
            "Standard Article",
            "Step-by-Step Guide",
            "Pros and Cons Format",
            "Comparison Format"
        ),
        index=1,
        help="Choose how you want your content to be structured"
    )
    
    length_option = st.selectbox(
        "Length Adjustment",
        (
            "Keep Original Length",
            "Make Shorter (50%)",
            "Make Shorter (70%)",
            "Make Longer (130%)",
            "Make Longer (150%)",
            "Make Longer (200%)"
        ),
        help="Adjust the length of your content"
    )

# Language Style Tab
with st.sidebar.expander("🎯 Language Style", expanded=True):
    tone_style = st.selectbox(
        "Tone",
        (
            "Formal",
            "Semi-formal",
            "Casual"
        ),
        index=1,
        help="Choose the tone of voice for your content"
    )
    
    writing_style = st.multiselect(
        "Writing Enhancements",
        [
            "Sentence Restructuring",
            "Word Variation",
            "Improve Coherence"
        ],
        default=["Improve Coherence"],
        help="Select writing enhancement options"
    )

# SEO Settings Tab
with st.sidebar.expander("🎯 SEO Settings", expanded=True):
    keywords = st.text_area(
        "Target Keywords",
        value="""ซื้อคริปโต
ซื้อคริปโตตัวไหนดี
ซื้อคริปโตที่ไหนดี
ซื้อคริปโตยังไง
""",
        help="Enter keywords (one per line)\nFirst keyword = main keyword (used 2x)\nOther keywords (used 1x)",
        height=100,
    )

# Content Input Area
st.subheader("""Paste Your English or Thai Content Here. 
**The output will always be Thai""")
existing_content = st.text_area(
    "Input Content",
    value="""วิธีซื้อเหรียญคริปโตสำหรับมือใหม่ ในปี 2024

การซื้อเหรียญคริปโตได้รับความสนใจจากนักลงทุนทั้งในสภาวะตลาดหมีและตลาดกระทิง เพราะคริปโตเป็นสินทรัพย์ที่มีความผันผวนสูงมากและสามารถทำการซื้อขายได้ตลอด 24 ชั่วโมง อย่างไรก็ตาม การลงทุนในสินทรัพย์ประเภทนี้อาจเป็นเรื่องยากสำหรับผู้เริ่มต้นเพราะมีวิธีการที่ค่อนข้างจะซับซ้อนจากสินทรัพย์ประเภทอื่น ๆ คู่มือนี้จะนำพาคุณได้เรียนรู้วิธีซื้อคริปโตอย่างละเอียดตั้งแต่วิธีการเปิดบัญชี วิธีการเก็บรักษาเหรียญคริปโต ความเสี่ยงในการลงทุน กลยุทธ์ในการลงทุน และขั้นตอนในการซื้อ

การซื้อขายเหรียญคริปโตสำหรับมือใหม่

หากคุณยังไม่มีประสบการณ์ในการลงทุนซื้อเหรียญคริปโตมาก่อน มีสิ่งสำคัญ 3 ประการที่คุณควรทราบก่อนเริ่มต้นการลงทุน

คริปโตคืออะไร
คริปโตหรือคริปโตเคอร์เรนซี่ (Cryptocurrency) คือสินทรัพย์ดิจิทัลที่ได้รับการออกแบบมาเพื่อเป็นตัวกลางในการแลกเปลี่ยนเช่นเดียวกับเงินสกุลทั่วไป เช่น บาท ปอนด์ และยูโร ปัจจุบันนี้มีคริปโตหลายสกุลเงิน เช่น Bitcoin, Ethereum, Ripple, Dodge และ Solona ซึ่งแต่ละสกุลเงินจะมีมูลค่าที่แตกต่างกัน บล็อกเชนธุรกรรมทั้งหมดจะถูกดำเนินการผ่านบล็อกเชน (Blockchain) ซึ่งไม่มีตัวกลางอย่างธนาคาร ส่งผลให้ธุรกรรมทั้งหมดจะไม่มีการถูกบันทึก ไม่สามารถตรวจสอบย้อนหลัง ปลอมแปลง และทำลายได้ การหาเหรียญคริปโตสามารถทำได้ในหลายวิธี เช่น การซื้อเหรียญคริปโต การเล่นเกม Play to Earn และการขุดเหรียญด้วยเครื่องมือ

Rug Pull คืออะไร?

Rug Pull แปลว่า ดึงพรม เป็นคำแสลงที่เอาไว้ใช้เรียกเหตุการณ์ราคาเหรียญตกต่ำอย่างรวดเร็วจนทำให้นักลงทุนเกิดภาวะ ‘ล้มทั้งยืน’ คล้ายกับการถูกดึงพรมออกจากเท้าอย่างรวดเร็ว

เหตุการณ์นี้มักจะเกิดขึ้นในกรณีที่นักลงทุนได้ลงทุนซื้อเหรียญคริปโต จากนั้นถูกเจ้าของโครงการหรือนักพัฒนาเหรียญเทขายเหรียญทั้งหมดที่มีอยู่ในมือและนำเงินไป ส่งผลให้ราคาเหรียญตกต่ำอย่างรวดเร็ว

รวมไปถึงนักลงทุนไม่สามารถขายเหรียญและนำเงินออกมาจากกระดานเทรดได้

การเสนอขาย ICO ปลอม
มิจฉาชีพหลอกลวงว่าเป็นนักพัฒนาโครงการหรือบริษัทและเสนอขายเหรียญ ICO ซึ่งเหรียญดังกล่าวไม่มีอยู่จริง ไม่ได้รับการรับรอง หรือไม่ถูกลิสต์บนกระดานเทรดใด ๆ เมื่อเหรียญได้ถูกจำหน่ายไปจำนวนหนึ่งแล้ว โครงการขายเหรียญได้ถูกปิดตัวลงและนักลงทุนถูกลอยแพไปพร้อมกับเหรียญที่ไม่มีมูลค่า

การโจรกรรมข้อมูล
นักลงทุนอาจถูกโจรกรรมข้อมูลต่าง ๆ เช่น ข้อมูลส่วนบุคคล ข้อมูลทางการเงิน และข้อมูลกุญแจสาธารณะด้วยกลโกงต่าง ๆ เช่น การขโมยผ่าน Malware เป็นต้น Malware เพื่อลดความเสี่ยงจากการลงทุนให้ได้มากที่สุด นักลงทุนควรศึกษาข้อมูลด้านความปลอดภัยและความเสี่ยงอย่างถี่ถ้วน
""",
    height=300,
)

def generate_prompt(
    content_type,
    tone_style,
    existing_content,
    length_option,
    keywords,
    writing_style
):
    # Define mappings
    format_mapping = {
        "Standard Article": "Structure as a regular article with clear paragraphs and sections.",
        "Step-by-Step Guide": "Present the information as numbered steps with clear instructions.",
        "Pros and Cons Format": "Organize the content into clear Advantages and Disadvantages sections.",
        "Comparison Format": "Structure the content to highlight key comparison points between options."
    }

    tone_mapping = {
        "Formal": "Use formal language suitable for professional and academic contexts.",
        "Semi-formal": "Use clear, professional language that's accessible while maintaining authority.",
        "Casual": "Use simple, conversational language that's easy to understand."
    }

    prompt = f"""Transform this content into Thai with the following requirements:

1. **Content Format:** {format_mapping[content_type]}
   - Provide the output in plain text format without any markdown symbols (no #, *, -, etc.).
   - Use clear paragraph breaks with double line spacing between sections.
   - For headings, simply put them on their own line without any special formatting.

2. **Tone:** {tone_mapping[tone_style]}

3. **Writing Enhancements:**"""

    if "Sentence Restructuring" in writing_style:
        prompt += "\n- Vary sentence structure and convert between active/passive voice where appropriate."
    if "Word Variation" in writing_style:
        prompt += "\n- Use appropriate synonyms and varied vocabulary while maintaining meaning."
    if "Improve Coherence" in writing_style:
        prompt += "\n- Ensure smooth transitions and logical flow between sentences and paragraphs."

    prompt += f"\n\n4. **Length:** "
    if length_option == "Keep Original Length":
        prompt += "Maintain the original word count of the content. The number of words in the transformed content should be as close as possible to the original without any reduction or expansion."
    elif length_option == "Make Shorter (50%)":
        prompt += "Reduce the content length by about 50% while maintaining key information."
    elif length_option == "Make Shorter (70%)":
        prompt += "Reduce the content length by about 30% while maintaining key information."
    elif length_option == "Make Longer (130%)":
        prompt += "Expand the content by about 30% with relevant details and examples."
    elif length_option == "Make Longer (150%)":
        prompt += "Expand the content by about 50% with relevant details and examples."
    elif length_option == "Make Longer (200%)":
        prompt += "Double the content length with relevant details, examples, and elaboration."

    # Keywords Instructions
    if keywords.strip():
        keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]
        if keyword_list:
            prompt += "\n\n5. **SEO Keywords:**"
            if len(keyword_list) > 0:
                prompt += f"\n- **Main keyword (use 2 times):** {keyword_list[0]}"
            if len(keyword_list) > 1:
                prompt += f"\n- **Secondary keywords (use 1 time each):** {', '.join(keyword_list[1:])}"

    prompt += f"""

**Important:** 
- Format the output as plain text without any markdown symbols or special formatting.
- Use double line breaks between sections for clarity.

---

**Original Content:**
{existing_content}
"""
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
            temperature=0.9,
            max_tokens=8000
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
                existing_content,
                length_option,
                keywords,
                writing_style
            )
            transformed_content = get_transformed_content(prompt)
            st.session_state.edited_content = transformed_content
            st.subheader("Transformed Content")
            st.text_area(
                "Edit Transformed Content:",
                value=transformed_content,
                height=400,
                key="editor"
            )

            # Option to Download Edited Content
            st.download_button(
                label="📥 Download Edited Content",
                data=st.session_state.editor,
                file_name="transformed_content.txt",
                mime="text/plain",
            )
