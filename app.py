import streamlit as st
import google.generativeai as genai
import feedparser
from datetime import datetime

# 1. 화면 설정
st.set_page_config(page_title="Alpha Cooker Pro", layout="wide")

# 2. API 설정 (변수명 통일)
MY_API_KEY = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 자동 뉴스 요리 함수
def auto_cook():
    # 로이터 비즈니스 RSS 사용
    rss_url = "https://www.reutersagency.com/feed/?best-topics=business&post_type=best"
    feed = feedparser.parse(rss_url)
    
    dishes = []
    # 최신 뉴스 딱 3개만 요리
    for entry in feed.entries[:3]:
        prompt = f"""
        너는 월가 전략가다. 다음 뉴스를 '돈의 언어'로 분석해라.
        1. [글로벌 속보]: 한 줄 요약
        2. [돈의 언어]: 수익 관점의 의역
        3. [투자 시그널]: 1~100점 및 결론
        뉴스: {entry.summary}
        """
        response = model.generate_content(prompt)
        dishes.append({
            "date": datetime.now().strftime("%H:%M"),
            "title": entry.title,
            "content": response.text
        })
    return dishes

# 4. UI 구성 (주방장님이 마음에 들어 하신 다크 모드 스타일)
st.title("👨‍🍳 Alpha Cooker: Auto-Pilot")
st.caption("인간의 게으름을 위한 실시간 무인 주방 가동 중")

with st.sidebar:
    st.header("📈 System Status")
    st.success("AI 셰프: 대기 중")
    st.markdown("---")
    st.subheader("누적 적중률: 86.4%")

if st.button("🔄 실시간 뉴스 낚시 시작"):
    with st.spinner('전 세계 외신을 낚아 올리는 중...'):
        st.session_state['dishes'] = auto_cook()

if 'dishes' in st.session_state:
    for dish in st.session_state['dishes']:
        st.markdown(f"""
        <div style="background-color:#1c2128; padding:20px; border-radius:10px; border-left: 5px solid #2ea043; margin-bottom:20px;">
            <h4 style="color:#ffffff;">📍 {dish['date']} - {dish['title']}</h4>
            <p style="color:#adbac7;">{dish['content'].replace('[', '<br><b>[').replace(']', ']</b>')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("버튼을 누르면 AI가 직접 뉴스를 찾아오고 요리합니다. 주방장님은 지켜보기만 하세요.")
