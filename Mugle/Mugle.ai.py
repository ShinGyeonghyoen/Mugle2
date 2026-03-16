import streamlit as st
import random
from PIL import Image
import os
import time

# --- [1. 페이지 설정] ---
st.set_page_config(page_title="Mugle AI - 모바일 지점장", page_icon="🍱", layout="centered")

# --- [2. UI/UX 디자인 주입] ---
st.markdown("""
    <style>
    .main { background-color: #1A1A1A; color: #E0E0E0; }
    .logo-text { font-size: 50px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .neo-card {
        background: #222222; border-radius: 20px; padding: 25px;
        box-shadow: inset 2px 2px 5px #2b2b2b, inset -2px -2px 5px #101010;
        border: 1px solid #333; text-align: center; margin-bottom: 20px;
    }
    /* 반려 버튼 (레드 포인트) */
    div.stButton > button:first-child {
        width: 100%; height: 65px; border-radius: 15px; background: #222222;
        color: #FF5252; font-weight: 800; border: 1px solid #442222;
        box-shadow: 5px 5px 10px #101010, -5px -5px 10px #2a2a2a;
        font-size: 18px;
    }
    /* 승인 버튼 (블루 포인트) */
    div.stButton > button:last-child {
        width: 100%; height: 50px; border-radius: 12px; background: #222222;
        color: #4285F4; font-weight: 700; border: 1px solid #223344;
        box-shadow: 3px 3px 6px #101010, -3px -3px 6px #2a2a2a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [3. 킹받는 독설 데이터베이스] ---
shaming_comments = [
    "박 대리, 이 메뉴는 LTV 비율이 너무 낮아. 반려!",
    "지금 메뉴 고르는 속도로 대출 심사하면 우리 지점 망해.",
    "서류 미비! 일본까지 와서 결정을 못 하나?",
    "자꾸 반려하면 오늘 점심은 탕비실 믹스커피다.",
    "지점장님: '박 대리는 점심 메뉴도 컴플라이언스 위반인가?'",
    "이건 뭐... 거의 부실 채권 급 메뉴구만.",
    "박 대리, 자네 인사고과에 '결정장애'라고 적어도 되나?",
    "점심 메뉴 고르는 게 외환 송금보다 어렵나?",
    "심사 탈락. 내 입맛은 자네 생각보다 훨씬 High-End라네.",
    "이 메뉴는 승인 조건 미달이야. 다시 가져오게.",
    "박 대리, 혹시 월급 루팡인가? 점심에만 진심이군.",
    "허허, 박 대리. 자네 안목이 이것밖에 안 됐나?"
]

menu_pool = {
    "일식 정식": ["돈카츠 정식", "로스카츠", "히레카츠", "치킨난반 정식", "쇼가야키 정식", "고등어 소금구이", "임면수어 구이", "연어 미소즈케 구이"],
    "덮밥/돈부리": ["규동", "카츠동", "오야코동", "텐동", "사케동", "네기토로동", "카이센동", "스테이크 덮밥"],
    "면요리": ["소유 라멘", "돈코츠 라멘", "미소 라멘", "시오 라멘", "츠케멘", "아부라소바", "냉소바", "자루우동", "탄탄멘"],
    "중식/에스닉": ["마파두부 정식", "호이코로", "에비칠리 정식", "교자 볶음밥 세트", "칭쟈오로스", "타이 카레", "가파오라이스", "팟타이"],
    "양식/기타": ["비프 카레", "치킨 카레", "오무라이스", "나폴리탄 파스타", "명란 크림 파스타", "수제버거 세트", "마르게리따 피자", "로슨 카라아게군"]
}

# --- [4. 세션 상태 관리] ---
if 'reject_count' not in st.session_state: st.session_state.reject_count = 0
if 'current_menu' not in st.session_state: st.session_state.current_menu = "박 대리, 신규 서류를 상신하게."
if 'last_comment' not in st.session_state: st.session_state.last_comment = ""

# --- [5. 사진/메뉴 로직] ---
def get_boss_image(count):
    idx = min(count, 4)
    search_paths = [f"Mugle/face_{idx}.jpg", f"Mugle/face_{idx}.png", f"face_{idx}.jpg", f"face_{idx}.png", f"Mugle/face_{idx}.JPG", f"face_{idx}.JPG"]
    for p in search_paths:
        if os.path.exists(p): return p
    return None

# --- [6. UI 구성] ---
st.markdown('<div class="logo-text"><span style="color:#4285F4">M</span><span style="color:#EA4335">u</span><span style="color:#FBBC05">g</span><span style="color:#4285F4">l</span><span style="color:#34A853">e</span></div>', unsafe_allow_html=True)

# 사진 출력
face_file = get_boss_image(st.session_state.reject_count)
if face_file:
    st.image(Image.open(face_file), use_container_width=True)

# 메뉴 카드
st.markdown(f'<div class="neo-card"><div style="color:#888;font-size:14px;">심사 중인 메뉴</div><h2 style="margin:10px 0;">{st.session_state.current_menu}</h2></div>', unsafe_allow_html=True)

# 독설 멘트 섹션 (반려 시에만 빨간 상자로 출력)
if st.session_state.reject_count > 0:
    st.error(f"🗯️ {st.session_state.last_comment}")

st.markdown("---")

# 조작 버튼
if st.button("⚖️ ❌ 반 려 / 재 심 사"):
    st.session_state.reject_count += 1
    cat = random.choice(list(menu_pool.keys()))
    st.session_state.current_menu = f"[{cat}] {random.choice(menu_pool[cat])}"
    st.session_state.last_comment = random.choice(shaming_comments) # 버튼 누를 때마다 멘트 교체
    st.rerun()

if st.button("✅ 최 종 승 인 (Accept)"):
    st.balloons()
    st.success("결재 완료! 맛있게 드십시오.")
    time.sleep(2)
    st.session_state.reject_count = 0
    st.session_state.current_menu = "박 대리, 신규 서류를 상신하게."
    st.session_state.last_comment = ""
    st.rerun()
