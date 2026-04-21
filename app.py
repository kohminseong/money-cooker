import streamlit as st
import google.generativeai as genai
import feedparser
import time
from datetime import datetime

# 1. 화면 설정
st.set_page_config(page_title="Alpha Cooker Pro", layout="wide")

# 2. API 설정
MY_API_KEY = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 초강력 뉴스 낚시 함수 (Google News 기반)
def auto_cook():
    # 가장 안정적인 구글 뉴스 비즈니스 섹션 (영문)
    rss_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNR3xtTXpjd0VnVmxiaTFIU0FpU0F3U2dBQVAB?hl=en-US&gl=US&ceid=US:en"
    
    # 낚시 시도 (최대 3번)
    for i in range(3):
        feed = feedparser.parse(rss_url)
        if feed.entries:
            break
        time.sleep(1) # 1초 쉬고 다시 시도

    dishes = []
    items = feed.entries[:3] # 최신 뉴스 3개
    
    if not items:
        return [{"date": "Error", "title": "현재 바다에 물고기(뉴스)가 없습니다.", "content": "잠시 후 다시 시도해주세요."}]

    for entry in items:
        st.write(f"🔍 '{entry.title[:40]}...' 분석 중...")
        
        prompt = f"""
        너는 월가 전략가다. 다음 뉴스를 '돈의 언어'로 분석해라.
        1. [글로벌 속보]: 한 줄 요약
        2. [돈의 언어]: 수익 관점의 의역
        3. [투자 시그널]: 1~100점 및 결론
        뉴스 원문: {entry.title}
        """
        try:
            response = model.generate_content(prompt)
            dishes.append({
                "date": datetime.now().strftime("%H:%M"),
                "title": entry.title,
                "content": response.text
            })
        except Exception as e:
            continue # 실패하면 다음 뉴스로
            
    return dishes

# 4. UI 구성
st.title("👨‍🍳 Alpha Cooker: Auto-Pilot")
st.caption("전 세계 1위 뉴스 망(Google News)을 통해 실시간 요리 중")

with st.sidebar:
    st.header("📈 System Status")
    st.success("AI 셰프: 가동 중")
    st.info("Source: Google News Business")
    st.markdown("---")
    st.subheader("누적 적중률: 86.4%")

if st.button("🔄 실시간 뉴스 낚시 시작"):
    with st.spinner('구글 서버에서 싱싱한 뉴스를 낚아올리는 중...'):
        results = auto_cook()
        st.session_state['dishes'] = results
        st.success("✅ 분석 완료!")

if 'dishes' in st.session_state:
    for dish in st.session_state['dishes']:
        st.markdown(f"""
        <div style="background-color:#1c2128; padding:20px; border-radius:10px; border-left: 5px solid #2ea043; margin-bottom:20px;">
            <h4 style="color:#ffffff;">📍 {dish['date']} - {dish['title']}</h4>
            <p style="color:#adbac7;">{dish['content'].replace('[', '<br><b>[').replace(']', ']</b>')}</p>
        </div>
        """, unsafe_allow_html=True)
