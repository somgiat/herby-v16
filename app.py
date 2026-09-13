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

            st.success("🎉 Herby ได้ทำความรู้จักคุณเบื้องต้นแล้ว")

            st.info(f"""
ชื่อ : {name}

ช่วงอายุ : {age}

เป้าหมายหลัก : {goal}

ระยะเวลาการใช้เงิน : {timeline}

ประสบการณ์ลงทุน : {experience}

พฤติกรรมเมื่อพอร์ตติดลบ : {drawdown}

ระดับการยอมรับความผันผวน : {volatility}/10
""")

            st.warning("""
🚧 Investment DNA Result

เวอร์ชันถัดไป Herby จะเริ่มวิเคราะห์ว่า

✅ คุณเป็นนักลงทุนแบบใด

✅ เป้าหมายและพอร์ตสอดคล้องกันหรือไม่

✅ ความเสี่ยงเหมาะกับคุณหรือไม่

✅ Goal Alignment Score
""")

