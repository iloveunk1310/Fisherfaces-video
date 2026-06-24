"""
Face Recognition in Subspaces  — Manim animation
=========================================================

Render:
    manim pc1.py FaceSubspace -pqh 
"""

from manim import *
import numpy as np
import os

Text.set_default(font="Be Vietnam Pro")
# ══════════════════════════════════════════════════════════════════════════════
#  Synthetic face generator
# ══════════════════════════════════════════════════════════════════════════════
def generate_face(path: str, size: int = 64) -> None:
    arr = np.full((size, size), 18, dtype=np.uint8)
    cx, cy = size // 2, int(size * 0.53)

    # Oval mặt
    for y in range(size):
        for x in range(size):
            dx = (x - cx) / (size * 0.36)
            dy = (y - cy) / (size * 0.45)
            r2 = dx**2 + dy**2
            if r2 < 1.0:
                arr[y, x] = int(140 + 50 * (1 - r2))

    # Mắt
    for ex_, ey_ in [
        (cx - int(size * 0.17), cy - int(size * 0.14)),
        (cx + int(size * 0.17), cy - int(size * 0.14)),
    ]:
        for y in range(size):
            for x in range(size):
                if (x - ex_) ** 2 / (size * 0.075) ** 2 + \
                   (y - ey_) ** 2 / (size * 0.055) ** 2 < 1:
                    arr[y, x] = 30

    # Miệng
    for y in range(cy + int(size * 0.18), cy + int(size * 0.25)):
        for x in range(cx - int(size * 0.18), cx + int(size * 0.19)):
            if arr[y, x] > 40:
                arr[y, x] = 55

    from PIL import Image
    Image.fromarray(arr).convert("RGB").save(path)


# ══════════════════════════════════════════════════════════════════════════════
#  Scene chính
# ══════════════════════════════════════════════════════════════════════════════
class FaceSubspace(ThreeDScene):

    
    FACE_PATH = "face.jpg"

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"

    # ── Khởi động ──────────────────────────────────────────────────────────────
    def construct(self):
        if not os.path.exists(self.FACE_PATH):
            fallback = "/tmp/_mface.png"
            generate_face(fallback)
            self.FACE_PATH = fallback

        self._arr8 = self._to_gray8(self.FACE_PATH, n=8)

        # Bắt đầu ở góc nhìn 2D (camera nhìn thẳng từ trên)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        self._s1_matrix()    # 0:00 – 0:12  ảnh → ma trận pixel
        self._s2_flatten()   # 0:12 – 0:24  trải phẳng → vector → chấm
        self._s3_cloud()     # 0:24 – 0:40  không gian 3D + đám mây điểm
        self._s4_subspace()  # 0:40 – 0:55  mặt phẳng con + chiếu

    # ── Tiện ích ───────────────────────────────────────────────────────────────
    @staticmethod
    def _to_gray8(path: str, n: int = 8) -> np.ndarray:
        try:
            from PIL import Image
            return np.array(Image.open(path).convert("L").resize((n, n)))
        except Exception:
            rng = np.random.default_rng(0)
            return rng.integers(50, 220, (n, n), dtype=np.uint8)

    @staticmethod
    def _gray_color(v: int):
        t = v / 255.0
        return rgb_to_color([t, t, t])

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân cảnh 1 — Ảnh khuôn mặt → Ma trận pixel  (0:00 – 0:12)
    # ══════════════════════════════════════════════════════════════════════════
    def _s1_matrix(self):
        title_p0 = Text("PHẦN 1: TỔNG QUAN BÀI TOÁN", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        # Ảnh gốc fade in
        face = ImageMobject(self.FACE_PATH).set_height(3.4).move_to(ORIGIN)
        self.play(FadeIn(face), run_time=1.0)
        self.wait(0.4)

        # Lưới 8×8 đè lên ảnh — mỗi ô = một pixel
        CELL = 0.41
        cells = VGroup()
        nums  = VGroup()
        for r in range(8):
            for c in range(8):
                v = int(self._arr8[r, c])
                sq = Square(
                    side_length=CELL,
                    fill_color=self._gray_color(v), fill_opacity=0.85,
                    stroke_color=WHITE, stroke_width=0.8,
                ).move_to([(c - 3.5) * CELL, (3.5 - r) * CELL, 0])
                cells.add(sq)
                nums.add(
                    Text(str(v), font_size=7, color=WHITE)
                    .move_to(sq.get_center())
                )

        self.play(FadeIn(cells), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.025),
            run_time=1.3,
        )

        # Nhãn giải thích
        lbl = Text("ma trận pixel m × n", font_size=26, color=YELLOW)\
                  .shift(DOWN * 2.3)
        self.play(Write(lbl), run_time=0.7)
        self.wait(5.8)
        self.play(FadeOut(face), FadeOut(lbl), run_time=0.5)

        # Lưu cho phân cảnh 2
        self._cells = cells
        self._nums  = nums

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân cảnh 2 — Trải phẳng → vector → chấm sáng  (0:12 – 0:24)
    # ══════════════════════════════════════════════════════════════════════════
    def _s2_flatten(self):
        cells = self._cells

        # Sắp xếp column-major
        col_major = [cells[r * 8 + c] for c in range(8) for r in range(8)]

        # Vị trí đích: cột dọc bên phải
        CELL_NEW = 0.085          # chiều cao mỗi ô sau khi thu nhỏ
        STACK_X  = 3.1
        half_h   = 64 * CELL_NEW / 2
        targets  = [
            np.array([STACK_X, half_h - i * CELL_NEW, 0]) for i in range(64)
        ]
        scale_f  = CELL_NEW / 0.41   # tỉ lệ thu nhỏ

        self.play(FadeOut(self._nums), run_time=0.25)

        # Animate từng ô dịch về vị trí trong vector
        self.play(
            LaggedStart(
                *[c.animate.move_to(t).scale(scale_f)
                  for c, t in zip(col_major, targets)],
                lag_ratio=0.013,
            ),
            run_time=2.5,
        )

        vec_lbl = MathTex(
            r"\mathbf{x} \in \mathbb{R}^{mn}", font_size=30, color=YELLOW,
        ).move_to([-2.3, 0, 0])
        self.play(Write(vec_lbl), run_time=0.7)
        self.wait(0.5)

        # Thu nhỏ toàn bộ vector → một chấm sáng (1 ảnh = 1 điểm)
        self.play(
            VGroup(*col_major).animate.move_to(ORIGIN),
            FadeOut(vec_lbl),
            run_time=0.9, rate_func=smooth,
        )
        dot = Dot(ORIGIN, radius=0.18, color=WHITE)
        self.play(
            FadeOut(VGroup(*col_major)),
            FadeIn(dot, scale=2.5),
            run_time=0.6,
        )

        cap = Text(
            "1 ảnh khuôn mặt  =  1 điểm trong không gian nhiều chiều",
            font_size=23, color=GREY_A,
        ).shift(DOWN * 2.3)
        self.play(Write(cap), run_time=0.8)
        self.wait(4.8)
        self.play(FadeOut(dot), FadeOut(cap), run_time=0.5)

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân cảnh 3 — Không gian 3D + phân bố dữ liệu  (0:24 – 0:40)
    # ══════════════════════════════════════════════════════════════════════════
    def _s3_cloud(self):
        # Chuyển camera sang góc nhìn 3D
        self.move_camera(phi=70 * DEGREES, theta=-58 * DEGREES, run_time=1.5)

        axes = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-3, 3, 1],
            x_length=7.5, y_length=7.5, z_length=5.5,
            axis_config={
                "stroke_width": 2, "include_tip": True, "tip_length": 0.22,
            },
        )
        self.play(Create(axes), run_time=1.0)

        # Nhãn số chiều 
        hint = Text(
            "Không gian ảnh\nN x M  (số pixel)",
            font_size=21, color=YELLOW,
        ).to_corner(UR, buff=0.3)
        self.add_fixed_in_frame_mobjects(hint)
        self.play(FadeIn(hint, shift=LEFT * 0.15), run_time=0.7)

        # Hai cụm điểm (xanh = class A, đỏ = class B)
        np.random.seed(99)
        dot_info = [] 
        all_dots = VGroup()

        clusters = [
            (self.BLUE_C, np.array([-1.3,  0.7,  0.7])),
            (self.RED_C,  np.array([ 1.3, -0.7, -0.7])),
        ]
        for color, center in clusters:
            pts = np.random.randn(20, 3) * np.array([0.5, 0.45, 0.5]) + center
            for p in pts:
                d = Dot3D(
                    point=axes.c2p(*p),
                    color=color, radius=0.07, fill_opacity=0.9,
                )
                all_dots.add(d)
                dot_info.append((d, p))

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in all_dots], lag_ratio=0.04),
            run_time=2.0,
        )

        # Xoay camera chậm rãi cho người xem thấy không gian
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(hint), run_time=0.4)

        # Lưu cho phân cảnh 4
        self._axes3d   = axes
        self._dot_info = dot_info

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân cảnh 4 — Mặt phẳng con + chiếu điểm  (0:40 – 0:55)
    # ══════════════════════════════════════════════════════════════════════════
    def _s4_subspace(self):
        axes     = self._axes3d
        dot_info = self._dot_info

        self.move_camera(phi=62 * DEGREES, theta=-45 * DEGREES, run_time=1.2)

        # ── Mặt phẳng con: z = 0 (subspace 2D) ───────────────────────────────
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-3.0, 3.0],
            v_range=[-3.0, 3.0],
            fill_color=BLUE_D,
            fill_opacity=0.28,
            checkerboard_colors=False,
            stroke_width=0.5,
        )
        plane.set_stroke(BLUE_B, opacity=0.15)

        sub_lbl = Text(
            "Không gian con khuôn mặt  (manifold 2D)",
            font_size=22, color=BLUE_B,
        ).to_corner(UL, buff=0.3)
        self.add_fixed_in_frame_mobjects(sub_lbl)

        self.play(
            Create(plane),
            FadeIn(sub_lbl, shift=RIGHT * 0.2),
            run_time=1.3,
        )
        self.wait(3)

        # ── Chiếu từng điểm 3D xuống mặt phẳng (z → 0) ──────────────────────
        drop_lines = VGroup()
        proj_anims = []

        for dot, pos3d in dot_info:
            proj3d = np.array([pos3d[0], pos3d[1], 0.0])
            line = DashedLine(
                axes.c2p(*pos3d),
                axes.c2p(*proj3d),
                color=GREY_B,
                stroke_width=0.9, stroke_opacity=0.5,
                dash_length=0.12,
            )
            drop_lines.add(line)
            proj_anims.append(
                AnimationGroup(
                    Create(line),
                    dot.animate.move_to(axes.c2p(*proj3d)),
                )
            )

        self.play(
            LaggedStart(*proj_anims, lag_ratio=0.04),
            run_time=3.5,
        )

        # ── Kết: tên các phương pháp ──────────────────────────────────────────
        final_cap = Text(
            "PCA  ·  LDA  ·  Fisherfaces",
            font_size=22, color=WHITE, line_spacing=1.25,
        ).shift(DOWN * 2.4)
        self.add_fixed_in_frame_mobjects(final_cap)
        self.play(Write(final_cap), run_time=1.0)

        # Xoay nhẹ để kết thúc
        self.begin_ambient_camera_rotation(rate=0.07)
        self.wait(7.5)
        self.stop_ambient_camera_rotation()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
