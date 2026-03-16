import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Liquid Dark", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 리퀴드 글래스 & 칼각 버튼 & 애니메이션] ---
st.markdown("""
    <style>
    /* 룰렛 애니메이션: 2초간 위아래로 빠르게 회전하는 효과 */
    @keyframes rouletteEffect {
        0% { transform: translateY(-100px); opacity: 0; }
        20% { transform: translateY(0); opacity: 1; }
        40% { transform: translateY(-20px); }
        60% { transform: translateY(0); }
        80% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }

    /* 리퀴드 글래스 & Mac 다크 테마 배경 */
    .stApp {
        background: radial-gradient(circle at top left, #2C2C2E, #000000);
        background-attachment: fixed;
    }

    /* Mugle 로고: 대폭 상향 */
    .logo-container { 
        text-align: center; padding: 20px 0; font-size: 100px; font-weight: 900;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));
    }
    
    /* 맥북 윈도우 스타일 (리퀴드 글래스 효과) */
    .mac-window {
        background: rgba(44, 44, 46, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    /* 메뉴 표시창: 애니메이션 2초 적용 */
    .menu-display {
        background: rgba(0, 0, 0, 0.5); border-radius: 12px; padding: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
        animation: rouletteEffect 2s cubic-bezier(0.25, 1, 0.5, 1);
    }

    /* 독설 텍스트 */
    .shaming-text {
        color: #FF453A; font-weight: 800; font-size: 26px;
        text-align: center; margin: 20px 0;
        text-shadow: 0 0 10px rgba(255, 69, 58, 0.5);
    }

    /* ⭐ 반려/승인 버튼: 메뉴창 너비에 딱 맞춰 50%씩 분할 */
    [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        gap: 10px !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 75px !important;
        border-radius: 14px !important; font-size: 22px !important;
        font-weight: 700 !important; border: none !important;
        transition: transform 0.1s;
    }
    
    /* 반려 버튼 (어두운 글래스) */
    div.stButton:nth-child(1) > button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    /* 승인 버튼 (애플 블루 글래스) */
    div.stButton:nth-child(2) > button {
        background: rgba(10, 132, 255, 0.8) !important;
        color: #FFFFFF !important;
    }

    div.stButton > button:active { transform: scale(0.96); }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 데이터 및 세션 로직] ---
menu_pool = {
    "일식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "라멘", "츠케멘", "아부라소바", "냉소바"],
    "덮밥": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥"],
    "중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "타이 카레", "가파오라이스", "팟타이"],
    "양식/편의점": ["비프 카레", "오무라이스", "파스타", "수제버거", "로슨 카라아게군", "패밀리마트 치킨"]
}

shaming_comments = ["자네 안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비! 다시 골라오게.", "점심 결재도 못 받아서 어쩌나?"]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ""
if 'last_comment' not in st.session_state: st.session_state.last_comment = ""
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
    st.markdown('<div class="mac-window" style="text-align:center; padding:40px;"><h2>📥 결재 서류 대기 중</h2></div>', unsafe_allow_html=True)
    if st.button("📄 결재 시작"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()

else:
    # 룰렛 애니메이션 연출 (2초 대기)
    if st.session_state.spinning:
        with st.empty():
            for _ in range(10):
                cat = random.choice(list(menu_pool.keys()))
                temp_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
                st.markdown(f'<div class="mac-window"><div class="menu-display"><h2>{temp_menu}</h2></div></div>', unsafe_allow_html=True)
                time.sleep(0.15)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    st.markdown(f"""
        <div class="mac-window">
            <div class="menu-display">
                <h2 style="margin:0; font-weight:900; color:#FFFFFF; font-size:35px;">{st.session_state.current_menu}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {st.session_state.last_comment}</div>', unsafe_allow_html=True)

    # ⭐ 버튼 칼각 레이아웃
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("⚖️ 반 려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.session_state.last_comment = random.choice(shaming_comments)
            st.rerun()
    with btn_col2:
        if st.button("✅ 승 인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
