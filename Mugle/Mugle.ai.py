import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Mac OS 룰렛", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 애니메이션 및 빅-버튼 적용] ---
st.markdown("""
    <style>
    @keyframes slideDown {
        0% { transform: translateY(-30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    .main { background-color: #F5F5F7; color: #1D1D1F; font-family: -apple-system, sans-serif; }
    
    /* 로고 섹션 */
    .logo-container { 
        text-align: center; padding: 10px 0; display: flex; justify-content: center; align-items: center; 
        font-size: 32px; font-weight: 800;
    }
    .apple-logo { font-size: 24px; color: #555; margin: 0 10px; }
    
    /* 맥북 창 스타일 */
    .mac-window {
        background-color: #FFFFFF; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        padding: 12px; margin-bottom: 10px; border: 1px solid #EAEAEA;
    }
    
    .mac-title-bar { height: 18px; margin-bottom: 10px; display: flex; align-items: center; }
    .dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 룰렛 애니메이션 적용 */
    .menu-display {
        background-color: #FAFAFA; border-radius: 8px; padding: 25px; 
        text-align: center; border: 1px solid #EDEDED;
        animation: slideDown 0.4s ease-out; /* 위에서 아래로 떨어지는 효과 */
    }

    /* 킹받는 독설: 폰트 크기 상향 */
    .shaming-text {
        color: #FF1744; font-weight: 800; font-size: 20px; /* 기존보다 훨씬 크게 */
        text-align: center; margin: 15px 0; line-height: 1.4;
        filter: drop-shadow(1px 1px 0px white);
    }

    /* 버튼 스타일: 너비 50%씩 꽉 차게 */
    div.stButton > button {
        width: 100% !important; height: 60px !important; /* 높이도 키움 */
        border-radius: 10px !important; font-size: 18px !important;
        font-weight: 700 !important; transition: transform 0.1s;
    }
    div.stButton > button:active { transform: scale(0.95); }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메뉴 및 독설 DB] ---
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
st.markdown('<div class="logo-container"><span class="apple-logo"></span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span><span class="apple-logo"></span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center;"><h4 style="margin:10px 0;">📥 신규 결재 대기 중</h4><p style="font-size:14px; color:#666;">박 대리, 오늘 점심은 뭔가?</p></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신 시작"):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()
else:
    # 지점장 사진
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1.5, 4, 1.5])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    # 메뉴창 (애니메이션 포함)
    st.markdown(f"""
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="menu-display">
                <h2 style="margin:0; font-weight:800; color:#1D1D1F;">{st.session_state.current_menu}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 독설 폰트 상향
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {st.session_state.last_comment}</div>', unsafe_allow_html=True)

    # 하단 버튼 (너비 50%씩 꽉 채움)
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
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
            st.success("점심 식사 승인 완료!")
            time.sleep(2)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
