import streamlit as st

st.set_page_config(
    page_title="Herby",
    page_icon="❤️",
    layout="centered"
)

# --------------------
# Session State
# --------------------

if "started" not in st.session_state:
    st.session_state.started = False

# --------------------
# Landing Page
# --------------------

if not st.session_state.started:

    st.title("❤️ Herby")

    st.subheader("Your Digital Financial Mentor")

    st.markdown("""
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์

### เราช่วยให้คุณไม่ลืมเป้าหมาย
""")

    st.write("")

    st.markdown("""
นักลงทุนจำนวนมากรู้วิธีลงทุน

แต่ไม่ได้ลงทุนตามแผนที่วางไว้

### Herby ช่วยคุณ

✅ เข้าใจตัวเอง

✅ เข้าใจพอร์ต

✅ ไม่หลุดจากเป้าหมาย

✅ ลงทุนอย่างมีสติมากขึ้น
""")

    st.write("")

    if st.button("🚀 เริ่มต้นกับ Herby", key="start_herby"):
        st.session_state.started = True
        st.rerun()

# --------------------
# DNA Assessment
# --------------------

else:

    st.title("👋 ยินดีต้อนรับ")

    st.write(
        """
Herby อยากรู้จักคุณสักนิด 😊

เพื่อช่วยให้คำแนะนำสอดคล้องกับตัวคุณมากขึ้น
"""
    )

    name = st.text_input(
        "คุณอยากให้ Herby เรียกคุณว่าอะไร?"
    )

    if name:

        st.success(f"❤️ ยินดีที่ได้รู้จักนะ {name}")

        st.write(
            """
Herby อยากเข้าใจเป้าหมาย
และวิธีการลงทุนของคุณ

เพื่อช่วยให้คุณไม่หลุดจากสิ่งที่สำคัญที่สุด
"""
        )

        st.divider()

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

        st.divider()

    if st.button("➡️ วิเคราะห์ Investment DNA", key="dna_button"):

        st.balloons()

    # ประเมิน DNA แบบง่าย V1

    dna_type = "Balanced Investor"

    if drawdown == "ทยอยซื้อเพิ่ม" and volatility >= 7:
        dna_type = "🚀 Growth Hunter"

    elif drawdown == "ถือไว้" and volatility >= 5:
        dna_type = "📈 Long-Term Builder"

    elif drawdown == "ขายบางส่วน":
        dna_type = "⚖️ Balanced Investor"

    elif drawdown == "ขายทั้งหมด":
        dna_type = "🛡️ Capital Protector"

    st.success(f"❤️ ยินดีที่ได้รู้จักนะ {name}")

    st.header("🧬 Investment DNA Result")

    st.markdown(f"""
### Herby คิดว่าคุณมีลักษณะใกล้เคียงกับ

# {dna_type}
""")

    st.markdown("""
Herby มองว่าคุณมีแนวโน้มเป็นนักลงทุนที่
ให้ความสำคัญกับเป้าหมายระยะยาว
และพยายามตัดสินใจตามแนวทางที่สอดคล้องกับตัวเอง

แน่นอนว่าผลลัพธ์นี้เป็นเพียงจุดเริ่มต้น

Herby จะเรียนรู้เกี่ยวกับคุณมากขึ้น
เมื่อเราเดินทางต่อไปด้วยกัน ❤️
""")

    st.divider()

    st.subheader("✅ จุดแข็งที่ Herby เห็น")

    st.markdown("""
✅ มีเป้าหมายการลงทุนที่ชัดเจน

✅ เริ่มเข้าใจระดับความเสี่ยงของตนเอง

✅ กล้าที่จะวางแผนเพื่ออนาคต
""")

    st.divider()

    st.subheader("💡 สิ่งที่ Herby อยากชวนคิด")

    st.markdown("""
💡 อย่าปล่อยให้ความรู้สึกระยะสั้น
ทำให้คุณหลุดจากเป้าหมายระยะยาว

💡 ทบทวนเป้าหมายของตัวเองอย่างน้อยปีละ 1 ครั้ง

💡 ความสำเร็จในการลงทุน
ไม่ได้วัดจากผลตอบแทนเพียงอย่างเดียว
แต่วัดจากการเดินทางที่สอดคล้องกับชีวิตของคุณ
""")

    st.divider()

    if st.button("➡️ ไปตั้งค่าพอร์ตของฉัน", key="portfolio_button"):

        st.info("""
🚧 Portfolio Setup

ในขั้นตอนถัดไป Herby จะช่วยคุณ

✅ เพิ่มสินทรัพย์ที่ถืออยู่

✅ วิเคราะห์ความสอดคล้องกับเป้าหมาย

✅ เริ่มคำนวณ Goal Alignment Score

Coming Soon 🚀
""")

