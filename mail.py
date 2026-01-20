import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="덕새와 함께하는 전공 찾기",
    page_icon="🦆",
    layout="centered"
)

# 2. 감성적 UI + 덕새 활용을 위한 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 (Noto Sans KR 적용) */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');
    
    .stApp {
        /* 덕성 버건디와 핑크를 활용한 부드러운 그라데이션 */
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 타이틀 스타일 */
    h1 {
        color: #8E1B3E; /* 덕성 버건디 */
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 덕새 이미지 스타일 클래스 (중앙 정렬 및 그림자) */
    .deoksae-main {
        display: block;
        margin: 0 auto 20px auto;
        max-width: 280px; /* 이미지 크기 조절 */
        height: auto;
        border-radius: 20px; /* 이미지 둥글게 */
        box-shadow: 5px 5px 15px rgba(142, 27, 62, 0.15); /* 부드러운 그림자 */
    }

    /* 메인 카드 디자인 */
    .question-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(142, 27, 62, 0.08);
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid #fff0f5;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 65px;
        background-color: white;
        color: #555;
        border: 2px solid #FFD1DC;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stButton>button:hover {
        background-color: #fff0f5;
        color: #8E1B3E;
        border-color: #8E1B3E;
        transform: translateY(-3px);
        box-shadow: 0 5px 10px rgba(142, 27, 62, 0.15);
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
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (이전과 동일)
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

# 4. 세션 상태 초기화
if 'scores' not in st.session_state:
    st.session_state.scores = {"HUMAN": 0, "SOCIAL": 0, "BIZ": 0, "TECH": 0, "ART": 0}
if 'step' not in st.session_state:
    st.session_state.step = 0

# 5. 질문 리스트
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

# 함수: 답변 선택 시 점수 계산 및 다음 단계 이동
def next_step(type_key):
    st.session_state.scores[type_key] += 1
    st.session_state.step += 1

# --- 메인 화면 로직 ---

# 1) 시작 화면 (덕새 등장!)
if st.session_state.step == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # [핵심] static 폴더의 실제 이미지를 불러옵니다.
    st.markdown("""
        <img src="static/deoksae_welcome.png" class="deoksae-main" alt="반가워하는 덕새">
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🌸 덕새와 함께 찾는 나의 꽃길 🌸</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='question-card'>
            <p style='font-size: 1.15em; color: #555; line-height: 1.6;'>
                반가워요, 25학번 새내기 여러분! 🦆<br>
                저 <b>덕새</b>가 여러분의 전공 고민을 해결해 드릴게요.<br><br>
                가벼운 마음으로 몇 가지 질문에 답해보세요.<br>
                당신에게 딱 맞는 <b>전공 꽃길</b>을 물어다 줄게요!
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    if st.button("덕새랑 전공 찾으러 가기! ✨"):
        st.session_state.step = 1
        st.rerun()

# 2) 질문 진행 화면
elif st.session_state.step <= len(questions):
    q_idx = st.session_state.step - 1
    cur_q = questions[q_idx]

    # 진행바 표시
    progress = q_idx / len(questions)
    st.progress(progress)
    
    st.markdown(f"""
        <div class='question-card' style='margin-top: 20px;'>
            <span style='font-size: 3em;'>🤔</span>
            <h3 style='color: #8E1B3E; margin-top: 10px; font-weight: 700;'>{cur_q['q']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # 답변 버튼들
    for answer_text, type_key in cur_q['a']:
        if st.button(answer_text):
            next_step(type_key)
            st.rerun()

# 3) 결과 화면 (덕새 축하!)
else:
    st.balloons() # 축하 효과
    st.markdown("<br>", unsafe_allow_html=True)
    
    # [핵심] static 폴더의 축하 이미지를 불러옵니다.
    st.markdown("""
        <img src="static/deoksae_party.png" class="deoksae-main" alt="축하하는 덕새">
    """, unsafe_allow_html=True)

    st.markdown("<h1>🎉 덕새가 물어온 전공 뉴스 🎉</h1>", unsafe_allow_html=True)
    
    # 점수 정렬 (높은 순)
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3] # 상위 3개 추출

    st.write("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-bottom: 20px; font-size: 1.1em;'>
            "너의 가능성은 무궁무진해!"<br>
            덕새가 분석한 <b>최적의 전공 TOP 3</b>를 소개할게. 🦆💕
        </div>
        """, unsafe_allow_html=True
    )

    # 순위별 출력 (배지 및 스타일 적용)
    ranks_data = [
        {"label": "🦆 덕새 Pick! 1순위", "bg": "#8E1B3E"},
        {"label": "🥈 2순위 추천", "bg": "#AFAFAF"},
        {"label": "🥉 3순위 추천", "bg": "#CFCFCF"}
    ]
    
    for i, (m_key, score) in enumerate(top_3):
        data = majors_db[m_key]
        rank_info = ranks_data[i]
        
        # 1순위 강조 스타일
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

    # 다시하기 버튼
    st.write("")
    st.write("")
    if st.button("🔄 덕새랑 다시 한번 찾아볼까?"):
        st.session_state.scores = {k:0 for k in st.session_state.scores}
        st.session_state.step = 0
        st.rerun()
