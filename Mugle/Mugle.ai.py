import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
# 아이폰 한 화면에 담기 위해 padding과 간격을 최소화하는 컴팩트 설정
st.set_page_config(
    page_title="Mugle AI - Mac OS 에디션", 
    page_icon="🍎", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- [2. 맥북 스타일 UI & 애플 로고 & 한 화면 최적화] ---
st.markdown("""
    <style>
    /* 전체 배경: Mac OS의 따뜻한 느낌의 회색 */
    .main { background-color: #F5F5F7; color: #1D1D1F; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* Mugle 로고 + 애플 로고: 미니멀하면서 엣지있게 */
    .logo-container { 
        text-align: center; padding: 5px 0 10px 0; display: flex; justify-content: center; align-items: center; 
        font-size: 28px; font-weight: 800;
    }
    .apple-logo {
        font-size: 20px; color: #555; margin: 0 8px; /* 깨문 사과 모양 삽입 */
    }
    
    /* 맥북 창 스타일 (카드): 크기를 줄이고 둥근 모서리 최적화 */
    .mac-window {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 10px; margin-bottom: 12px;
        border: 1px solid #EAEAEA;
    }
    
    /* Mac OS 타이틀 바 (신호등 버튼 추가) */
    .mac-title-bar {
        height: 20px; border-bottom: 1px solid #EAEAEA; margin-bottom: 10px; display: flex; align-items: center;
    }
    .dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 4px; }
    .dot-red { background-color: #FF5F57; }
    .dot-yellow { background-color: #FEBC2E; }
    .dot-green { background-color: #28C840; }

    /* 메뉴 표시창: 컴팩트하게 축소 */
    .menu-display {
        background-color: #FAFAFA;
        border-radius: 8px; padding: 15px; text-align: center; margin: 5px 0;
        border: 1px solid #EDEDED;
    }

    /* 맥북 버튼 스타일 (가로 나열 최적화) */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #1D1D1F !important;
        border-radius: 8px !important;
        border: 1px solid #DEDEDE !important;
        font-weight: 600 !important;
        height: 40px !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        border-color: #4285F4 !important; color: #4285F4 !important; background-color: #F0F6FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 매머드급 메뉴 데이터베이스 유지] ---
menu_pool = {
    "일식 정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 소금구이", "임면수어 구이", "미소카츠", "토리카라아게 정식", "연어 미소즈케 구이", "굴튀김 정식"],
    "덮밥/돈부리": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥", "회덮밥", "로스트비프동"],
    "면요리": ["소유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", "아부라소바", "냉소바", "자루우동", "카레우동", "야끼소바", "탄탄멘"],
    "중식/에스닉": ["마파두부 정식", "호이코로", "에비칠리 정식", "교자 볶음밥 세트", "칭쟈오로스", "타이 카레", "가파오라이스", "팟타이", "베트남 쌀국수", "나시고랭"],
    "양식": ["비프 카레", "치킨 카레", "오무라이스", "나폴리탄 파스타", "미트소스 파스타", "명란 크림 파스타", "수제버거 세트", "마르게리따 피자"],
    "편의점/로컬": ["로손 카라아게군", "패밀리마트 도시락", "세븐 야키소바빵", "마트 타임세일 스시", "서브웨이", "신오쿠보 떡볶이"]
}

shaming_comments = [
    "박 대리, 이 메뉴는 LTV 비율이 너무 낮아. 반려!", "지금 메뉴 고르는 속도로 대출 심사하면 우리 지점 망해.", 
    "서류 미비! 일본까지 와서 결정을 못 하나?", "자꾸 반려하면 오늘 점심은 탕비실 믹스커피다.", 
    "지점장님: '박 대리는 점심 메뉴도 컴플라이언스 위반인가?'", "허허, 박 대리. 자네 안목이 이것밖에 안 됐나?"
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

# --- [6. UI 구성: 한 화면 최적화 배치] ---

# 로고 섹션 (로고 크기 축소 + 애플 로고 양옆 삽입)
st.markdown('<div class="logo-container"><span class="apple-logo"></span><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span><span class="apple-logo"></span></div>', unsafe_allow_html=True)

if st.session_state.app_state == "READY":
    # --- 1단계: 서류 상신 대기 화면 (심플하게 축소) ---
    st.markdown('<div class="mac-window" style="text-align:center;"><div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div><h4 style="margin:5px 0;">📥 결재 서류 대기 중</h4><p style="font-size:12px; color:#555;">심사를 시작하려면 아래 버튼을 누르십시오.</p></div>', unsafe_allow_html=True)
    if st.button("📄 서류 상신 (심사 시작)"):
        st.session_state.app_state = "RUNNING"
        cat = random.choice(list(menu_pool.keys()))
        st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
        st.rerun()

else:
    # --- 2단계: 메인 결재 화면 ---
    
    # 지점장님 사진 크기 축소 (양옆 여백을 더 넓게 줘서 사진 사이즈를 눈에 띄게 줄임)
    face_file = get_boss_image(st.session_state.reject_count)
    col_img_left, col_img_mid, col_img_right = st.columns([1.8, 3.4, 1.8])
    with col_img_mid:
        if face_file:
            # use_container_width=True로 유지하되 columns 비율로 크기 조정
            st.image(Image.open(face_file), use_container_width=True)

    # 메뉴 표시창 (Mac OS 스타일, 컴팩트 축소)
    st.markdown(f"""
        <div class="mac-window">
            <div class="mac-title-bar"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div style="font-size:10px; color:#888; text-align:right;">심사 중인 메뉴</div>
            <div class="menu-display">
                <h3 style="color:#1D1D1F; margin:0; font-weight:700;">{st.session_state.current_menu}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 독설 멘트
    if st.session_state.reject_count > 0:
        st.markdown(f'<p style="color:#FF1744; font-weight:600; font-size:12px; text-align:center; margin-top:0;">💭 지점장님: {st.session_state.last_comment}</p>', unsafe_allow_html=True)

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
