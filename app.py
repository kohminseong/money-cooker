import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="Alpha Cooker", layout="wide")

# 2. API 설정
api_key = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=api_key)

# [필살기] 가장 호환성이 높은 모델 명칭으로 설정
# 2026년 기준 가장 범용적인 명칭입니다.
MODEL_NAME = 'gemini-1.5-pro'

# 3. 화면 UI
st.title("👨‍🍳 Alpha Cooker: 돈의 언어 번역기")
st.caption("통대생의 직관과 Gemini API가 결합된 초고속 뉴스 분석 엔진")
st.markdown("---")

raw_text = st.text_area("📢 분석할 영어 뉴스 원문을 여기에 붙여넣으세요:", height=250)

if st.button("🚀 돈의 언어로 요리하기"):
    if not raw_text:
        st.warning("분석할 텍스트를 입력해주세요.")
    else:
        prompt = f"""
        너는 통대 출신 언어 분석가이자 월스트리트 투자 전략가다. 
        다음 뉴스를 읽고 '돈의 언어'로 재해석해라. 
        1. [글로벌 속보]: 한국어 한 줄 핵심 요약
        2. [돈의 언어]: 수익 관점의 의역
        3. [언어적 뉘앙스]: 화자의 숨은 의도 분석
        4. [투자 시그널]: 1~100점 점수 및 결론
        
        뉴스 원문: {raw_text}
        """
        
        with st.spinner('🎯 분석 중...'):
            try:
                # 모델 선언 방식을 가장 안전하게 변경
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(prompt)
                
                st.success("✅ 분석 완료!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # 에러 발생 시 다른 모델로 즉시 재시도 (백업 로직)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    st.success("✅ 분석 완료 (백업 모델 사용)")
                    st.write(response.text)
                except Exception as e2:
                    st.error(f"모든 모델 가동 실패. 원인: {e2}")

st.markdown("---")
st.caption("© 2026 Alpha Cooker")
