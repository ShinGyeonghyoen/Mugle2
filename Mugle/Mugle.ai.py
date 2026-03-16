import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - 지점장님 결재함", page_icon="📠", layout="centered")

# --- [2. 윈도우 98 클래식 스타일 & 로고 강화] ---
st.markdown("""
    <style>
    .main { background-color: #C0C0C0; color: black; font-family: 'MS Sans Serif', 'Tahoma', sans-serif; }
    
    /* 로고 크기 대폭 확대 (80px) */
    .logo-text { 
        font-size: 80px; font-weight: 900; text-align: center; 
        padding: 20px 0; margin-bottom: 10px;
        filter: drop-shadow(2px 2px 0px #ffffff);
    }
    
    /* 윈도우 98 시스템 창 스타일 */
    .win-window {
        background-color: #C0C0C0;
        border-top: 2px solid #ffffff; border-left: 2px solid #ffffff;
        border-bottom: 2px solid #808080; border-right: 2px solid #808080;
        padding: 15px; margin-bottom: 20px;
    }
    
    .menu-display {
        background-color: #ffffff;
        border-top: 2px solid #808080; border-left: 2px solid #808080;
        border-bottom: 2px solid #ffffff; border-right: 2px solid #ffffff;
        padding: 25px; text-align: center; margin: 10px 0;
    }

    /* 윈도우 98 버튼 스타일 */
    .stButton > button {
        background-color: #C0C0C0 !important;
        color: black !important;
        border-top: 2px solid #ffffff !important; border-left: 2px solid #ffffff !important;
        border-bottom: 2px solid #808080 !important; border-right: 2px solid #808080 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 100% !important;
    }
    .stButton > button:active {
        border-top: 2px solid #808080 !important; border-left: 2px solid #808080 !important;
        border-bottom: 2px solid #ffffff !important; border-right: 2px solid #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 매머드급 메뉴 데이터베이스 복구] ---
menu_pool = {
    "일식 정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 소금구이", "임면수어 구이", "미소카츠", "토리카라아게 정식", "연어 미소즈케 구이", "굴튀김 정식"],
    "덮밥/돈부리": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥", "회덮밥", "로스트비프동"],
    "면요리": ["소유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", "아부라소바", "냉소바", "자루우동", "카레우동", "야끼소바", "탄탄멘"],
    "중식/에스닉": ["마파두부 정식", "호이코로", "에비칠리 정식", "교자 볶음밥 세트", "칭쟈오로스", "타이 카레", "가파오라이스", "팟타이", "베트남 쌀국수", "나시고랭"],
    "양식": ["비프 카레", "치킨 카레", "오무라이스", "나폴리탄 파스타", "미트소스 파스타", "명란 크림 파스타", "수제버거 세트", "마르게리따 피자"],
    "편의점/로컬": ["로손 카라아게군", "패밀리마트 도시락", "세븐 야키소바빵", "마트 타임세일 스시", "서브웨이", "신오쿠보 떡볶이"]
}

shaming_comments = [
    "박 대리, 이 메뉴는 LTV 비율이 너무 낮아. 반려!",
    "지금 메뉴 고르는 속도로 대출 심사하면 우리 지점 망해.",
    "서류 미비! 일본까지 와서 결정을 못 하나?",
    "자꾸 반려하면 오늘 점심은 탕비실 믹스커피다.",
    "지점장님: '박 대리는 점심 메뉴도 컴플라이언스 위반인가?'",
    "허허, 박 대리. 자네 안목이 이것밖에 안 됐나?"
]

# --- [4. 세션 상태 관리] ---
if 'app_state' not in st.session_state: st.session_state.app_state = "READY"
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = ""
if 'last_comment' not in st.session_state: st.session_state.last_comment = ""

# --- [5. 사진 경로 찾기 함수] ---
def get_boss_image(count):
    idx = min(count, 4)
    search_paths = [f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png", f"face_{idx}.jpg", f"face_{idx}.png"]
    for p in search_paths:
        if os.path.exists(p): return p
    return None

# --- [6. UI 구성] ---

# 로고 섹션 (80px 강화)
st.markdown('<div class="logo-text"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    # --- 1단계: 서류 상신 대기 화면 ---
    st.markdown('<div class="win-window" style="text-align:center;"><h3>📥 신규 결재 서류 대기 중</h3><p>심사를 시작하려면 아래 버튼을 누르십시오.</p></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신 (심사 시작)"):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

else:
    # --- 2단계: 메인 결재 화면 ---
    
    # 사진 크기 축소 (중앙 배치)
    face_file = get_boss_image(st.session_state.reject_count)
    col_img_left, col_img_mid, col_img_right = st.columns([1, 4, 1])
    with col_img_mid:
        if face_file:
            st.image(Image.open(face_file), use_container_width=True)

    # 메뉴 표시창
    st.markdown(f"""
        <div class="win-window">
            <div style="background-color:#000080; color:white; padding:2px 5px; font-size:12px; font-weight:bold;">Mugle_Approval_System.exe</div>
            <div class="menu-display">
                <h2 style="color:black; margin:0;">{st.session_state.current_menu}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 킹받는 독설
    if st.session_state.reject_count > 0:
        st.markdown(f'<p style="color:red; font-weight:bold; text-align:center;">🗯️ {st.session_state.last_comment}</p>', unsafe_allow_html=True)

    # 버튼 가로 배치 (1행)
    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        if st.button("⚖️ 반려 / 재심사"):
            st.session_state.reject_count += 1
            cat = random.choice(list(menu_pool.keys()))
            st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
            st.session_state.last_comment = random.choice(shaming_comments)
            st.rerun()

    with btn_col2:
        if st.button("✅ 최종 승인 (Accept)"):
            st.balloons()
            st.success("결재 완료! 맛있게 드십시오.")
            time.sleep(2)
            st.session_state.app_state = "READY"
            st.session_state.reject_count = 0
            st.rerun()
