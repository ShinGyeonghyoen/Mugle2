import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# 사진 전체를 비율에 맞게 조절하기 위해 Pillow 라이브러리가 필요합니다.
try:
    from PIL import Image, ImageTk
except ImportError:
    print("오류: 'pip install Pillow'를 실행하여 라이브러리를 설치해 주세요.")
    os._exit(1)

class MugleFinalMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Mugle AI - 지점장님 와이드 최적화")
        self.root.geometry("600x850") 
        self.root.configure(bg="#1A1A1A")

        self.reject_count = 0
        self.is_examining = False
        
        # 구글 스타일 컬러 및 테마
        self.google_colors = ["#4285F4", "#EA4335", "#FBBC05", "#34A853"]
        self.colors = {
            "bg": "#1A1A1A", "f_high": "#222222", "l_high": "#2A2A2A",
            "d_shadow": "#101010", "neon_b": "#00E5FF", "neon_r": "#FF1744", "text": "#E0E0E0"
        }

        # [기존 데이터 유지] 도쿄 현지 메뉴 DB
        self.menu_pool = {
            "일식": ["돈카츠 정식", "쇼가야키", "치킨 난반", "규동", "라멘", "소바", "텐동", "사케동"],
            "중식": ["마파두부 정식", "탄탄멘", "교자+볶음밥", "호이코로"],
            "양식": ["함바그 스테이크", "카츠카레", "나폴리탄", "오무라이스"],
            "간편식": ["로손 카라아게군", "세븐 도시락", "닛신 컵누들", "마트 타임세일 스시"]
        }
        
        self.shaming_comments = [
            "박 주임, 지점장님이 자네 결정 장애 때문에 고압 산소 치료 받으러 가신대.",
            "지금 메뉴 고르는 속도로 대출 심사하면 우리 지점 망해.",
            "지점장님: '박 주임은 점심 메뉴도 컴플라이언스 위반인가?'",
            "지금 지점장님이 너 모니터 뒤에서 째려보고 계신다. 3초 준다."
                 " 박 주임, 메뉴를 못 고르는구먼. 내가 정할테니 저녁에 시간잇나?"
        ]

        self.face_images = []
        self.load_resources()
        self.setup_ui()

    def load_resources(self):
        # [핵심 수정] 사진의 가로 비율(와이드)을 그대로 살려 리사이징합니다.
        target_w, target_h = 450, 250 

        for i in range(5):
            # 파일 형식이 jpg인 경우를 고려하여 유연하게 체크
            path_png = f"face_{i}.png"
            path_jpg = f"face_{i}.jpg"
            path = path_jpg if os.path.exists(path_jpg) else path_png

            if os.path.exists(path):
                try:
                    pil_img = Image.open(path)
                    # 와이드한 사진 전체가 보이도록 리사이징
                    pil_img = pil_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    self.face_images.append(ImageTk.PhotoImage(pil_img))
                except Exception as e:
                    print(f"이미지 로드 실패: {path} - {e}")
            else:
                print(f"파일 없음: {path}")

    def create_neo_frame(self, parent, width, height, bevel=3):
        frame = tk.Frame(parent, bg=self.colors["f_high"], width=width, height=height, bd=0)
        frame.pack_propagate(False)
        for i in range(bevel):
            tk.Frame(frame, bg=self.colors["l_high"], width=width, height=1).place(x=0, y=i)
            tk.Frame(frame, bg=self.colors["l_high"], width=1, height=height).place(x=i, y=0)
            tk.Frame(frame, bg=self.colors["d_shadow"], width=width, height=1).place(x=0, y=height-1-i)
            tk.Frame(frame, bg=self.colors["d_shadow"], width=1, height=height).place(x=width-1-i, y=0)
        return frame

    def setup_ui(self):
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True)

        # 1. Mugle 로고 (중앙)
        logo_f = tk.Frame(container, bg=self.colors["bg"])
        logo_f.pack(pady=20)
        for char, idx in [("M",0),("u",1),("g",2),("l",3),("e",1)]:
            tk.Label(logo_f, text=char, font=("Product Sans", 48, "bold"), 
                     fg=self.google_colors[idx], bg=self.colors["bg"]).pack(side="left")

        # 2. [수정] 지점장님 얼굴 영역 - 사진 비율에 맞춰 와이드하게 설정
        self.face_neo = self.create_neo_frame(container, width=460, height=260, bevel=4)
        self.face_neo.pack(pady=10)
        self.face_label = tk.Label(self.face_neo, bg=self.colors["f_high"])
        if self.face_images:
            self.face_label.config(image=self.face_images[0])
        else:
            self.face_label.config(text="지점장님 대기 중\n(face_0.jpg 필요)", fg="white")
        self.face_label.pack(expand=True)

        self.boss_status = tk.Label(container, text="● 지점장님 상태: 평온 (결재 대기 중)", 
                                    font=("나눔고딕", 11, "bold"), fg="#4CAF50", bg=self.colors["bg"])
        self.boss_status.pack(pady=5)

        # 3. 메뉴 디스플레이
        self.display_neo = self.create_neo_frame(container, width=460, height=150)
        self.display_neo.pack(pady=15)
        self.main_label = tk.Label(self.display_neo, text="박 주임, 서류를 접수하십시오.", 
                                   font=("나눔고딕", 16, "bold"), fg=self.colors["text"], bg=self.colors["f_high"])
        self.main_label.pack(expand=True)

        # 4. 버튼 컨트롤러
        btn_f = tk.Frame(container, bg=self.colors["bg"])
        btn_f.pack(pady=20)
        
        self.start_btn = tk.Button(btn_f, text="신 규 서 류 심 사   요 청", font=("나눔고딕", 11, "bold"), 
                                   width=40, height=2, command=self.roll_menu)
        self.start_btn.pack(pady=10)

        action_f = tk.Frame(btn_f, bg=self.colors["bg"])
        action_f.pack()
        tk.Button(action_f, text="승 인 (Accept)", width=18, height=2, command=self.approve).grid(row=0, column=0, padx=10)
        tk.Button(action_f, text="반 려 (Reject)", width=18, height=2, command=self.reject).grid(row=0, column=1, padx=10)

    def roll_menu(self):
        cat = random.choice(list(self.menu_pool.keys()))
        menu = random.choice(self.menu_pool[cat])
        self.main_label.config(text=f"분류: {cat}\n\n결재 상신: {menu}")

    def approve(self):
        messagebox.showinfo("결재 완료", "지점장님: '박 주임, 이번엔 결정이 빨랐구만.'")
        self.root.destroy()

    def reject(self):
        self.reject_count += 1
        # 반려 횟수에 따라 얼굴 변화
        if self.face_images:
            idx = min(self.reject_count, len(self.face_images)-1)
            self.face_label.config(image=self.face_images[idx])
        
        self.boss_status.config(text=f"● 지점장님 상태: 분노 가속화 ({self.reject_count}회 반려)", fg=self.colors["neon_r"])
        messagebox.showwarning("⚠️ 경고", random.choice(self.shaming_comments))
        
        if self.reject_count >= 7:
            messagebox.showerror("🚨 시스템 종료", "지점장님이 폭발하셨습니다. 도망치세요!")
            self.root.destroy()
        else:
            self.roll_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MugleFinalMaster(root)
    root.mainloop()