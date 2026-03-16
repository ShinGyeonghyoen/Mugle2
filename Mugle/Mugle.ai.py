import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Compact Mobile", page_icon="🍎", layout="centered")

# --- [2. UI/UX 디자인: 크기 최적화 및 로고 위치 조정] ---
st.markdown("""
    <style>
    /* 상단 여백 최소화 */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    
    @keyframes rouletteEffect {
        0% { transform: translateY(-10px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    .stApp {
        background: linear-gradient(180deg, #1C1C1E 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* 로고 위치 하향 조정 및 양옆 사과 아이콘 추가 */
    .logo-container { 
        text-align: center; 
        padding-top: 40px; /* 로고 위치 소폭 밑으로 조정 */
        padding-bottom: 10px;
        font-size: 42px; /* 로고 크기 축소 */
        font-weight: 900;
        letter-spacing: -1px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
    }
    .bite-apple { font-size: 30px; opacity: 0.9; }
    
    /* 사진 및 윈도우 크기 축소 */
    .mac-window {
        background: rgba(45, 45, 48, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
        padding: 10px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 5px;
    }

    /* 메뉴 표시창: 폰트 소폭 축소 및 패딩 최적화 */
    .menu-display {
        background: rgba(0, 0, 0, 0.5); border-radius: 8px; padding: 15px 5px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);
        animation: rouletteEffect 0.3s ease-out;
    }

    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF !important; 
        font-size: 20px; /* 폰트 크기 축소 */
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
    }

    .shaming-text {
        color: #FF453A; font-weight: 700; font-size: 14px;
        text-align: center; margin: 5px 0;
    }

    /* ⭐ 버튼 1줄 강제 구현 (Flexbox 사용) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* 무조건 가로 정렬 */
        flex-wrap: nowrap !important; /* 줄바꿈 금지 */
        gap: 8px !important;
    }
    
    div[data-testid="stHorizontalBlock"] > div {
        width: 50% !important; /* 가로 절반씩 점유 */
        flex: 1 1 auto !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 48px !important;
        border-radius: 10px !important; font-size: 15px !important;
        font-weight: 700 !important; border: none !important;
        padding: 0 !important; /* 버튼 내 여백 제거로 텍스트 잘림 방지 */
    }
    
    div.stButton:nth-child(1) > button { background: rgba(255, 255, 255, 0.15) !important; color: #FFFFFF !important; }
    div.stButton:nth-child(2) > button { background: #0A84FF !important; color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메가 데이터베이스: 유지] ---
menu_pool = {
    "🥩 고기/정식": [
        "돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", 
        "함바그 스테이크", "야키니쿠 정식", "우시카츠(규카츠)", "닭갈비 정식", 
        "가라아게 정식", "스테이크 쥬", "돼지김치볶음 정식", "멘치카츠"
    ],
    "🍜 면요리": [
        "쇼유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", 
        "아부라소바", "탄탄멘", "냉소바(자루소바)", "덴푸라 우동", "카레 우동", 
        "야키소바", "나폴리탄 파스타", "까르보나라", "봉골레 파스타", "미트소스 파스타"
    ],
    "🍚 덮밥/카레": [
        "규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", 
        "카이센동", "스테이크 덮밥", "마파두부 덮밥", "비프 카레", "드라이 카레", 
        "카츠 카레", "에비 카레", "회덮밥", "장어덮밥(우나쥬)"
    ],
    "🥢 중식/에스닉": [
        "마파두부 정식", "호이코로 정식", "에비칠리 정식", "칭쟈오로스", 
        "산쥬로 정식", "탕수육(스부타)", "교자 세트", "타이 그린 카레", 
        "가파오라이스", "팟타이", "나시고랭", "포(베트남 쌀국수)"
    ],
    "🏪 편의점/로컬": [
        "로슨 카라아게군", "세븐일레븐 나나치키", "패밀리마트 치킨", 
        "편의점 오뎅 세트", "삼각김밥 & 컵라면", "도큐스토어 도시락", 
        "요시노야 세트", "마츠야 규메시", "스키야 치즈규동"
    ],
    "🥗 건강/가벼운": [
        "시저 샐러드", "서브웨이 샌드위치", "포케 볼", "두부 스테이크 정식", 
        "오늘의 생선구이 정식", "미역국밥", "메밀싹 비빔밥" 
    ],
    "🥗 백종원": [
        "홍콩 반점", "새마을 식당/ 김치찌개", "조보아씨 내려와봐유", 
        "빽다방", "돌아갈까봐 그래유", "꽝이쥬?" 
    ]
}

shaming_comments = ["안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비!", "다시 골라오게.", "컴플라이언스 위반인가?"]

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

# --- [4. UI 구성: 듀얼 로고 적용] ---
st.markdown(f'''
    <div class="logo-container">
        <span class="bite-apple">🍎</span>
        <span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span>
        <span class="bite-apple">🍎</span>
    </div>
    ''', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center; padding:15px;"><h5 style="color:white; margin:0;">📥 결재 대기 중</h5></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()
else:
    if st.session_state.spinning:
        placeholder = st.empty()
        for _ in range(8):
            cat = random.choice(list(menu_pool.keys()))
            temp = f"[{cat}] {random.choice(menu_pool[cat])}"
            placeholder.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{temp}</h2></div></div>', unsafe_allow_html=True)
            time.sleep(0.1)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

    # 지점장 이미지: 가로 세로 비율 유지하며 소폭 축소
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([2.5, 4, 2.5])
    with c2:
        if face_file: st.image(Image.open(face_file), use_container_width=True)

    st.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{st.session_state.current_menu}</h2></div></div>', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)}</div>', unsafe_allow_html=True)

    # 버튼 레이아웃: 강제 1줄 배치
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("⚖️ 반려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.rerun()
    with b_col2:
        if st.button("✅ 승인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
