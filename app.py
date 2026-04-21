import streamlit as st
import google.generativeai as genai

# 웹사이트 제목 및 설정
st.set_page_config(page_title="Alpha Cooker", layout="wide")
st.title("👨‍🍳 Alpha Cooker: 돈의 언어 번역기")
st.caption("통대생의 직관과 Gemini API가 결합된 초고속 뉴스 요리사")

# API 키 입력
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 모델 명칭을 가장 표준적인 것으로 변경
        model = genai.GenerativeModel('gemini-pro')

        # 사용자 입력창
        raw_text = st.text_area("영어 뉴스 원문을 붙여넣으세요:", height=200)

        if st.button("돈의 언어로 요리하기"):
            prompt = f"""
            너는 통대 출신 언어 분석가이자 월스트리트 투자 전략가다. 
            다음 뉴스를 읽고 '돈의 언어'로 재해석해라.
            
            1. [글로벌 속보]: 한국어 한 줄 요약
            2. [돈의 언어]: 전문 용어 배제, 시장 수익 관점의 의역
            3. [언어적 뉘앙스]: 화자의 숨은 의도와 단어 선택의 날카로움 분석
            4. [투자 시그널]: 1~100점 점수 및 [매수/매도/관망] 결론
            
            뉴스 원문: {raw_text}
            """
            
            with st.spinner('요리 중...'):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader("🍳 오늘의 요리 결과")
                st.write(response.text)
    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 API Key를 입력하면 가동이 시작됩니다.")
