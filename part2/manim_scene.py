from manim import *
import numpy as np
from PIL import Image
import os

class SVDTheFinalCut(MovingCameraScene):
    def setup(self):
        # Bảng màu chuẩn 3Blue1Brown
        self.camera.background_color = "#0e0e0e"
        self.C_BLUE = "#58C4DD"
        self.C_YELLOW = "#E2E22E"
        self.C_RED = "#FC6255"
        self.C_GREEN = "#83C167"
        self.C_TEXT = "#E0E0E0"

        self.font_title = "Arial"
        self.font_note = "Arial"
        
        # Load ảnh và xử lý bằng NumPy
        img_path = "sample.jpg"
        self.has_image = os.path.exists(img_path)

        if self.has_image:
            img = Image.open(img_path).convert('RGB').resize((300, 300))
            self.img_array = np.array(img)
            
            svd_results = [np.linalg.svd(self.img_array[:, :, i], full_matrices=False) for i in range(3)]
            
            def get_img_mob(k):
                k = int(max(1, min(k, 300)))
                channels_comp = []
                for U, S, Vt in svd_results:
                    comp = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
                    channels_comp.append(np.clip(comp, 0, 255).astype(np.uint8))
                
                rgb = np.stack(channels_comp, axis=-1)
                mob = ImageMobject(rgb)
                mob.height = 4.0
                return mob
            
            self.get_img_mob = get_img_mob
        else:
            self.get_img_mob = lambda k: Square(side_length=4.0, fill_opacity=0.5, color=self.C_BLUE)

    def construct(self):
        self.phan_1_boi_canh()        
        self.phan_2_ban_chat_pixel()  
        self.phan_3_mo_xe_cong_thuc() 
        self.phan_4_hinh_hoc()        
        self.phan_5_the_gioi_thuc()   

    # ==========================================
    # PHẦN 1: BỐI CẢNH - NÉN ẢNH VÀ CƠN "NGỘP" DỮ LIỆU
    # ==========================================
    def phan_1_boi_canh(self):
        # [VO: "Bạn thử nghĩ xem... vào một chiếc điện thoại hay ổ cứng bé xíu?"]
        img_net = self.get_img_mob(200).move_to(ORIGIN) if self.has_image else Square(color=self.C_BLUE)
        self.play(FadeIn(img_net), run_time=2)
        self.wait(2)

        # [VO: "Ngày nay, ảnh chụp càng lúc càng nét... bộ nhớ của bạn sẽ đầy tràn chỉ trong chớp mắt."]
        raw_pixels = VGroup(*[
            Dot(radius=0.05, color=self.C_RED).move_to([
                np.random.uniform(-6, 6), np.random.uniform(-3.5, 3.5), 0
            ]) for _ in range(500) # Số lượng lớn tạo cảm giác ngộp
        ])
        
        self.play(FadeTransform(img_net, raw_pixels), run_time=3)
        self.play(Wiggle(raw_pixels), run_time=3) 
        self.wait(1)

        # [VO: "Nhưng thực tế thì máy bạn vẫn ổn đúng không? Bí mật không nằm ở việc vứt bớt dữ liệu đi một cách bừa bãi..."]
        svd_text = Text("SVD", weight=BOLD, font_size=90, color=self.C_YELLOW).add_background_rectangle()
        
        scanner = Rectangle(width=0.2, height=8, color=self.C_YELLOW, fill_opacity=0.8)
        scanner.set_glow_factor(1) 
        scanner.shift(LEFT * 8)

        self.wait(3.5)

        # [VO: "...mà là cách chúng ta sắp xếp lại mớ lộn xộn đó. Và 'người hùng' đứng sau phép màu dọn dẹp này chính là một thuật toán mang tên: SVD!"]
        self.play(GrowFromCenter(svd_text))
        self.wait(1)

        compressed_dots = VGroup(*[
            Dot(radius=0.06, color=self.C_YELLOW).move_to([
                np.random.uniform(-1.5, 1.5), np.random.uniform(-1.5, 1.5), 0
            ]) for _ in range(80) 
        ])

        self.play(
            scanner.animate.shift(RIGHT * 16),
            ReplacementTransform(raw_pixels, compressed_dots),
            svd_text.animate.scale(0.4).to_corner(UL),
            run_time=5,
            rate_func=linear
        )
        self.play(FadeOut(scanner))
        self.wait(1)

        img_compressed = self.get_img_mob(15).move_to(ORIGIN) 
        
        self.play(
            compressed_dots.animate.arrange_in_grid(10, 8, buff=0.1).move_to(ORIGIN),
            run_time=2
        )
        self.play(
            FadeTransform(compressed_dots, img_compressed),
            img_compressed.animate.scale(1.1).scale(1/1.1),
            run_time=3
        )
        
        self.wait(2)
        self.play(FadeOut(img_compressed), FadeOut(svd_text))
        self.dots_p1 = compressed_dots

    # ==========================================
    # PHẦN 2: BẢN CHẤT PIXEL - KHI HÌNH ẢNH HÓA MA TRẬN
    # ==========================================
    def phan_2_ban_chat_pixel(self):
        # [VO: "Với máy tính, một bức ảnh phong cảnh hay nụ cười cũng chỉ là một bảng lưới chứa đầy những con số."] 
        rgb_base = Square(side_length=1.5, fill_opacity=0.7)
        r_layer = rgb_base.copy().set_color(RED).move_to(RIGHT * 3)
        g_layer = rgb_base.copy().set_color(GREEN).move_to(RIGHT * 3.3 + DOWN * 0.3)
        b_layer = rgb_base.copy().set_color(BLUE).move_to(RIGHT * 3.6 + DOWN * 0.6)
        rgb_group = VGroup(r_layer, g_layer, b_layer)

        self.play(self.dots_p1.animate.shift(LEFT*3), FadeIn(rgb_group, shift=UP), run_time=2)
        self.wait(2) 

        # [VO: "Mỗi điểm ảnh được tạo ra từ ba lớp màu: Đỏ, Xanh lá và Xanh dương."]
        self.play(Wiggle(r_layer), run_time=0.6)
        self.play(Wiggle(g_layer), run_time=0.6)
        self.play(Wiggle(b_layer), run_time=0.6)
        self.wait(1)

        # [VO: "Ảnh càng nét, bảng số này càng khổng lồ. Nhưng khoan đã, bạn hãy để ý xem!"]
        self.play(FadeOut(rgb_group), self.dots_p1.animate.shift(RIGHT*3).scale(1.2), run_time=2)

        # [VO: "Những khoảng trời xanh rộng lớn hay những mảng tường xám... màu sắc của chúng lặp đi lặp lại rất nhiều."]
        mat = Matrix([
            ["255", "255", "240", "240"],
            ["255", "255", "240", "240"],
            ["120", "120", "80", "80"],
            ["120", "120", "80", "80"]
        ]).set_color(self.C_TEXT).scale(2.5)
        
        self.play(self.camera.frame.animate.scale(2.5), ReplacementTransform(self.dots_p1, mat), run_time=2)
        
        entries = mat.get_entries()
        sky_box = SurroundingRectangle(VGroup(*[entries[i] for i in range(8)]), color=self.C_YELLOW, buff=0.15)
        wall_box = SurroundingRectangle(VGroup(*[entries[i] for i in range(8, 16)]), color=self.C_GREEN, buff=0.15)
        
        self.play(Create(sky_box), Create(wall_box), run_time=2)
        self.wait(4)

        # [VO: "SVD được sinh ra để nhìn thấu sự lặp lại nhàm chán này. Nó quét qua hàng triệu con số, gom những thứ giống nhau lại, và chỉ giữ đúng những phần 'hồn' cốt lõi nhất để tạo nên bức ảnh."]
        self.play(Wiggle(sky_box), Wiggle(wall_box), run_time=2)
        self.wait(6)
        
        self.play(FadeOut(sky_box), FadeOut(wall_box), self.camera.frame.animate.scale(1/2.5), mat.animate.scale(0.3).to_corner(UL), run_time=2)
        self.ma_tran_A_nho = mat

    # ==========================================
    # PHẦN 3: "MỔ XẺ" MA TRẬN - CÔNG THỨC SVD
    # ==========================================
    def phan_3_mo_xe_cong_thuc(self):
        # --- PHẦN 2.2 & 3.2: CHÉO HÓA VS SVD ---
        # [VO: "Nhưng trước khi mổ xẻ SVD, hãy nhìn lại một người anh em của nó: Chéo hóa ma trận."]
        diag_formula = MathTex(r"A", r"=", r"P", r"D", r"P^{-1}", font_size=50)
        svd_formula = MathTex(r"A_{m \times n}", r"=", r"U", r"\Sigma", r"V^T", font_size=50)
        
        diag_formula[2].set_color(self.C_BLUE)   # P
        diag_formula[3].set_color(self.C_YELLOW) # D
        diag_formula[4].set_color(self.C_RED)    # P^-1

        svd_formula[2].set_color(self.C_BLUE)    # U
        svd_formula[3].set_color(self.C_YELLOW)  # Sigma
        svd_formula[4].set_color(self.C_RED)     # V^T

        self.play(Write(diag_formula), run_time=2)
        self.wait(2)

        # [VO: "Với một ma trận vuông, ta phân rã thành A = PDP^-1. D là ma trận chứa trị riêng (co giãn), P là vector riêng (định hướng)."]
        self.wait(4)

        # [VO: "SVD thực chất là một sự nâng cấp mạnh mẽ..."]
        self.play(
            diag_formula.animate.shift(LEFT * 3),
            svd_formula.animate.shift(RIGHT * 3)
        )
        self.play(Write(svd_formula), run_time=2)
        
        self.wait(5)

        self.play(
            FadeOut(diag_formula),
            svd_formula.animate.move_to(ORIGIN).scale(1.3)
        )

        # --- PHẦN 3.1: GIẢI THÍCH CHI TIẾT U, SIGMA, V^T ---
        # [VO: "Với mọi ma trận A kích thước mxn, ta luôn có thể phân rã thành U, Sigma, và V^T."]
        self.wait(2)

        # [VO: "Trong đó: U là Ma trận trực giao. Các cột gọi là vector suy biến trái..."]
        u_desc = VGroup(
            Text("U: Vector suy biến trái (từ", font=self.font_note, font_size=22, color=self.C_BLUE),
            MathTex(r"AA^T", font_size=30, color=self.C_BLUE),
            Text(")", font=self.font_note, font_size=22, color=self.C_BLUE)
        ).arrange(RIGHT, buff=0.1).next_to(svd_formula, DOWN, buff=1)
        
        self.play(FadeIn(u_desc), Indicate(svd_formula[2], color=self.C_BLUE))
        self.wait(3)

        # [VO: "Sigma: Ma trận 'giả' đường chéo chứa các giá trị suy biến..."]
        sigma_desc = VGroup(
            MathTex(r"\Sigma", font_size=30, color=self.C_YELLOW),
            Text(": Giá trị suy biến (", font=self.font_note, font_size=22, color=self.C_YELLOW),
            MathTex(r"\sigma_i = \sqrt{\lambda_i}", font_size=30, color=self.C_YELLOW),
            Text(")", font=self.font_note, font_size=22, color=self.C_YELLOW)
        ).arrange(RIGHT, buff=0.1).next_to(u_desc, DOWN)
        
        self.play(FadeIn(sigma_desc), Indicate(svd_formula[3], color=self.C_YELLOW))
        self.wait(3)

        # [VO: "V: Ma trận trực giao. Các cột gọi là vector suy biến phải..."]
        v_desc = VGroup(
            MathTex(r"V^T", font_size=30, color=self.C_RED),
            Text(": Vector suy biến phải (từ", font=self.font_note, font_size=22, color=self.C_RED),
            MathTex(r"A^TA", font_size=30, color=self.C_RED),
            Text(")", font=self.font_note, font_size=22, color=self.C_RED)
        ).arrange(RIGHT, buff=0.1).next_to(sigma_desc, DOWN)
        
        self.play(FadeIn(v_desc), Indicate(svd_formula[4], color=self.C_RED))
        self.wait(4)

        self.play(FadeOut(u_desc), FadeOut(sigma_desc), FadeOut(v_desc), FadeOut(self.ma_tran_A_nho))

# --- PHẦN 3.3: MỔ XẺ VÀ CẮT BỎ ---
        # [VO: "Và đây là lúc toán học ra tay!..."]
        # Ép Sigma vào giữa tâm, sau đó đưa U và V^T ra hai bên
        self.play(
            svd_formula[3].animate.move_to(ORIGIN),           # Đưa tâm điểm Sigma vào chính giữa màn hình
            svd_formula[2].animate.move_to(LEFT * 2.5),       # Cố định U ở bên trái
            svd_formula[4].animate.move_to(RIGHT * 2.5),      # Cố định V^T ở bên phải
            FadeOut(svd_formula[0]), FadeOut(svd_formula[1]), # Ẩn "A_{m \times n} =" đi
            run_time=2
        )
        self.wait(1)

        # Trái tim của cả hệ thống...
        sigma_box = SurroundingRectangle(svd_formula[3], color=self.C_YELLOW, buff=0.3)
        self.play(Create(sigma_box), svd_formula[3].animate.scale(1.2), run_time=2)
        self.wait(4)

        # [VO: "Những con số mang đặc điểm chính sẽ được ưu tiên..."]
        cross_line = Line(DOWN, UP, color=RED).scale(1.2).move_to(svd_formula[4]).rotate(PI/4)
        cross_line2 = Line(DOWN, UP, color=RED).scale(1.2).move_to(svd_formula[4]).rotate(-PI/4)
        
        self.play(Create(cross_line), Create(cross_line2), svd_formula[4].animate.set_opacity(0.3), run_time=1.5)
        self.wait(3.5)
        
        self.play(FadeOut(svd_formula), FadeOut(sigma_box), FadeOut(cross_line), FadeOut(cross_line2))
    # ==========================================
    # PHẦN 4: MÔ PHỎNG HÌNH HỌC & SỨC MẠNH TỐI GIẢN
    # ==========================================
    def phan_4_hinh_hoc(self):
        # [VO: "Vậy thực chất SVD làm điều đó như thế nào? Về mặt hình học, phép biến đổi tuyến tính này giống như một điệu nhảy 3 bước..."]
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.2})
        circle = Circle(radius=1.5, color=self.C_TEXT, fill_opacity=0.1)
        vec_i = Vector([1.5, 0], color=self.C_GREEN)
        vec_j = Vector([0, 1.5], color=self.C_RED)
        grid = VGroup(plane, circle, vec_i, vec_j)
        
        self.play(FadeIn(grid), run_time=2)
        self.wait(3)

        # [VO: "...Xoay dữ liệu bởi V^T để tìm ra góc nhìn rõ nhất..."]
        V_T = [[0.866, 0.5], [-0.5, 0.866]]
        Sigma = [[2.0, 0], [0, 0.4]]
        U_mat = [[0.707, -0.707], [0.707, 0.707]]
        
        label = Text("1. Xoay (V^T)", color=self.C_RED, font=self.font_note).to_corner(UR)
        self.play(Write(label), grid.animate.apply_matrix(V_T), run_time=2)
        self.wait(2)
        
        # [VO: "...kéo giãn bởi Sigma để phóng to những điểm quan trọng..."]
        label2 = Text("2. Co giãn (Sigma)", color=self.C_YELLOW, font=self.font_note).to_corner(UR)
        self.play(Transform(label, label2), grid.animate.apply_matrix(Sigma), run_time=2)
        self.wait(2)
        
        # [VO: "...và xoay thêm lần nữa bởi U để mọi thứ về đúng vị trí."]
        label3 = Text("3. Xoay (U)", color=self.C_BLUE, font=self.font_note).to_corner(UR)
        self.play(Transform(label, label3), grid.animate.apply_matrix(U_mat), run_time=2)
        self.wait(2)

        # [VO: "Điểm mấu chốt là các bước xoay này được thực hiện bởi các ma trận trực giao, giúp bảo toàn hoàn toàn cấu trúc không gian ban đầu."]
        self.wait(4)

        self.play(FadeOut(grid), FadeOut(label), run_time=2)
        
        if self.has_image:
            img_mo = self.get_img_mob(2).move_to(ORIGIN) 
            img_net = self.get_img_mob(150).move_to(ORIGIN) 
            
            # [VO: "Nhờ 'điệu nhảy' chặt chẽ này, dù ta có vứt bỏ đi đến 90% lượng dữ liệu thừa..."]
            self.play(FadeIn(img_mo), run_time=2)
            self.wait(2.5) 
            
            # [VO: "...bức ảnh được khôi phục lại vẫn cực kỳ sắc nét."] 
            self.play(FadeTransform(img_mo, img_net), run_time=3)
            self.wait(3) 
            
            self.play(FadeOut(img_net))
        else:
            self.wait(6)

    # ==========================================
    # PHẦN 5: TỪ HÌNH ẢNH ĐẾN THẾ GIỚI THỰC
    # ==========================================
    def phan_5_the_gioi_thuc(self):
        text_config = {"font": "Arial", "font_size": 22}

        # 1. CARD NETFLIX
        rec_box = RoundedRectangle(width=3, height=2, color=self.C_BLUE).move_to(LEFT * 4)
        rec_text = Text("Gợi ý nội dung", color=self.C_BLUE, **text_config).next_to(rec_box, UP)
        
        movies = VGroup(*[Square(side_length=0.4, fill_opacity=0.2, color=self.C_BLUE) for _ in range(6)])
        movies.arrange_in_grid(2, 3, buff=0.2).move_to(rec_box)
        
        # 2. CARD NLP 
        nlp_box = RoundedRectangle(width=3, height=2, color=self.C_GREEN).move_to(ORIGIN)
        nlp_text = Text("Ngôn ngữ AI", color=self.C_GREEN, **text_config).next_to(nlp_box, UP)
        w1 = Text("Xe hơi", **text_config).move_to(nlp_box.get_center() + LEFT*0.8)
        w2 = Text("Ô tô", **text_config).move_to(nlp_box.get_center() + RIGHT*0.8)
        
        # 3. CARD LỌC NHIỄU 
        sig_box = RoundedRectangle(width=3, height=2, color=self.C_RED).move_to(RIGHT * 4)
        sig_text = Text("Lọc nhiễu dữ liệu", color=self.C_RED, **text_config).next_to(sig_box, UP)
        signal = FunctionGraph(lambda x: np.sin(3*x) + 0.3*np.cos(15*x), x_range=[-1, 1], color=self.C_RED).scale(0.5).move_to(sig_box)
        clean_signal = FunctionGraph(lambda x: np.sin(3*x), x_range=[-1, 1], color=self.C_YELLOW).scale(0.5).move_to(sig_box)

        # [VO: "Bước ra khỏi những tấm hình, SVD thực sự là một 'trợ thủ' đắc lực... Bạn nghĩ Netflix hay YouTube biết đọc tâm trí khi gợi ý phim?"]
        self.play(FadeIn(rec_box), Write(rec_text), Create(movies), run_time=1.5)
        self.play(Indicate(rec_box, color=self.C_YELLOW, scale_factor=1.05)) 
        
        # [VO: "Thật ra, SVD đang phân tích thói quen của hàng triệu người... đoán trúng phóc gu của bạn."]
        self.play(movies[1].animate.set_fill(self.C_YELLOW, 0.8), movies[4].animate.set_fill(self.C_YELLOW, 0.8))
        self.wait(5) 

        # [VO: "Khi bạn chat với AI, SVD giúp máy tính hiểu rằng 'xe hơi' và 'ô tô' có chung ý nghĩa bằng cách gom những từ này lại gần nhau. Về bản chất, đây là nghệ thuật giảm chiều dữ liệu!"]
        self.play(FadeIn(nlp_box), Write(nlp_text), FadeIn(w1), FadeIn(w2), run_time=1.5)
        self.play(Indicate(nlp_box, color=self.C_YELLOW, scale_factor=1.05))
        self.play(
            w1.animate.shift(RIGHT*0.4).set_color(self.C_YELLOW), 
            w2.animate.shift(LEFT*0.4).set_color(self.C_YELLOW), 
            run_time=2
        )
        self.play(Flash(nlp_box, color=self.C_YELLOW)) 
        self.wait(4)

        # [VO: "Và không dừng lại ở đó, trong các nghiên cứu khoa học, SVD còn hoạt động như một chiếc màng lọc thông minh... kỹ thuật Khử nhiễu - Denoising."]
        self.play(FadeIn(sig_box), Write(sig_text), Create(signal), run_time=1.5)
        self.play(Indicate(sig_box, color=self.C_YELLOW, scale_factor=1.05))
        self.wait(1)
        self.play(Transform(signal, clean_signal), run_time=2) 
        self.wait(3)

        # [VO: "SVD không chỉ là một mớ công thức khô khan trên bảng đen, nó là cách toán học dọn dẹp sự hỗn loạn để tìm ra chân lý!"]
        self.play(
            FadeOut(VGroup(rec_box, rec_text, movies, nlp_box, nlp_text, sig_box, sig_text, signal, clean_signal, w1, w2)), 
            run_time=2
        )
        
        final_text = Text("CHÂN LÝ TỪ SỰ HỖN LOẠN", color=self.C_YELLOW, font="Arial", weight=BOLD).scale(1.2)
        self.play(Write(final_text), run_time=3)
        self.wait(4)
        self.play(FadeOut(final_text))