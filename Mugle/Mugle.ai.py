import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정: 모바일 뷰포트 최적화] ---
st.set_page_config(page_title="Mugle AI - Master Paik", page_icon="🍎", layout="centered")

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

    /* Mugle 로고: 크기 최적화 및 위치 상향 */
    .logo-container { 
        text-align: center; padding-top: 10px; padding-bottom: 5px;
        font-size: 38px; font-weight: 900;
        display: flex; justify-content: center; align-items: center; gap: 10px;
    }
    
    /* 신사과 로고: 한 입 베어 문 사과 */
    .bite-apple {
        font-size: 28px; opacity: 0.9;
    }
    
    /* 지점장 이미지: 모바일 크기 최적화 */
    .boss-img-container {
        display: flex; justify-content: center; margin-bottom: 10px;
    }
    .boss-img-container img {
        max-width: 80% !important; border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    /* 맥북 다크 윈도우 스타일 (Dark Gray) */
    .mac-window {
        background: rgba(45, 45, 48, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 12px; padding: 12px; 
        border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 10px;
    }

    /* 메뉴 표시창: 룰렛 애니메이션 2초 적용 */
    .menu-display {
        background: rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 20px 5px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
        animation: rouletteSlide 2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* 고대비 메뉴 텍스트: 완전 화이트 적용 */
    .menu-text {
        margin: 0; font-weight: 800; color: #FFFFFF !important; 
        font-size: 22px; line-height: 1.4;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }

    /* 반려 독설 텍스트 */
    .shaming-text { color: #FF453A; font-weight: 700; font-size: 14px; text-align: center; margin-bottom: 10px; }

    /* ⭐ 버튼 칼각: 메뉴창 너비 50%씩 꽉 차게 고정 (Flexbox) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; align-items: center !important;
        gap: 8px !important;
    }
    
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 50% !important;
        min-width: 0 !important;
    }
    
    div.stButton > button {
        width: 100% !important; height: 48px !important;
        border-radius: 10px !important; font-size: 16px !important;
        font-weight: 700 !important; border: none !important;
    }
    
    /* 반려 버튼 (iOS 다크 그레이) */
    div.stButton:nth-child(1) > button { background: rgba(255, 255, 255, 0.1) !important; color: #FFFFFF !important; }
    /* 승인 버튼 (iOS 블루) */
    div.stButton:nth-child(2) > button { background: #0A84FF !important; color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 통합 데이터베이스] ---
menu_pool = {
    "🥩 고기/정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반", "쇼가야키", "함바그", "야키니쿠", "규카츠", "가라아게", "돼지김치볶음"],
    "🍜 면요리": ["쇼유 라멘", "돈코츠 라멘", "미소 라멘", "츠케멘", "아부라소바", "탄탄멘", "냉소바", "카레 우동", "파스타"],
    "🍚 덮밥/카레": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "비프 카레", "카츠 카레", "장어덮밥"],
    "🥢 중식/에스닉": ["마파두부", "호이코로", "에비칠리", "교자 세트", "타이 카레", "가파오라이스", "팟타이", "쌀국수"],
    "🏪 편의점/로컬": ["로슨 카라아게", "세븐 나나치키", "패미마 치킨", "편의점 오뎅", "요시노야", "마츠야", "스키야"],
    "🥗 건강/가벼운": ["시저 샐러드", "서브웨이", "포케 볼", "두부 스테이크", "생선구이", "미역국밥"]
}

shaming_comments = ["안목이 이것뿐인가?", "박 대리, 서류 미비일세!", "반려하겠네.", "다시 골라오게."]

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")

def get_boss_image(count):
    idx = min(count, 4)
    # 이미지 파일 경로 확인 로직 (local/github 대응)
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---

# 로고 (신사과 로고 복구)
st.markdown('<div class="logo-container"><span class="bite-apple">🍎</span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center;"><h5 style="color:white; margin:0;">📥 서류 상신 대기 중</h5></div>', unsafe_allow_html=True)
    if st.button("📄 결재 상신"):
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
        st.session_state.app_state = "RUNNING"
        st.rerun()
else:
    # 지점장 이미지
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        st.markdown('<div class="boss-img-container">', unsafe_allow_html=True)
        st.image(Image.open(face_file))
        st.markdown('</div>', unsafe_allow_html=True)

    # 메뉴 표시창 (룰렛 애니메이션 적용)
    cat_name, menu_name = st.session_state.current_menu
    st.markdown(f'''
        <div class="mac-window">
            <div class="menu-display">
                <div class="menu-text">[{cat_name}]<br>{menu_name}</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 반려 코멘트 복구
    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)} ({st.session_state.reject_count}회 반려)</div>', unsafe_allow_html=True)

    # 버튼: 무조건 1줄 배치 (Flexbox)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚖️ 반려"):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
            st.rerun()
    with col2:
        if st.button("✅ 승인"):
            st.balloons()
            time.sleep(1)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
            # --- [기존 코드의 승인(READY) 섹션 수정] ---

if st.session_state.app_state == "READY":
    if st.session_state.final_choice:
        st.balloons()
        
        # 🎰 파칭코 피버 + GIF 세리머니
        st.markdown(f'''
            <div class="fever-window">
                <div class="menu-display">
                    <div class="menu-text" style="color:#FFD700 !important; font-size:24px;">🎰 승인 확정! 🎰</div>
                    <div class="menu-text" style="padding: 15px 0;">오늘 점심은<br><span style="font-size:26px; color:#0A84FF;">{st.session_state.final_choice}</span></div>
                    
                    <div style="display: flex; justify-content: center; padding: 10px 0;">
                        <img src="{https://github.com/ShinGyeonghyoen/Mugle2/blob/main/Mugle/dance.gif}" style="width: 100%; border-radius: 12px; border: 2px solid #FFD700;">
                    </div>
                    
                    <div class="menu-text" style="font-size:14px; color:#32CD32; margin-top:5px;">🕺 기쁨의 춤사위 발동! 💃</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
