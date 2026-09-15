# HERBY_V0_9_APP.py
import streamlit as st, json, os
from datetime import datetime
st.set_page_config(page_title='Herby V0.9',page_icon='💚',layout='centered')
PROFILE_DB='herby_profiles.json'
AGE_OPTIONS=['18-24 ปี','25-34 ปี','35-44 ปี','45-54 ปี','55 ปีขึ้นไป']
GOAL_OPTIONS=['เกษียณ','อิสรภาพทางการเงิน','สร้างความมั่งคั่งระยะยาว','ซื้อบ้าน','การศึกษาบุตร','อื่น ๆ']
TIMELINE_OPTIONS=['น้อยกว่า 3 ปี','3-5 ปี','5-10 ปี','10-20 ปี','มากกว่า 20 ปี']
EXPERIENCE_OPTIONS=['ยังไม่เคยลงทุน','น้อยกว่า 1 ปี','1-3 ปี','3-10 ปี','มากกว่า 10 ปี']
ASSET_OPTIONS=['เงินฝาก','พันธบัตร','ตราสารหนี้','กองทุนรวม','RMF / SSF','REIT','ทองคำ','ETF','หุ้นไทย','หุ้นต่างประเทศ','Bitcoin','Cryptocurrency','ยังไม่แน่ใจ']
FEELING_OPTIONS=['กังวลมากและอยากขายออกทันที','กังวล แต่คงขายบางส่วน','ไม่สบายใจ แต่ยังถือไว้ได้','มองว่าเป็นเรื่องปกติของการลงทุน','มองว่าอาจเป็นโอกาสในการซื้อเพิ่ม']

def load_profiles():
    if not os.path.exists(PROFILE_DB): return {}
    return json.load(open(PROFILE_DB,'r',encoding='utf-8'))

def save_profiles(d):
    json.dump(d,open(PROFILE_DB,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

def analyze_answers(a):
    v=a['volatility']
    if a['experience'] in ['ยังไม่เคยลงทุน','น้อยกว่า 1 ปี'] and 'ยังไม่แน่ใจ' in a['assets']:
        style='🌱 ผู้เริ่มสำรวจโลกการลงทุน'; stage='Emerging Investor'
    elif v<=3:
        style='🛡️ ผู้รักษาความมั่นคง'; stage='Safety Focused'
    elif v>=7:
        style='📈 ผู้สร้างการเติบโตอย่างมีวินัย'; stage='Growth Focused'
    else:
        style='⚖️ ผู้แสวงหาสมดุล'; stage='Developing Investor'
    return {'assessment_date':datetime.now().strftime('%Y-%m-%d'),'learning_stage':stage,'style':{'name':style}}

for k,v in {'page':'home','user':None}.items(): st.session_state.setdefault(k,v)
profiles=load_profiles()

if st.session_state.page=='home':
    st.title('💚 Herby V0.9')
    if st.button('💚 ฉันเป็นผู้ใช้ใหม่'): st.session_state.page='register'; st.rerun()
    if st.button('💚 ฉันเคยทำแบบประเมินแล้ว'): st.session_state.page='login'; st.rerun()
elif st.session_state.page=='register':
    n=st.text_input('Nickname'); p=st.text_input('PIN 4 หลัก',type='password',max_chars=4)
    if st.button('💚 ตรวจสอบและสร้างโปรไฟล์'):
        if n in profiles: st.error('❌ ชื่อนี้ถูกใช้งานแล้ว')
        elif len(p)!=4 or not p.isdigit(): st.error('PIN ต้องเป็นตัวเลข 4 หลัก')
        else:
            profiles[n]={'pin':p}; save_profiles(profiles); st.session_state.user=n; st.session_state.page='questionnaire'; st.rerun()
elif st.session_state.page=='login':
    n=st.text_input('Nickname'); p=st.text_input('PIN 4 หลัก',type='password',max_chars=4)
    if st.button('💚 เข้าใช้งาน'):
        if n in profiles and profiles[n]['pin']==p: st.session_state.user=n; st.session_state.page='dashboard'; st.rerun()
        else: st.error('ข้อมูลไม่ถูกต้อง')
elif st.session_state.page=='questionnaire':
    with st.form('q'):
        age=st.selectbox('อายุ',AGE_OPTIONS); goal=st.selectbox('เป้าหมาย',GOAL_OPTIONS)
        timeline=st.selectbox('ระยะเวลา',TIMELINE_OPTIONS); exp=st.selectbox('ประสบการณ์',EXPERIENCE_OPTIONS)
        assets=st.multiselect('สินทรัพย์',ASSET_OPTIONS); feel=st.radio('ลดลง 30%',FEELING_OPTIONS)
        vol=st.slider('ความผันผวน',1,10,5); sb=st.form_submit_button('💚 วิเคราะห์')
    if sb:
        profiles[st.session_state.user]['profile']=analyze_answers({'experience':exp,'assets':assets,'volatility':vol})
        save_profiles(profiles); st.session_state.page='about'; st.rerun()
elif st.session_state.page=='about':
    st.header('❤️ ทำไม Herby ถึงถามคำถามเหล่านี้?')
    st.write('Herby ไม่ได้พยายามตัดสินคุณ แต่กำลังทำความเข้าใจตัวคุณ')
    st.write('ก่อนถามว่าควรลงทุนอะไร ต้องถามก่อนว่าคนที่จะลงทุนคือใคร?')
    if st.button('💚 เข้า Dashboard'): st.session_state.page='dashboard'; st.rerun()
elif st.session_state.page=='dashboard':
    r=profiles.get(st.session_state.user,{}).get('profile',{})
    st.title('💚 Dashboard')
    st.write(f'สวัสดี {st.session_state.user} 👋')
    st.write('📅 ประเมินล่าสุด',r.get('assessment_date','-'))
    st.write('📈 สไตล์ล่าสุด',r.get('style',{}).get('name','-'))
    st.write('🌱 Learning Stage',r.get('learning_stage','-'))
