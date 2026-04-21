import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Alpha Cooker", layout="wide")
st.title("👨‍🍳 Alpha Cooker: 최종 가동 엔진")

# [중요] 새로 발급받은 키를 여기에 넣으세요
api_key = "AIzaSyADT31nruQgmiCQuc6rihvYxsl22Kygo1c" 

try:
    genai.configure(api_key=api_key)
    
    # 서버가 허용하는 모델 목록을 직접 확인
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        st.error("이 API 키로 사용할 수 있는 모델이 없습니다. AI Studio에서 설정을 확인하세요.")
    else:
        # 사용 가능한 모델 중 첫 번째 것을 자동으로 선택 (예: models/gemini-1.5-flash)
        target_model = available_models[0]
        model = genai.GenerativeModel(target_model)
        
        st.success(f"✅ 연결 성공! 현재 사용 모델: {target_model}")
        
        raw_text = st.text_area("영어 뉴스 원문을 붙여넣으세요:", height=200)
        
        if st.button("🚀 돈의 언어로 요리하기"):
            prompt = f"너는 월가 투자 전문가다. 다음 뉴스를 '돈의 언어'로 한국어로 분석해줘: {raw_text}"
            with st.spinner('분석 중...'):
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"분석 실패: {e}")
except Exception as e:
    st.error(f"서버 접속 자체에 실패했습니다: {e}")
