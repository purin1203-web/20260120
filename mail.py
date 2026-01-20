import streamlit as st
import pandas as pd

# 1. 페이지 설정 (아이콘, 타이틀)
st.set_page_config(page_title="MBTI 커리어 탐색기", page_icon="🚀", layout="centered")

# 2. 커스텀 CSS (화려한 UI 디자인)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #ffefba, #ffffff);
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #FF7070;
        color: white;
    }
    .mbti-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
        border-left: 10px solid #FF4B4B;
        margin-bottom: 20px;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MBTI 데이터 정의
mbti_data = {
    "ISTJ": {"job": "회계사, 공무원, 사서", "desc": "신중하고 철저하며 책임감이 강합니다. 💼", "color": "#A1A1A1"},
    "ISFJ": {"job": "간호사, 교사, 사회복지사", "desc": "타인을 돕는 것을 좋아하고 헌신적입니다. 🏥", "color": "#77DD77"},
    "INFJ": {"job": "작가, 심리상담사, 예술가", "desc": "통찰력이 뛰어나고 이상주의적입니다. ✍️", "color": "#B19CD9"},
    "INTJ": {"job": "전략가, 분석가, 연구원", "desc": "분석적이고 독립적인 문제 해결사입니다. 🔬", "color": "#779ECB"},
    "ISTP": {"job": "엔지니어, 운동선수, 조종사", "desc": "도구와 기계 조작에 능숙하고 냉철합니다. 🛠️", "color": "#FFB347"},
    "ISFP": {"job": "디자이너, 작곡가, 요리사", "desc": "예술적 감각이 뛰어나고 따뜻합니다. 🎨", "color": "#FFDAC1"},
    "INFP": {"job": "소설가, 시인, NGO 활동가", "desc": "창의적이고 가치 중심적인 삶을 지향합니다. 🧚", "color": "#CFCFCF"},
    "INTP": {"job": "프로그래머, 철학자, 물리학자", "desc": "논리적이고 지적 호기심이 매우 높습니다. 💻", "color": "#B39EB5"},
    "ESTP": {"job": "영업직, 기업가, 경찰관", "desc": "적응력이 빠르고 에너지가 넘칩니다. ⚡", "color": "#FF6961"},
    "ESFP": {"job": "연예인, 여행 가이드, 마케터", "desc": "사교적이며 현재의 즐거움을 중시합니다. 🎭", "color": "#FDFD96"},
    "ENFP": {"job": "홍보 전문가, 크리에이터, 상담가", "desc": "열정적이고 창의적인 아이디어가 많습니다. 🌟", "color": "#FFD1DC"},
    "ENTP": {"job": "발명가, 변호사, 컨설턴트", "desc": "토론을 즐기며 새로운 도전을 좋아합니다. 💡", "color": "#AEC6CF"},
    "ESTJ": {"job": "경영자, 프로젝트 매니저, 군인", "desc": "조직적이고 실무적인 능력이 뛰어납니다. 📋", "color": "#DEA5A4"},
    "ESFJ": {"job": "인사 담당자, 승무원, 초등교사", "desc": "친절하고 협조적이며 동료애가 강합니다. 🍎", "color": "#CB99C9"},
    "ENFJ": {"job": "정치인, 코치, 외교관", "desc": "타인을 성장시키고 이끄는 리더십이 있습니다. 🎤", "color": "#F49AC2"},
    "ENTJ": {"job": "CEO, 정치인, 경영 컨설턴트", "desc": "비전이 뚜렷하며 추진력이 대단합니다. 🏆", "color": "#FFB7CE"}
}

# 4. 메인 화면 구성
st.markdown("<h1>✨ MBTI 맞춤형 커리어 탐색기 ✨</h1>", unsafe_allow_html=True)
st.write("---")

st.markdown("### 🔍 당신의 MBTI는 무엇인가요?")
mbti_choice = st.selectbox("리스트에서 선택해 주세요 👇", list(mbti_data.keys()))

if st.button("내 직업 추천 확인하기! 🚀"):
    st.balloons()  # 화려한 풍선 효과
    
    # 결과 출력
    result = mbti_data[mbti_choice]
    
    st.markdown(f"""
        <div class="mbti-card">
            <h2 style='color: #FF4B4B;'>🌟 {mbti_choice}를 위한 추천</h2>
            <p style='font-size: 1.2em;'><b>특징:</b> {result['desc']}</p>
            <hr>
            <p style='font-size: 1.5em;'><b>🎯 추천 직업:</b> <span style='color: #007BFF;'>{result['job']}</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    # 추가 팁
    st.info(f"💡 {mbti_choice} 유형은 자신의 강점을 살릴 수 있는 환경에서 가장 빛이 납니다!")

# 5. 하단 푸터
st.write("---")
st.caption("🌈 본 프로그램은 교육용이며 성격 유형에 따른 일반적인 경향성을 나타냅니다.")
