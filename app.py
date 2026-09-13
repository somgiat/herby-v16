import streamlit as st

st.set_page_config(
    page_title="Herby",
    page_icon="❤️",
    layout="centered"
)

# ----------------------
# Session State
# ----------------------

if "started" not in st.session_state:
    st.session_state.started = False

# ----------------------
# Landing Page
# ----------------------

if not st.session_state.started:

    st.title("❤️ Herby")

    st.subheader("Your Digital Financial Mentor")

    st.markdown("""
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์

### เราช่วยให้คุณไม่ลืมเป้าหมาย
""")

    st.markdown("""
นักลงทุนจำนวนมากรู้วิธีลงทุน

แต่ไม่ได้ลงทุนตามแผนที่วางไว้

### Herby ช่วยคุณ

✅ เข้าใจตัวเอง

✅ เข้าใจพอร์ต

✅ ไม่หลุดจากเป้าหมาย

✅ ลงทุนอย่างมีสติมากขึ้น
""")

    if st.button("🚀 เริ่มต้นกับ Herby"):

        st.session_state.started = True

        st.rerun()

# ----------------------
# DNA Assessment
# ----------------------

else:

    st.title("👋 ยินดีต้อนรับ")

    st.write("""
Herby อยากรู้จักคุณสักนิด 😊

เพื่อช่วยให้คำแนะนำสอดคล้องกับตัวคุณมากขึ้น
""")

    name = st.text_input(
        "คุณอยากให้ Herby เรียกคุณว่าอะไร?"
    )

    if name:

        st.success(
            f"❤️ ยินดีที่ได้รู้จักนะ {name}"
        )

        age = st.selectbox(
            "คุณอยู่ในช่วงอายุใด?",
            [
                "18-24 ปี",
                "25-34 ปี",
                "35-44 ปี",
                "45-54 ปี",
                "55 ปีขึ้นไป"
            ]
        )

        goal = st.selectbox(
            "เป้าหมายหลักในการลงทุนของคุณคืออะไร?",
            [
                "เกษียณ",
                "อิสรภาพทางการเงิน",
                "สร้างความมั่งคั่งระยะยาว",
                "ซื้อบ้าน",
                "การศึกษาบุตร",
                "อื่น ๆ"
            ]
        )

        timeline = st.selectbox(
            "คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?",
            [
                "น้อยกว่า 3 ปี",
                "3-5 ปี",
                "5-10 ปี",
                "10-20 ปี",
                "มากกว่า 20 ปี"
            ]
        )

        experience = st.selectbox(
            "คุณมีประสบการณ์การลงทุนมากแค่ไหน?",
            [
                "ยังไม่เคยลงทุน",
                "น้อยกว่า 1 ปี",
                "1-3 ปี",
                "3-10 ปี",
                "มากกว่า 10 ปี"
            ]
        )

        drawdown = st.radio(
            "หากพอร์ตของคุณลดลง 30% คุณจะทำอย่างไร?",
            [
                "ขายทั้งหมด",
                "ขายบางส่วน",
                "ถือไว้",
                "ทยอยซื้อเพิ่ม"
            ]
        )

        volatility = st.slider(
            "คุณยอมรับความผันผวนเพื่อโอกาสเติบโตได้มากแค่ไหน?",
            1,
            10,
            5
        )

        if st.button("➡️ วิเคราะห์ Investment DNA"):

            if drawdown == "ทยอยซื้อเพิ่ม" and volatility >= 7:
                dna_type = "🚀 Growth Hunter"

            elif drawdown == "ถือไว้" and volatility >= 5:
                dna_type = "📈 Long-Term Builder"

            elif drawdown == "ขายทั้งหมด":
                dna_type = "🛡️ Capital Protector"

            else:
                dna_type = "⚖️ Balanced Investor"

            st.balloons()

            st.header("🧬 Investment DNA Result")

           

Herby มองว่าคุณเป็นนักลงทุนที่มีแนวโน้ม
สอดคล้องกับเป้าหมายระยะยาว

ผลลัพธ์นี้เป็นเพียงจุดเริ่มต้น

Herby จะเรียนรู้เกี่ยวกับคุณมากขึ้น
เมื่อเราเดินทางต่อไปด้วยกัน "❤️"
""")

# ------------------
# What Herby Noticed
# ------------------

st.divider()

st.subheader("👀 What Herby Noticed")

observations = []

# Goal vs Timeline

if goal == "เกษียณ" and timeline in ["น้อยกว่า 3 ปี", "3-5 ปี"]:

    observations.append(
        """
🎯 Herby สังเกตว่า

คุณเลือกเป้าหมาย "เกษียณ"

แต่ระบุว่าจะใช้เงินภายในเวลาไม่นาน

Herby อยากชวนให้ทบทวนอีกครั้งว่า

เงินก้อนนี้เป็นเงินเพื่อเกษียณจริงหรือไม่
"""
    )

# Risk mismatch

if drawdown == "ขายทั้งหมด" and volatility >= 7:

    observations.append(
        """
⚠️ Herby สังเกตว่า

คุณระบุว่าสามารถรับความผันผวนได้สูง

แต่มีแนวโน้มขายทั้งหมดเมื่อพอร์ตลดลง 30%

สิ่งนี้อาจสะท้อนว่า
ความเสี่ยงที่ยอมรับได้จริง
ต่ำกว่าที่คาดไว้
"""
    )

# Growth mindset

if drawdown == "ทยอยซื้อเพิ่ม" and volatility >= 7:

    observations.append(
        """
🚀 Herby สังเกตว่า

คุณมีแนวโน้มมองความผันผวน
เป็นโอกาสมากกว่าความน่ากลัว

พฤติกรรมนี้พบได้บ่อยในนักลงทุนระยะยาว
ที่เน้นการเติบโต
"""
    )

# New investor

if experience == "ยังไม่เคยลงทุน":

    observations.append(
        """
🌱 Herby สังเกตว่า

คุณกำลังอยู่ในช่วงเริ่มต้นของการเดินทาง

ไม่จำเป็นต้องรีบเก่งทันที

การเรียนรู้และสร้างวินัย
สำคัญกว่าการหาหุ้นที่ดีที่สุด
"""
    )

# No observation found

if len(observations) == 0:

    observations.append(
        """
✅ Herby สังเกตว่า

คำตอบของคุณส่วนใหญ่
สอดคล้องกันในทิศทางเดียวกัน

นี่เป็นสัญญาณที่ดี

เพราะการลงทุนที่มีเป้าหมายชัดเจน
มักนำไปสู่การตัดสินใจที่มั่นคงกว่า
"""
    )

for item in observations:

    st.info(item)

            st.subheader("✅ จุดแข็งที่ Herby เห็น")

            st.markdown("""
✅ เริ่มเข้าใจเป้าหมายของตัวเอง

✅ กล้าวางแผนเพื่ออนาคต

✅ เริ่มเข้าใจความเสี่ยงที่ยอมรับได้
""")

            st.subheader("💡 สิ่งที่ Herby อยากชวนคิด")

            st.markdown("""
💡 อย่าปล่อยให้อารมณ์ระยะสั้น
ทำให้คุณหลุดจากเป้าหมายระยะยาว

💡 ทบทวนเป้าหมายอย่างน้อยปีละ 1 ครั้ง

💡 ความสำเร็จในการลงทุน
ไม่ได้วัดจากผลตอบแทนเพียงอย่างเดียว
""")

            if st.button("➡️ ไปตั้งค่าพอร์ตของฉัน"):

                st.info("""
🚧 Portfolio Setup Coming Soon

Herby จะช่วยคุณ

✅ เพิ่มสินทรัพย์

✅ วิเคราะห์พอร์ต

✅ คำนวณ Goal Alignment

✅ ติดตามการเดินทางของคุณ
""")
