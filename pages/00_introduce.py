import streamlit as st

st.set_page_config(page_title="나의 자기소개", page_icon="🙂")

with st.sidebar:
    # --------------------------------------------------------------------
    # 👇 [수정할 곳] 아래 따옴표("") 안에 원하는 사진의 인터넷 주소를 넣으세요.
    # --------------------------------------------------------------------
    image_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80"
    
    st.image(image_url, width=250)
    
    st.title("김코딩 (Kim Coding)")
    st.write("💻 **풀스택 개발자 지망생**")
    st.write("📍 서울, 대한민국")
    st.link_button("👉 깃허브 방문하기", "https://github.com")

# 메인 화면
st.title("안녕하세요! 반갑습니다 👋")
st.divider()

st.header("📌 저를 소개합니다")
st.write("""
안녕하세요! 저는 **호기심 많은 개발자 김코딩**입니다.
문제를 해결하는 과정에서 즐거움을 느끼며, 매일 새로운 기술을 배우고 있습니다.

* **좋아하는 것**: 파이썬, 자동화, 맛있는 커피 ☕
* **현재 목표**: 나만의 웹 서비스 런칭하기
""")

st.divider()

st.header("🛠 사용 가능한 기술")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Languages")
    st.checkbox("Python", value=True)
with col2:
    st.subheader("Tools")
    st.checkbox("Streamlit", value=True)
