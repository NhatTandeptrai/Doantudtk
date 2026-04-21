from manim import *

class OutroCamOn(Scene):
    def construct(self):
        # Bảng màu chuẩn từ các video trước
        C_BLUE = "#58C4DD"
        C_YELLOW = "#E2E22E"
        C_TEXT = "#E0E0E0"
        font_main = "Arial"

        # ==========================================
        # 1. TIÊU ĐỀ CẢM ƠN (0s - 2.5s)
        # ==========================================
        thank_you_text = Text(
            "Cảm ơn thầy và các bạn đã theo dõi!",
            font=font_main,
            font_size=45,
            color=C_YELLOW,
            weight=BOLD
        )
        
        self.play(Write(thank_you_text), run_time=1.5)
        self.wait(1.0) # Tổng: 2.5s

        # ==========================================
        # 2. THÔNG TIN NHÓM & LỚP (2.5s - 4.5s)
        # ==========================================
        # Đẩy chữ cảm ơn lên trên
        self.play(
            thank_you_text.animate.to_edge(UP, buff=1.0).scale(0.8),
            run_time=1.0
        )

        group_info = Text(
            "Thực hiện bởi: Nhóm 2 - Lớp 24CTT2\nMôn: Toán ứng dụng và Thống kê",
            font=font_main,
            font_size=30,
            color=C_BLUE,
            t2c={"Nhóm 2": C_YELLOW, "24CTT2": C_YELLOW} # Đổi màu điểm nhấn
        ).next_to(thank_you_text, DOWN, buff=0.5)

        self.play(FadeIn(group_info, shift=UP), run_time=1.0) # Tổng: 4.5s

        # ==========================================
        # 3. DANH SÁCH THÀNH VIÊN (4.5s - 8.0s)
        # ==========================================
        members = [
            "24120442 | Đỗ Đức Duy Thắng",
            "24120437 | Nguyễn Nhật Tân",
            "24120449 | Nguyễn Tấn Thành",
            "24120453 | Trần Hồng Thiên",
            "24120443 | Nguyễn Quang Thắng"
        ]

        member_mobjects = VGroup(*[
            Text(member, font=font_main, font_size=28, color=C_TEXT)
            for member in members
        ])
        
        # Sắp xếp danh sách thẳng hàng dọc
        member_mobjects.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        member_mobjects.next_to(group_info, DOWN, buff=0.8)

        # Hiệu ứng hiện từng người một (Lagged Start)
        self.play(
            AnimationGroup(
                *[FadeIn(mob, shift=RIGHT*0.5) for mob in member_mobjects],
                lag_ratio=0.2
            ),
            run_time=3.5
        ) # Tổng: 8.0s

        # ==========================================
        # 4. CHỜ ĐỂ ĐỌC VÀ KẾT THÚC (8.0s - 12.0s)
        # ==========================================
        self.wait(6) # Giữ khung hình tĩnh để người xem đọc tên (Tổng: 10.5s)

        # Tắt dần mọi thứ để kết thúc video mượt mà
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.5
        ) # Tổng: 12.0s