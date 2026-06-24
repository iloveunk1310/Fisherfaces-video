"""
Phân cảnh 3 — PCA: Eigenfaces & điểm yếu
==================================================
Render:   manim pc3.py PCA -pql
"""

from tkinter import CENTER
from manim import *
import numpy as np
import os

# Đường dẫn tuyệt đối đến thư mục chứa file .py này
_HERE = os.path.dirname(os.path.abspath(__file__))
Text.set_default(font="Be Vietnam Pro")

# ══════════════════════════════════════════════════════════════════════════════
#  Tạo ảnh eigenface tổng hợp
# ══════════════════════════════════════════════════════════════════════════════
def _eigenface_array(mode: int, size: int = 52) -> np.ndarray:
    cx, cy = size // 2, size // 2
    Y, X = np.mgrid[0:size, 0:size]
    dx = (X - cx) / (size * 0.38)
    dy = (Y - cy) / (size * 0.46)
    mask = np.clip(1.3 - (dx**2 + dy**2), 0, 1) ** 0.5

    patterns = [
        lambda u, v: np.exp(-(u**2 + v**2) / 0.5),
        lambda u, v: -u * np.exp(-(u**2 * 0.4 + v**2)),
        lambda u, v: -v * np.exp(-(u**2 + v**2 * 0.4)),
        lambda u, v: np.cos(np.pi * u) * np.exp(-v**2),
        lambda u, v: np.sin(np.pi * (u + v) * 0.8),
    ]
    core = patterns[mode % len(patterns)](dx, dy)
    rng  = np.random.default_rng(mode * 13 + 7)
    arr  = (core + rng.normal(0, 0.07, (size, size))) * mask
    lo, hi = arr.min(), arr.max()
    return ((arr - lo) / (hi - lo + 1e-8) * 210 + 22).astype(np.uint8)


def save_eigenfaces(n: int = 5) -> list:
    """
    Lưu n eigenfaces vào cùng thư mục với file .py.
    Trả về list đường dẫn TUYỆT ĐỐI để ImageMobject load được.
    """
    paths = []
    try:
        from PIL import Image
        for i in range(n):
            p = os.path.join(_HERE, f"face/face_{i}.jpg")   # ← absolute path, cùng thư mục .py
            Image.fromarray(_eigenface_array(i)).convert("RGB").save(p)
            paths.append(p)
    except Exception as exc:
        print(f"[warn] eigenface save failed: {exc}")
    return paths


# ══════════════════════════════════════════════════════════════════════════════
#  Helper: 1 dòng chú thích
# ══════════════════════════════════════════════════════════════════════════════
def _ann_row(sym_tex: str, desc: str, color) -> VGroup:
    return VGroup(
        MathTex(sym_tex, font_size=28, color=color),
        Text(desc, font_size=16, color=GREY_A),
    ).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)


# ══════════════════════════════════════════════════════════════════════════════
#  Scene chính
# ══════════════════════════════════════════════════════════════════════════════
class PCA(Scene):

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    PCA_C  = "#FFD54F"
    EIG_C  = "#CE93D8"

    def construct(self):
        # ── Dữ liệu (cùng seed với PCA vs LDA) ────────────────────────────────
        np.random.seed(2025)
        n = 15
        a = np.radians(45)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        Cov = R @ np.diag([2.2, 0.12]) @ R.T
        L   = np.linalg.cholesky(Cov)

        self._bp = (L @ np.random.randn(2, n)).T + [-2.0, 0.0]
        self._rp = (L @ np.random.randn(2, n)).T + [ 2.0, 0.0]

        all_pts  = np.vstack([self._bp, self._rp])
        centered = all_pts - all_pts.mean(0)
        _, _, Vt = np.linalg.svd(centered, full_matrices=False)
        self._dir = Vt[0] if Vt[0, 0] > 0 else -Vt[0]

        # ── Eigenfaces ────────────────────────────────────────────────────────
        self._ef_paths = save_eigenfaces(5)

        # ── Shared mobjects ────────────────────────────────────────────────────
        self._axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=8.5, y_length=4.8,
            axis_config={"color": WHITE, "include_tip": True, "stroke_width": 2},
        ).shift(UP * 0.8)

        self._bdots = VGroup(*[
            Dot(self._axes.c2p(*p), color=self.BLUE_C, radius=0.10)
            for p in self._bp
        ])
        self._rdots = VGroup(*[
            Dot(self._axes.c2p(*p), color=self.RED_C, radius=0.10)
            for p in self._rp
        ])

        d = self._dir
        self._pca_line = Line(
            self._axes.c2p(-4.5*d[0], -4.5*d[1]),
            self._axes.c2p( 4.5*d[0],  4.5*d[1]),
            color=self.PCA_C, stroke_width=2.5,
        )
        self._drops = VGroup(*[
            Line(
                self._axes.c2p(*p),
                self._axes.c2p(*(float(np.dot(p, d)) * d)),
                color=c, stroke_width=0.9, stroke_opacity=0.5,
            )
            for pts, c in [(self._bp, self.BLUE_C), (self._rp, self.RED_C)]
            for p in pts
        ])

        self._s1_projection()
        self._s2_formula()
        self._s3_eigenfaces()
        self._s4_weakness()

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân đoạn 1 — Chiếu PCA  (2:00 – 2:10)
    # ══════════════════════════════════════════════════════════════════════════
    
    def _s1_projection(self):
        title_p0 = Text("PHẦN 3: PCA - Phân tích thành phần chính", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        self.play(Create(self._axes), run_time=0.7)
        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in [*self._bdots, *self._rdots]],
                lag_ratio=0.05,
            ),
            run_time=1.2,
        )

        pca_tag = VGroup(
            Text("PCA", font_size=24, color=self.PCA_C, weight=BOLD),
            Text("(Principal Component Analysis)", font_size=16, color=GREY_A),
        ).arrange(RIGHT, buff=0.2).next_to(self._axes, DOWN, buff=0.22)

        self.play(Create(self._pca_line), Write(pca_tag), run_time=0.9)
        self.play(
            LaggedStart(*[Create(l) for l in self._drops], lag_ratio=0.025),
            run_time=1.2,
        )
        self.wait(4.0)
        self._pca_tag = pca_tag

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân đoạn 2 — Công thức PCA  (2:10 – 2:30)
    # ══════════════════════════════════════════════════════════════════════════
    def _s2_formula(self):
        # 1. GOM NHÓM VÀ THU NHỎ (Shrink & Shift)
        # Gom toàn bộ các mobject đã được khởi tạo từ _s1_projection
        left_group = VGroup(
            self._axes, 
            *self._bdots, 
            *self._rdots, 
            self._pca_line, 
            *self._drops, 
            self._pca_tag
        )
        
        # Di chuyển toàn bộ cụm sang bên trái màn hình
        self.play(
            left_group.animate.scale(0.7).to_edge(LEFT, buff=0.8),
            run_time=1.5
        )
        self.wait(0.5)

        # 2. XÂY DỰNG PANEL CÔNG THỨC BÊN PHẢI
        right_panel = VGroup()
        title = Text("Cơ chế cốt lõi của PCA", font_size=26, color=YELLOW, weight=BOLD)
        
        # Công thức 1: Phép chiếu (Tạo điểm y trên trục PCA)
        step1_title = Text("1. Phép chiếu 1D:", font_size=20, color=WHITE)
        eq1 = MathTex(r"y_i = \mathbf{w}^\top \mathbf{x}_i", font_size=45)
        # Tô màu đồng bộ với hình bên trái
        eq1[0][0:2].set_color(GREEN_B)       # y_i (Kết quả chiếu)
        eq1[0][3:5].set_color(self.PCA_C)    # w (Trục PCA)
        eq1[0][6:8].set_color(self.BLUE_C)   # x_i (Điểm dữ liệu gốc)
        step1 = VGroup(step1_title, eq1).arrange(DOWN, aligned_edge=LEFT)
        
        # Công thức 2: Tối đa hóa phương sai (Độ trải rộng của dữ liệu)
        step2_title = Text("2. Tối đa độ phân tán:", font_size=20, color=WHITE)
        eq2 = MathTex(r"\mathbf{w}^* = \arg\max_{\mathbf{w}} \text{Var}(y)", font_size=45)
        eq2[0][0:2].set_color(self.PCA_C)
        step2 = VGroup(step2_title, eq2).arrange(DOWN, aligned_edge=LEFT)
        
        # Căn chỉnh Panel bên phải
        right_panel.add(title, step1, step2).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        right_panel.to_edge(RIGHT, buff=1.0).shift(UP * 0.5)

        # Hiện tiêu đề và công thức 1
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(step1, shift=UP*0.2), run_time=1.0)

        # 3. TRỰC QUAN HÓA CÔNG THỨC 1 TRÊN HỆ TRỤC TRÁI
        # Lấy một điểm gốc đại diện
        sample_dot = self._bdots[-1] 
        sample_drop = self._drops[-1] 
        origin = self._axes.c2p(0, 0)
        
        # Vẽ Vector w (Chỉ phương của trục PCA)
        w_vec = Arrow(origin, self._pca_line.point_from_proportion(0.8), buff=0, color=self.PCA_C, stroke_width=4)
        w_lbl = MathTex(r"\mathbf{w}", color=self.PCA_C, font_size=32).next_to(w_vec.get_end(), UP, buff=0.1)

        # Vẽ Vector x_i (Tọa độ điểm gốc)
        x_vec = Arrow(origin, sample_dot.get_center(), buff=0, color=self.BLUE_C, stroke_width=3)
        x_lbl = MathTex(r"\mathbf{x}_i", color=self.BLUE_C, font_size=32).next_to(x_vec.get_end(), RIGHT, buff=0.1)

        # Đánh dấu Điểm y_i (Hình chiếu vuông góc)
        y_dot = Dot(sample_drop.get_end(), color=GREEN_B, radius=0.08)
        y_lbl = MathTex(r"y_i", color=GREEN_B, font_size=32).next_to(y_dot, DOWN, buff=0.1)

        # Hiệu ứng tuần tự cho Vector
        self.play(GrowArrow(w_vec), Write(w_lbl), run_time=1.0)
        self.play(GrowArrow(x_vec), Write(x_lbl), run_time=1.0)
        self.play(
            sample_drop.animate.set_color(GREEN_B).set_stroke(width=3), 
            FadeIn(y_dot, scale=0.5), 
            Write(y_lbl), 
            run_time=1.5
        )
        self.wait(0.5)

        # Hiện công thức 2
        self.play(FadeIn(step2, shift=UP*0.2), run_time=1.0)

        # 4. TRỰC QUAN HÓA CÔNG THỨC 2 (Phương sai)
        # Tạo một thanh đo lường bao trọn các hình chiếu trên trục PCA
        p_start = self._pca_line.point_from_proportion(0.15)
        p_end = self._pca_line.point_from_proportion(0.85)
        
        spread_arrow = DoubleArrow(p_start, p_end, buff=0, color=YELLOW, stroke_width=4)
        
        # Tính vector pháp tuyến để đẩy thanh đo này ra xa trục PCA một chút
        v = p_end - p_start
        n = np.array([-v[1], v[0], 0])
        if np.linalg.norm(n) > 0:
            n = n / np.linalg.norm(n) * 0.5  # Độ xa
        spread_arrow.shift(n)
        

        self.play(GrowFromCenter(spread_arrow), run_time=1.5)

        # Tạm nghỉ ở cuối phân cảnh
        self.wait(4.0)
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.2,
            rate_func=smooth
        )
        self.play(
            left_group.animate.scale(1 / 0.7).move_to(ORIGIN), 
            run_time=0.1,
            rate_func=smooth
        )
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.2,
            rate_func=smooth
        )
        self.wait(0.5)

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân đoạn 3 — Eigenfaces xuất hiện  (2:30 – 2:55)
    # ══════════════════════════════════════════════════════════════════════════
    def _s3_eigenfaces(self):
        ef_title = Text(
            "Eigenfaces  —  các khuôn mặt khác nhau",
            font_size=21, color=self.EIG_C,
        ).shift(UP * 0.5)

        n_ef = min(5, len(self._ef_paths))

        # dùng Group
        imgs = Group()
        lbls = VGroup()  

        for i in range(n_ef):
            pth = self._ef_paths[i] if i < len(self._ef_paths) else ""
            if pth and os.path.exists(pth):
                img = ImageMobject(pth).scale_to_fit_height(1.05)
            else:
                img = Rectangle(
                    height=1.05, width=0.88,
                    fill_color=self.EIG_C, fill_opacity=0.3,
                    stroke_color=self.EIG_C, stroke_width=1.2,
                )
            imgs.add(img)
            lbls.add(MathTex(rf"\phi_{{{i+1}}}", font_size=20, color=self.EIG_C))

        imgs.arrange(RIGHT, buff=0.35)
        imgs.next_to(ef_title, DOWN, buff=0.3)
        for i in range(len(lbls)):
            lbls[i].next_to(imgs[i], DOWN, buff=0.1)

        self.play(Write(ef_title), run_time=0.5)

        # không dùng LaggedStart với list có thể rỗng
        # → hiện từng ảnh riêng lẻ bằng vòng for
        for im in imgs:
            self.play(FadeIn(im, scale=1.3), run_time=0.28)

        if len(lbls) > 0:
            self.play(
                LaggedStart(*[Write(l) for l in lbls], lag_ratio=0.2),
                run_time=0.8,
            )

        self.wait(6.0)

        # Khôi phục scatter plot
        self.play(
            FadeOut(ef_title), FadeOut(imgs), FadeOut(lbls),
            run_time=0.6,
        )
        self.play(
            FadeIn(self._axes),
            FadeIn(self._bdots),
            FadeIn(self._rdots),
            FadeIn(self._pca_line),
            run_time=0.7,
        )
        # Ảnh Người A đè lên cụm đỏ
        person_lbl = Text(
            "Người A — cùng người, khác ánh sáng",
            font_size=16, color=self.RED_C,
        ).shift(DOWN * 2.3)
        self.play(Write(person_lbl), run_time=0.5)

        # face_at dùng Group vì chứa ImageMobject
        sel = [0, 2, 5, 8, 11]
        face_at = Group()
        for k, idx in enumerate(sel):
            pt  = self._rp[idx]
            pth = self._ef_paths[k % max(len(self._ef_paths), 1)] \
                  if self._ef_paths else ""
            if pth and os.path.exists(pth):
                f = ImageMobject(pth).scale_to_fit_height(0.68)\
                        .move_to(self._axes.c2p(*pt))
            else:
                f = Rectangle(
                    height=0.68, width=0.58,
                    fill_color=self.RED_C, fill_opacity=0.3,
                    stroke_color=self.RED_C,
                ).move_to(self._axes.c2p(*pt))
            face_at.add(f)

        self.play(FadeOut(self._rdots), run_time=0.3)
        for f in face_at:
            self.play(FadeIn(f, scale=1.2), run_time=0.18)
        self.wait(3.5)

        # xóa person_lbl TRƯỚC khi sang phân đoạn 4
        # → không còn "Person A" trên màn khi Classification Error xuất hiện
        self.play(
            FadeOut(face_at),
            FadeOut(person_lbl),
            FadeIn(self._rdots),
            run_time=0.6,
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  Phân đoạn 4 — Điểm yếu PCA: Overlap  (2:55 – 3:20)
    # ══════════════════════════════════════════════════════════════════════════
    def _s4_weakness(self):
        d = self._dir

        # Trục 1D
        nl = NumberLine(x_range=[-5, 5, 1], length=8.5,
                        color=WHITE, stroke_width=2).shift(DOWN * 2.3)
        ticks = VGroup(*[
            Line(UP * 0.10, DOWN * 0.10, color=GREY_B, stroke_width=1.5)
            .move_to(nl.n2p(x)) for x in range(-4, 5)
        ])
        nl_lbl = Text("trục PCA (chiếu 1D)", font_size=16, color=GREY_A)\
                     .next_to(nl, DOWN, buff=0.14)

        self.play(Create(nl), FadeIn(ticks), Write(nl_lbl), run_time=0.8)

        b_sc = [float(np.dot(p, d)) for p in self._bp]
        r_sc = [float(np.dot(p, d)) for p in self._rp]

        b1d = VGroup(*[
            Dot(nl.n2p(np.clip(s, -4.9, 4.9)), color=self.BLUE_C, radius=0.085)
            for s in b_sc
        ])
        r1d = VGroup(*[
            Dot(nl.n2p(np.clip(s, -4.9, 4.9)), color=self.RED_C, radius=0.085)
            for s in r_sc
        ])
        self.play(
            LaggedStart(*[GrowFromCenter(dd) for dd in [*b1d, *r1d]], lag_ratio=0.03),
            run_time=1.0,
        )
        self.wait(1.5)

        # Cảnh báo
        illum_lbl = Text(
            "Phương sai trong cùng một lớp (ánh sáng)  >>  Phương sai giữa các lớp",
            font_size=15, color=YELLOW,
        ).to_edge(UP, buff=0.12)
        self.play(Write(illum_lbl), run_time=0.8)

        # Kéo giãn cụm đỏ
        r_mean = float(np.mean(r_sc))
        r_wide = [r_mean + (s - r_mean) * 2.5 for s in r_sc]
        r1d_wide = VGroup(*[
            Dot(nl.n2p(np.clip(s, -4.9, 4.9)), color=self.RED_C, radius=0.085)
            for s in r_wide
        ])

        spread_note = Text("Người A phân tán (biến đổi ánh sáng)",
                           font_size=13, color=self.RED_C)\
                          .next_to(nl, UP, buff=0.18).shift(RIGHT * 1.8)

        self.play(
            Transform(r1d, r1d_wide),
            FadeIn(spread_note, shift=LEFT * 0.1),
            run_time=1.5, rate_func=smooth,
        )
        self.wait(0.4)

        # Overlap ellipse
        b_lo, b_hi = min(b_sc), max(b_sc)
        r_lo, r_hi = min(r_wide), max(r_wide)
        ov_lo = max(b_lo, r_lo)
        ov_hi = min(b_hi, r_hi)

        if ov_lo < ov_hi:
            ov_cx = (nl.n2p(ov_lo)[0] + nl.n2p(ov_hi)[0]) / 2
            ov_wd = max(abs(nl.n2p(ov_hi)[0] - nl.n2p(ov_lo)[0]) + 0.2, 0.4)
            ov_el = Ellipse(
                width=ov_wd, height=0.50,
                color=YELLOW, stroke_width=2.5,
                fill_color=YELLOW, fill_opacity=0.08,
            ).move_to([ov_cx, nl.get_center()[1], 0])
            self.play(FadeOut(spread_note), Create(ov_el), run_time=0.5)
            for _ in range(3):
                self.play(ov_el.animate.set_stroke(opacity=0.15), run_time=0.2)
                self.play(ov_el.animate.set_stroke(opacity=1.00), run_time=0.2)
        else:
            ov_el = VMobject()
            self.play(FadeOut(spread_note), run_time=0.3)

        # Nhãn lỗi ở góc riêng + BackgroundRectangle → không đè text khác
        err_txt = VGroup(
            MathTex(r"\times", font_size=32, color=RED),
            Text("Lỗi phân loại!", font_size=19, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.15)
        err_txt.to_corner(UR, buff=0.35).shift(DOWN * 0.55)

        err_bg = BackgroundRectangle(
            err_txt, color=BLACK, fill_opacity=0.88, buff=0.14,
        )
        err_full = VGroup(err_bg, err_txt)

        self.play(FadeIn(err_full, scale=1.3), run_time=0.6)
        self.wait(1.0)

        # Kết luận
        self.wait(8.0)

        # Fade out toàn bộ
        self.play(
            FadeOut(VGroup(
                self._axes, self._bdots, self._rdots, self._pca_line,
                nl, ticks, nl_lbl, b1d, r1d,
                illum_lbl, err_full,
            )),
            FadeOut(ov_el),
            run_time=1.5,
        )