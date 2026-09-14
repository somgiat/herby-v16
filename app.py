import streamlit as st

st.set_page_config(page_title="Herby", page_icon="❤️", layout="centered")

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    st.title("❤️ Herby")
    st.subheader("Your Digital Financial Mentor")

    st.markdown("""
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์
### เราช่วยให้คุณไม่ลืมเป้าหมาย
""")

    if st.button("🚀 เริ่มต้นกับ Herby"):
        st.session_state.started = True
        st.rerun()

else:

    st.title("👋 ยินดีต้อนรับ")

    name = st.text_input("คุณอยากให้ Herby เรียกคุณว่าอะไร?")

    if name:

        age = st.selectbox("คุณอยู่ในช่วงอายุใด?", ["18-24 ปี","25-34 ปี","35-44 ปี","45-54 ปี","55 ปีขึ้นไป"])

        goal = st.selectbox("เป้าหมายหลักในการลงทุนของคุณคืออะไร?", ["เกษียณ","อิสรภาพทางการเงิน","สร้างความมั่งคั่งระยะยาว","ซื้อบ้าน","การศึกษาบุตร","อื่น ๆ"])

        timeline = st.selectbox("คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?", ["น้อยกว่า 3 ปี","3-5 ปี","5-10 ปี","10-20 ปี","มากกว่า 20 ปี"])

        experience = st.selectbox("คุณมีประสบการณ์การลงทุนมากแค่ไหน?", ["ยังไม่เคยลงทุน","น้อยกว่า 1 ปี","1-3 ปี","3-10 ปี","มากกว่า 10 ปี"])

        asset_interest = st.multiselect(
            "คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?",
            ["หุ้นไทย","หุ้นต่างประเทศ","ETF","กองทุนรวม","RMF / SSF","REIT","ทองคำ","พันธบัตร","Bitcoin","Cryptocurrency","เงินฝาก","ยังไม่แน่ใจ"]
        )

        drawdown = st.radio("หากพอร์ตของคุณลดลง 30% คุณจะทำอย่างไร?", ["ขายทั้งหมด","ขายบางส่วน","ถือไว้","ทยอยซื้อเพิ่ม"])

        volatility = st.slider("คุณยอมรับความผันผวนเพื่อโอกาสเติบโตได้มากแค่ไหน?",1,10,5)

        if st.button("➡️ วิเคราะห์ Investment DNA"):

            issues = []

            if goal == "เกษียณ" and timeline in ["น้อยกว่า 3 ปี","3-5 ปี"]:
                issues.append("🎯 เป้าหมายเกษียณมักเป็นเป้าหมายระยะยาว แต่คุณระบุว่าจะใช้เงินในเวลาไม่นาน")

            if drawdown == "ขายทั้งหมด" and volatility >= 7:
                issues.append("⚠️ คุณระบุว่ารับความผันผวนได้สูง แต่จะขายทั้งหมดเมื่อพอร์ตลดลง 30%")

            if "Bitcoin" in asset_interest and volatility <= 3:
                issues.append("₿ คุณสนใจ Bitcoin แต่ระบุว่ารับความผันผวนได้ต่ำ")

            if issues:
                st.warning("👀 Herby พบข้อมูลที่อาจส่งผลต่อความแม่นยำในการประเมิน")
                for item in issues:
                    st.info(item)

                confirm = st.checkbox("✅ ฉันเข้าใจและยืนยันคำตอบเดิม")

                if not confirm:
                    st.stop()

            if drawdown == "ทยอยซื้อเพิ่ม" and volatility >= 7:
                dna_type = "🚀 Growth Hunter"
            elif drawdown == "ถือไว้" and volatility >= 5:
                dna_type = "📈 Long-Term Builder"
            elif drawdown == "ขายทั้งหมด":
                dna_type = "🛡️ Capital Protector"
            else:
                dna_type = "⚖️ Balanced Investor"

            st.header("🧬 Investment DNA Result")
            st.markdown(f"# {dna_type}")

            st.subheader("🤔 ทำไม Herby ถึงคิดแบบนั้น?")
            st.write(f"🎯 เป้าหมาย: {goal}")
            st.write(f"⏳ ระยะเวลา: {timeline}")
            st.write(f"📚 ประสบการณ์: {experience}")
            st.write(f"📉 พอร์ต -30%: {drawdown}")
            st.write(f"⚡ ความผันผวน: {volatility}/10")

            st.subheader("👀 What Herby Noticed")

            if goal == "เกษียณ" and timeline in ["น้อยกว่า 3 ปี","3-5 ปี"]:
                st.info("Herby สังเกตว่าเป้าหมายและระยะเวลาอาจยังไม่สอดคล้องกัน")

            if experience == "ยังไม่เคยลงทุน":
                st.info("Herby สังเกตว่าคุณกำลังเริ่มต้นเส้นทางการลงทุน การเรียนรู้สำคัญกว่าการหาหุ้นที่ดีที่สุด")

            if st.button("➡️ ไปตั้งค่าพอร์ตของฉัน"):
                st.success("Portfolio Setup Coming Soon")
