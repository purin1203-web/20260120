import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="나의 꽃, 나의 전공 찾기",
    page_icon="🌸",
    layout="centered"
)

# 2. 감성적인 UI를 위한 커스텀 CSS (덕성 버건디 & 파스텔 무드)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #fff 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 타이틀 스타일 */
    h1 {
        color: #8E1B3E; /* 덕성 버건디 */
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 카드 디자인 */
    .question-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(142, 27, 62, 0.1);
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 60px;
        background-color: white;
        color: #555;
        border: 2px solid #FFD1DC;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FFD1DC;
        color: #8E1B3E;
        border-color: #8E1B3E;
        transform: translateY(-2px);
    }

    /* 결과 카드 스타일 */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
        border-left: 8px solid #8E1B3E;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .rank-badge {
        background-color: #8E1B3E;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (덕성여대 단과대 및 전공 분류 기반 재구성)
# 실제 로직을 위해 성향(key)을 매핑합니다.
majors_db = {
    "HUMAN": {
        "name": "인문과학 & 글로벌융합",
        "majors": ["국어국문학전공", "영어영문학전공", "문헌정보학전공", "사학전공"],
        "careers": ["작가/에디터", "기록물 관리 전문가", "문화재 전문가", "글로벌 마케터"],
        "desc": "언어와 문화를 통해 세상의 깊이를 이해하는 당신에게 추천해요. 📚"
    },
    "SOCIAL": {
        "name": "사회과학 & 심리",
        "majors": ["심리학전공", "사회학전공", "아동가족학전공", "사회복지학전공"],
        "careers": ["임상심리사", "데이터 분석가(사회조사)", "가족 상담 전문가", "NGO 활동가"],
        "desc": "사람의 마음과 사회 현상에 따뜻한 관심을 가진 당신에게 딱이에요. 🤝"
    },
    "BIZ": {
        "name": "경영 & 국제통상",
        "majors": ["경영학전공", "국제통상학전공", "회계학전공"],
        "careers": ["기업 경영 컨설턴트", "공인회계사(CPA)", "무역 전문가", "금융권 종사자"],
        "desc": "세상의 흐름을 읽고 실용적인 가치를 창출하는 리더형 인재시군요! 💼"
    },
    "TECH": {
        "name": "과학기술 & IT",
        "majors": ["컴퓨터공학전공", "IT미디어공학전공", "사이버보안전공", "바이오공학전공"],
        "careers": ["풀스택 개발자", "정보보안 전문가", "바이오 연구원", "UX/UI 엔지니어"],
        "desc": "논리적인 사고로 미래를 코딩하는 당신, 기술의 최전선이 어울려요. 💻"
    },
    "ART": {
        "name": "Art & Design",
        "majors": ["동양화과", "서양화과", "실내디자인과", "시각디자인과", "텍스타일디자인과"],
        "careers": ["일러스트레이터", "공간 디자이너", "브랜드 디자이너", "큐레이터"],
        "desc": "남다른 감각으로 세상을 아름답게 채우는 예술가적 기질이 보여요. 🎨"
    }
}

# 4. 세션 상태 초기화 (점수 저장용)
if 'scores' not in st.session_state:
    st.session_state.scores = {"HUMAN": 0, "SOCIAL": 0, "BIZ": 0, "TECH": 0, "ART": 0}
if 'step' not in st.session_state:
    st.session_state.step = 0

# 5. 질문 리스트 (간소화된 알고리즘)
questions = [
    {
        "q": "Q1. 주말 오후, 나에게 가장 힐링이 되는 시간은?",
        "a": [
            ("좋아하는 소설책을 읽거나 다이어리 꾸미기", "HUMAN"),
            ("친구의 고민을 들어주고 조언해주기", "SOCIAL"),
            ("새로 나온 앱이나 IT 기기 리뷰 영상 보기", "TECH"),
            ("전시회를 가거나 예쁜 카페 사진 보정하기", "ART")
        ]
    },
    {
        "q": "Q2. 조별 과제에서 내가 가장 선호하는 역할은?",
        "a": [
            ("자료를 조사하고 보고서를 매끄럽게 정리하기", "HUMAN"),
            ("팀원들의 의견을 조율하고 분위기 띄우기", "SOCIAL"),
            ("PPT를 만들거나 발표 자료 시각화하기", "ART"),
            ("일정을 관리하고 효율적인 방향 제시하기", "BIZ")
        ]
    },
    {
        "q": "Q3. 내가 생각하는 '멋진 커리어 우먼'의 모습은?",
        "a": [
            ("글로벌 기업에서 프로젝트를 리딩하는 CEO", "BIZ"),
            ("세상을 바꾸는 기술을 개발하는 엔지니어", "TECH"),
            ("사람들의 아픔을 치유해주는 전문가", "SOCIAL"),
            ("나만의 브랜드나 작품을 세상에 알리는 아티스트", "ART")
        ]
    },
    {
        "q": "Q4. 요즘 뉴스에서 가장 관심 가는 키워드는?",
        "a": [
            ("인공지능, 챗GPT, 신약 개발", "TECH"),
            ("경제 동향, 주식, 환율", "BIZ"),
            ("사회적 이슈, 인권, 복지 정책", "SOCIAL"),
            ("문학상 수상작, 베스트셀러, 역사", "HUMAN")
        ]
    },
    {
        "q": "Q5. 대학 생활 4년 동안 꼭 해보고 싶은 것은?",
        "a": [
            ("교환학생 가서 다양한 문화 체험하기", "HUMAN"),
            ("창업 동아리에서 내 아이디어 실현하기", "BIZ"),
            ("코딩 부트캠프나 실험실 인턴 참여하기", "TECH"),
            ("졸업 전시회나 공모전에서 수상하기", "ART")
        ]
    }
]

# 함수: 답변 선택 시 점수 계산 및 다음 단계 이동
def next_step(type_key):
    st.session_state.scores[type_key] += 1
    st.session_state.step += 1

# --- 메인 화면 로직 ---

# 1) 시작 화면
if st.session_state.step == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1>🌸 덕성, 너의 꿈이 피어나는 곳 🌸</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='question-card'>
            <p style='font-size: 1.2em; color: #555;'>
                반가워요, 25학번 새내기 여러분! 👋<br>
                아직 전공 선택이 고민되시나요?<br><br>
                몇 가지 간단한 질문을 통해<br>
                <b>나에게 가장 잘 어울리는 전공</b>을 찾아드릴게요.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    if st.button("내 전공 찾기 시작하기 ✨"):
        st.session_state.step = 1
        st.rerun()

# 2) 질문 진행 화면
elif st.session_state.step <= len(questions):
    q_idx = st.session_state.step - 1
    cur_q = questions[q_idx]

    # 진행바
    progress = q_idx / len(questions)
    st.progress(progress)
    
    st.markdown(f"<div class='question-card'><h3>{cur_q['q']}</h3></div>", unsafe_allow_html=True)

    # 답변 버튼들
    for answer_text, type_key in cur_q['a']:
        if st.button(answer_text):
            next_step(type_key)
            st.rerun()

# 3) 결과 화면
else:
    st.balloons() # 축하 효과
    st.markdown("<h1>🎉 당신을 위한 전공 레시피 🎉</h1>", unsafe_allow_html=True)
    
    # 점수 정렬 (높은 순)
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3] # 상위 3개 추출

    st.write("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-bottom: 20px;'>
            덕성에서의 4년이 가장 빛날 수 있도록,<br>
            AI가 분석한 <b>최적의 전공 TOP 3</b>를 소개합니다.
        </div>
        """, unsafe_allow_html=True
    )

    # 순위별 출력
    ranks = ["🥇 1순위 추천", "🥈 2순위 추천", "🥉 3순위 추천"]
    
    for i, (m_key, score) in enumerate(top_3):
        data = majors_db[m_key]
        
        # 1순위는 조금 더 강조
        border_color = "#8E1B3E" if i == 0 else "#ddd"
        bg_color = "#fff0f5" if i == 0 else "white"
        
        st.markdown(f"""
            <div class="result-card" style="border-left: 8px solid {border_color}; background-color: {bg_color};">
                <span class="rank-badge">{ranks[i]}</span>
                <h2 style="color: #333; margin-top: 10px;">{data['name']}</h2>
                <p style="font-size: 1.1em;">{data['desc']}</p>
                <hr style="border-top: 1px dashed #bbb;">
                <p><b>🎓 관련 전공:</b> {', '.join(data['majors'])}</p>
                <p><b>💼 추천 진로:</b> {', '.join(data['careers'])}</p>
            </div>
        """, unsafe_allow_html=True)

    # 다시하기 버튼
    st.write("")
    if st.button("🔄 테스트 다시 하기"):
        st.session_state.scores = {k:0 for k in st.session_state.scores}
        st.session_state.step = 0
        st.rerun()
