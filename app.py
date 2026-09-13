import streamlit as st

st.set_page_config(
    page_title="Herby",
    page_icon="❤️",
    layout="centered"
)

# ====================
# Session State
# ====================

if "started" not in st.session_state:
    st.session_state.started = False

# ====================
# Landing Page
# ====================

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

    Herby ช่วยคุณ

    ✅ เข้าใจตัวเอง

    ✅ เข้าใจพอร์ต

    ✅ ไม่หลุดจากเป้าหมาย

    ✅ เห็นพัฒนาการของตัวเอง
    """)

    st.write("")

    if st.button("🚀 เริ่มต้นกับ Herby"):
        st.session_state.started = True
        st.rerun()

# ====================
# Welcome Page
# ====================

else:

    st.title("👋 ยินดีต้อนรับ")

    st.write(
        "Herby อยากรู้จักคุณสักนิด 😊 เพื่อช่วยให้คำแนะนำสอดคล้องกับตัวคุณมากขึ้น"
    )

    name = st.text_input(
        "คุณอยากให้ Herby เรียกคุณว่าอะไร?"
    )

    if name:

        st.success(f"❤️ ยินดีที่ได้รู้จักนะ {name}")

        st.divider()

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

        st.write(f"ประสบการณ์ของคุณ : {experience}")

        risk = st.radio(
            "หากพอร์ตลดลง 30% คุณจะทำอย่างไร?",
            [
                "ขายทั้งหมด",
                "ขายบางส่วน",
                "ถือไว้",
                "ทยอยซื้อเพิ่ม"
            ]
        )

        st.write(f"คำตอบของคุณ : {risk}")

        if st.button("➡️ ไปคำถามถัดไป"):

            st.info("""
            🚧 DNA Assessment Phase 2

            พรุ่งนี้เราจะเพิ่ม

            ✅ อายุ

            ✅ เป้าหมายการลงทุน

            ✅ ระยะเวลาการใช้เงิน

            ✅ ความเสี่ยงที่ยอมรับได้

            ✅ Investment DNA Result
            """)
✅ เห็นพัฒนาการของตัวเอง
""")

st.write("")

if st.button("🚀 เริ่มต้นกับ Herby"):
    st.success("ยินดีต้อนรับ 😊")
