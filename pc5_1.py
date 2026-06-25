"""
PC5 – Part 1: Fisherfaces Pipeline (PCA + LDA)
====================================================================
Render:  manim pc5_1.py Fisher1 -pqh
"""

from manim import *
import numpy as np

Text.set_default(font="Be Vietnam Pro")

class Fisher1(Scene):

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    PCA_C  = "#9C27B0"  # Tím đặc trưng cho PCA
    LDA_C  = "#FF8C42"  # Cam đặc trưng cho LDA
    TEXT_C = "#E0E0E0"

    def construct(self):
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 1: Hiển thị ảnh gốc & Biến đổi thành Khối ma trận 3D (0:00 - 0:10)
        # ══════════════════════════════════════════════════════════════════════
        title_p0 = Text("PHẦN 5: FISHERFACES", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        # 1. Tiêu đề lớn cạnh trên
        title = Text("Thuật toán Fisherfaces = PCA + FLD", font_size=36, weight=BOLD, color=YELLOW)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.0)

        # 2. Khởi tạo 10 ảnh của 2 người
        b_images = Group(*[
            ImageMobject(filename_or_array=f"face/face1/image_{i}.jpg").set_height(0.8)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.25)
        
        r_images = Group(*[
            ImageMobject(filename_or_array=f"face/face2/image_{i}.jpg").set_height(0.8)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.25)
        
        # Gom cụm và đẩy lên nửa trên màn hình (Y > -1.5) để chừa chỗ cho phụ đề
        all_images = Group(b_images, r_images).arrange(DOWN, buff=0.4).shift(UP * 0.9)
        
        self.play(FadeIn(all_images, shift=UP*0.2), run_time=1.2)
        self.wait(5.0)

        # 3. Biến mỗi ảnh thành một ma trận pixel riêng biệt
        prep_text = Text("Chuyển đổi từng ảnh thành các ma trận pixel độc lập", font_size=18, color=GREEN_B)
        prep_text.move_to(DOWN * 0.8)
        self.play(FadeIn(prep_text), run_time=0.6)

        # Tạo danh sách phẳng để xử lý đồng bộ biến đổi
        flat_image_list = []
        for img in b_images: flat_image_list.append((img, self.BLUE_C))
        for img in r_images: flat_image_list.append((img, self.RED_C))

        matrices = VGroup()
        fade_out_anims = []
        fade_in_anims = []

        for img, color in flat_image_list:
            # Tạo lưới ma trận ô vuông (mô phỏng pixel ảnh) kích thước 5x5
            matrix = VGroup()
            for r in range(5):
                for c in range(5):
                    matrix.add(Square(
                        side_length=0.13, fill_color=color, fill_opacity=0.85, 
                        stroke_width=0.4, stroke_color=BLACK
                    ))
            matrix.arrange_in_grid(5, 5, buff=0)
            matrix.move_to(img.get_center()) # Đặt trùng vị trí với ảnh tương ứng
            matrices.add(matrix)
            
            fade_out_anims.append(FadeOut(img, scale=0.8))
            fade_in_anims.append(FadeIn(matrix, scale=1.2))

        # Thực hiện hiệu ứng rã ảnh thành ma trận toán học đồng thời
        self.play(*fade_out_anims, *fade_in_anims, run_time=1.5)
        self.wait(3.0)
        self.play(FadeOut(prep_text), run_time=0.4)
        # 4. Xếp chồng các ma trận lên nhau tạo thành khối dữ liệu 3D
        stack_text = Text("Chuyển đổi ma trận thành các điểm trên không gian nhiều chiều", font_size=18, color=GREEN_B)
        stack_text.move_to(DOWN * 0.8)
        self.play(FadeIn(stack_text), run_time=0.6)
        

        # Vị trí trung tâm của khối 3D nằm bên cánh trái panel
        stack_center = LEFT * 4.6 + UP * 0.9
        stack_anims = []

        for idx, mat in enumerate(matrices):
            offset_3d = idx * 0.07 * RIGHT + idx * 0.07 * UP
            stack_anims.append(mat.animate.move_to(stack_center + offset_3d))

        self.play(*stack_anims, run_time=2.0, rate_func=smooth)
        self.wait(2.0)
        self.play(FadeOut(stack_text), run_time=0.4)
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 2: Phễu lọc PCA (0:10 - 0:17)
        # ══════════════════════════════════════════════════════════════════════

        # Tạo hình khối phễu cho PCA 
        pca_funnel = Polygon(
            [-0.6, 1.2, 0], [0.6, 0.5, 0], [0.6, -0.5, 0], [-0.6, -1.2, 0],
            color=self.PCA_C, fill_color=self.PCA_C, fill_opacity=0.25, stroke_width=2.5
        )
        pca_lbl = Text("PCA", font_size=26, weight=BOLD, color=PURPLE_A).move_to(pca_funnel)
        pca_group = VGroup(pca_funnel, pca_lbl).move_to(LEFT * 1.3 + UP * 1.1)
        pca_desc = Text("Giảm chiều (M ảnh)", font_size=16, color=self.TEXT_C).next_to(pca_group, DOWN, buff=0.3)

        self.play(FadeIn(pca_group, shift=LEFT*0.2), Write(pca_desc), run_time=1.0)

        # Tạo khối hộp dữ liệu nhỏ gọn đã rút gọn đặc trưng từ PCA
        pca_grid = VGroup()
        for i in range(4):
            for j in range(4):
                c = self.BLUE_C if np.random.random() > 0.5 else self.RED_C
                pca_grid.add(Square(side_length=0.18, fill_color=c, fill_opacity=0.9, stroke_width=0.4, stroke_color=BLACK))
        pca_grid.arrange_in_grid(4, 4, buff=0)
        
        # Diễn hoạt: Toàn bộ khối ma trận 3D thu nhỏ chui vào miệng phễu PCA
        self.play(
            matrices.animate.move_to(pca_funnel.get_left()).scale(0.1).set_opacity(0),
            run_time=1.5, rate_func=rush_into
        )
        
        # Diễn hoạt: Ma trận nhỏ gọn cô đọng đi ra từ đầu bên phải của PCA
        pca_grid.move_to(pca_funnel.get_right()).scale(0.1)
        self.play(
            pca_grid.animate.next_to(pca_group, RIGHT, buff=0.8).scale(10),
            run_time=1.5, rate_func=rush_from
        )
        self.wait(2.0)


        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 3: Phễu lọc LDA và Phân cụm Hoàn hảo (0:17 - 0:25)
        # ══════════════════════════════════════════════════════════════════════

        # Tạo hình khối phễu cho LDA
        lda_funnel = Polygon(
            [-0.5, 0.6, 0], [0.5, 0.15, 0], [0.5, -0.15, 0], [-0.5, -0.6, 0],
            color=self.LDA_C, fill_color=self.LDA_C, fill_opacity=0.25, stroke_width=2.5
        )
        lda_lbl = Text("FLD", font_size=22, weight=BOLD, color=ORANGE).move_to(lda_funnel)
        lda_group = VGroup(lda_funnel, lda_lbl).move_to(RIGHT * 2.6 + UP * 1.1)
        lda_desc = Text("Tối đa khoảng cách lớp", font_size=16, color=self.TEXT_C).next_to(lda_group, DOWN, buff=0.3)

        self.play(FadeIn(lda_group, shift=LEFT*0.2), Write(lda_desc), run_time=1.0)

        # Khởi tạo các cụm điểm phân tán chuẩn
        np.random.seed(10)
        blue_dots = VGroup(*[Dot(color=self.BLUE_C, radius=0.08).move_to([np.random.normal(5.6, 0.25), np.random.normal(1.9, 0.2), 0]) for _ in range(15)])
        red_dots  = VGroup(*[Dot(color=self.RED_C, radius=0.08).move_to([np.random.normal(5.6, 0.25), np.random.normal(0.3, 0.2), 0]) for _ in range(15)])
        
        # Mũi tên định hướng luồng phân tách bắn ra từ phễu LDA
        arrow_b = CurvedArrow(lda_funnel.get_right(), blue_dots.get_left() + LEFT*0.1, angle=-TAU/8, color=self.BLUE_C)
        arrow_r = CurvedArrow(lda_funnel.get_right(), red_dots.get_left() + LEFT*0.1, angle=TAU/8, color=self.RED_C)

        # Diễn hoạt: Ma trận rút gọn đi vào phễu LDA
        self.play(
            pca_grid.animate.move_to(lda_funnel.get_left()).scale(0.1).set_opacity(0),
            run_time=1.5, rate_func=rush_into
        )

        # Diễn hoạt: Phóng luồng mũi tên rẽ nhánh và bung ra các quần thể điểm phân cụm
        self.play(Create(arrow_b), Create(arrow_r), run_time=0.8)
        self.play(GrowFromCenter(blue_dots), GrowFromCenter(red_dots), run_time=1.0)
        
        # Dòng text kết luận
        final_text = Text("Phân loại hoàn hảo", font_size=18, color=GREEN_C, weight=BOLD).next_to(red_dots, DOWN, buff=0.4)
        self.play(FadeIn(final_text, shift=UP*0.2), run_time=0.5)
        self.wait(3.0)
        # Chọn ngẫu nhiên ảnh số 0 đại diện cho mỗi người 
        flash_img_b = ImageMobject(filename_or_array="face/face1/image_0.jpg").set_height(1.1)
        flash_img_r = ImageMobject(filename_or_array="face/face2/image_0.jpg").set_height(1.1)
        
        # Di chuyển ảnh đè chính xác lên tâm của cụm dot tương ứng
        flash_img_b.move_to(blue_dots.get_center())
        flash_img_r.move_to(red_dots.get_center())

        # Tạo viền màu tương ứng bao quanh ảnh để tăng tính đồng bộ nhận diện
        border_b = RoundedRectangle(corner_radius=0.04, width=flash_img_b.get_width()+0.08, 
                                    height=1.18, color=self.BLUE_C, stroke_width=3).move_to(flash_img_b)
        border_r = RoundedRectangle(corner_radius=0.04, width=flash_img_r.get_width()+0.08, 
                                    height=1.18, color=self.RED_C, stroke_width=3).move_to(flash_img_r)
        
        flash_group_b = Group(flash_img_b, border_b)
        flash_group_r = Group(flash_img_r, border_r)

        # Vòng lặp tạo hiệu ứng nhấp nháy 3 lần liên tục
        for _ in range(3):
            self.play(FadeIn(flash_group_b), FadeIn(flash_group_r), run_time=0.25)
            self.play(FadeOut(flash_group_b), FadeOut(flash_group_r), run_time=0.25)
            
        # Lần nhấp nháy cuối cùng sẽ giữ lại ảnh trên màn hình để người xem kịp quan sát
        self.play(FadeIn(flash_group_b), FadeIn(flash_group_r), run_time=0.25)
        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 4: Phân loại một ảnh mới (Inference)
        # ══════════════════════════════════════════════════════════════════════
        self.wait(1.5)
        
        self.play(FadeOut(final_text), run_time=0.5)
        inference_title = Text("Phân loại ảnh mới", color=YELLOW, font_size=22, weight=BOLD).shift(DOWN * 1.7)
        self.play(Write(inference_title))

        # 1. Dùng ảnh thật 
        unknown_img = ImageMobject("face/face1/image_4.jpg").set_height(0.85)
        unknown_rect = RoundedRectangle(corner_radius=0.05, width=unknown_img.width+0.05, height=unknown_img.height+0.05, 
                                        color=YELLOW, stroke_width=3).move_to(unknown_img)
        unknown_group = Group(unknown_img, unknown_rect).move_to(LEFT * 4.5 + UP * 1.5)
        
        unknown_lbl = Text("Ảnh cần phân loại", font_size=16, color=YELLOW).next_to(unknown_group, DOWN, buff=0.2)

        self.play(FadeIn(unknown_group, shift=DOWN*0.2), Write(unknown_lbl), run_time=1.0)
        self.wait(0.8)

        # 2. Chiếu ảnh đi qua PCA
        self.play(
            unknown_group.animate.move_to(pca_funnel.get_center()).scale(0.5),
            FadeOut(unknown_lbl),
            run_time=1.2
        )
        
        # 3. Chiếu ảnh đi qua FLD
        self.play(
            unknown_group.animate.move_to(lda_funnel.get_center()).scale(0.6),
            run_time=1.2
        )

        # 4. Trở thành vector đặc trưng
        new_dot = Dot(color=YELLOW, radius=0.12)
        target_point = flash_img_b.get_center() + LEFT * 1.4 + DOWN * 0.55
        new_dot.move_to(target_point)

        # 
        # Bước a: Cho bức ảnh thu nhỏ lại và bay về vị trí của dấu chấm
        self.play(
            unknown_group.animate.move_to(target_point).scale(0.15),
            run_time=0.7, rate_func=smooth
        )
        # Bước b: Tráo đổi ảnh bằng dấu chấm vàng
        self.play(
            FadeOut(unknown_group),
            GrowFromCenter(new_dot),
            run_time=0.3
        )
        
        new_dot_lbl = Text("Vector đặc trưng mới", font_size=14, color=YELLOW).next_to(unknown_group, UP, buff=0.1)
        self.play(FadeIn(new_dot_lbl))
        self.wait(1.0)

        # 5. Nhấp nháy 2 ảnh trung tâm trước khi đo để nhấn mạnh sự đối chiếu
        for _ in range(2):
            self.play(
                flash_group_b.animate.set_opacity(0.3).scale(1.1),
                flash_group_r.animate.set_opacity(0.3).scale(1.1), 
                run_time=0.2
            )
            self.play(
                flash_group_b.animate.set_opacity(1.0).scale(1/1.1),
                flash_group_r.animate.set_opacity(1.0).scale(1/1.1), 
                run_time=0.2
            )
        self.wait(0.5)

        # 6. Đo khoảng cách Euclidean
        line_b = DashedLine(unknown_group.get_center(), flash_img_b.get_center(), color=self.BLUE_C, stroke_width=2.5)
        line_r = DashedLine(unknown_group.get_center(), flash_img_r.get_center(), color=self.RED_C, stroke_width=2.5)

        d1_tex = MathTex("d_1", font_size=20, color=self.BLUE_C).next_to(line_b.get_center(), UP, buff=0.05)
        d2_tex = MathTex("d_2", font_size=20, color=self.RED_C).next_to(line_r.get_center(), DOWN, buff=0.05)

        self.play(Create(line_b), Write(d1_tex), run_time=0.8)
        self.play(Create(line_r), Write(d2_tex), run_time=0.8)
        self.wait(1.0)

        # 7. Kết luận
        conclusion = Text("Vì d1 < d2", font_size=22, weight=BOLD, color=YELLOW).next_to(inference_title, DOWN, buff=0.2)
        conclusion2 = Text("==> Ảnh thuộc class 1!", font_size=22, weight=BOLD, color=RED).next_to(inference_title, DOWN, buff=0.35)
        self.play(Write(conclusion), run_time=0.5)
        self.play(Write(conclusion2), run_time=0.5)
        # Rung cụm xanh để chốt kết quả
        self.play(
            Wiggle(flash_group_b, scale_value=1.15), 
            Wiggle(blue_dots, scale_value=1.1), 
            run_time=3
        )

        self.wait(3.5)

        # Dọn dẹp màn hình
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)