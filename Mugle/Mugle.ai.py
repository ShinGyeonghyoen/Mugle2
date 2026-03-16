import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - 모바일 지점장", page_icon="🍱", layout="centered")

# --- [2. 네움포리즘 & 구글 스타일 UI] ---
st.markdown("""
    <style>
    .main { background-color: #1A1A1A; color: #E0E0E0; }
    .logo-text { font-size: 50px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .neo-card {
        background: #222222; border-radius: 20px; padding: 20px;
        box-shadow: inset 2px 2px 5px #2b2b2b, inset -2px -2px 5px #101010;
        border: 1px solid #333; text-align: center; margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100%; height: 60px; border-radius: 15px; background: #222222;
        color: #E0E0E0; font-weight: bold; border: 1px solid #333;
        box-shadow: 5px 5px 10px #101010, -5px -5px 10px #2a2a2a;
    }
    div.stButton > button:hover { border-color: #4285F4; color: #4285F4; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 매머드급 메뉴 데이터베이스] ---
menu_pool = {
    "일식 정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 소금구이", "임면수어 구이", "미소카츠", "토리카라아게 정식", "연어 미소즈케 구이", "굴튀김 정식"],
    "덮밥/돈부리": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥", "회덮밥", "로스트비프동"],
    "면요리": ["소유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", "아부라소바", "냉소바", "자루우동", "카레우동", "야끼소바", "탄탄멘"],
    "중식/에스닉": ["마파두부 정식", "호이코로", "에비칠리 정식", "교자 볶음밥 세트", "칭쟈오로스", "타이 카레", "가파오라이스", "팟타이", "베트남 쌀국수", "나시고랭"],
    "양식": ["비프 카레", "치킨 카레", "오무라이스", "나폴리탄 파스타", "미트소스 파스타", "명란 크림 파스타", "수제버거 세트", "마르게리따 피자"],
    "편의점/분식": ["로손 카라아게군", "패밀리마트 도시락", "세븐 야키소바빵", "마트 타임세일 스시", "서브웨이", "신오쿠보 떡볶이"]
}

shaming_comments = [
    "박 주임, 이 메뉴는 LTV 비율이 너무 낮아. 반려!", "지금 메뉴 고르는 속도로 대출 심사하면 은행 망해.", 
    "서류 미비! 일본까지 와서 결정을 못 하나?", "자꾸 이러면 오늘 점심은 탕비실 믹스커피다."
]

# --- [4. 세션 상태 및 로직] ---
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = "상신 대기 중..."

def roll_menu():
    cat = random.choice(list(menu_pool.keys()))
    st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"

# --- [5. UI 구성] ---
st.markdown('<div class="logo-text"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

# 지점장님 사진 (와이드 비율 대응)
face_path = f"Mugle/face_{min(st.session_state.reject_count, 4)}.jpg"
try:
    img = Image.open(face_path)
    st.image(img, use_container_width=True)
except:
    st.warning("사진 로딩 중... (파일 경로 확인 필요)")

st.markdown(f'<div class="neo-card"><h3>{st.session_state.current_menu}</h3></div>', unsafe_allow_html=True)

if st.session_state.reject_count > 0:
    st.error(random.choice(shaming_comments))

if st.button("⚖️ 신 규 서 류 심 사 / 반 려"):
    st.session_state.reject_count += 1
    roll_menu()
    st.rerun()

if st.button("✅ 최 종 승 인 (Accept)"):
    st.balloons()
    st.success("결재 완료! 맛있게 먹게.")
    st.session_state.reject_count = 0
