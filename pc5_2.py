"""
PC5 – Part 2: Solving Singular Matrix
====================================================================
Render:  manim pc5_2.py Fisherface -pqh
"""

from manim import *
import numpy as np

Text.set_default(font="Be Vietnam Pro")

class Fisherface(Scene):
    # Hệ màu đồng nhất
    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    PCA_C  = "#9C27B0"  
    LDA_C  = "#FF8C42"  
    SW_C   = "#EF9A9A"
    SB_C   = "#66BB6A"

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 1: Giải quyết Ma trận suy biến S_W (0:00 - 0:20)
        # ══════════════════════════════════════════════════════════════════════
        
        # 1. Tạo ma trận khổng lồ S_w 
        np.random.seed(42)
        mat_data = []
        for i in range(7):
            row = []
            for j in range(7):
                # Tạo 85% xác suất là số 0
                val = "0" if np.random.random() > 0.15 else str(round(np.random.uniform(0.1, 2.5), 1))
                row.append(val)
            mat_data.append(row)
            
        big_matrix = Matrix(mat_data, h_buff=0.7, v_buff=0.6).scale(0.55)
        big_matrix.set_color(self.SW_C)
        
        sw_label = MathTex(r"\mathbf{S}_w", font_size=50, color=self.SW_C).next_to(big_matrix, UP, buff=0.2)
        sw_group = VGroup(big_matrix, sw_label).move_to(UP * 1.2)

        # Cảnh báo nổ đỏ
        warn_text = Text("MA TRẬN SUY BIẾN!", font_size=32, color=RED, weight=BOLD)
        warn_text.next_to(sw_group, DOWN, buff=0.5)

        # Nhấp nháy cảnh báo
        self.play(FadeIn(sw_group), FadeIn(warn_text, shift=UP*0.2), run_time=1.0)
        for _ in range(2):
            self.play(warn_text.animate.set_color(YELLOW), run_time=0.2)
            self.play(warn_text.animate.set_color(RED), run_time=0.2)
        self.wait(1.5)

        # 2. Kéo W_PCA kẹp vào hai bên
        wpca_t = MathTex(r"\mathbf{W}_{PCA}^\top", font_size=60, color=self.PCA_C)
        wpca_n = MathTex(r"\mathbf{W}_{PCA}", font_size=60, color=self.PCA_C)
        
        # Đặt 2 ma trận chiếu ở 2 bên mép màn hình, rồi bay vào kẹp lấy S_w
        wpca_t.move_to(LEFT * 6 + UP * 1.2)
        wpca_n.move_to(RIGHT * 6 + UP * 1.2)
        
        self.play(
            wpca_t.animate.next_to(big_matrix, LEFT, buff=0.2),
            wpca_n.animate.next_to(big_matrix, RIGHT, buff=0.2),
            FadeOut(sw_label),
            run_time=2.5, rate_func=smooth
        )
        self.wait(1.0)

        # 3. Phép biến đổi Transform nén khối ma trận khổng lồ
        # Tạo ma trận nhỏ gọn không suy biến
        small_mat_data = [["2.1", "0.4", "-0.1"], ["0.4", "1.5", "0.2"], ["-0.1", "0.2", "3.0"]]
        small_matrix = Matrix(small_mat_data).scale(0.8).set_color(WHITE)
        new_sw_label = MathTex(r"\tilde{\mathbf{S}}_w =", font_size=45, color=self.SW_C)
        
        compact_group = VGroup(new_sw_label, small_matrix).arrange(RIGHT, buff=0.2).move_to(UP * 1.2)

        sandwich_group = VGroup(wpca_t, big_matrix, wpca_n)

        # Nổ tung Text & Nén ma trận đồng thời
        self.play(
            Transform(sandwich_group, compact_group),
            Flash(warn_text.get_center(), color=RED, flash_radius=2.5, line_length=0.8, num_lines=15),
            FadeOut(warn_text),
            run_time=2.5
        )
        self.wait(0.5)

        # 4. Ký hiệu nghịch đảo -1 xuất hiện lơ lửng êm ái
        inv_symbol = MathTex(r"^{-1}", font_size=55, color=YELLOW)
        inv_symbol.next_to(small_matrix.get_corner(UR), RIGHT, buff=0.1).shift(UP * 0.2)
        
        success_text = Text("Ma trận đã có thể nghịch đảo!", font_size=20, color=GREEN_C).next_to(compact_group, DOWN, buff=0.5)

        self.play(
            FadeIn(inv_symbol, shift=DOWN * 0.3), # Lơ lửng rơi nhẹ xuống đúng vị trí
            FadeIn(success_text, shift=UP * 0.2),
            run_time=1.5
        )
        self.wait(6.0) 

        # Dọn dẹp Phase 1
        self.play(FadeOut(sandwich_group), FadeOut(inv_symbol), FadeOut(success_text), run_time=1.0)


        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 2: Tổng quát hóa công thức W_Fisher (0:20 - 0:40)
        # ══════════════════════════════════════════════════════════════════════
        
        # 1. Hiển thị công thức mục tiêu khổng lồ
        f_main = MathTex(
            r"\mathbf{W}_{Fisher} = \arg\max_{\mathbf{W}} \frac{",  # [0]
            r"| \mathbf{W}^\top \mathbf{S}_b \mathbf{W} |",          # [1]
            r"}{",                                                   # [2]
            r"| \mathbf{W}^\top \mathbf{S}_w \mathbf{W} |",          # [3]
            r"}",                                                    # [4]
            font_size=48
        ).move_to(UP * 2.0)
        f_main[1].set_color(self.SB_C)
        f_main[3].set_color(self.SW_C)

        self.play(Write(f_main), run_time=2)
        self.wait(2)

        # 2. Phân tách thành 2 giai đoạn (W_PCA * W_FLD)
        breakdown_text = Text("Được giải quyết qua 2 giai đoạn liên tiếp:", font_size=20, color=WHITE)
        breakdown_text.next_to(f_main, DOWN, buff=0.5)
        
        f_fisher = MathTex(
            r"\mathbf{W}_{Fisher} =", 
            r"\mathbf{W}_{PCA}", 
            r"\cdot", 
            r"\mathbf{W}_{FLD}",
            font_size=55
        ).next_to(breakdown_text, DOWN, buff=0.4)
        
        f_fisher[1].set_color(self.PCA_C)
        f_fisher[3].set_color(self.LDA_C)

        self.play(FadeIn(breakdown_text), FadeIn(f_fisher, shift=UP*0.2), run_time=1.2)
        self.wait(1.5)

        # 3. Chú thích rõ ràng vai trò của từng ma trận
        # Box chú thích PCA
        pca_box = VGroup(
            Text("1. PCA", font_size=18, weight=BOLD, color=self.PCA_C),
            Text("Nén đặc trưng", font_size=16, color=WHITE),
            Text("Khắc phục suy biến Sw", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        pca_box.next_to(f_fisher[1], DOWN, buff=0.8).shift(LEFT * 1.5)
        
        # Mũi tên chỉ từ W_PCA xuống
        arrow_pca = Arrow(f_fisher[1].get_bottom(), pca_box.get_top(), buff=0.1, color=self.PCA_C, stroke_width=2)

        # Box chú thích FLD
        fld_box = VGroup(
            Text("2. FLD", font_size=18, weight=BOLD, color=self.LDA_C),
            Text("Tối đa khoảng cách 2 lớp", font_size=16, color=WHITE),
            Text("Gom cụm chặt chẽ", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        fld_box.next_to(f_fisher[3], DOWN, buff=0.8).shift(RIGHT * 1.5)
        
        # Mũi tên chỉ từ W_FLD xuống
        arrow_fld = Arrow(f_fisher[3].get_bottom(), fld_box.get_top(), buff=0.1, color=self.LDA_C, stroke_width=2)

        # Hiệu ứng hiện chú thích
        self.play(GrowArrow(arrow_pca), FadeIn(pca_box, shift=DOWN*0.2), run_time=1.0)
        self.play(GrowArrow(arrow_fld), FadeIn(fld_box, shift=DOWN*0.2), run_time=1.0)

        self.wait(5.0)

        # Phai mờ toàn bộ
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)