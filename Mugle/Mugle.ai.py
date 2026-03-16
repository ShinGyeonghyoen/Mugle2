import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Compact", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 컴팩트 스케일 & 리퀴드 글래스] ---
st.markdown("""
    <style>
    /* 전체 스캔 가능하도록 여백 축소 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    @keyframes rouletteEffect {
        0% { transform: translateY(-20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    /* iOS 스타일 미드나잇 다크 배경 */
    .stApp {
        background: linear-gradient(180deg, #1C1C1E 0%, #050505 100%);
        background-attachment: fixed;
    }

    /* Mugle 로고: 크기 최적화 (기존 100px -> 60px) */
    .logo-container { 
        text-align: center; padding: 10px 0; font-size: 60px; font-weight: 900;
        letter-spacing: -1.5px;
    }
    
    /* 리퀴드 글래스 윈도우: 높이 축소 */
    .mac-window {
        background: rgba(45, 45, 48, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        padding: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 8px;
    }

    /* 메뉴 표시창: 폰트 및 패딩 최적화 */
    .menu-display {
        background: rgba(0, 0, 0, 0.4); border-radius: 10px; padding: 25px 15px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
        animation: rouletteEffect 0.4s ease-out;
    }

    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF; font-size: 26px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }

    /* 독설 텍스트: 컴팩트 사이즈 */
    .shaming-text {
        color: #FF453A; font-weight: 700; font-size: 18px;
        text-align: center; margin: 10px 0;
    }

    /* ⭐ 버튼 칼각 및 사이즈 최적화 */
    [data-testid="stHorizontalBlock"] {
        gap: 10px !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important; /* 높이 축소 */
        border-radius: 12px !important; font-size: 17px !important;
        font-weight: 700 !important; border: none !important;
    }
    
    /* 반려 버튼 */
    div.stButton:nth-child(1) > button {
        background: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
    }
    /* 승인 버튼 */
    div.stButton:nth-child(2) > button {
        background: #0A84FF !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 로직 유지] ---
menu_pool = {
    "일식": ["돈카츠 정식", "로스카츠", "히레카츠", "라멘", "츠케멘", "냉소바"],
    "덮밥": ["규동", "카츠동", "오야코동", "텐동", "사케동", "카이센동"],
    "중식/에스닉": ["마파두부", "에비칠리", "타이 카레", "팟타이"],
    "양식/편의점": ["비프 카레", "오무라이스", "파스타", "수제버거", "로슨 카라아게군"]
}
shaming_comments = ["안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비!", "다시 골라오게."]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ""
if 'spinning' not in st.session_state: st.session_state.spinning = False

def get_boss_image(count):
    idx = min(count, 4)
    search_paths = [f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png", f"face_{idx}.jpg", f"face_{idx}.png"]
    for p in search_paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---

st.markdown('<div class="logo-container"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding:25px;"><h3 style="color:white; margin:0;">📥 결재 대기 중</h3></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()
else:
    # 1.2초 룰렛 시스템 (전체 속도감 상향)
    if st.session_state.spinning:
        placeholder = st.empty()
        for _ in range(8):
            cat = random.choice(list(menu_pool.keys()))
            temp = f"[{cat}] {random.choice(menu_pool[cat])}"
            placeholder.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{temp}</h2></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

    # 지점장 이미지 크기 최적화
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1.5, 4, 1.5]) # 이미지 가로폭 살짝 축소
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    st.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text" style="font-size:24px;">{st.session_state.current_menu}</h2></div></div>', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)}</div>', unsafe_allow_html=True)

    # 버튼 레이아웃 (한눈에 들어오도록 높이 축소)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("⚖️ 반려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.rerun()
    with b_col2:
        if st.button("✅ 승인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
