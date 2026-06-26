"""
Final Scene
=============================================================
Render:  manim pc_final.py FinalScene -pqh
"""

from manim import *
import numpy as np

Text.set_default(font="Be Vietnam Pro")

class FinalScene(ThreeDScene):
    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        #  P1: ĐIỂM HẠN CHẾ - GIỚI HẠN TUYẾN TÍNH (0s - 10s)
        # ══════════════════════════════════════════════════════════════════════
        title_p0 = Text("PHẦN KẾT", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.0, 2.0, 1], z_range=[-2.0, 2.0, 1],
            x_length=6, y_length=5, z_length=4
        )

        title_p1 = Text("Điểm hạn chế: Giới hạn tuyến tính", font_size=32, color=RED, weight=BOLD)
        title_p1.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title_p1)

        n = 45
        t = np.linspace(0, np.pi, n)
        bx = np.cos(t) - 0.5; by = np.sin(t) - 0.25
        rx = 1 - np.cos(t) - 0.5; ry = 0.5 - np.sin(t) - 0.25

        blue_dots = VGroup(*[Dot(axes.c2p(x, y, 0), radius=0.08, color=self.BLUE_C) for x, y in zip(bx, by)])
        red_dots  = VGroup(*[Dot(axes.c2p(x, y, 0), radius=0.08, color=self.RED_C)  for x, y in zip(rx, ry)])

        self.play(Write(title_p1), FadeIn(axes), GrowFromCenter(blue_dots), GrowFromCenter(red_dots), run_time=1.5)
        self.wait(1.0)

        fail_line = Line(axes.c2p(-2, -1.5, 0), axes.c2p(2, 1.5, 0), color=WHITE, stroke_width=4)
        cross_mark = Cross(fail_line, stroke_color=RED, stroke_width=6, scale_factor=0.3)

        desc_p1 = Text("Bản chất FLD là tuyến tính -> Không thể phân chia", font_size=18, color=WHITE)
        self.add_fixed_in_frame_mobjects(desc_p1)
        desc_p1.next_to(axes, DOWN, buff=0.5).to_edge(DOWN, buff=0.5)

        self.play(Create(fail_line), FadeIn(desc_p1, shift=UP*0.2), run_time=1.0)
        self.play(Create(cross_mark))
        self.wait(2.0)

        self.play(FadeOut(fail_line), FadeOut(cross_mark), FadeOut(desc_p1))


        # ══════════════════════════════════════════════════════════════════════
        #  P2: PHƯƠNG PHÁP THAY THẾ & KERNEL TRICK (10s - 35s)
        # ══════════════════════════════════════════════════════════════════════
        
        title_p2 = Text("Phương pháp thay thế: Kernel Trick", font_size=32, color=GREEN_C, weight=BOLD)
        title_p2.to_edge(UP, buff=0.3)
        #self.add_fixed_in_frame_mobjects(title_p2)
        
        self.play(Transform(title_p1, title_p2))

        def kernel(x, y):
            peak = np.exp(-((x + 0.5)**2 + (y - 0.25)**2) * 2.5)
            valley = np.exp(-((x - 0.5)**2 + (y + 0.25)**2) * 2.5)
            return (peak - valley) * 1.5

        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, run_time=2.0)

        self.play(
            *[d.animate.move_to(axes.c2p(x, y, kernel(x, y))) for d, x, y in zip(blue_dots, bx, by)],
            *[d.animate.move_to(axes.c2p(x, y, kernel(x, y))) for d, x, y in zip(red_dots, rx, ry)],
            run_time=2.0, rate_func=smooth
        )

        p1_c = axes.c2p(-2.5, -2.0, 0); p2_c = axes.c2p( 2.5, -2.0, 0)
        p3_c = axes.c2p( 2.5,  2.0, 0); p4_c = axes.c2p(-2.5,  2.0, 0)
        plane = Polygon(p1_c, p2_c, p3_c, p4_c, fill_color=WHITE, fill_opacity=0.3, stroke_width=1, stroke_color=WHITE)
        plane.shift(RIGHT * 5)

        self.play(plane.animate.shift(LEFT * 5), run_time=1.5)
        
        self.move_camera(theta=-135 * DEGREES, run_time=3.0, rate_func=there_and_back)

        self.play(FadeOut(axes), FadeOut(blue_dots), FadeOut(red_dots), FadeOut(plane), FadeOut(title_p1), run_time=1.0)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES) 

        center_node = Text("Các hướng tiếp cận hiện đại", font_size=26, color=YELLOW, weight=BOLD)
        
        nodes = [
            Text("Kernel Fisherfaces", font_size=20, color=GREEN_C),
            Text("LBP (Local Binary Patterns)", font_size=20, color=self.BLUE_C),
            Text("3D Face Models", font_size=20, color=self.RED_C),
            Text("CNN (Deep Learning)", font_size=20, color=PURPLE_B)
        ]
        for n in nodes:
            n.move_to(ORIGIN)

        self.play(Write(center_node), run_time=0.8)
        
        self.play(
            nodes[0].animate.move_to(UP * 2.2 + LEFT * 3.8),
            nodes[1].animate.move_to(UP * 2.2 + RIGHT * 3.8),
            nodes[2].animate.move_to(DOWN * 2.2 + LEFT * 3.8),
            nodes[3].animate.move_to(DOWN * 2.2 + RIGHT * 3.8),
            run_time=1.2, rate_func=smooth
        )

        lines = [
            Line(center_node.get_center(), nodes[0].get_center(), buff=1.2, color=WHITE, stroke_opacity=0.5),
            Line(center_node.get_center(), nodes[1].get_center(), buff=1.2, color=WHITE, stroke_opacity=0.5),
            Line(center_node.get_center(), nodes[2].get_center(), buff=1.2, color=WHITE, stroke_opacity=0.5),
            Line(center_node.get_center(), nodes[3].get_center(), buff=1.2, color=WHITE, stroke_opacity=0.5)
        ]
        
        self.play(*[Create(l) for l in lines], run_time=1.0)
        self.wait(4.5)

        self.play(FadeOut(VGroup(*nodes, *lines, center_node)), run_time=1.0)


        # ══════════════════════════════════════════════════════════════════════
        #  P3: LỜI KẾT & CREDIT (35s - 50s)
        # ══════════════════════════════════════════════════════════════════════
        
        quote = Text("Fisherfaces: Phương pháp chuẩn mực của\n  nhận dạng và phân loại khuôn mặt",
                     font_size=32, color=YELLOW, weight=BOLD)
        
        self.play(FadeIn(quote, shift=UP*0.3), run_time=1.5)
        self.wait(4.0)
        self.play(FadeOut(quote), run_time=1.0)

        # 1. NHÓM THEO KHỐI
        block1 = VGroup(
            Text("Đạo diễn hình ảnh", font_size=18, color=GREY_A),
            Text("Nguyễn Nhật Minh", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        
        block2 = VGroup(
            Text("Biên kịch", font_size=18, color=GREY_A),
            Text("Nguyễn Nhật Minh", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        block4 = VGroup(
            Text("Phụ trách hậu cần", font_size=18, color=GREY_A),
            Text("Nguyễn Nhật Minh", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        block3 = VGroup(
            Text("Sinh viên thực hiện", font_size=18, color=GREY_A),
            Text("Nguyễn Nhật Minh - 23122010", font_size=24, color=self.BLUE_C, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        credit = VGroup(
            Text("Cảm ơn các thầy hướng dẫn:", font_size=18, color=GREY_A),
            Text("PGS.TS Lê Hoàng Thái", font_size=24, color=self.BLUE_C, weight=BOLD),
            Text("Thầy Nguyễn Thanh Tình", font_size=24, color=self.BLUE_C, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        credits_group = VGroup(
            Text("THE END", font_size=50, color=YELLOW, weight=BOLD),
            block1,
            block2,
            block4,
            credit,
            block3,
            Text("Cảm ơn thầy và các bạn đã theo dõi!", font_size=24, color=GREEN_B)
        ).arrange(DOWN, buff=1.2) # Khoảng cách giữa các khối

        # Đặt Credit tít dưới đáy màn hình 
        credits_group.move_to(DOWN * 9.0) 
        credits_group.set_z_index(0)

        # 2. TẠO FOOTER VÀ MẶT NẠ CHE
        fit_text = Text("FIT@HCMUS", font_size=40, color=BLUE_D, weight=BOLD).to_edge(DOWN, buff=0.4)
        
        # Đường kẻ ngang ngay trên chữ FIT
        separator = Line(LEFT * 8, RIGHT * 8, stroke_width=2, color=GRAY).next_to(fit_text, UP, buff=0.3)
        
        # Hình chữ nhật màu đen dùng làm lớp ngụy trang che dòng Credit trôi qua
        mask_rect = Rectangle(width=16, height=4, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        mask_rect.next_to(separator, DOWN, buff=0)
        
        # Gộp mặt nạ, đường kẻ và FIT lại
        footer_group = VGroup(mask_rect, separator, fit_text)
        footer_group.set_z_index(10)
        
        self.play(FadeIn(footer_group), run_time=1.0)
        
        # Cảnh cuộn chữ 
        self.play(credits_group.animate.shift(UP * 16.5), run_time=11.0, rate_func=linear)
        
        self.wait(1.0)
        self.play(FadeOut(credits_group), FadeOut(footer_group), run_time=1.5)
        self.wait(1.0)