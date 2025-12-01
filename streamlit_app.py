import streamlit as st
import random
import time

# ---------- ฟังก์ชันสร้างโจทย์ ----------
def generate_question(level):
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)

    if level == "ง่าย":
        r = (1, 10)
    elif level == "ปานกลาง":
        r = (1, 30)
    else:
        r = (1, 100)

    a = random.randint(*r)
    b = random.randint(*r)

    if op == '/':
        a = a * b

    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer


# ---------- UI เริ่มต้น ----------
st.set_page_config(page_title="เกมคิดเลขเร็ว", page_icon="🧮", layout="centered")

st.markdown("""
<style>
.big-number {
    font-size: 60px;
    text-align: center;
    font-weight: bold;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧮 เกมคิดเลขเร็ว")
st.write("ทดสอบความเร็วในการคิดเลขของคุณ!")

# ---------- Session State Setup ----------
if "started" not in st.session_state:
    st.session_state.started = False
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 5
if "count" not in st.session_state:
    st.session_state.count = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "level" not in st.session_state:
    st.session_state.level = "ง่าย"


# ---------- เริ่มเกม ----------
if not st.session_state.started:
    st.subheader("เลือกระดับความยาก")
    level = st.selectbox("ระดับ", ["ง่าย", "ปานกลาง", "ยาก"])

    rounds = st.slider("จำนวนข้อ", 3, 20, 5)

    if st.button("🚀 เริ่มเกม"):
        st.session_state.level = level
        st.session_state.total = rounds
        st.session_state.started = True
        st.session_state.score = 0
        st.session_state.count = 0
        st.session_state.start_time = time.time()

        q, ans = generate_question(level)
        st.session_state.question = q
        st.session_state.answer = ans

    st.stop()

# ---------- โชว์โจทย์ ----------
st.markdown(f"<div class='big-number'>{st.session_state.question}</div>", unsafe_allow_html=True)

user = st.text_input("คำตอบของคุณ", key="answer_box")

col1, col2 = st.columns(2)
submit = col1.button("ตอบเลย ✔️")
giveup = col2.button("ข้าม ✖️")


# ---------- ตรวจคำตอบ ----------
if submit:
    try:
        user_val = float(user)
        if abs(user_val - st.session_state.answer) < 1e-6:
            st.success("ถูกต้อง! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"ผิด! คำตอบที่ถูกคือ {st.session_state.answer}")
    except:
        st.warning("กรุณากรอกตัวเลขนะครับ")

    st.session_state.count += 1

    if st.session_state.count >= st.session_state.total:
        st.session_state.started = False
    else:
        q, ans = generate_question(st.session_state.level)
        st.session_state.question = q
        st.session_state.answer = ans

    st.experimental_rerun()


# ---------- ข้ามข้อ ----------
if giveup:
    st.warning(f"ข้าม! คำตอบคือ {st.session_state.answer}")
    st.session_state.count += 1

    if st.session_state.count >= st.session_state.total:
        st.session_state.started = False
    else:
        q, ans = generate_question(st.session_state.level)
        st.session_state.question = q
        st.session_state.answer = ans

    st.experimental_rerun()


# ---------- สรุปผล ----------
if not st.session_state.started and st.session_state.count > 0:
    total_time = time.time() - st.session_state.start_time

    st.header("🎉 ผลลัพธ์สุดท้าย")
    st.metric("คะแนน", f"{st.session_state.score} / {st.session_state.total}")
    st.metric("เวลาที่ใช้ทั้งหมด", f"{total_time:.2f} วินาที")

    if st.button("🔁 เล่นอีกครั้ง"):
        st.session_state.started = False
        st.session_state.score = 0
        st.session_state.count = 0
        st.experimental_rerun()
