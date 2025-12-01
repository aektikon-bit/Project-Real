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
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, score, total, level, int(total_time)])


def update_leaderboard(name, score):
    file = "leaderboard.csv"

    exists = os.path.isfile(file)
    rows = []

    if exists:
        with open(file, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))

    # ห้ามเขียนซ้ำหัวตาราง
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
        return f"{a} × {b} = {a*b}"
    elif op == "/":
        return f"{a} ÷ {b} = {ans} เพราะ {a} = {b} × {int(ans)}"
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

    # ให้หารลงตัวเท่านั้น
    if op == "/":
        a = a * b
        answer = a / b
    else:
        answer = eval(f"{a}{op}{b}")

    question = f"{a} {op} {b}"
    return a, op, b, question, answer


# ==========================================================
# Streamlit UI
# ==========================================================

st.set_page_config(page_title="เกมคิดเลขเร็ว", page_icon="🧮", layout="wide")

st.title("🧮 เกมคิดเลขเร็ว — เวอร์ชันอัปเกรด")


# -------------------------
# Setup Session State
# -------------------------
defaults = {
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
}

for key, default in defaults.items():
    st.session_state.setdefault(key, default)


# ==========================================================
# Start Screen
# ==========================================================
if not st.session_state.started:
    st.subheader("เริ่มเล่น")
    st.session_state.name = st.text_input("ชื่อผู้เล่น", value=st.session_state.get("name", "Player"))

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
        st.session_state.update({"a": a, "b": b, "op": op, "question": q, "answer": ans})

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
st.header(f"ข้อที่ {st.session_state.count+1} / {st.session_state.total}")
st.markdown(f"<h1 style='font-size:70px; text-align:center;'>{st.session_state.question}</h1>", unsafe_allow_html=True)

user_input = st.text_input("คำตอบของคุณ", key="input_answer")

col1, col2 = st.columns(2)
submit = col1.button("✔️ ตอบเลย")
giveup = col2.button("✖️ ข้าม")


# ==========================================================
# Answer Check
# ==========================================================
def next_question():
    if st.session_state.count >= st.session_state.total:
        st.session_state.started = False
    else:
        a, op, b, q, ans = generate_question(st.session_state.level)
        st.session_state.update({"a": a, "b": b, "op": op,
                                 "question": q, "answer": ans})


if submit:
    try:
        user_val = float(user_input)
        if abs(user_val - st.session_state.answer) < 1e-6:
            st.success("ถูกต้อง! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"ผิด! คำตอบคือ {st.session_state.answer}")
            st.info("🧠 วิธีคิด:")
            st.write(explain_solution(st.session_state.a, st.session_state.op,
                                      st.session_state.b, st.session_state.answer))
    except:
        st.warning("กรุณากรอกเป็นตัวเลข!")
        st.stop()

    st.session_state.count += 1
    next_question()
    st.experimental_rerun()


if giveup:
    st.warning(f"ข้าม! คำตอบคือ {st.session_state.answer}")
    st.session_state.count += 1
    next_question()
    st.experimental_rerun()


# ==========================================================
# Result Screen
# ==========================================================
if not st.session_state.started and st.session_state.count > 0:
    total_time = int(time.time() - st.session_state.start_time)

    st.header("🎉 ผลลัพธ์ของคุณ")
    st.metric("คะแนนรวม", f"{st.session_state.score}/{st.session_state.total}")
    st.metric("เวลาที่ใช้ทั้งหมด", f"{total_time} วินาที")

    save_stats(st.session_state.name, st.session_state.score,
               st.session_state.total, st.session_state.level, total_time)

    update_leaderboard(st.session_state.name, st.session_state.score)

    if st.button("🔁 เล่นอีกครั้ง"):
        for key in defaults:
            st.session_state[key] = defaults[key]
        st.experimental_rerun()
