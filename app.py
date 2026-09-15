# HERBY_V0_9_FULL_APP.py
# Full Pack Prototype based on V0.8 + V0.9 Scope
import streamlit as st, json, os
from datetime import datetime

st.set_page_config(page_title="Herby V0.9 Full", page_icon="💚", layout="centered")
DB='herby_profiles.json'

AGE_OPTIONS=["18-24 ปี","25-34 ปี","35-44 ปี","45-54 ปี","55 ปีขึ้นไป"]
GOAL_OPTIONS=["เกษียณ","อิสรภาพทางการเงิน","สร้างความมั่งคั่งระยะยาว","ซื้อบ้าน","การศึกษาบุตร","อื่น ๆ"]
TIMELINE_OPTIONS=["น้อยกว่า 3 ปี","3-5 ปี","5-10 ปี","10-20 ปี","มากกว่า 20 ปี"]
EXPERIENCE_OPTIONS=["ยังไม่เคยลงทุน","น้อยกว่า 1 ปี","1-3 ปี","3-10 ปี","มากกว่า 10 ปี"]
ASSET_OPTIONS=["เงินฝาก","พันธบัตร","ตราสารหนี้","กองทุนรวม","RMF / SSF","REIT","ทองคำ","ETF","หุ้นไทย","หุ้นต่างประเทศ","Bitcoin","Cryptocurrency","ยังไม่แน่ใจ"]
BEHAVIOR_OPTIONS=["ขายออกทั้งหมดทันที","ขายบางส่วนเพื่อลดความเสี่ยง","ยังถือไว้ แม้จะไม่สบายใจ","ถือไว้ เพราะมองว่าเป็นเรื่องปกติของการลงทุน","ซื้อเพิ่ม เพราะมองว่าเป็นโอกาส"]

for k,v in {'page':'home','user':None}.items(): st.session_state.setdefault(k,v)

def load_db():
    if not os.path.exists(DB): return {}
    with open(DB,'r',encoding='utf-8') as f: return json.load(f)

def save_db(d):
    with open(DB,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

def analyze(a):
    obs=[]
    if a['goal'] in ['อิสรภาพทางการเงิน','สร้างความมั่งคั่งระยะยาว'] and a['timeline'] in ['น้อยกว่า 3 ปี','3-5 ปี']:
        obs.append('เป้าหมายต้องการการเติบโต แต่มีกรอบเวลาค่อนข้างสั้น')
    if a['vol']<=3 and 'ซื้อเพิ่ม' in a['behavior']:
        obs.append('ระดับความผันผวนต่ำ แต่คาดว่าจะซื้อเพิ่มเมื่อพอร์ตลดลง')
    if a['vol']>=7 and 'ขาย' in a['behavior']:
        obs.append('รับความผันผวนสูง แต่คาดว่าจะลดความเสี่ยงเมื่อเกิดแรงกดดัน')

    if len(obs)>=2:
        style='🧭 ผู้กำลังค้นหาจุดสมดุล'
    elif a['vol']<=3:
        style='🛡️ ผู้รักษาความมั่นคง'
    elif a['vol']>=7:
        style='📈 ผู้สร้างการเติบโตอย่างมีวินัย'
    else:
        style='⚖️ ผู้แสวงหาสมดุล'

    return {
      'assessment_date':datetime.now().strftime('%Y-%m-%d'),
      'style':style,
      'learning_stage':a['experience'],
      'observations':obs,
      'insight':'Herby กำลังช่วยให้คุณเข้าใจความต้องการ ความกังวล และความพร้อมรับความเสี่ยงของตัวเอง'
    }

profiles=load_db()

if st.session_state.page=='home':
    st.title('💚 Herby V0.9 Full')
    if st.button('💚 ฉันเป็นผู้ใช้ใหม่',use_container_width=True): st.session_state.page='register'; st.rerun()
    if st.button('💚 ฉันเคยทำแบบประเมินแล้ว',use_container_width=True): st.session_state.page='login'; st.rerun()

elif st.session_state.page=='register':
    st.header('Registration')
    n=st.text_input('Nickname')
    p=st.text_input('PIN 4 หลัก',type='password',max_chars=4)
    if st.button('💚 ตรวจสอบและสร้างโปรไฟล์'):
        if n in profiles: st.error('❌ ชื่อนี้ถูกใช้งานแล้ว')
        elif not (p.isdigit() and len(p)==4): st.error('PIN ต้องมี 4 หลัก')
        else:
            profiles[n]={'pin':p,'history':[]}
            save_db(profiles)
            st.session_state.user=n
            st.session_state.page='questionnaire'
            st.rerun()

elif st.session_state.page=='login':
    n=st.text_input('Nickname')
    p=st.text_input('PIN 4 หลัก',type='password')
    if st.button('💚 Login'):
        if n in profiles and profiles[n]['pin']==p:
            st.session_state.user=n
            st.session_state.page='dashboard'
            st.rerun()
        else: st.error('ข้อมูลไม่ถูกต้อง')

elif st.session_state.page=='questionnaire':
    st.header('🌱 Investment Self Discovery')
    with st.form('form'):
        age=st.selectbox('อายุ',AGE_OPTIONS)
        goal=st.selectbox('เป้าหมาย',GOAL_OPTIONS)
        timeline=st.selectbox('ระยะเวลา',TIMELINE_OPTIONS)
        exp=st.selectbox('ประสบการณ์',EXPERIENCE_OPTIONS)
        assets=st.multiselect('สินทรัพย์',ASSET_OPTIONS)
        behavior=st.radio('หากคุณลงทุน 1,000,000 บาท และวันถัดมาพอร์ตเหลือ 700,000 บาท คุณจะทำอย่างไร?',BEHAVIOR_OPTIONS)
        vol=st.slider('ระดับความผันผวนที่คิดว่ารับได้',1,10,5)
        submit=st.form_submit_button('💚 วิเคราะห์')
    if submit:
        res=analyze({'goal':goal,'timeline':timeline,'experience':exp,'behavior':behavior,'vol':vol})
        profiles=load_db()
        profiles[st.session_state.user]['last']=res
        profiles[st.session_state.user]['history'].append(res)
        save_db(profiles)
        st.session_state.page='about'
        st.rerun()

elif st.session_state.page=='about':
    st.header('❤️ ทำไม Herby ถึงถามคำถามเหล่านี้?')
    st.write('Herby ไม่ได้พยายามตัดสินคุณ และไม่ได้ถามเพื่อหาคำตอบว่าถูกหรือผิด')
    st.write('ก่อนถามว่าควรลงทุนอะไร ต้องถามก่อนว่าคนที่จะลงทุนคือใคร')
    st.write('Founder เคยเป็นนักลงทุนประเภท ใครบอกว่าดี...ซื้อ 🤣 ใครบอกว่ากำลังมา...ซื้อ 🤣')
    if st.button('💚 เข้า Dashboard'): st.session_state.page='dashboard'; st.rerun()

elif st.session_state.page=='dashboard':
    data=profiles.get(st.session_state.user,{})
    last=data.get('last',{})
    st.title('💚 Dashboard')
    st.subheader(f'สวัสดี {st.session_state.user} 👋')
    st.success('Herby จำคุณได้')
    st.write('📅 ประเมินล่าสุด:',last.get('assessment_date','-'))
    st.write('📈 สไตล์ล่าสุด:',last.get('style','-'))
    st.write('🌱 Learning Stage:',last.get('learning_stage','-'))
    if last:
        st.markdown('### 🔎 สิ่งที่ Herby สังเกตเห็น')
        for o in last.get('observations',[]): st.info(o)
        st.markdown('### 🌟 What Herby Learned About You')
        st.write(last.get('insight',''))
    st.markdown('### 📚 ประวัติการประเมิน')
    for i,h in enumerate(data.get('history',[]),1):
        st.write(f'{i}. {h.get("assessment_date")} - {h.get("style")}')
