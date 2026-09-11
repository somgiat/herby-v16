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

st.divider()

st.subheader("📊 สถานะปัจจุบัน")

st.success("""
  ⭐ คะแนนความสอดคล้องกับเป้าหมาย : 84/100

🎯 เป้าหมาย : เกษียณอายุในอีก 7 ปี

✅ สถานะ : คุณยังอยู่บนเส้นทาง

📈 แนวโน้ม : ดีขึ้นจากเดือนก่อน +2
""")


st.caption(
    "วัดว่าพอร์ตและการตัดสินใจของคุณสอดคล้องกับเป้าหมายมากแค่ไหน"
)

st.divider()

st.subheader("🎯 เป้าหมายหลัก")

st.progress(62)

st.success("""
เกษียณอายุ 60 ปี

เหลืออีก 7 ปี

ความคืบหน้า 62%
""")

st.divider()

st.subheader("💌 ข้อความจากเฮอร์บี้")

st.info("""
คุณไม่ได้ลงทุนเพื่อดูราคาหุ้นทุกวัน

คุณลงทุนเพื่ออิสรภาพในอีก 7 ปีข้างหน้า
""")
