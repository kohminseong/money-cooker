import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="Alpha Cooker", layout="wide")

# 2. API 설정 (보안 주의: 작동 확인 후 나중에 Secrets로 옮기세요)
api_key = "AIzaSyDlmb6HwSedIEPQX-lQcSTrSFrSqM9bRE8"
genai.configure(api_key=api_key)

# 3. 화면 UI
st.title("👨‍🍳 Alpha Cooker: 돈의 언어 번역기")
st.caption("통대생의 직관과 Gemini API가 결합된 초고속 뉴스 분석 엔진")
st.markdown("---")

raw_text = st.text_area("📢 분석할 영어 뉴스 원문을 여기에 붙여넣으세요:", height=250)

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
            # [2026 최신 패치] 가장 인식률이 높은 모델 명칭 시도 순서
            success = False
            for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
                try:
                    # 'models/'를 생략하고 이름만 넣는 방식이 최신 표준입니다.
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    
                    st.success(f"✅ 분석 완료! (사용한 모델: {model_name})")
                    st.markdown("---")
                    st.write(response.text)
                    success = True
                    break # 성공하면 멈춤
                except Exception:
                    continue # 실패하면 다음 모델로
            
            if not success:
                st.error("구글 API 서버에서 모델을 찾을 수 없습니다. API 키의 활성화 상태나 권한을 확인해주세요.")

st.markdown("---")
st.caption("© 2026 Alpha Cooker")
