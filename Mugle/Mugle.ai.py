import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Deep Dark", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 가독성 강화 & 리퀴드 글래스 스타일] ---
st.markdown("""
    <style>
    /* 룰렛 애니메이션: 2초간 긴장감 있게 회전 */
    @keyframes rouletteEffect {
        0% { transform: translateY(-30px); opacity: 0; }
        10% { opacity: 1; }
        100% { transform: translateY(0); }
    }

    /* iOS 스타일의 세련된 다크 배경 (Midnight Blue Gradient) */
    .stApp {
        background: linear-gradient(180deg, #1C1C1E 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* Mugle 로고: 화이트/컬러 조합으로 가독성 상향 */
    .logo-container { 
        text-align: center; padding: 25px 0; font-size: 85px; font-weight: 900;
        letter-spacing: -2px;
    }
    
    /* 리퀴드 글래스 윈도우: 가독성을 위해 투명도 조절 */
    .mac-window {
        background: rgba(45, 45, 48, 0.6);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
        padding: 24px; border: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 15px;
    }

    /* 메뉴 표시창: 화이트 텍스트가 가장 잘 보이도록 설계 */
    .menu-display {
        background: rgba(0, 0, 0, 0.4); border-radius: 12px; padding: 40px 20px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);
        animation: rouletteEffect 0.5s ease-out;
    }

    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF; font-size: 34px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }

    /* 독설 텍스트: 선명한 네온 레드 */
    .shaming-text {
        color: #FF453A; font-weight: 700; font-size: 24px;
        text-align: center; margin: 20px 0;
        filter: drop-shadow(0 0 8px rgba(255, 69, 58, 0.3));
    }

    /* ⭐ 버튼 칼각: 50% 너비 고정 및 가독성 폰트 */
    [data-testid="stHorizontalBlock"] {
        gap: 12px !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 70px !important;
        border-radius: 16px !important; font-size: 20px !important;
        font-weight: 700 !important; border: none !important;
    }
    
    /* 반려 버튼 (Glassy Gray) */
    div.stButton:nth-child(1) > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    /* 승인 버튼 (Solid Apple Blue) */
    div.stButton:nth-child(2) > button {
        background: #0A84FF !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(10, 132, 255, 0.3);
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
shaming_comments = ["자네 안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비!", "다시 골라오게."]

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
    st.markdown('<div class="mac-window" style="text-align:center; padding:40px;"><h2 style="color:white;">📥 결재 대기 중</h2></div>', unsafe_allow_html=True)
    if st.button("📄 결재 서류 상신"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()
else:
    # 2초 룰렛 시스템
    if st.session_state.spinning:
        placeholder = st.empty()
        for _ in range(12):
            cat = random.choice(list(menu_pool.keys()))
            temp = f"[{cat}] {random.choice(menu_pool[cat])}"
            placeholder.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{temp}</h2></div></div>', unsafe_allow_html=True)
            time.sleep(0.12)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

    # 지점장 이미지 및 메뉴 표시
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    st.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{st.session_state.current_menu}</h2></div></div>', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)}</div>', unsafe_allow_html=True)

    # 버튼 레이아웃 (50:50 정렬)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("⚖️ 반 려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.rerun()
    with b_col2:
        if st.button("✅ 승 인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
