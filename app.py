# HERBY V0.5
# Replace entire V0.4 file with this code

import streamlit as st

st.set_page_config(page_title="Herby V0.5", page_icon="❤️", layout="centered")

ASSET_RISK = {
    "เงินฝาก": 20,
    "พันธบัตร": 20,
    "ตราสารหนี้": 25,
    "กองทุนรวม": 50,
    "RMF / SSF": 55,
    "REIT": 60,
    "ทองคำ": 60,
    "ETF": 80,
    "หุ้นไทย": 80,
    "หุ้นต่างประเทศ": 90,
    "Bitcoin": 100,
    "Cryptocurrency": 100
}

GOAL_SCORE = {
    "เกษียณ": 70,
    "อิสรภาพทางการเงิน": 90,
    "สร้างความมั่งคั่งระยะยาว": 85,
    "ซื้อบ้าน": 50,
    "การศึกษาบุตร": 60,
    "อื่น ๆ": 50
}

TIMELINE_SCORE = {
    "น้อยกว่า 3 ปี": 20,
    "3-5 ปี": 40,
    "5-10 ปี": 60,
    "10-20 ปี": 80,
    "มากกว่า 20 ปี": 100
}

EXPERIENCE_SCORE = {
    "ยังไม่เคยลงทุน": 20,
    "น้อยกว่า 1 ปี": 30,
    "1-3 ปี": 50,
    "3-10 ปี": 70,
    "มากกว่า 10 ปี": 90
}


def calculate_risk_score(volatility, drawdown):
    score = volatility * 10
    if drawdown == "ขายทั้งหมด":
        score -= 20
    elif drawdown == "ขายบางส่วน":
        score -= 10
    elif drawdown == "ถือไว้":
        score += 5
    elif drawdown == "ทยอยซื้อเพิ่ม":
        score += 15
    return max(0, min(score, 100))


def calculate_asset_score(selected_assets):
    if not selected_assets:
        return 50
    scores = [ASSET_RISK[a] for a in selected_assets if a in ASSET_RISK]
    return round(sum(scores)/len(scores)) if scores else 50


if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title('❤️ Herby')
    st.subheader('Your Digital Financial Mentor')
    st.markdown('### เราไม่ได้ช่วยคุณเลือกสินทรัพย์
### เราช่วยให้คุณเข้าใจตัวเองมากขึ้น')

    if st.button('🚀 เริ่มต้นกับ Herby'):
        st.session_state.started = True
        st.rerun()

else:
    st.title('👋 ยินดีต้อนรับ')

    name = st.text_input('คุณอยากให้ Herby เรียกคุณว่าอะไร?')

    if name:
        age = st.selectbox('คุณอยู่ในช่วงอายุใด?', ['18-24 ปี','25-34 ปี','35-44 ปี','45-54 ปี','55 ปีขึ้นไป'])

        goal = st.selectbox('เป้าหมายหลักในการลงทุนของคุณคืออะไร?', ['เกษียณ','อิสรภาพทางการเงิน','สร้างความมั่งคั่งระยะยาว','ซื้อบ้าน','การศึกษาบุตร','อื่น ๆ'])

        timeline = st.selectbox('คุณคาดว่าจะใช้เงินก้อนนี้เมื่อไร?', ['น้อยกว่า 3 ปี','3-5 ปี','5-10 ปี','10-20 ปี','มากกว่า 20 ปี'])

        experience = st.selectbox('คุณมีประสบการณ์การลงทุนมากแค่ไหน?', ['ยังไม่เคยลงทุน','น้อยกว่า 1 ปี','1-3 ปี','3-10 ปี','มากกว่า 10 ปี'])

        asset_interest = st.multiselect('คุณสนใจสินทรัพย์ประเภทใดเป็นพิเศษ?', [
            'เงินฝาก','พันธบัตร','ตราสารหนี้','กองทุนรวม','RMF / SSF','REIT','ทองคำ',
            'ETF','หุ้นไทย','หุ้นต่างประเทศ','Bitcoin','Cryptocurrency'
        ])

        drawdown = st.radio('หากพอร์ตของคุณลดลง 30% คุณจะทำอย่างไร?', ['ขายทั้งหมด','ขายบางส่วน','ถือไว้','ทยอยซื้อเพิ่ม'])

        volatility = st.slider('คุณยอมรับความผันผวนได้มากแค่ไหน?',1,10,5)

        if st.button('🧬 วิเคราะห์ Investment DNA'):

            risk_score = calculate_risk_score(volatility, drawdown)
            asset_score = calculate_asset_score(asset_interest)
            goal_score = GOAL_SCORE[goal]
            timeline_score = TIMELINE_SCORE[timeline]
            experience_score = EXPERIENCE_SCORE[experience]

            issues = []

            if abs(risk_score - asset_score) >= 40:
                issues.append('ระดับความเสี่ยงที่คุณยอมรับ ไม่สอดคล้องกับประเภทสินทรัพย์ที่คุณสนใจ')

            if goal_score - asset_score >= 40:
                issues.append('สินทรัพย์ที่คุณเลือก อาจไม่สนับสนุนเป้าหมายทางการเงินที่คุณต้องการ')

            if timeline_score >= 80 and asset_score <= 30:
                issues.append('คุณมีระยะเวลาลงทุนยาว แต่ยังเลือกสินทรัพย์ความเสี่ยงต่ำเป็นหลัก')

            if experience_score <= 30 and ('Bitcoin' in asset_interest or 'Cryptocurrency' in asset_interest):
                issues.append('คุณเพิ่งเริ่มลงทุน แต่สนใจสินทรัพย์ที่มีความผันผวนสูงมาก')

            confidence = max(50, 100 - (len(issues) * 15))

            if risk_score >= 80 and asset_score >= 80:
                persona = '🚀 Growth-Oriented Investor'
            elif risk_score >= 70 and asset_score <= 40:
                persona = '⚖️ Ambitious but Cautious Investor'
            elif risk_score <= 40 and asset_score <= 40:
                persona = '🛡️ Capital Protector'
            else:
                persona = '📈 Balanced Investor'

            st.header('🌟 What Herby Learned About You')

            if goal_score >= 80 and timeline_score >= 80 and asset_score <= 40:
                st.success('คุณมีเป้าหมายเชิงรุกและมีระยะเวลาลงทุนยาว แต่ยังเลือกสินทรัพย์ความเสี่ยงต่ำ Herby มองว่าคุณกำลังมองหาความมั่นใจมากกว่าผลตอบแทนสูงสุด')
            else:
                st.success('Herby พบว่าคำตอบของคุณมีความสอดคล้องกันในหลายมิติ และสะท้อนรูปแบบนักลงทุนที่ชัดเจน')

            if issues:
                st.subheader('🚨 Smart Notice Engine')
                for issue in issues:
                    st.warning(issue)

            st.header('🧬 Investment DNA Result')
            st.write(persona)
            st.metric('DNA Confidence', f'{confidence}%')

            c1,c2,c3,c4 = st.columns(4)
            c1.metric('Risk', risk_score)
            c2.metric('Asset', asset_score)
            c3.metric('Goal', goal_score)
            c4.metric('Timeline', timeline_score)
