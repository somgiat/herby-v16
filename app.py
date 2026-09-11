import streamlit as st

st.set_page_config(
    page_title="Herby",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ Herby")

st.subheader("Your Digital Financial Mentor")

st.markdown("""
### เราไม่ได้ช่วยคุณเลือกสินทรัพย์

## เราช่วยให้คุณไม่ลืมเป้าหมาย
""")
st.subheader("📊 Purpose Score")

st.metric(
    "คะแนนความสอดคล้องกับเป้าหมาย",
    "84/100",
    "+2"
)
``
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Purpose Score",
        "84",
        "+2"
    )

with col2:
    st.metric(
        "Years To Goal",
        "7",
        "-0.2"
    )

st.divider()

st.subheader("🎯 เป้าหมายหลัก")

st.success("""
เกษียณอายุในอีก 7 ปี

ความคืบหน้า 62%
""")

st.divider()

st.subheader("📝 ข้อความจากเฮอร์บี้")

st.info("""
ตลาดเปลี่ยนทุกวัน

แต่เป้าหมายของคุณไม่ควรเปลี่ยนทุกวัน
""")
st.divider()

st.subheader("🎯 เป้าหมายหลัก")

goal_progress = 62

st.progress(goal_progress)

st.success("""
เกษียณอายุ 60 ปี

เหลืออีก 7 ปี

ความคืบหน้า 62%
""")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "ความคืบหน้า",
        "62%"
    )

with col2:
    st.metric(
        "เหลือเวลา",
        "7 ปี"
    )
    st.divider()

st.subheader("💌 ข้อความจากเฮอร์บี้")

st.info("""
คุณไม่ได้ลงทุนเพื่อดูราคาหุ้นทุกวัน

คุณลงทุนเพื่ออิสรภาพในอีก 7 ปีข้างหน้า
""")
