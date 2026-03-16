import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Mac Dark", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 다크모드 & 와이드 버튼 & 대형 로고] ---
st.markdown("""
    <style>
    @keyframes slideDown {
        0% { transform: translateY(-30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    /* 다크모드 배경 및 기본 텍스트 */
    .main { background-color: #1E1E1E; color: #FFFFFF; font-family: -apple-system, sans-serif; }
    
    /* Mugle 로고: 대폭 상향 (100px) */
    .logo-container { 
        text-align: center; padding: 20px 0; display: flex; justify-content: center; align-items: center; 
        font-size: 100px; font-weight: 900;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.1));
    }
    .apple-logo { font-size: 60px; color: #FFFFFF; margin: 0 20px; opacity: 0.9; }
    
    /* 맥북 다크 윈도우 스타일 */
    .mac-window {
        background-color: #2D2D2D; border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        padding: 15px; margin-bottom: 5px; border: 1px solid #3D3D3D;
    }
    
    .mac-title-bar { height: 20px; margin-bottom: 12px; display: flex; align-items: center; }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 룰렛 애니메이션 & 다크 테마 */
    .menu-display {
        background-color: #1A1A1A; border-radius: 10px; padding: 30px; 
        text-align: center; border: 1px solid #333333;
        animation: slideDown 0.4s ease-out;
    }

    /* 킹받는 독설: 폰트 더 크게 & 밝은 레드 */
    .shaming-text {
        color: #FF4D4D; font-weight: 800; font-size: 24px;
        text-align: center; margin: 20px 0; line-height: 1.5;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* 버튼 스타일: 메뉴창 너비의 절반씩 정확히 50% 분할 */
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        border-radius: 10px !important; font-size: 20px !important;
        font-weight: 700 !important; border: none !important;
        transition: all 0.2s;
    }
    
    /* 반려 버튼 (다크 그레이) */
    div.stButton:nth-child(1) > button {
        background-color: #3D3D3D !important; color: #FFFFFF !important;
    }
    /* 승인 버튼 (애플 블루) */
    div.stButton:nth-child(2) > button {
        background-color: #007AFF !important; color: #FFFFFF !important;
    }
    
    div.stButton > button:active { transform: scale(0.97); opacity: 0.8; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메뉴 및 독설 DB 유지] ---
menu_pool = {
    "일식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 구이", "라멘", "츠케멘", "아부라소바", "냉소바"],
    "덮밥": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥"],
    "중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "타이 카레", "가파오라이스", "팟타이"],
    "양식/편의점": ["비프 카레", "오무라이스", "파스타", "수제버거", "로슨 카라아게군", "패밀리마트 치킨"]
}

shaming_comments = [
    "박 대리, 이 메뉴는 LTV 비율이 너무 낮아. 반려!",
    "지금 메뉴 고르는 속도로 대출 심사하면 우리 지점 망해.",
    "서류 미비! 일본까지 와서 결정을 못 하나?",
    "자꾸 반려하면 오늘 점심은 탕비실 믹스커피다.",
    "지점장님: '박 대리는 점심 메뉴도 컴플라이언스 위반인가?'",
    "허허, 박 대리. 자네 안목이 이것밖에 안 됐나?"
]

# --- [4. 세션 관리] ---
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

# --- [5. UI 구성] ---

# 압도적인 로고 크기
st.markdown('<div class="logo-container"><span class="apple-logo"></span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span><span class="apple-logo"></span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding:40px;"><h2 style="margin:0; color:#007AFF;">📥 서류 대기 중</h2><p style="font-size:18px; color:#888; margin-top:10px;">박 대리, 오늘 결재판 가져오게.</p></div>', unsafe_allow_html=True)
    if st.button("📄 결재 서류 상신"):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()
else:
    # 지점장 사진
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1.2, 4, 1.2])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    # 메뉴창 (다크 룰렛 애니메이션)
    st.markdown(f"""
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="menu-display">
                <h1 style="margin:0; font-weight:800; color:#FFFFFF; font-size:32px;">{st.session_state.current_menu}</h1>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 더 킹받는 독설
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {st.session_state.last_comment}</div>', unsafe_allow_html=True)

    # 하단 버튼: 너비 50%씩 딱 맞게 나열
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
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
            st.success("결재 승인! 고생했네 박 대리.")
            time.sleep(2)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
