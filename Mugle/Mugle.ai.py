import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - Full Menu", page_icon="🍱", layout="centered")

# --- [2. 모바일 최적화 CSS] ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    .stApp { background: linear-gradient(180deg, #1C1C1E 0%, #000000 100%); background-attachment: fixed; }
    .logo-container { text-align: center; padding-top: 10px; padding-bottom: 5px; font-size: 32px; font-weight: 900; display: flex; justify-content: center; align-items: center; gap: 8px; }
    .bite-apple { font-size: 24px; }
    .boss-img-container { display: flex; justify-content: center; margin-bottom: 10px; }
    .boss-img-container img { max-width: 80% !important; border-radius: 10px; }
    .mac-window { background: rgba(45, 45, 48, 0.8); backdrop-filter: blur(15px); border-radius: 12px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 10px; }
    .menu-display { background: rgba(0, 0, 0, 0.4); border-radius: 8px; padding: 12px 5px; text-align: center; }
    .menu-text { margin: 0; font-weight: 800; color: #FFFFFF !important; font-size: 18px; line-height: 1.4; }
    .paik-logo { width: 40px; margin-bottom: 8px; border-radius: 50%; }
    .shaming-text { color: #FF453A; font-weight: 700; font-size: 13px; text-align: center; margin-bottom: 10px; }

    /* 버튼 1줄 강제 배치 */
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; align-items: center !important; gap: 8px !important; }
    div[data-testid="stHorizontalBlock"] > div { flex: 1 1 50% !important; min-width: 0 !important; }
    div.stButton > button { width: 100% !important; height: 45px !important; border-radius: 8px !important; font-size: 14px !important; font-weight: 700 !important; padding: 0 !important; white-space: nowrap !important; }
    div.stButton:nth-child(1) > button { background: rgba(255, 255, 255, 0.1) !important; color: #FFFFFF !important; border: 1px solid rgba(255,255,255,0.2) !important; }
    div.stButton:nth-child(2) > button { background: #0A84FF !important; color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 이전 데이터베이스 (Full Menu)] ---
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

if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ("", "")

def get_boss_image(count):
    idx = min(count, 4)
    paths = [f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.jpg"]
    for p in paths:
        if os.path.exists(p): return p
    return None

# --- [4. UI 구성] ---
st.markdown(f'<div class="logo-container"><span class="bite-apple">🍎</span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span><span class="bite-apple">🍎</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    st.markdown('<div class="mac-window" style="text-align:center;"><h5 style="color:white; margin:0;">📥 서류 상신 대기</h5></div>', unsafe_allow_html=True)
    if st.button("📄 결재 상신"):
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = (cat, random.choice(menu_pool[cat]))
        st.session_state.app_state = "RUNNING"
        st.rerun()
else:
    face_file = get_boss_image(st.session_state.reject_count)
    if face_file:
        st.markdown('<div class="boss-img-container">', unsafe_allow_html=True)
        st.image(Image.open(face_file), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    cat_name, menu_name = st.session_state.current_menu
    paik_html = f'<img src="{paik_logo_url}" class="paik-logo"><br>' if cat_name == "👨‍🍳 백종원" else ""
    
    st.markdown(f'''
        <div class="mac-window">
            <div class="menu-display">
                {paik_html}
                <h2 class="menu-text">[{cat_name}]<br>{menu_name}</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    if st.session_state.reject_count > 0:
        st.markdown(f'<div class="shaming-text">🗯️ {random.choice(shaming_comments)} ({st.session_state.reject_count}회)</div>', unsafe_allow_html=True)

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
