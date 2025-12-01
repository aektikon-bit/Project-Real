import streamlit as st
import random

# ตั้งค่า page
st.set_page_config(page_title="🧠 Quiz Game", page_icon="📝", layout="centered")

# CSS สวยๆ
st.markdown("""
<style>
.app-title { text-align:center; color:#FF5733; font-weight:bold; font-size:40px; margin-bottom:10px; }
.question-box { background-color:#F0F8FF; padding:20px; border-radius:15px; margin-bottom:20px; box-shadow:2px 2px 10px #aaa; }
.big-emoji { font-size:120px; text-align:center; }
.option-button button { background-color:#1E90FF; color:white; font-size:18px; padding:12px 20px; margin:5px; border-radius:10px; width:100%; }
.info-box { text-align:center; font-size:20px; color:#333; font-weight:bold; margin-top:15px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='app-title'>🧠 Quiz Game 🧠</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>ตอบคำถามให้ถูกเพื่อสะสมคะแนน!</p>", unsafe_allow_html=True)

# คำถาม
quiz = [
    {"question": "ประเทศไทยมีเมืองหลวงชื่ออะไร?", "options": ["กรุงเทพฯ", "เชียงใหม่", "ภูเก็ต", "นครราชสีมา"], "answer": "กรุงเทพฯ"},
    {"question": "สัตว์ตัวใดบินได้?", "options": ["ปลา", "นก", "ช้าง", "สุนัข"], "answer": "นก"},
    {"question": "2 + 3 = ?", "options": ["4", "5", "6", "7"], "answer": "5"},
    {"question": "สีของท้องฟ้าวันแจ่มใส?", "options": ["แดง", "ฟ้า", "เขียว", "ดำ"], "answer": "ฟ้า"},
]

# session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = random.choice(quiz)
if 'รอบ' not in st.session_state:
    st.session_state.รอบ = 1
if 'คะแนน' not in st.session_state:
    st.session_state.คะแนน = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

question = st.session_state.current_question

# แสดงคำถาม
st.markdown(f"<div class='question-box'><h3>{question['question']}</h3></div>", unsafe_allow_html=True)

# แสดงตัวเลือกเป็นปุ่ม
for option in question['options']:
    if st.button(option) and not st.session_state.answered:
        st.session_state.answered = True
        if option == question['answer']:
            st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
            st.success("ถูกต้อง! ✅")
            st.session_state.คะแนน += 1
        else:
            st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)
            st.error(f"ผิด! คำตอบที่ถูกคือ: {question['answer']} 😅")

# ปุ่มต่อไป
if st.session_state.answered:
    if st.button("คำถามต่อไป"):
        st.session_state.current_question = random.choice(quiz)
        st.session_state.รอบ += 1
        st.session_state.answered = False
        st.experimental_rerun()  # เรียก rerun เฉพาะที่ปุ่ม "คำถามต่อไป"
        
# แสดงรอบและคะแนน
st.markdown(f"<p class='info-box'>รอบที่ {st.session_state.รอบ} | คะแนน: {st.session_state.คะแนน}</p>", unsafe_allow_html=True)
