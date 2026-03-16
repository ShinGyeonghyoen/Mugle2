import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정 및 초기화] ---
st.set_page_config(page_title="Mugle AI - Master", page_icon="🍎", layout="centered")

# --- [2. 깃허브 RAW 주소 설정] ---
# 주소 끝에 ?raw=true를 붙여야 엑박 없이 GIF가 출력됩니다.
DANCE_VIDEO_URL = "https://github.com/ShinGyeonghyoen/Mugle2/blob/main/Mugle/dance.gif?raw=true"

# --- [3. UI/UX 디자인 (CSS)] ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { background: linear-gradient(180deg, #1C1C1E 0%, #000000 100%); font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1.5rem !important; max-width: 450px !important; }

    .logo-container { text-align: center; padding-bottom: 10px; font-size: 32px; font-weight: 900; }
    
    .boss-box { display: flex; justify-content: center; margin-bottom: 15px; }
    .boss-box img { width: 80% !important; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }

    /* 룰렛 애니메이션 */
    @keyframes rouletteSlide {
        0% { transform: translateY(-30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    .mac-window {
        background: rgba(44, 44, 46, 0.8); backdrop-filter: blur(20px);
        border-radius: 18px; padding: 15px; border: 0.5px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px; text-align: center;
    }

    .menu-display {
        background: rgba(28, 28, 30, 0.6); border-radius: 12px; padding: 25px 10px;
        animation: rouletteSlide 0.5s ease-out;
    }

    .menu-text { margin: 0; font-weight: 800; color: #FFFFFF !important; font-size: 22px; }

    /* 파칭코 피버 애니메이션 */
    @keyframes feverTime {
        0% { border: 3px solid #0A84FF; }
        50% { border: 3px solid #FFD700; }
        100% { border: 3px solid #0A84FF; }
    }
    .fever-window { border-radius: 18px; animation: feverTime 0.3s infinite; padding: 5px; }

    .shaming-text { color: #FF453A; font-weight: 700; font-size: 14px; margin-bottom: 10px; text-align: center; }

    /* 버튼 스타일 */
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 12px !important;
        font-size: 16px !important; font-weight: 700 !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [4. 데이터베이스 및 로직] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반", "쇼가야키", "함바그", "야키니쿠", "규카츠", "가라아게", "돼지김치볶음", "제육볶음", "순두부", "김치찌개", "된장찌개"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "츠케멘", "아부라소바", "탄탄멘", "냉소바", "카레 우동", "파슷하"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "비프 카레", "카츠 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "카레", "가파오라이스", "팟타이", "쌀국수"],
    "🏪 편의점/로컬": ["로슨", "세븐일레븐", "훼미리마트", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["샐러드", "서브웨이", "포케 볼", "생선구이", "맥도날드", "버거킹", "KFC", "미역국"],
    "👨‍🍳 백종원": ["홍콩 반점", "새마을 식당", "조보아씨 내려와 봐유", "빽다방", "돌아갈까봐 그래유"]
}
shaming_comments = ["안목이 이것뿐인가?", "박 대리, 서류 미비일세!", "반려하겠네.", "다시 골라오게."]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")
if 'final_choice' not in st.session_state: st.session_state.final_choice = None

def get_boss_image(count):
    idx = min(count, 4)
    paths = [f"face_{idx}.png", f"face_{idx}.jpg", f"Mugle/face_{idx}.png"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [5. 메인 레이아웃] ---
st.markdown('<div class="logo-container">🍎 <span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span> 🍎</div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    if st.session_state.final_choice:
        st.balloons()
        st.markdown(f'''
            <div class="fever-window">
                <div class="mac-window">
                    <div class="menu-text" style="color:#FFD700 !important; font-size:24px; margin-bottom:10px;">🎰 승인 확정! 🎰</div>
                    <div class="menu-text" style="margin-bottom:15px;">오늘 점심은<br><span style="color:#0A84FF;">{st.session_state.final_choice}</span></div>
                    <img src="{DANCE_VIDEO_URL}" style="width:100%; border-radius:12px; border:2px solid #FFD700;">
                    <div class="menu-text" style="font-size:14px; color:#32CD32; margin-top:10px;">🕺 기쁨의 춤사위 발동! 💃</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("🔄 새로운 결재 올리기"):
            st.session_state.final_choice = None
            st.rerun()
    else:
        st.markdown('<div class="mac-window"><div class="menu-text" style="color:#8E8E93 !important;">📂 결재 상신 대기 중...</div></div>', unsafe_allow_html=True)
        if st.button("🚀 결재 상신"):
            st.session_state.app_state = "RUNNING"
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()

else:
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        st.markdown('<div class="boss-box">', unsafe_allow_html=True)
        st.image(Image.open(face_file))
        st.markdown('</div>', unsafe_allow_html=True)

    cat_name, menu_name = st.session_state.current_menu
    st.markdown(f'''
        <div class="mac-window">
            <div class="menu-display">
                <div class="menu-text">[{cat_name}]<br>{menu_name}</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ 반려"):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()
    with col2:
        if st.button("✅ 승인"):
            st.session_state.final_choice = f"{cat_name} - {menu_name}"
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
