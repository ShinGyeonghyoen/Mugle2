import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정: 모바일 최적화] ---
st.set_page_config(page_title="Mugle AI", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 태그 노출 원천 봉쇄 및 콤팩트 레이아웃] ---
st.markdown("""
    <style>
    /* 전체 배경 및 여백 설정 */
    .block-container { padding: 0.5rem !important; }
    .stApp { background: #1C1C1E; }

    /* 로고 섹션: 사과 로고 복구 */
    .logo-container { 
        text-align: center; padding: 15px 0; font-size: 32px; font-weight: 900;
        display: flex; justify-content: center; align-items: center; gap: 10px;
    }
    
    /* 맥 윈도우 스타일 메뉴창 (태그 노출 방지를 위해 최소화) */
    .mac-window {
        background: #2C2C2E; border-radius: 14px;
        padding: 10px; border: 1px solid #38383A; margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* 룰렛 애니메이션 */
    @keyframes roulette {
        0% { transform: scale(0.98); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }

    .menu-display {
        background: #F2F2F7; border-radius: 10px; padding: 30px 10px; 
        text-align: center; animation: roulette 0.2s ease-out;
    }

    /* 텍스트 가독성 강화 */
    .menu-text {
        margin: 0; font-weight: 800; color: #1C1C1E !important; 
        font-size: 24px; line-height: 1.4;
    }

    .shaming-text { color: #FF453A; font-weight: 700; font-size: 15px; text-align: center; margin-bottom: 10px; }

    /* 버튼: 모바일 무조건 1줄 배치 (50:50) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; gap: 10px !important;
    }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 50% !important; }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 12px !important;
        font-size: 17px !important; font-weight: 700 !important; border: none !important;
    }
    /* 반려 버튼 */
    div.stButton:nth-child(1) > button { background: #3A3A3C !important; color: #FFFFFF !important; }
    /* 승인 버튼 */
    div.stButton:nth-child(2) > button { background: #0A84FF !important; color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메뉴 데이터베이스 유지] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반", "쇼가야키", "함바그", "야키니쿠", "규카츠", "가라아게", "돼지김치볶음"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "츠케멘", "아부라소바", "탄탄멘", "냉소바", "카레 우동", " 파슷하"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "비프 카레", "카츠 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "카레", "가파오라이스", "팟타이", "쌀국수"],
    "🏪 편의점/로컬": ["로슨 카라아게", "세븐 나나치키", "패미마 치킨", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["샐러드", "서브웨이", "포케 볼", "생선구이", " 맥도날드", "버거킹", "KFC",  "미역국"],
    "👨‍🍳 백종원": ["홍콩 반점", "새마을 식당", "조보아씨 내려와 봐유", "빽다방", "돌아갈까봐 그래유"]
}

shaming_comments = ["안목이 이것뿐인가?", "박 대리, 서류 미비일세!", "반려하겠네.", "그럴싸쥬?", "두잔 마시고 시작하게", " 내 성격 까먹었나 보네", "오늘 회식가게도 자네가 잡게"]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")
if 'spinning' not in st.session_state: st.session_state.spinning = False

def get_boss_image(count):
    idx = min(count, 4)
    # 로컬 경로 및 파일명 패턴 대응
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---

# 1) 로고 섹션 (사과 로고 복구)
st.markdown('<div class="logo-container">🍎 <span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span> 🍎</div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding: 40px 10px; color:white;">📂 상신 대기 중...</div>', unsafe_allow_html=True)
    if st.button("🚀 결재 상신"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()
else:
    # 2) 룰렛 애니메이션 효과
    if st.session_state.spinning:
        placeholder = st.empty()
        for _ in range(8):
            cat = random.choice(list(menu_pool.keys()))
            menu = random.choice(menu_pool[cat])
            placeholder.markdown(f'<div class="mac-window"><div class="menu-display"><div class="menu-text">[{cat}]<br>{menu}</div></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
        st.rerun()

    # 3) 지점장 이미지 섹션 (복구 완료)
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        # 모바일 최적화를 위해 컬럼을 활용한 자동 스케일링
        _, mid, _ = st.columns([1, 8, 1])
        with mid:
            st.image(Image.open(face_file), use_container_width=True)

    # 4) 메뉴 표시창 (버그 수정 핵심: 문자열 결합 방식 변경)
    cat_name, menu_name = st.session_state.current_menu
    display_html = f'''
        <div class="mac-window">
            <div class="menu-display">
                <div class="menu-text">[{cat_name}]<br>{menu_name}</div>
            </div>
        </div>
    '''
    st.markdown(display_html, unsafe_allow_html=True)

    # 5) 반려 코멘트
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)} ({st.session_state.reject_count}회)</div>', unsafe_allow_html=True)

    # 6) 하단 버튼 (모바일 1줄 배치 고정)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ 반려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.rerun()
    with col2:
        if st.button("✅ 승인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
