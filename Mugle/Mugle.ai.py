import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정: 모바일 뷰포트 최적화] ---
st.set_page_config(page_title="Mugle AI - Full Fix", page_icon="🍱", layout="centered")

# --- [2. UI/UX 디자인: 리퀴드 글래스 & 칼각 버튼 & 애니메이션] ---
st.markdown("""
    <style>
    /* 여백 최소화 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    
    /* 룰렛 애니메이션: 2초간 위아래로 튕기며 회전하는 효과 */
    @keyframes rouletteSlide {
        0% { transform: translateY(-50px); opacity: 0; }
        15% { transform: translateY(0); opacity: 1; }
        25% { transform: translateY(-10px); }
        35% { transform: translateY(0); }
        45% { transform: translateY(-5px); }
        55% { transform: translateY(0); }
        65% { transform: translateY(-2px); }
        100% { transform: translateY(0); }
    }

    /* iOS 스타일의 세련된 다크 배경 (Midnight Blue Gradient) */
    .stApp {
        background: linear-gradient(180deg, #1C1C1E 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* Mugle 로고: 크기 최적화 */
    .logo-container { 
        text-align: center; padding: 15px 0; font-size: 60px; font-weight: 900;
        letter-spacing: -1.5px;
    }
    
    /* 맥북 다크 윈도우 스타일 (Dark Gray) */
    .mac-window {
        background-color: #1C1C1E; border-radius: 14px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
        padding: 15px; border: 1px solid #38383A; margin-bottom: 10px;
    }
    
    .mac-title-bar { height: 18px; margin-bottom: 12px; display: flex; align-items: center; }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 룰렛 애니메이션 2초 적용 */
    .menu-display {
        background: rgba(0, 0, 0, 0.4); border-radius: 10px; padding: 25px 10px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
        animation: rouletteSlide 2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* 고대비 메뉴 텍스트: 완전 화이트 적용 */
    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF !important; 
        font-size: 24px; text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }

    .paik-logo {
        width: 40px; margin-bottom: 8px; border-radius: 50%;
    }

    /* 독설 텍스트 */
    .shaming-text {
        color: #FF453A; font-weight: 700; font-size: 16px;
        text-align: center; margin: 10px 0;
    }

    /* ⭐ 버튼 칼각: 메뉴창 너비 50%씩 꽉 차게 고정 (Flexbox) */
    [data-testid="stHorizontalBlock"] {
        gap: 8px !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        border-radius: 10px !important; font-size: 17px !important;
        font-weight: 700 !important; border: none !important;
        margin-top: 5px !important;
    }
    
    /* 반려 버튼 (iOS 다크 그레이) */
    div.stButton:nth-child(1) > button {
        background: rgba(255, 255, 255, 0.15) !important; color: #FFFFFF !important;
    }
    /* 승인 버튼 (iOS 블루) */
    div.stButton:nth-child(2) > button {
        background: #0A84FF !important; color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 메가 데이터베이스: Full Menu 복구] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "함바그 스테이크", "야키니쿠 정식", "가라아게 정식", "스테이크 쥬", "돼지김치볶음 정식", "멘치카츠", "규카츠"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", "아부라소바", "탄탄멘", "냉소바", "덴푸라 우동", "카레 우동", "야키소바", "나폴리탄 파스타", "까르보나라", "봉골레", "미트소스"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥", "마파두부 덮밥", "비프 카레", "드라이 카레", "카츠 카레", "에비 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부 정식", "호이코로 정식", "에비칠리 정식", "칭쟈오로스", "산쥬로 정식", "탕수육(스부타)", "교자 세트", "타이 그린 카레", "가파오라이스", "팟타이", "나시고랭", "포(쌀국수)"],
    "🏪 편의점/로컬": ["로슨 카라아게군", "세븐 나나치키", "패미마 치킨", "편의점 오뎅", "삼각김밥&컵라면", "도큐스토어 도시락", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["시저 샐러드", "서브웨이", "포케 볼", "두부 스테이크", "생선구이 정식", "미역국밥", "메밀싹 비빔밥"],
    "👨‍🍳 백종원": ["홍콩 반점", "새마을 식당 / 김치찌개", "조보아씨 내려와봐유", "빽다방", "돌아갈까봐 그래유", "꽝이쥬?"]
}

shaming_comments = ["안목이 이것밖에 안 됐나?", "박 대리, 반려!", "서류 미비!", "다시 골라오게.", "컴플라이언스 위반인가?", "그럴싸쥬?"]
paik_logo_url = "http://googleusercontent.com/image_collection/image_retrieval/12235863623553003209_0"

# --- [4. 상태 관리] ---
if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")
if 'spinning' not in st.session_state: st.session_state.spinning = False

def get_boss_image(count):
    idx = min(count, 4)
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [5. UI 구성] ---

# 로고
st.markdown('<div class="logo-container"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center;"><h5 style="color:white; margin:0;">📥 상신 대기 중...</h5></div>', unsafe_allow_html=True)
    if st.button("📄 결재 상신"):
        st.session_state.app_state = "RUNNING"
        st.session_state.spinning = True
        st.rerun()
else:
    # 2초 룰렛 시스템 완전 복구
    if st.session_state.spinning:
        placeholder = st.empty()
        for _ in range(12): # 룰렛 지속 시간 상향
            cat = random.choice(list(menu_pool.keys()))
            temp = f"[{cat}] {random.choice(menu_pool[cat])}"
            placeholder.markdown(f'<div class="mac-window"><div class="menu-display"><h2 class="menu-text">{temp}</h2></div></div>', unsafe_allow_html=True)
            time.sleep(0.12)
        st.session_state.spinning = False
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
        st.rerun()

    # 지점장 용안 완전 복구 (Columns 비율 최적화로 부담 줄임)
    face_file = get_boss_image(st.session_state.reject_count)
    c1, c2, c3 = st.columns([1.5, 4, 1.5])
    with c2:
        if face_file:
            # use_container_width=True로 유지하되 c2 너비에 맞춰 크기 조정
            st.image(Image.open(face_file), use_container_width=True)

    # 메뉴 표시창
    cat_name, menu_name = st.session_state.current_menu
    paik_html = f'<img src="{paik_logo_url}" class="paik-logo"><br>' if cat_name == "👨‍🍳 백종원" else ""
    
    st.markdown(f'''
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="menu-display">
                {paik_html}
                <h2 class="menu-text">[{cat_name}]<br>{menu_name}</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # 킹받는 독설
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)} ({st.session_state.reject_count}회)</div>', unsafe_allow_html=True)

    # 하단 버튼: 무조건 1줄 배치 (50:50 정렬)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("⚖️ 반 려"):
            st.session_state.reject_count += 1
            st.session_state.spinning = True
            st.rerun()
    with b_col2:
        if st.button("✅ 승 인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
