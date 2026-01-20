import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="덕새와 함께하는 전공 찾기",
    page_icon="🦆",
    layout="centered"
)

# 2. 감성적 UI + 덕새 활용을 위한 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 타이틀 스타일 */
    h1 {
        color: #8E1B3E; /* 덕성 버건디 */
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
        word-break: keep-all;
    }
    
    /* 덕새 이미지 스타일 */
    .deoksae-banner {
        display: block;
        margin: 0 auto 20px auto;
        width: 100%;
        max-width: 600px;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(142, 27, 62, 0.1);
        transition: transform 0.3s ease;
    }
    
    .deoksae-banner:hover {
        transform: scale(1.02);
    }

    /* 질문 카드 디자인 */
    .question-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid #FFD1DC;
        box-shadow: 0 4px 10px rgba(142, 27, 62, 0.05);
    }
    
    .question-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #8E1B3E;
        margin-bottom: 15px;
    }

    /* 라디오 버튼 스타일 커스텀 (Streamlit 기본 위젯 사용하되 깔끔하게) */
    .stRadio > div {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }

    /* 결과 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 65px;
        background-color: #8E1B3E;
        color: white;
        border: none;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(142, 27, 62, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #A93C5E;
        transform: translateY(-2px);
    }

    /* 결과 카드 스타일 */
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .rank-badge {
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의
majors_db = {
    "HUMAN": {
        "name": "인문과학 & 글로벌융합",
        "majors": ["국어국문학전공", "영어영문학전공", "문헌정보학전공", "사학전공", "글로벌융합대학"],
        "careers": ["작가/에디터", "기록물 관리 전문가", "문화재 전문가", "국제기구 종사자", "콘텐츠 기획자"],
        "desc": "언어와 문화를 통해 세상의 깊이를 이해하는 당신에게 추천해요. 📚"
    },
    "SOCIAL": {
        "name": "사회과학 & 심리",
        "majors": ["심리학전공", "사회학전공", "아동가족학전공", "사회복지학전공", "정치외교학전공"],
        "careers": ["임상심리사", "데이터 분석가(사회조사)", "가족 상담 전문가", "NGO 활동가", "정책 전문가"],
        "desc": "사람의 마음과 사회 현상에 따뜻한 관심을 가진 당신에게 딱이에요. 🤝"
    },
    "BIZ": {
        "name": "경영 & 국제통상",
        "majors": ["경영학전공", "국제통상학전공", "회계학전공"],
        "careers": ["기업 경영 컨설턴트", "공인회계사(CPA)", "무역 전문가", "금융권 종사자", "마케터"],
        "desc": "세상의 흐름을 읽고 실용적인 가치를 창출하는 리더형 인재시군요! 💼"
    },
    "TECH": {
        "name": "과학기술 & IT",
        "majors": ["컴퓨터공학전공", "IT미디어공학전공", "사이버보안전공", "바이오공학전공", "수학/통계학전공"],
        "careers": ["풀스택 개발자", "정보보안 전문가", "바이오 연구원", "UX/UI 엔지니어", "데이터 사이언티스트"],
        "desc": "논리적인 사고로 미래를 코딩하는 당신, 기술의 최전선이 어울려요. 💻"
    },
    "ART": {
        "name": "Art & Design",
        "majors": ["동양화과", "서양화과", "실내디자인과", "시각디자인과", "텍스타일디자인과"],
        "careers": ["일러스트레이터", "공간 디자이너", "브랜드 디자이너", "큐레이터", "웹툰 작가"],
        "desc": "남다른 감각으로 세상을 아름답게 채우는 예술가적 기질이 보여요. 🎨"
    }
}

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
            ("인공지능, 챗GPT, 신약 개발, 우주", "TECH"),
            ("경제 동향, 주식, 환율, 마케팅", "BIZ"),
            ("사회적 이슈, 인권, 심리, 복지 정책", "SOCIAL"),
            ("문학상 수상작, 역사, 철학, 문화 트렌드", "HUMAN")
        ]
    },
    {
        "q": "Q5. 대학 생활 4년 동안 꼭 해보고 싶은 것은?",
        "a": [
            ("교환학생 가서 다양한 문화 깊이 체험하기", "HUMAN"),
            ("창업 동아리에서 내 아이디어 수익화하기", "BIZ"),
            ("코딩 부트캠프나 실험실 인턴 참여하기", "TECH"),
            ("졸업 전시회나 공모전에서 대상 수상하기", "ART")
        ]
    }
]

# 4. 세션 상태 관리 (페이지 이동용)
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'scores' not in st.session_state:
    st.session_state.scores = {"HUMAN": 0, "SOCIAL": 0, "BIZ": 0, "TECH": 0, "ART": 0}

# 함수: 페이지 이동
def go_to_test():
    st.session_state.page = 'test'

def go_to_result():
    st.session_state.page = 'result'

def reset_test():
    st.session_state.scores = {k:0 for k in st.session_state.scores}
    st.session_state.page = 'intro'

# --- 메인 화면 로직 ---

# 1) 시작 화면 (Intro)
if st.session_state.page == 'intro':
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <img src="static/deoksae_main.png" class="deoksae-banner" alt="덕새 배너">
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🌸 덕새와 함께 찾는 나의 꽃길 🌸</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;'>
            <p style='font-size: 1.15em; color: #555; line-height: 1.6; margin: 0;'>
                반가워요, 25학번 새내기 여러분!<br>
                민주동산에 나타난 행운의 까치, <b>덕새</b>예요! 🦆<br><br>
                여러분의 꿈은 어떤 색깔인가요?<br>
                저와 함께 <b>나에게 딱 맞는 전공</b>을 알아보러 가요!
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    
    if st.button("덕새랑 전공 찾으러 가기! ✨"):
        go_to_test()
        st.rerun()

# 2) 진단 문항 화면 (Test - 한 페이지에 모두 표시)
elif st.session_state.page == 'test':
    st.markdown("<h1>🤔 나에게 맞는 전공은?</h1>", unsafe_allow_html=True)
    st.write("아래 질문에 가장 마음이 가는 답변을 선택해주세요.")
    st.write("---")

    # 점수 계산을 위한 임시 저장소
    temp_answers = {}

    # 질문 반복 출력
    for i, q_data in enumerate(questions):
        st.markdown(f"""
        <div class="question-box">
            <div class="question-title">{q_data['q']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 선택지 구성 (text만 보여주고, 선택 시 index 저장)
        options = [a[0] for a in q_data['a']]
        choice = st.radio(
            label="답변을 선택하세요", 
            options=options, 
            index=None, 
            key=f"q_{i}", 
            label_visibility="collapsed"
        )
        
        # 선택된 답변의 type 찾기
        if choice:
            for ans_text, ans_type in q_data['a']:
                if ans_text == choice:
                    temp_answers[i] = ans_type

    st.markdown("<br>", unsafe_allow_html=True)

    # 결과 확인 버튼
    if st.button("결과 확인하기 💌"):
        # 모든 질문에 답했는지 확인
        if len(temp_answers) < len(questions):
            st.warning("아직 선택하지 않은 문항이 있어요! 덕새가 기다리고 있어요 🦆")
        else:
            # 점수 집계
            st.session_state.scores = {k:0 for k in st.session_state.scores} # 초기화
            for q_idx, type_key in temp_answers.items():
                st.session_state.scores[type_key] += 1
            
            go_to_result()
            st.rerun()

# 3) 결과 화면 (Result)
elif st.session_state.page == 'result':
    st.balloons()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <img src="static/deoksae_main.png" class="deoksae-banner" alt="덕새 배너">
    """, unsafe_allow_html=True)

    st.markdown("<h1>🎉 덕새가 물어온 추천 전공 🎉</h1>", unsafe_allow_html=True)
    
    # 점수 정렬
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]

    st.write("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-bottom: 20px; font-size: 1.1em;'>
            "새로운 100년을 향해 힘차게 날아볼까요?"<br>
            덕새가 분석한 <b>최적의 전공 TOP 3</b>입니다. 🦆💕
        </div>
        """, unsafe_allow_html=True
    )

    ranks_data = [
        {"label": "🦆 덕새 Pick! 1순위", "bg": "#8E1B3E"},
        {"label": "🥈 2순위 추천", "bg": "#AFAFAF"},
        {"label": "🥉 3순위 추천", "bg": "#CFCFCF"}
    ]
    
    for i, (m_key, score) in enumerate(top_3):
        data = majors_db[m_key]
        rank_info = ranks_data[i]
        
        border_style = "3px solid #8E1B3E" if i == 0 else "2px solid #eee"
        bg_color = "#fffafa" if i == 0 else "white"
        
        st.markdown(f"""
            <div class="result-card" style="border: {border_style}; background-color: {bg_color};">
                <span class="rank-badge" style="background-color: {rank_info['bg']};">{rank_info['label']}</span>
                <h2 style="color: #333; margin-top: 15px; font-weight: 700;">{data['name']}</h2>
                <p style="font-size: 1.15em; color: #555; line-height: 1.5;">{data['desc']}</p>
                <hr style="border-top: 1px dashed #bbb; margin: 20px 0;">
                <p style='margin-bottom: 10px;'><b>🎓 관련 전공:</b> <span style='color: #8E1B3E;'>{', '.join(data['majors'])}</span></p>
                <p><b>💼 추천 진로:</b> {', '.join(data['careers'])}</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 처음으로 돌아가기"):
        reset_test()
        st.rerun()
