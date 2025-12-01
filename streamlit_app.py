import streamlit as st
import random
import time 

# ตั้งค่า page
st.set_page_config(page_title="📝 เกมคิดเลขเร็ว", page_icon="📝", layout="centered")

def generate_question():
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)
  
    # ตัวเลข
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    
    # ปรับกรณีหารให้ลงตัว
    if op == '/':
        a = a * b

 question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

# โจทย์
def speed_math(rounds=5):
    print("=== โปรแกรมฝึกคิดเลขเร็ว ===")
    score = 0
    start_time = time.time()

    for i in range(rounds):
        q, ans = generate_question()
        print(f"\nโจทย์ข้อ {i+1}: {q}")
        
        user = float(input("คำตอบของคุณ: "))
        if abs(user - ans) < 1e-6:
            print("✔ ถูกต้อง!")
            score += 1
        else:
            print(f"✘ ผิดครับ คำตอบที่ถูกคือ {ans}")

    total_time = time.time() - start_time
    print("\n=== สรุปผล ===")
    print(f"คะแนน: {score}/{rounds}")
    print(f"เวลาที่ใช้: {total_time:.2f} วินาที")


