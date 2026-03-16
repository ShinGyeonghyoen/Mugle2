import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - iOS Dark", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: Flexbox 기반 버튼 & iOS 다크 테마] ---
st.markdown("""
    <style>
    @keyframes slideDown {
        0% { transform: translateY(-30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    /* iOS/Mac OS 진한 다크모드 배경 */
    .main { background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }
    
    /* Mugle 로고: 초대형 (100px) */
    .logo-container { 
        text-align: center; padding: 15px 0; display: flex; justify-content: center; align-items: center; 
        font-size: 100px; font-weight: 900;
    }
    .apple-logo { font-size: 60px; color: #FFFFFF; margin: 0 15px; }
    
    /* Mac 윈도우 스타일 (Dark Gray) */
    .mac-window {
        background-color: #1C1C1E; border-radius: 14px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
        padding: 15px; margin-bottom: 5px; border: 1px solid #38383A;
    }
    
    .mac-title-bar { height: 18px; margin-bottom: 12px; display: flex; align-items: center; }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 룰렛 애니메이션 */
    .menu-display {
        background-color: #2C2C2E; border-radius: 10px; padding: 25px; 
        text-align: center; border: 1px solid #3A3A3C;
        animation: slideDown 0.4s ease-out;
    }

    /* 독설 텍스트 */
    .shaming-text {
        color: #FF453A; font-weight: 700; font-size: 22px;
        text-align: center; margin: 15px 0; line-height: 1.4;
    }

    /* ⭐ 핵심: 버튼 칼각 조정 (Flexbox) */
    [data-testid="stHorizontalBlock"] {
        gap: 8px !important; /* 버튼 사이 간격 */
    }
    
    div.stButton > button {
        width: 100% !important; /* 컬럼 너비에 꽉 차게 */
        height: 55px !important;
        border-radius: 12px !important; 
        font-size: 18px !important; /* 폰트 사이즈 조정 */
        font-weight: 600 !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 반려 버튼 스타일 */
    div.stButton:nth-child(1) > button {
        background-color: #3A3A3C !important; color: #FFFFFF !important;
    }
    /* 승인 버튼 스타일 */
    div.stButton:nth-child(2) > button {
        background-color: #0A84FF !important; color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 데이터베이스 및 세션 로직 유지] ---
menu_pool = {
    "일식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 구이", "라멘", "츠케멘", "아부라소바", "냉소바"],
    "덮밥": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥"],
    "중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "타이 카레", "가파오라이스", "팟타이"],
    "양식/편의점": ["비프 카레", "오무라이스", "파스타", "수제버거", "로슨 카라아게군", "패밀리마트 치킨"]
}

shaming_comments = ["박 대리, 반려!", "서류 미비!", "자네 안목이 이것밖에 안 됐나?", "다시 골라오게."]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ""
if 'last_comment' not in st.session_state: st.session_state.last_comment = ""

def get_boss_image(count):
    idx = min(count, 4)
    search_paths = [f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png", f"face_{idx}.jpg", f"face_{idx}.png"]
    for p in search_paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---

# 대형 로고
st.markdown('<div class="logo-container"><span class="apple-logo"></span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span><span class="apple-logo"></span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding:30px;"><h3>📋 신규 결재 대기</h3></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신"):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()
else:
    # 지점장 사진
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    # 메뉴창
    st.markdown(f"""
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="menu-display">
                <h2 style="margin:0; font-weight:800; color:#FFFFFF;">{st.session_state.current_menu}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {st.session_state.last_comment}</div>', unsafe_allow_html=True)

    # ⭐ 버튼 정렬: 컬럼을 통해 메뉴창 너비의 정확히 절반씩 차지
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("⚖️ 반 려"):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
            st.session_state.last_comment = random.choice(shaming_comments)
            st.rerun()
    with btn_col2:
        if st.button("✅ 승 인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
