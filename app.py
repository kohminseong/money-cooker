import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="Alpha Cooker", layout="wide")

# 2. API 키 설정 (보안상 주의)
api_key = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=api_key)

# [핵심 수정] 모델 이름 앞에 'models/'를 명확히 붙였습니다.
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 3. 화면 UI 구성
st.title("👨‍🍳 Alpha Cooker: 돈의 언어 번역기")
st.caption("통대생의 직관과 Gemini API가 결합된 초고속 뉴스 분석 엔진")
st.markdown("---")

# 4. 입력창
raw_text = st.text_area("📢 분석할 영어 뉴스 원문을 여기에 붙여넣으세요:", height=250)

# 5. 실행 로직
if st.button("🚀 돈의 언어로 요리하기"):
    if not raw_text:
        st.warning("분석할 텍스트를 입력해주세요.")
    else:
        # 비즈니스 로직 프롬프트
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
                response = model.generate_content(prompt)
                st.success("✅ 분석 완료!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                # 상세 에러 메시지 출력
                st.error(f"요리 중 오류가 발생했습니다. 원인: {e}")

st.markdown("---")
st.caption("© 2026 Alpha Cooker")
