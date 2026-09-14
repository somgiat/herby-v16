import streamlit as st

st.set_page_config(page_title="Herby V0.4", page_icon="❤️", layout="centered")

if "started" not in st.session_state:
    st.session_state.started = False
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

# Greeting Screen
if not st.session_state.started:
    st.title("❤️ Herby")
    st.subheader("Your Digital Financial Mentor")
    st.markdown("""
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์
### เราช่วยให้คุณเข้าใจตัวเองมากขึ้น
""")

    if st.button("🚀 เริ่มต้นกับ Herby"):
        st.session_state.started = True
        st.rerun()

else:
    st.title("👋 ยินดีต้อนรับสู่ Herby")

    name = st.text_input("คุณอยากให้ Herby เรียกคุณว่าอะไร?")

    if name:
        st.success(f"ยินดีที่ได้รู้จัก {name} 😊")

        age = st.selectbox(
            "คุณอยู่ในช่วงอายุใด?",
            ["18-24 ปี", "25-34 ปี", "35-44 ปี", "45-54 ปี", "55 ปีขึ้นไป"]
        )

        goal = st.selectbox(
            "เป้าหมายหลักในการลงทุนของคุณคืออะไร?",
            ["เกษียณ", "อิสรภาพทางการเงิน", "สร้างความมั่งคั่งระยะยาว", "ซื้อบ้าน", "การศึกษาบุตร", "อื่น ๆ"]
        )

        timeline = st.selectbox(
            "คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?",
            ["น้อยกว่า 3 ปี", "3-5 ปี", "5-10 ปี", "10-20 ปี", "มากกว่า 20 ปี"]
        )

        experience = st.selectbox(
            "คุณมีประสบการณ์การลงทุนมากแค่ไหน?",
            ["ยังไม่เคยลงทุน", "น้อยกว่า 1 ปี", "1-3 ปี", "3-10 ปี", "มากกว่า 10 ปี"]
        )

        asset_interest = st.multiselect(
            "คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?",
            ["หุ้นไทย", "หุ้นต่างประเทศ", "ETF", "กองทุนรวม", "RMF / SSF", "REIT", "ทองคำ", "Bitcoin", "เงินฝาก", "ยังไม่แน่ใจ"]
        )

        drawdown = st.radio(
            "หากพอร์ตของคุณลดลง 30% คุณจะทำอย่างไร?",
            ["ขายทั้งหมด", "ขายบางส่วน", "ถือไว้", "ทยอยซื้อเพิ่ม"]
        )

        volatility = st.slider(
            "คุณยอมรับความผันผวนได้มากแค่ไหน?",
            1, 10, 5
        )

        if st.button("🧬 วิเคราะห์ Investment DNA"):

            # Consistency Check + Smart Notice Engine
            issues = []

            if goal == "เกษียณ" and timeline in ["น้อยกว่า 3 ปี", "3-5 ปี"]:
                issues.append("เป้าหมายเกษียณมักเป็นเป้าหมายระยะยาว แต่คุณต้องการใช้เงินเร็ว")

            if drawdown == "ขายทั้งหมด" and volatility >= 7:
                issues.append("คุณบอกว่ารับความผันผวนได้สูง แต่จะขายทั้งหมดเมื่อพอร์ตติดลบหนัก")

            if "Bitcoin" in asset_interest and volatility <= 3:
                issues.append("คุณสนใจ Bitcoin แต่ระบุว่ารับความผันผวนได้ต่ำ")

            if issues:
                st.warning("🚨 Smart Notice Engine")
                for i in issues:
                    st.info(i)

                st.session_state.confirmed = False
                c1, c2 = st.columns(2)

                with c1:
                    if st.button("✅ ยืนยันคำตอบเดิม"):
                        st.session_state.confirmed = True

                with c2:
                    st.button("✏️ กลับไปแก้ไข")

                if not st.session_state.confirmed:
                    st.stop()

            # Multi-Factor DNA Scoring
            score = 0

            score += volatility * 4

            if drawdown == "ทยอยซื้อเพิ่ม":
                score += 25
            elif drawdown == "ถือไว้":
                score += 15
            elif drawdown == "ขายบางส่วน":
                score += 5

            if timeline in ["10-20 ปี", "มากกว่า 20 ปี"]:
                score += 20
            elif timeline == "5-10 ปี":
                score += 10

            if experience in ["3-10 ปี", "มากกว่า 10 ปี"]:
                score += 15
            elif experience == "1-3 ปี":
                score += 8

            # DNA Result (พระรอง)
            if score >= 80:
                dna_type = "🚀 Growth Hunter"
            elif score >= 60:
                dna_type = "📈 Long-Term Builder"
            elif score >= 40:
                dna_type = "⚖️ Balanced Investor"
            else:
                dna_type = "🛡️ Capital Protector"

            emerging = experience in ["ยังไม่เคยลงทุน", "น้อยกว่า 1 ปี"]

            # What Herby Learned (พระเอก)
            st.header("🌟 What Herby Learned About You")

            learnings = []

            if goal == "เกษียณ":
                learnings.append("คุณให้ความสำคัญกับความมั่นคงในอนาคต")

            if drawdown == "ทยอยซื้อเพิ่ม":
                learnings.append("คุณมีแนวโน้มมองวิกฤตเป็นโอกาส")

            if volatility >= 7:
                learnings.append("คุณยอมรับความเสี่ยงได้ค่อนข้างสูง")
            elif volatility <= 3:
                learnings.append("คุณให้ความสำคัญกับการปกป้องเงินต้น")

            if timeline in ["10-20 ปี", "มากกว่า 20 ปี"]:
                learnings.append("คุณมีมุมมองการลงทุนระยะยาว")

            if emerging:
                learnings.append("คุณอยู่ในช่วง Emerging Investor และกำลังสร้างรากฐานการลงทุน")

            for item in learnings:
                st.success(item)

            # Emerging Investor Section
            if emerging:
                st.subheader("🌱 Emerging Investor")
                st.info("Herby มองว่าช่วงนี้ควรเน้นการเรียนรู้และสร้างวินัยมากกว่าการหาหุ้นตัวที่ดีที่สุด")

            # DNA Result (พระรอง)
            st.header("🧬 Investment DNA Result")
            st.markdown(f"## {dna_type}")
            st.metric("DNA Score", score)
