import streamlit as st      st.successnfig(
    page_title="Herby",
    page_icon="❤️",
    layout="wide"
)

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
    st.success("ยินดีต้อนรับ 😊")
