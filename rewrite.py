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
ซื้อเหรียญคริปโตแอพไหนดี""",
        help="Enter keywords (one per line)\nFirst keyword = main keyword (used 2x)\nOther keywords (used 1x)",
        height=100,
    )

# Content Input Area
st.subheader("""Paste Your English or Thai Content Here. 
            ** The output will always be Thai""")
existing_content = st.text_area(
    "",
    value="""วิธีซื้อเหรียญคริปโตสำหรับมือใหม่ ในปี 2024

วิธีซื้อเหรียญคริปโตสำหรับมือใหม่ ในปี 2024

การซื้อเหรียญคริปโตได้รับความสนใจจากนักลงทุนทั้งในสภาวะตลาดหมีและตลาดกระทิง เพราะคริปโตเป็นสินทรัพย์ที่มีความผันผวนสูงมากและสามารถทำการซื้อขายได้ตลอด 24 ชั่วโมงอย่างไรก็ตาม การลงทุนในสินทรัพย์ประเภทนี้อาจเป็นเรื่องยากสำหรับผู้เริ่มต้นเพราะมีวิธีการที่ค่อนข้างจะซับซ้อนจากสินทรัพย์ประเภทอื่น ๆ คู่มือนี้จะนำพาคุณได้เรียนรู้วิธีซื้อคริปโตอย่างละเอียดตั้งแต่วิธีการเปิดบัญชี วิธีการเก็บรักษาเหรีญคริปโต ความเสี่ยงในการลงทุน กลยุทธ์ในการลงทุน และขั้นตอนในการซื้อ

การซื้อขายเหรียญคริปโตสำหรับมือใหม่

หากคุณยังไม่มีประสบการณ์ในการลงทุนซื้อเหรียญคริปโตมาก่อน มีสิ่งสำคัญ 3 ประการที่คุณควรทราบก่อนเริ่มต้นการลงทุน

คริปโตคืออะไร
คริปโตหรือคริปโตเคอร์เรนซี่ (Cryptocurrency) คือสินทรัพย์ดิจิทัลที่ได้รับการออกแบบมาเพื่อเป็นตัวกลางในการแลกเปลี่ยนเช่นเดียวกับเงินสกุลทั่วไป เช่น บาท ปอนด์ และยูโร ปัจจุบันนี้มีคริปโตหลายสกุลเงิน เช่น Bitcoin, Ethereum, Ripple, Dodge และ Solona ซึ่งแต่ละสกุลเงินจะมีมูลค่าที่แตกต่างกันบล็อกเชนธุรกรรมทั้งหมดจะถูกดำเนินการผ่านบล็อกเชน (Blockchain) ซึ่งไม่มีตัวกลางอย่างธนาคาร ส่งผลให้ธุรกรรมทั้งหมดจะไม่มีการถูกบันทึก ไม่สามารถตรวจสอบย้อนหลัง ปลอมแปลง และทำลายได้การหาเหรียญคริปโตสามารถทำได้ในหลายวิธี เช่น การซื้อเหรียญคริปโต การเล่นเกม Play to Earn และการขุดเหรียญด้วยเครื่องมือ

บล็อกเชน (Blockchain) คืออะไร?

บล็อกเชน คือเทคโนโลยีทางคอมพิวเตอร์ที่มีกลไกฐานข้อมูลขั้นสูงและจะจัดเก็บข้อมูลในรูปแบบบล็อกที่เชื่อมโยงกันเป็นลูกโซ่ ก่อตั้งขึ้นในปี 2011 โดยบริษัท Blockchain.com Inc. สหรัฐอเมริกา ได้รับการออกแบบมาเพื่อรองรับการทำธุรกรรมคริปโตเคอร์เรนซี่โดยเฉพาะ

การทำธุรกรรมผ่านบล็อกเชนจะมีความปลอดภัยกว่าการทำธุรกรรมทางอิเล็กทรอนิกส์ทั่วไป เพราะเป็นเทคโนโลยีที่ยากต่อการถอดรหัสทางคณิตศาสตร์ซึ่งไม่สามารถย้อนกลับ ทำซ้ำ หรือปลอมแปลงได้

คริปโตต้องการที่จัดเก็บ
คริปโตเป็นสินทรัพย์ที่จำเป็นต้องได้รับการเก็บรักษาอย่างปลอดภัย เพราะถ้าหากสินทรัพย์ได้ถูกทำลายหรือสูญหายจากวิธีการใด ๆ ผู้ถือจะไม่สามารถเรียกสินทรัพย์คืนกลับมาได้เนื่องจากการทำธุรกรรมทั้งหมดได้ถูกนำเนินการผ่านบล็อกเชนผู้ถือจำเป็นต้องจัดเก็บคริปโตในกระเป๋าดิจิทัล (Digital Wallet) ซึ่งกระเป๋าดิจิทัลแต่ละใบจะมีกุญแจ 2 ตัว ได้แก่

กุญแจส่วนตัว (Private Key)
กุญแจส่วนตัวจะถูกใช้เพื่อเป็นที่อยู่กระเป๋าดิจิทัลซึ่งเปรียบเสมือนเลขที่บัญชีธนาคาร

กุญแจสาธารณะ (Public Key)
กุญแจสาธารณะจะถูกใช้ในการเข้าถึงกระเป๋าดิจิทัลซึ่งเปรียบเสมือนรหัสผ่านผู้ถือจำเป็นต้องเก็บรักษากุญแจสาธารณะเป็นอย่างดีและเป็นความลับ ซึ่งวิธีเก็บเหรียญคริปโตให้ปลอดภัยมี 2 วิธีการคือ Hot Wallet และ Cold Wallet

ช่องทางในการซื้อ Cryptocurrency
นักลงทุนสามารถซื้อ Crypto กับกระดานเทรด โดยกระดานเทรดแต่ละกระดานจะมีคุณสมบัติและฟังก์ชันที่เหมือนและ/หรือแตกต่างกันไป เช่น การมีคุณสมบัติเป็นกระเป๋าดิจิทัลไปในตัว การเทรดแบบฟิวเจอร์ และการเทรดแบบสปอต สิ่งสำคัญคือความปลอดภัย นักลงทุนควรเลือกซื้อคริปโตกับกระดานเทรดที่เชื่อถือได้ มีระบบรักษาความปลอดภัยสูง และใช้งานง่าย เช่น OKX, Bitget และ Bybitนักลงทุนทุกคนควรให้ความใส่ใจคือความรู้ นักลงทุนควรศึกษาข้อมูลอย่างละเอียดและทำความเข้าใจเป็นอย่างดี เพราะการลงทุนในคริปโตมีความเสี่ยงสูงมาก

ความเสี่ยงของการลงทุนคริปโต

ก่อนที่คุณจะเริ่มต้นซื้อเหรียญคริปโตเหรีญใด ๆ เก็บเข้ากระเป๋าสตางค์ดิจิทัล คุณควรทราบถึงความเสี่ยงในการลงทุนในสินทรัพย์ประเภทนี้

ยังไม่มีกฎหมายรองรับ
การลงทุนในคริปโตยังไม่มีกฎหมายรองรับในบางประเทศ อีกทั้งในบางประเทศยังสั่งห้ามไม่ให้มีกิจกรรมใด ๆ ที่เกี่ยวข้องกับคริปโต

การปั่นราคา
อาจมีการปั่นราคาเหรียญให้สูงจนเกินจริงเพื่อดึงดูดความสนใจจากนักลงทุนให้เข้าซื้อและสร้างความหวังว่าจะเป็นเหรียญที่น่าลงทุนและมีโอกาสเติบโตในอนาคต เมื่อนักลงทุนทำการเข้าซื้อแล้ว ราคาเหรียญกลับชะลอตัวและลดลงอย่างต่อเนื่อง

การทุบราคา
คริปโตเป็นสินทรัพย์ที่มีความผันผวนสูงมาก ราคาของเหรียญสามารถเพิ่มขึ้นเป็น +40% หรือ อาจเกิดเหตุการณ์ Rug Pull ที่ราคาลดลงเป็น -60% ได้อย่างรวดเร็วการทุบราคา

Rug Pull คืออะไร?

Rug Pull แปลว่า ดึงพรม เป็นคำแสลงที่เอาไว้ใช้เรียกเหตุการณ์ราคาเหรียญตกต่ำอย่างรวดเร็วจนทำให้นักลงทุนเกิดภาวะ ‘ล้มทั้งยืน’ คล้ายกับการถูกดึงพรมออกจากเท้าอย่างรวดเร็ว

เหตุการณ์นี้มักจะเกิดขึ้นในกรณีที่นักลงทุนได้ลงทุนซื้อเหรียญคริปโต จากนั้นถูกเจ้าของโครงการหรือนักพัฒนาเหรียญเทขายเหรียญทั้งหมดที่มีอยู่ในมือและนำเงินไป ส่งผลให้ราคาเหรียญตกต่ำอย่างรวดเร็ว

รวมไปถึงนักลงทุนไม่สามารถขายเหรียญและนำเงินออกมาจากกระดานเทรดได้

การเสนอขาย ICO ปลอม
มิจฉาชีพหลอกลวงว่าเป็นนักพัฒนาโครงการหรือบริษัทและเสนอขายเหรียญ ICO ซึ่งเหรียญดังกล่าวไม่มีอยู่จริง ไม่ได้รับการรับรอง หรือไม่ถูกลิสต์บนกระดานเทรดใด ๆ เมื่อเหรียญได้ถูกจำหน่ายไปจำนวนหนึ่งแล้ว โครงการขายเหรียญได้ถูกปิดตัวลงและนักลงทุนถูกลอยแพไปพร้อมกับเหรียญที่ไม่มีมูลค่า

การโจรกรรมข้อมูล
นักลงทุนอาจถูกโจรกรรมข้อมูลต่าง ๆ เช่น ข้อมูลส่วนบุคคล ข้อมูลทางการเงิน และข้อมูลกุญแจสาธารณะด้วยกลโกงต่าง ๆ เช่น การขโมยผ่าน Malware เป็นต้นMalwareเพื่อลดความเสี่ยงจากการลงทุนให้ได้มากที่สุด นักลงทุนควรศึกษาข้อมูลด้านความปลอดภัยและความเสี่ยงอย่างถี่ถ้วน

กลยุทธ์การลงทุนคริปโตแบบไหนเหมาะกับคุณ

มีกลยุทธ์ในการลงทุนคริปโตให้เลือกมากมาย เราได้คัดเลือกกลยุทธ์ที่น่าสนใจและเหมาะสำหรับนักลงทุน 2 กลุ่ม ดังนี้

นักลงทุนมือใหม่
หาเหรียญคริปโตฟรี
นักลงทุนควรหาเหรียญคริปโตฟรีแทนการซื้อเหรียญเพราะจะมีความเสี่ยงต่ำที่สุด เช่น การเล่นเกม Play to Earn, การหา Fan Token และการหา Airdrop

ซื้อเหรียญหลัก
นักลงทุนควรซื้อเหรียญคริปโตหลัก เช่น Bitcoin, Ethereum และ Tron เพราะเหรียญเหล่านี้จะได้รับความสนใจและเป็นที่รู้จักโดยทั่วไป ทำให้มีสภาพคล่องสูงเพราะมีการซื้อขายจำนวนมาก

ซื้อและถือยาว
นักลงทุนควรซื้อเหรียญในข้างต้นในภาวะตลาดหมีและถือยาวจนกว่าจะกลับมาสู่ภาวะตลาดกระทิงอีกครั้งซึ่งอาจจะใช้เวลา 6-24 เดือน

นักลงทุนมีประสบการณ์
เทรดที่แนวต้านและแนวรับ
นักลงทุนควรมองหาแนวรับและแนวต้านของราคาโดยการตั้งกรอบราคาที่เหมาะสมไว้ เช่น Bitcoin ที่ 65,000-70,000 ดอลลาร์สหรัฐฯ จากนั้นเข้าซื้อและขายเหรียญตามกรอบราคา

เทรดจากเส้น
นักลงทุนควรเข้าซื้อเหรียญตามแนวเส้นเทรนด์ MACD และ RSI โดยเส้นเหล่านี้จะสามารถบอกทิศทางของราคาเหรียญในอนาคต

เทรดแบบถัวเฉลี่ย
การถัวเฉลี่ยจะเหมาะในสถานการณ์ที่ราคาต้นทุนของเหรียญที่มีอยู่ในพอร์ตติดลบมาก ๆ วิธีการคือนักลงทุนควรซื้อเหรียญใหม่เพิ่มในราคาที่ต่ำกว่าเพื่อถัวเฉลี่ยราคาต้นทุนให้ติดลบน้อยลงและรอคอยให้ราคาเหรียญกลับมาเพิ่มอีกครั้ง

ซื้อเหรียญคริปโต ยังไง?

หากคุณเป็นนักลงทุนมือใหม่ที่ไม่มีประสบการณ์ในการซื้อเหรียญคริปโตมาก่อน เราขอแนะนำให้คุณเลือกลงทุนกับกระดานเทรดที่มีคุณสมบัติเป็นกระเป๋าดิจิทัลร่วมด้วยเพื่อความสะดวกในการซื้อและการจัดเก็บเหรียญมีกระดานเทรดหลายกระดานที่มีคุณสมบัติดังกล่าว ซึ่ง ณ ที่นี้เราขอแนะนำ OKX เพราะใช้งานง่ายและมีค่าธรรมเนียมต่ำมากต่อไปนี้คือขั้นตอนในการซื้อเหรียญคริปโตกับ OKX

ขั้นตอนที่ 1: เปิดบัญชีกับ OKX
เปิดบัญชีกับ OKX

ให้คุณไปที่เว็บไซต์ของ OKX คลิกที่ปุ่ม ‘Sign Up’ ทำการลงทะเบียน ยืนยันตัวตน และเติมเครดิตเข้าสู่บัญชีผู้ใช้ให้สำเร็จ

เปิดบัญชีกับ OKX
ขั้นตอนที่ 2: เลือกประเภทเหรียญ
ให้คุณไปที่ส่วน ‘Trade’ และเลือก ‘Spot’ จากนั้นเลือกประเภทเหรียญคริปโตหรือกรอกชื่อย่อของเหรียญที่แถบด้านซ้ายมือ เช่น BTC, ETH หรือ XRP หน้าจอจะแสดงกราฟราคาแบบเรียลไทม์และราคาย้อนหลัง ให้คุณพิจารณาการซื้อเหรียญจากราคาปัจจุบันอย่างถี่ถ้วน

ขั้นตอนที่ 3: ซื้อเหรียญซื้อเหรียญคริปโตบน OKX
ให้คุณคลิกที่ปุ่มสีเขียวที่มีคำว่า ‘Buy’ และตรวจสอบข้อมูลดังต่อไปนี้

Price (USDT) คือราคาเหรียญ ณ เวลานั้น
Amount (BTC) คือจำนวนเหรียญที่จะได้รับเมื่อซื้อสำเร็จ
Total (USDT) คือจำนวนเงินที่ต้องการซื้อเหรียญ
ให้คุณกรอกจำนวนเงินลงในช่อง ‘Total (USDT)’ และหน้าจอจะแสดงจำนวนเหรียญที่คุณจะได้รับหากการซื้อสำเร็จ จากนั้นคลิกที่ปุ่ม ‘Buy BTC’

ขั้นตอนที่ 4: ตรวจสอบเหรียญ
คุณสามารถตรวจสอบเหรียญที่คุณมีได้ที่บัญชีผู้ใช้โดยคลิกที่ส่วน ‘Assets’ และไปที่ ‘My Assets’ โดยหน้าจอจะแสดงรายการเหรียญที่คุณมีทั้งหมดในพอร์ตพร้อมกับผลกำไรและขาดทุน ณ ปัจจุบัน*โปรดทราบว่าการลงทุนในคริปโตมีความเสี่ยงสูงมาก นักลงทุนควรศึกษาข้อมูลและพิจารณาความเสี่ยงให้ดีก่อนตัดสินใจ

สรุป

คริปโตเป็นสินทรัพย์ดิจิทัลที่มีมูลค่าและมีประโยชน์ เช่น ใช้เพื่อการรับและส่งเงิน ใช้เพื่อการค้ำประกัน และใช้เพื่อการเกร็งกำไร การซื้อเหรียญคริปโตเป็นการลงทุนรูปแบบหนึ่ง แต่การลงทุนรูปแบบนี้มีความเสี่ยงสูงมากเพราะราคาเหรียญสามารถเปลี่ยนแปลงในแต่ละวันได้อย่างรวดเร็วสิ่งสำคัญคือความปลอดภัย นักลงทุนควรเลือกใช้กระเป๋าดิจิทัลและใช้บริการกับกระดานเทรดและ/หรือผู้ให้บริการที่เชื่อถือได้และมีระบบรักษาความปลอดภัยสูงในที่นี้เราขอแนะนำ OKX ซึ่งเป็นกระดานเทรดที่ใช้งานง่าย มีระบบรักษาความปลอดภัยที่ยอดเยี่ยม และมีค่าธรรมเนียมต่ำ

ไปยัง OKX
คำถามที่พบบ่อย

การซื้อคริปโตถูกกฎหมายในประเทศไทยหรือไม่?
คุณสามารถซื้อคริปโตในประเทศไทยได้โดยไม่ผิดกฎหมาย แต่โปรดทราบว่าคริปโตยังไม่ได้รับการยอมรับให้สามารถชำระหนี้ได้ตามกฎหมาย

หากฉันซื้อหรือขายเหรียญคริปโต ฉันต้องเสียภาษีหรือไม่?
หากคุณซื้อเหรียญคริปโต คุณต้องเสียภาษีมูลค่าเพิ่ม (Vat) และหากคุณขายเหรียญคริปโต คุณต้องเสียภาษีเงินได้ ซึ่งจำนวนภาษีจะเป็นไปตามอัตราที่กฎหมายกำหนด ทั้งนี้ เราขอแนะนำให้คุณปรึกษาผู้เชี่ยวชาญหรือศึกษาข้อมูลเพิ่มเติมจากเว็บไซต์ของกรมสรรพากร

หากขาดทุนจากการลงทุนในคริปโตยังคงต้องเสียภาษีหรือไม่?
แม้ว่าคุณจะขาดทุนจากการลงทุนในคริปโต คุณยังคงต้องเสียภาษีเงินได้ตามอัตราที่กฎหมายกำหนด ทั้งนี้ เราขอแนะนำให้คุณปรึกษาผู้เชี่ยวชาญหรือศึกษาข้อมูลเพิ่มเติมจากเว็บไซต์ของกรมสรรพากร
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

1. Content Format: {format_mapping[content_type]}
Provide the output in plain text format without any markdown symbols (no #, *, -, etc.).
Use clear paragraph breaks with double line spacing between sections.
For headings, simply put them on their own line without any special formatting.

2. Tone: {tone_mapping[tone_style]}

3. Writing Enhancements:"""

    if "Sentence Restructuring" in writing_style:
        prompt += "\n- Vary sentence structure and convert between active/passive voice where appropriate"
    if "Word Variation" in writing_style:
        prompt += "\n- Use appropriate synonyms and varied vocabulary while maintaining meaning"
    if "Improve Coherence" in writing_style:
        prompt += "\n- Ensure smooth transitions and logical flow between sentences and paragraphs"

    prompt += f"\n\n4. Length: "
    if length_option == "Make Shorter (50%)":
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
            prompt += "\n\n5. SEO Keywords:"
            if len(keyword_list) > 0:
                prompt += f"\n- Main keyword (use 2 times): {keyword_list[0]}"
            if len(keyword_list) > 1:
                prompt += f"\n- Secondary keywords (use 1 time each): {', '.join(keyword_list[1:])}"

    prompt += f"\n\nImportant: Format the output as plain text without any markdown symbols or special formatting. Use double line breaks between sections for clarity.\n\nOriginal Content:\n{existing_content}"
    return prompt

def get_transformed_content(prompt):
    try:
        if not client:
            return "Please enter a valid API key in the settings."
            
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",  # or any other OpenRouter model you prefer
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
                existing_content,
                length_option,
                keywords,
                writing_style
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
