"""
Face Recognition - Intro Scene
===================================
Lệnh render: python -m manim pc0.py IntroScene -pqh <--disable_caching>
"""

from manim import *
import numpy as np
import random

Text.set_default(font="Be Vietnam Pro")
class IntroScene(Scene):
    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 0: Lời tựa mở đầu
        # ══════════════════════════════════════════════════════════════════════
        self.wait(0.5)
        # Nội dung lời tựa
        line1 = Text("Công nghệ nhận dạng khuôn mặt ngày càng đóng vai trò thiết yếu,", font_size=26)
        line2 = Text("với những ứng dụng khắp mọi mặt đời sống trong thời đại 4.0.", font_size=26)
        line3 = Text("Một trong những ứng dụng quan trọng và mạnh mẽ nhất của nó là...", font_size=26)
        line4 = Text("TRUY VẾT VÀ NHẬN DIỆN MỤC TIÊU TRONG ĐÁM ĐÔNG.", font_size=30, color=RED, weight=BOLD)
        
        intro_group = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.6)
        
        # VỀ ÂM THANH BÀN PHÍM LÁCH CÁCH
        self.add_sound("sound/typing.mp3") 
        
        # Hiệu ứng gõ từng chữ: rate_func=linear giúp tốc độ gõ đều đặn
        self.wait(0.5)
        self.play(Write(line1, rate_func=linear), run_time=2.5)
        self.wait(0.5)
        self.add_sound("sound/typing.mp3")
        self.play(Write(line2, rate_func=linear), run_time=2.5)
        self.wait(0.5)
        self.play(Write(line3, rate_func=linear), run_time=2.5)
        self.wait(0.5)
        self.play(Write(line4, rate_func=linear), run_time=2.0)
        # Giữ dòng chữ trên màn hình 2 giây để người xem kịp đọc
        self.wait(2.0)
        # Phai mờ lời tựa để chuyển sang cảnh Truy nã (Phase 1)
        self.play(FadeOut(intro_group), run_time=1.0)
        self.wait(0.5)
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 1: Lệnh truy nã (0s - 5s)
        # ══════════════════════════════════════════════════════════════════════
        
        wanted_poster = ImageMobject("face/temp.png").set_height(6.5)
        self.play(FadeIn(wanted_poster, scale=0.9), run_time=2)
        self.wait(3)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 1.5: Camera quét đám đông (5s - 15s)
        # ══════════════════════════════════════════════════════════════════════
        
        crowd_img = ImageMobject("face/crowd.webp").set_height(8.5)
        
        # 1. Tính toán toạ độ mục tiêu chính xác 100% theo tỷ lệ bạn cung cấp
        img_width = crowd_img.width
        img_height = crowd_img.height
        
        target_x = crowd_img.get_left()[0] + (10 / 17) * img_width
        target_y = crowd_img.get_top()[1] - (3.5 / 9) * img_height
        target_pos = np.array([target_x, target_y, 0])

        self.play(FadeOut(wanted_poster), FadeIn(crowd_img), run_time=1.5)

        dark_overlay = Rectangle(width=16, height=9, fill_color=BLACK, fill_opacity=0.75, stroke_width=0)
        self.play(FadeIn(dark_overlay), run_time=0.5)

        # Biểu tượng con mắt (Camera)
        eye_top = ArcBetweenPoints(LEFT, RIGHT, angle=-PI/2, stroke_color=GREEN, stroke_width=4)
        eye_bottom = ArcBetweenPoints(LEFT, RIGHT, angle=PI/2, stroke_color=GREEN, stroke_width=4)
        pupil = Circle(radius=0.2, fill_color=GREEN, fill_opacity=1, stroke_width=0)
        camera_eye = VGroup(eye_top, eye_bottom, pupil).scale(0.5).to_corner(UL, buff=0.5)
        
        eye_label = Text("SURVEILLANCE", font_size=16, color=GREEN).next_to(camera_eye, DOWN)
        camera_group = VGroup(camera_eye, eye_label)
        self.play(FadeIn(camera_group), run_time=1)

        # Vùng sáng quét (Scanner)
        scanner_radius = 1.2
        scanner_circle = Circle(radius=scanner_radius, color=GREEN, stroke_width=3)
        scanner_glow = Circle(radius=scanner_radius, fill_color=WHITE, fill_opacity=0.2, stroke_width=0)
        scanner = VGroup(scanner_circle, scanner_glow)
        scanner.move_to(LEFT * 4 + UP * 2)

        beam = always_redraw(lambda: Polygon(
            pupil.get_center(),
            scanner.get_top() + LEFT * 0.2,
            scanner.get_bottom() + LEFT * 0.2,
            fill_color=GREEN, fill_opacity=0.15, stroke_width=0
        ))

        self.play(FadeIn(scanner), FadeIn(beam), run_time=1)

        # Di chuyển scanner
        self.play(scanner.animate.move_to(RIGHT * 3 + UP * 2), run_time=2, rate_func=there_and_back_with_pause)
        self.play(scanner.animate.move_to(LEFT * 2 + DOWN * 2), run_time=1.5)
        
        # Scanner khóa mục tiêu tại target_pos (toạ độ 10/17 ngang, 3.5/9 dọc)
        self.play(scanner.animate.move_to(target_pos), run_time=1.5)

        lock_box = Square(side_length=1.5, color=RED, stroke_width=4).move_to(target_pos)
        lock_text = Text("TARGET LOCKED", font_size=20, color=RED, weight=BOLD).next_to(lock_box, DOWN)
        
        self.play(
            Create(lock_box), Write(lock_text),
            scanner_circle.animate.set_color(RED), pupil.animate.set_color(RED),
            run_time=0.5
        )
        self.wait(0.5)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 2: Phóng to và So sánh (15s - 20s)
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeOut(camera_group), FadeOut(beam), FadeOut(scanner), FadeOut(lock_text), run_time=0.5)

        extracted_face = ImageMobject("face/wanted.png").set_height(1.5).move_to(target_pos)
        self.add(extracted_face)

        self.play(
            FadeOut(crowd_img), FadeOut(dark_overlay),
            extracted_face.animate.set_height(4.5).move_to(RIGHT * 3),
            lock_box.animate.scale(4.5/1.5).move_to(RIGHT * 3),
            run_time=1.5
        )

        wanted_photo = ImageMobject("face/wanted.png").set_height(4.5).move_to(LEFT * 3)
        wanted_box = Square(side_length=4.5, color=GREEN, stroke_width=4).move_to(wanted_photo)
        db_text = Text("DATABASE", font_size=24, color=GREEN).next_to(wanted_box, UP)
        live_text = Text("LIVE SCAN", font_size=24, color=RED).next_to(lock_box, UP)

        self.play(FadeIn(wanted_photo, shift=RIGHT*0.5), Create(wanted_box), Write(db_text), Write(live_text), run_time=1)

        match_line = Line(wanted_box.get_right(), lock_box.get_left(), color=YELLOW, stroke_width=3)
        match_percent = Text("MATCH: 99.8%", color=YELLOW, font_size=32, weight=BOLD).move_to(match_line.get_center() + UP*0.3)
        
        self.play(Create(match_line), Write(match_percent), run_time=1)
        self.wait(3.0)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 3: Lưới Ma Trận Số Hoá Ảnh (20s - 30s+)
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(
            FadeOut(wanted_photo), FadeOut(wanted_box), FadeOut(db_text), 
            FadeOut(live_text), FadeOut(match_line), FadeOut(match_percent),
            FadeOut(lock_box),
            extracted_face.animate.move_to(ORIGIN).set_height(3.4), 
            run_time=1.5
        )

        digitize_title = Text("Rời rạc hoá thành Ma trận Pixel", color=GREEN_B, font_size=28).to_edge(DOWN, buff=1.0)
        self.play(Write(digitize_title), run_time=0.5)

        # Tạo Lưới đè lên ảnh — mỗi ô = một pixel 
        CELL = 0.41
        cells = VGroup()
        nums  = VGroup()
        
        # Hàm tạo màu Grayscale tương ứng với giá trị v
        def get_gray_color(value):
            return rgb_to_color([value/255.0, value/255.0, value/255.0])

        for r in range(8):
            for c in range(4):
                # Tạo giá trị pixel ngẫu nhiên mô phỏng ảnh
                v = random.randint(50, 240) 
                sq = Square(
                    side_length=CELL,
                    fill_color=get_gray_color(v), fill_opacity=0.85,
                    stroke_color=WHITE, stroke_width=0.8,
                ).move_to([(c - 1.5) * CELL, (3.5 - r) * CELL, 0])
                
                cells.add(sq)
                nums.add(
                    Text(str(v), font_size=10, color=WHITE).move_to(sq.get_center())
                )

        self.play(FadeIn(cells), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.025),
            run_time=2.5,
        )

        self.wait(8.0)

	#hiển thị phương pháp: Fisherface

        # Xoá toàn bộ mobjects ở cuối
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=2)