import streamlit as st
import random
from PIL import Image
import os

# --- [1. 페이지 설정 및 초기화] ---
st.set_page_config(page_title="Mugle AI - Celebration", page_icon="🍎", layout="centered")

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")
if 'final_choice' not in st.session_state: st.session_state.final_choice = None

# --- [2. 깃허브 영상 주소 설정] ---
# 박 대리님이 깃허브에 올린 파일의 'Raw' 주소를 여기에 붙여넣으세요.
DANCE_VIDEO_URL = "https://raw.githubusercontent.com/ShinGyeonghyeon/Mugle2/main/dance.gif"

# --- [3. UI/UX 디자인 (CSS)] ---
# f-string 충돌 방지를 위해 별도의 문자열로 관리합니다.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { background-color: #000000; font-family: 'Inter', sans-serif; }
    
    .block-container { 
        padding-top: 2.5rem !important; 
        max-width: 450px !important; 
    }

    .logo-container { 
        text-align: center; padding-bottom: 15px; font-size: 28px; font-weight: 900;
        display: flex; justify-content: center; align-items: center; gap: 8px;
    }
    
    .boss-box {
        display: flex; justify-content: center; align-items: center;
        width: 100%; margin-bottom: 12px;
    }
    .boss-box img {
        width: 70% !important; border-radius: 18px;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.08);
    }

    .ios-window {
        background: rgba(44, 44, 46, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 2px;
        border: 0.5px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 12px;
    }
    
    .traffic-lights { display: flex; gap: 5px; padding: 10px 14px; }
    .light { width: 10px; height: 10px; border-radius: 50%; }
    .red { background: #FF5F56; } .yellow { background: #FFBD2E; } .green { background: #27C93F; }

    .menu-display {
        background: rgba(28, 28, 30, 0.6);
        margin: 0 8px 8px 8px;
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
    }

    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF !important; 
        font-size: 20px; line-height: 1.4;
    }

    /* 파칭코 번쩍번쩍 애니메이션 */
    @keyframes feverTime {
        0% { border: 3px solid #0A84FF; box-shadow: 0 0 10px #0A84FF; }
        25% { border: 3px solid #FFD700; box-shadow: 0 0 20px #FFD700; }
        50% { border: 3px solid #FF453A; box-shadow: 0 0 10px #FF453A; }
        75% { border: 3px solid #32CD32; box-shadow: 0 0 20px #32CD32; }
        100% { border: 3px solid #0A84FF; box-shadow: 0 0 10px #0A84FF; }
    }

    .fever-window {
        background: rgba(44, 44, 46, 0.9);
        border-radius: 18px;
        padding: 2px;
        margin-bottom: 15px;
        animation: feverTime 0.3s infinite;
    }

    .celebration-media {
        width: 100%;
        border-radius: 12px;
        margin-top: 10px;
        border: 2px solid #FFD700;
    }

    button {
        height: 50px !important; border-radius: 14px !important;
        font-size: 16px !important; font-weight: 700 !important;
    }
    div.stButton > button { background-color: #0A84FF !important; color: #FFFFFF !important; border: none !important; }
    
    .shaming-text { color: #FF453A; font-weight: 600; font-size: 13px; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [4. 데이터 및 헬퍼 함수] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반", "쇼가야키", "함바그", "야키니쿠", "규카츠", "가라아게", "돼지김치볶음", "제육볶음", "순두부", "김치찌개", "된장찌개"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "츠케멘", "아부라소바", "탄탄멘", "냉소바", "카레 우동", "파슷하"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "비프 카레", "카츠 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "카레", "가파오라이스", "팟타이", "쌀국수"],
    "🏪 편의점/로컬": ["로슨", "세븐일레븐", "훼미리마트", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["샐러드", "서브웨이", "포케 볼", "생선구이", "맥도날드", "버거킹", "KFC", "미역국"],
    "👨‍🍳 백종원": ["홍콩 반점", "새마을 식당", "조보아씨 내려와 봐유", "빽다방", "돌아갈까봐 그래유"]
}

def get_boss_image(count):
    idx = min(count, 4)
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [5. 메인 UI 렌더링] ---

st.markdown('<div class="logo-container">🍎 <span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span> 🍎</div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    if st.session_state.final_choice:
        st.balloons()
        # 최종 승인 결과 (파칭코 연출 + 댄스 영상)
        st.markdown(f'''
            <div class="fever-window">
                <div class="traffic-lights">
                    <div class="light red"></div><div class="light yellow"></div><div class="light green"></div>
                </div>
                <div class="menu-display">
                    <div class="menu-text" style="color:#FFD700 !important; font-size:24px;">🎰 승인 확정! 🎰</div>
                    <div class="menu-text" style="padding: 10px 0;">오늘 점심은<br><span style="font-size:26px; color:#0A84FF;">{st.session_state.final_choice}</span></div>
                    <img src="{DANCE_VIDEO_URL}" class="celebration-media">
                    <div class="menu-text" style="font-size:14px; color:#32CD32; margin-top:10px;">🕺 기쁨의 춤사위 발동! 💃</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        if st.button("🔄 새로운 결재 올리기", use_container_width=True):
            st.session_state.final_choice = None
            st.rerun()
    else:
        st.markdown('<div class="ios-window"><div class="menu-display"><div class="menu-text" style="color:#8E8E93 !important;">📂 결재 상신 대기 중...</div></div></div>', unsafe_allow_html=True)
        if st.button("🚀 결재 상신", use_container_width=True):
            st.session_state.app_state = "RUNNING"
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()

else:
    # 결재 진행 화면 (지점장님 얼굴 + 메뉴)
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        st.markdown('<div class="boss-box">', unsafe_allow_html=True)
        st.image(Image.open(face_file))
        st.markdown('</div>', unsafe_allow_html=True)

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ 반려", use_container_width=True):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()
    with col2:
        if st.button("✅ 승인", use_container_width=True):
            st.session_state.final_choice = f"{cat_name} - {menu_name}"
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
