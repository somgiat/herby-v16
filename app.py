import streamlit as st

st.set_page_config(page_title="Herby V0.6", page_icon="❤️", layout="centered")

HIGH_RISK = ["Bitcoin","Cryptocurrency","หุ้นไทย","หุ้นต่างประเทศ","ETF"]
LOW_RISK = ["เงินฝาก","พันธบัตร","ตราสารหนี้"]

if "started" not in st.session_state:
    st.session_state.started = False

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
    st.title("👋 ยินดีต้อนรับ")

    name = st.text_input("คุณอยากให้ Herby เรียกคุณว่าอะไร?")

    if name:
        st.success(f"สวัสดี {name} 👋 ยินดีต้อนรับสู่ Herby")

        goal = st.selectbox("เป้าหมายหลักในการลงทุนของคุณคืออะไร?",[
            "เกษียณ","อิสรภาพทางการเงิน","สร้างความมั่งคั่งระยะยาว","ซื้อบ้าน","การศึกษาบุตร","อื่น ๆ"
        ])

        timeline = st.selectbox("คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?",[
            "น้อยกว่า 3 ปี","3-5 ปี","5-10 ปี","10-20 ปี","มากกว่า 20 ปี"
        ])

        experience = st.selectbox("คุณมีประสบการณ์การลงทุนมากแค่ไหน?",[
            "ยังไม่เคยลงทุน","น้อยกว่า 1 ปี","1-3 ปี","3-10 ปี","มากกว่า 10 ปี"
        ])

        assets = st.multiselect(
            "คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?",
            ["เงินฝาก","พันธบัตร","ตราสารหนี้","กองทุนรวม","RMF / SSF","REIT","ทองคำ","ETF","หุ้นไทย","หุ้นต่างประเทศ","Bitcoin","Cryptocurrency"]
        )

        drawdown = st.radio(
            "หากพอร์ตของคุณลดลง 30% คุณจะทำอย่างไร?",
            ["ขายทั้งหมด","ขายบางส่วน","ถือไว้","ทยอยซื้อเพิ่ม"]
        )

        volatility = st.slider("คุณยอมรับความผันผวนได้มากแค่ไหน?",1,10,5)

        if st.button("🔍 วิเคราะห์สไตล์การลงทุน"):

            issues = []

            if experience == "ยังไม่เคยลงทุน" and any(a in assets for a in HIGH_RISK):
                issues.append("คุณยังไม่เคยลงทุน แต่สนใจสินทรัพย์ที่มีความผันผวนสูง")

            if drawdown == "ขายทั้งหมด" and any(a in assets for a in HIGH_RISK):
                issues.append("คุณสนใจสินทรัพย์ความเสี่ยงสูง แต่มีแนวโน้มขายเมื่อพอร์ตขาดทุนหนัก")

            if goal == "อิสรภาพทางการเงิน" and len(assets) > 0 and all(a in LOW_RISK for a in assets):
                issues.append("เป้าหมายต้องการการเติบโต แต่สินทรัพย์ที่เลือกเน้นความมั่นคง")

            if volatility >= 7 and len(assets) > 0 and all(a in LOW_RISK for a in assets):
                issues.append("คุณบอกว่ารับความเสี่ยงได้สูง แต่เลือกสินทรัพย์ความเสี่ยงต่ำ")

            st.header("🌟 What Herby Learned About You")

            if experience == "ยังไม่เคยลงทุน" and any(a in assets for a in ["Bitcoin","Cryptocurrency"]):
                st.info("Herby สังเกตว่าคุณสนใจสินทรัพย์ที่มีโอกาสเติบโตสูงมาก แต่ยังไม่มีประสบการณ์ลงทุนมาก่อน คุณอาจกำลังสนใจโอกาสทำกำไรมากกว่าการรับรู้ความเสี่ยงจริง การเรียนรู้เรื่องการบริหารความเสี่ยงอาจสำคัญที่สุดในช่วงนี้")

            elif len(issues) >= 2:
                st.info("Herby พบว่าคุณกำลังอยู่ในช่วงค้นหาสไตล์การลงทุนของตัวเอง คุณสนใจการเติบโตในบางมุม แต่ยังมีความกังวลเรื่องความเสี่ยงในอีกหลายมุม ซึ่งเป็นเรื่องปกติของนักลงทุนที่กำลังเรียนรู้")

            else:
                st.info("Herby พบว่าคำตอบของคุณสะท้อนสไตล์การลงทุนที่ค่อนข้างชัดเจน และยังไม่พบความขัดแย้งสำคัญในพฤติกรรมการลงทุน")

            st.header("🚨 สิ่งที่ Herby สังเกตเห็น")
            if issues:
                for i in issues:
                    st.warning(i)
            else:
                st.success("ยังไม่พบความขัดแย้งที่สำคัญจากคำตอบของคุณ")

            if drawdown == "ขายทั้งหมด":
                style = "🛡️ นักลงทุนสายระมัดระวัง"
                desc = "ให้ความสำคัญกับการปกป้องเงินต้น และไม่สบายใจกับการขาดทุนรุนแรง"
            elif drawdown == "ขายบางส่วน":
                style = "⚖️ นักลงทุนสายสมดุล"
                desc = "พยายามสร้างสมดุลระหว่างการเติบโตและการควบคุมความเสี่ยง"
            elif drawdown == "ถือไว้":
                style = "📈 นักลงทุนสายเติบโต"
                desc = "เข้าใจว่าการลงทุนมีรอบขึ้นลง และพร้อมถือผ่านความผันผวนบางส่วน"
            else:
                style = "🚀 นักลงทุนสายรุก"
                desc = "มองความผันผวนเป็นโอกาสและเน้นการเติบโตระยะยาว"

            confidence = max(50,100-(len(issues)*15))

            st.header("📈 สไตล์การลงทุนปัจจุบันของคุณ")
            st.subheader(style)
            st.write(desc)

            st.metric("ความชัดเจนของรูปแบบการลงทุน", f"{confidence}%")

            st.header("💡 Herby แนะนำอะไรต่อ")

            if any(a in assets for a in ["Bitcoin","Cryptocurrency"]) and experience == "ยังไม่เคยลงทุน":
                st.write("เริ่มจากเรียนรู้การบริหารความเสี่ยง การจัดพอร์ต และการรับมือความผันผวน ก่อนเพิ่มเงินลงทุนจริง")
            elif drawdown == "ขายทั้งหมด":
                st.write("ลองศึกษาว่าคุณรับการขาดทุนได้จริงแค่ไหน เพราะความเข้าใจเรื่องความเสี่ยงสำคัญกว่าการเลือกสินทรัพย์")
            else:
                st.write("ศึกษาสินทรัพย์ที่สอดคล้องกับเป้าหมายและระยะเวลาลงทุนของคุณเพิ่มเติม")
