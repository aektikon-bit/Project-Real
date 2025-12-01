import streamlit as st
import random
import time
import csv
import os
from datetime import datetime


# ==========================================================
# Utility: Load/Save CSV
# ==========================================================

def save_stats(name, score, total, level, total_time):
    file = "stats.csv"
    header = ["timestamp", "name", "score", "total", "level", "time"]

    exists = os.path.isfile(file)
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([datetime.now(), name, score, total, level, total_time])


def update_leaderboard(name, score):
    file = "leaderboard.csv"
    header = ["name", "score"]

    exists = os.path.isfile(file)
    rows = []

    if exists:
        with open(file, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))

    rows.append([name, score])

    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def read_leaderboard():
    file = "leaderboard.csv"
    if not os.path.isfile(file):
        return []

    with open(file, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    # sort by score desc
    rows = sorted(rows, key=lambda x: int(x[1]), reverse=True)
    return rows[:10]


# ==========================================================
# Question Generator + Tutor Explain
# ==========================================================

def explain_solution(a, op, b, ans):
    if op == "+":
        return f"{a} + {b} = {ans}"
    elif op == "-":
        return f"{a} - {b} = {ans}"
    elif op == "*":
        return f"{a} × {b} = ({a} × {b//2}) × 2 (หรือแตกเป็น {a}×5 + {a}×{b-5})"
    elif op == "/":
        return f"{a} / {b} = {ans} เพราะ {a} = {b} × {int(ans)}"
    return ""


def generate_question(level):
    ops = ["+", "-", "*", "/"]
    op = random.choice(ops)

    if level == "ง่าย":
        r = (1, 10)
    elif level == "ปานกลาง":
        r = (1, 40)
    else:
        r = (1, 100)

    a = random.randint(*r)
    b = random.randint(*r)

    if op == "/":
        a = a * b

    question = f"{a} {op} {b}"
    answer = eval(question)
    return a, op, b, question, answer


# ==========================================================
# Streamlit UI
# ==========================================================

st.set_page_config(page_title="เกมคิดเลขเร็ว", page_icon="🧮", layout="wide")

st.markdown("""
<style>
.big-card {
    background: #ffffffcc;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}
.big-number {
    font-size: 70px;
    font-weight: bold;
    text-align: center;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)


st.title("🧮 เกมคิดเลขเร็ว — เวอร์ชันอัปเกรด")

# -------------------------
# Setup Session State
# -------------------------
for key, default in {
    "started": False,
    "a": None,
    "b": None,
    "op": None,
    "question": "",
    "answer": None,
    "score": 0,
    "total": 5,
    "count": 0,
    "start_time": None,
    "level": "ง่าย",
    "name": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ==========================================================
# Start Screen
# ==========================================================
if not st.session_state.started:
    st.subheader("เริ่มเล่น")
    name = st.text_input("ใส่ชื่อผู้เล่นก่อนเริ่ม (สำหรับ leaderboard)", value="Player")
    st.session_state.name = name

    level = st.selectbox("เลือกระดับความยาก", ["ง่าย", "ปานกลาง", "ยาก"])
    rounds = st.slider("จำนวนข้อ", 3, 20, 5)

    if st.button("🚀 เริ่มเกม"):
        st.session_state.level = level
        st.session_state.total = rounds
        st.session_state.score = 0
        st.session_state.count = 0
        st.session_state.start_time = time.time()
        st.session_state.started = True

        a, op, b, q, ans = generate_question(level)
        st.session_state.a, st.session_state.op, st.session_state.b = a, op, b
        st.session_state.question = q
        st.session_state.answer = ans

        st.experimental_rerun()

    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    lb = read_leaderboard()

    if lb:
        for i, (n, sc) in enumerate(lb, 1):
            st.write(f"**{i}. {n} — {sc} คะแนน**")
    else:
        st.write("ยังไม่มีคะแนนในระบบ")

    st.stop()


# ==========================================================
# Game Screen
# ==========================================================
st.markdown(f"<div class='big-card'><div class='big-number'>{st.session_state.question}</div></div>", unsafe_allow_html=True)

user_input = st.text_input("คำตอบของคุณ", key="answer_box")

col1, col2 = st.columns(2)
submit = col1.button("✔️ ตอบเลย")
giveup = col2.button("✖️ ข้าม")


# ==========================================================
# Answer Check
# ==========================================================
if submit:
    try:
        user_val = float(user_input)
        if abs(user_val - st.session_state.answer) < 1e-6:
            st.success("ถูกต้อง! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"ผิด! คำตอบคือ {st.session_state.answer}")
            st.info("🧠 วิธีคิดแบบลัด:")
            st.write(explain_solution(st.session_state.a, st.session_state.op, st.session_state.b, st.session_state.answer))

    except:
        st.warning("กรุณากรอกเป็นตัวเลข!")
        st.stop()

    st.session_state.count += 1

    if st.session_state.count >= st.session_state.total:
        st.session_state.started = False
    else:
        a, op, b, q, ans = generate_question(st.session_state.level)
        st.session_state.a, st.session_state.op, st.session_state.b = a, op, b
        st.session_state.question = q
        st.session_state.answer = ans

    st.experimental_rerun()

# ข้ามข้อ
if giveup:
    st.warning(f"ข้าม! คำตอบคือ {st.session_state.answer}")
    st.session_state.count += 1

    if st.session_state.count >= st.session_state.total:
        st.session_state.started = False
    else:
        a, op, b, q, ans = generate_question(st.session_state.level)
        st.session_state.a, st.session_state.op, st.session_state.b = a, op, b
        st.session_state.question = q
        st.session_state.answer = ans

    st.experimental_rerun()


# ==========================================================
# Result Screen
# ==========================================================
if not st.session_state.started and st.session_state.count > 0:
    total_time = time.time() - st.session_state.start_time

    st.header("🎉 ผลลัพธ์ของคุณ")
    st.metric("คะแนนรวม", f"{st.session_state.score}/{st.session_state.total}")
    st.metric("เวลาที่ใช้ทั้งหมด", f"{total_time:.2f} วินาที")

    # บันทึกสถิติ
    save_stats(st.session_state.name, st.session_state.score, st.session_state.total,
               st.session_state.level, total_time)

    # อัปเดต leaderboard
    update_leaderboard(st.session_state.name, st.session_state.score)

    if st.button("🔁 เล่นอีกครั้ง"):
        st.session_state.started = False
        st.session_state.count = 0
        st.experimental_rerun()
