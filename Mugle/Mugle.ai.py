import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 비율 조정 및 상단 여백 확보] ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; }
    
    /* 전체 컨테이너: 상단 여백을 충분히 주어 로고 가림 방지 */
    .block-container { 
        padding-top: 3rem !important; 
        padding-bottom: 1rem !important;
        max-width: 450px !important; 
    }

    /* 로고 섹션: 크기 살짝 줄임 */
    .logo-container { 
        text-align: center; padding-bottom: 20px; font-size: 28px; font-weight: 900;
        display: flex; justify-content: center; align-items: center; gap: 8px;
    }
    
    /* 지점장 이미지: 크기를 75%로 조절하여 비율 최적화 */
    .boss-box {
        display: flex; justify-content: center; align-items: center;
        width: 100%; margin-bottom: 15px;
    }
    .boss-box img {
        width: 75% !important; border-radius: 18px;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.08);
    }

    /* iOS/Mac 다크모드 메뉴창: 콤팩트 사이즈 */
    .ios-window {
        background: rgba(44, 44, 46, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 2px;
        border: 0.5px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
    }
    
    .traffic-lights { display: flex; gap: 5px; padding: 10px 14px; }
    .light { width: 10px; height: 10px; border-radius: 50%; }
    .red { background: #FF5F56; } .yellow { background: #FFBD2E; } .green { background: #27C93F; }

    .menu-display {
        background: rgba(28, 28, 30, 0.6);
        margin: 0 8px 8px 8px;
        border-radius: 12px;
        padding: 25px 10px; /* 패딩 축소 */
        text-align: center;
    }

    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF !important; 
        font-size: 20px; line-height: 1.4; /* 폰트 크기 조절 */
    }

    /* 버튼 스타일 */
    button {
        height: 50px !important; border-radius: 14px !important;
        font-size: 16px !important; font-weight: 700 !important;
    }
    div.stButton:nth-child(1) > button { background-color: #3A3A3C !important; color: #FFFFFF !important; border: none !important; }
    div.stButton:nth-child(2) > button { background-color: #0A84FF !important; color: #FFFFFF !important; border: none !important; }
    
    .shaming-text { color: #FF453A; font-weight: 600; font-size: 13px; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메뉴 데이터베이스] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반", "쇼가야키", "함바그", "야키니쿠", "규카츠", "가라아게", "돼지김치볶음"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "츠케멘", "아부라소바", "탄탄멘", "소바", "우동", "파슷하"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "비프 카레", "카츠 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "카레", "가파오라이스", "팟타이", "쌀국수"],
    "🏪 편의점/로컬": ["로손", "세븐일레븐", "패밀리마트", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["샐러드", "서브웨이", "포케 볼", "생선구이", "맥도날드", "버거킹", "KFC", "미역국"],
    "👨‍🍳 백종원": ["홍콩 반점", "새마을 식당", "조보아씨 내려와 봐유", "빽다방", "돌아갈까봐 그래유"]
}

shaming_comments = ["안목이 이것뿐인가?", "박 대리, 서류 미비일세!", "반려하겠네.", "그럴싸쥬?"]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")

def get_boss_image(count):
    idx = min(count, 4)
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---

# 로고 (상단 여백 적용됨)
st.markdown('<div class="logo-container">🍎 <span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span> 🍎</div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="ios-window"><div class="menu-display"><div class="menu-text" style="color:#8E8E93 !important;">📂 상신 대기 중...</div></div></div>', unsafe_allow_html=True)
    if st.button("🚀 결재 상신", use_container_width=True):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
        st.rerun()
else:
    # 지점장 이미지 센터링 및 크기 축소 적용
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        st.markdown('<div class="boss-box">', unsafe_allow_html=True)
        st.image(Image.open(face_file))
        st.markdown('</div>', unsafe_allow_html=True)

    # iOS 스타일 메뉴 표시창 (비율 조정 완료)
    cat_name, menu_name = st.session_state.current_menu
    st.markdown(f'''
        <div class="ios-window">
            <div class="traffic-lights">
                <div class="light red"></div><div class="light yellow"></div><div class="light green"></div>
            </div>
            <div class="menu-display">
                <div class="menu-text">[{cat_name}]<br>{menu_name}</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)} ({st.session_state.reject_count}회)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ 반려", use_container_width=True):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()
    with col2:
        if st.button("✅ 승인", use_container_width=True):
            st.balloons()
            time.sleep(1.5)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
