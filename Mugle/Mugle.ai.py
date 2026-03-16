import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - iOS Dark", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 다크모드 테마 & 애니메이션 강화] ---
st.markdown("""
    <style>
    /* 룰렛 애니메이션 강화: 위에서 아래로 튕기며 떨어지는 효과 */
    @keyframes rouletteSlide {
        0% { transform: translateY(-50px); opacity: 0; }
        60% { transform: translateY(10px); opacity: 1; }
        100% { transform: translateY(0); }
    }

    /* iOS/Mac OS 다크모드 배경 */
    .main { background-color: #000000; color: #FFFFFF; font-family: -apple-system, sans-serif; }
    
    /* Mugle 로고: 초대형 상향 */
    .logo-container { 
        text-align: center; padding: 20px 0; display: flex; justify-content: center; align-items: center; 
        font-size: 100px; font-weight: 900;
    }
    
    /* 맥북 다크 윈도우 스타일 */
    .mac-window {
        background-color: #1C1C1E; border-radius: 14px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        padding: 15px; border: 1px solid #38383A; margin-bottom: 10px;
    }
    
    .mac-title-bar { height: 18px; margin-bottom: 12px; display: flex; align-items: center; }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 애니메이션 클래스 적용 */
    .menu-display {
        background-color: #2C2C2E; border-radius: 10px; padding: 30px; 
        text-align: center; border: 1px solid #3A3A3C;
        animation: rouletteSlide 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* 독설 텍스트 크기 상향 */
    .shaming-text {
        color: #FF453A; font-weight: 800; font-size: 26px;
        text-align: center; margin: 20px 0; line-height: 1.4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
    }

    /* 버튼 칼각 정렬: 메뉴창 대비 50% 가로 너비 강제 적용 */
    div.stButton > button {
        width: 100% !important; height: 70px !important;
        border-radius: 12px !important; font-size: 22px !important;
        font-weight: 700 !important; border: none !important;
        margin-top: 10px !important;
    }
    
    /* 반려 버튼 (iOS 다크 그레이) */
    div.stButton:nth-child(1) > button {
        background-color: #3A3A3C !important; color: #FFFFFF !important;
    }
    /* 승인 버튼 (iOS 블루) */
    div.stButton:nth-child(2) > button {
        background-color: #0A84FF !important; color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메뉴 데이터베이스 및 세션 로직] ---
menu_pool = {
    "일식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 구이", "라멘", "츠케멘", "아부라소바", "냉소바"],
    "덮밥": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥"],
    "중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "타이 카레", "가파오라이스", "팟타이"],
    "양식/편의점": ["비프 카레", "오무라이스", "파스타", "수제버거", "로슨 카라아게군", "패밀리마트 치킨"]
}

shaming_comments = ["자네 안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비! 다시 골라오게.", "점심 결재도 못 받아서 어쩌나?"]

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
st.markdown('<div class="logo-container"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding:40px;"><h2>📥 결재 서류 대기</h2></div>', unsafe_allow_html=True)
    if st.button("📄 결재 시작"):
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

    # 메뉴창 (룰렛 애니메이션 적용)
    st.markdown(f"""
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="menu-display">
                <h2 style="margin:0; font-weight:900; color:#FFFFFF; font-size:32px;">{st.session_state.current_menu}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 독설 폰트
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {st.session_state.last_comment}</div>', unsafe_allow_html=True)

    # 버튼: 메뉴창 너비 50%씩 칼정렬
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
