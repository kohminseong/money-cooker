import streamlit as st
import google.generativeai as genai

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="Alpha Cooker", layout="wide")

# 2. 보안 설정: Streamlit Secrets에서 API 키를 자동으로 가져옴
try:
    # Streamlit 관리자 페이지의 Secrets 항목에 GEMINI_API_KEY가 저장되어 있어야 합니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 가장 빠르고 안정적인 최신 모델 선택
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("⚠️ API 키 설정 오류: Streamlit Cloud 설정(Secrets)에서 GEMINI_API_KEY를 확인하세요.")
    st.stop()

# 3. 화면 UI 구성
st.title("👨‍🍳 Alpha Cooker: 돈의 언어 번역기")
st.caption("통대생의 직관과 Gemini API가 결합된 초고속 뉴스 분석 엔진")
st.markdown("---")

# 4. 입력창 (사이드바가 아닌 메인 화면에 크게 배치)
raw_text = st.text_area("📢 분석할 영어 뉴스 원문을 여기에 붙여넣으세요:", height=250, placeholder="영문 경제 뉴스나 트윗을 입력하세요...")

# 5. 실행 버튼 및 로직
if st.button("🚀 돈의 언어로 요리하기"):
    if not raw_text:
        st.warning("분석할 텍스트를 입력해주세요.")
    else:
        # 통대생의 페르소나를 주입한 마스터 프롬프트
        prompt = f"""
        너는 통대 출신 언어 분석가이자 월스트리트 투자 전략가다. 
        다음 뉴스를 읽고 '돈의 언어'로 재해석해라. 
        단순 번역이 아니라, 이 정보가 시장의 '돈'을 어디로 움직일지 분석하는 것이 목적이다.

        출력 양식:
        1. [글로벌 속보]: 한국어 한 줄 핵심 요약
        2. [돈의 언어]: 전문 용어를 걷어내고, 수익 관점에서 이 뉴스가 시장에 던지는 진짜 의미
        3. [언어적 뉘앙스]: 화자의 단어 선택(확신, 회피, 경고 등)에 담긴 숨은 의도 분석
        4. [투자 시그널]: 1~100점 사이의 점수와 [매수/매도/관망] 결론

        뉴스 원문:
        {raw_text}
        """
        
        # 실제 요리(분석) 시작
        with st.spinner('🎯 전 세계 데이터를 기반으로 요리 중...'):
            try:
                response = model.generate_content(prompt)
                st.success("✅ 분석 완료!")
                st.markdown("---")
                st.subheader("🍳 오늘의 요리 결과")
                # 결과 출력
                st.write(response.text)
            except Exception as e:
                st.error(f"요리 중 오류가 발생했습니다. 원인: {e}")

# 6. 하단 푸터
st.markdown("---")
st.caption("© 2026 Alpha Cooker - 통대생의 문해력으로 시장을 읽습니다.")
