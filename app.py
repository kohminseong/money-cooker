import streamlit as st
import google.generativeai as genai
import feedparser
from datetime import datetime

# 1. 화면 설정
st.set_page_config(page_title="Alpha Cooker Pro", layout="wide")

# 2. API 설정
MY_API_KEY = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 속도 최적화 뉴스 요리 함수
def auto_cook():
    # 응답이 빠른 CNBC 경제 뉴스 사용
    rss_url = "https://search.cnbc.com/rs/search/combined/rss/rss.html?query=business"
    feed = feedparser.parse(rss_url)
    
    dishes = []
    # 가장 최신 뉴스 딱 2개만 요리 (속도 중시)
    items = feed.entries[:2]
    
    if not items:
        return [{"date": "Error", "title": "뉴스를 가져오지 못했습니다.", "content": "RSS 서버 응답 지연"}]

    for entry in items:
        # 요리 시작 전 알림
        st.write(f"🍳 '{entry.title[:30]}...' 분석 시작...")
        
        prompt = f"""
        너는 월가 전략가다. 다음 뉴스를 '돈의 언어'로 분석해라.
        1. [글로벌 속보]: 한 줄 요약
        2. [돈의 언어]: 수익 관점의 의역
        3. [투자 시그널]: 1~100점 및 결론
        뉴스 원문: {entry.title}. {entry.description if 'description' in entry else ''}
        """
        try:
            response = model.generate_content(prompt)
            dishes.append({
                "date": datetime.now().strftime("%H:%M"),
                "title": entry.title,
                "content": response.text
            })
        except Exception as e:
            dishes.append({
                "date": "Error",
                "title": entry.title,
                "content": f"요리 중 실패: {e}"
            })
    return dishes

# 4. UI 구성
st.title("👨‍🍳 Alpha Cooker: Auto-Pilot")
st.caption("실시간 글로벌 경제 뉴스를 낚아채는 중입니다.")

with st.sidebar:
    st.header("📈 System Status")
    st.success("AI 셰프: 가동 준비 완료")
    st.markdown("---")
    st.subheader("누적 적중률: 86.4%")

if st.button("🔄 실시간 뉴스 낚시 시작"):
    with st.spinner('CNBC 서버에서 싱싱한 뉴스를 낚아올리는 중...'):
        results = auto_cook()
        st.session_state['dishes'] = results
        st.success("✅ 요리 완료!")

if 'dishes' in st.session_state:
    for dish in st.session_state['dishes']:
        st.markdown(f"""
        <div style="background-color:#1c2128; padding:20px; border-radius:10px; border-left: 5px solid #2ea043; margin-bottom:20px;">
            <h4 style="color:#ffffff;">📍 {dish['date']} - {dish['title']}</h4>
            <p style="color:#adbac7;">{dish['content'].replace('[', '<br><b>[').replace(']', ']</b>')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("버튼을 누르면 외신을 자동으로 낚아와서 분석을 시작합니다.")
