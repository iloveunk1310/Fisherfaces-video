"""
Phân cảnh 2 — PCA vs LDA
==================================================
Render:   manim pc2.py PCAvsLDA -pql 
"""
from manim import *
import numpy as np
Text.set_default(font="Be Vietnam Pro")

class PCAvsLDA(Scene):
    def construct(self):
        np.random.seed(2025)
        n = 15

        # Within-class covariance rotated at 45° → PCA ≈ +12°, LDA ≈ −40°
        angle_cov = np.radians(45)
        R = np.array([[np.cos(angle_cov), -np.sin(angle_cov)],
                      [np.sin(angle_cov),  np.cos(angle_cov)]])
        Cov = R @ np.diag([2.2, 0.12]) @ R.T
        L = np.linalg.cholesky(Cov)

        blue_pts = (L @ np.random.randn(2, n)).T + [-2.0, 0.0]
        red_pts  = (L @ np.random.randn(2, n)).T + [ 2.0, 0.0]
        all_pts  = np.vstack([blue_pts, red_pts])

        # PCA 
        centered = all_pts - all_pts.mean(axis=0)
        _, _, Vt = np.linalg.svd(centered, full_matrices=False)
        pca_dir = Vt[0] if Vt[0, 0] > 0 else -Vt[0]
        pca_angle = float(np.arctan2(pca_dir[1], pca_dir[0]))

        # LDA
        mu_b, mu_r = blue_pts.mean(0), red_pts.mean(0)
        Sw = ((blue_pts - mu_b).T @ (blue_pts - mu_b) +
              (red_pts  - mu_r).T @ (red_pts  - mu_r))
        lda_raw = np.linalg.solve(Sw, mu_r - mu_b)
        lda_dir = lda_raw / np.linalg.norm(lda_raw)
        if lda_dir[0] < 0:
            lda_dir = -lda_dir
        lda_angle = float(np.arctan2(lda_dir[1], lda_dir[0]))

        # ── Colors & layout ────────────────────────────────────────────────────
        BLUE_C   = "#4FC3F7"
        RED_C    = "#EF5350"
        LINE_C   = "#FFD54F"
        PCA_C    = "#FFD54F"
        LDA_C    = "#FF8C42"

        UP_SHIFT = UP * 0.85

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=9, y_length=5,
            axis_config={
                "color": WHITE, "include_tip": True,
                "stroke_width": 2, "tip_length": 0.2,
            },
        ).shift(UP_SHIFT)

        number_line = NumberLine(
            x_range=[-5, 5, 1], length=9,
            color=WHITE, stroke_width=2,
            include_numbers=False,
        ).shift(DOWN * 2.3)

        tick_marks = VGroup(*[
            Line(UP * 0.1, DOWN * 0.1, color=GREY_B, stroke_width=1.5)
            .move_to(number_line.n2p(x))
            for x in range(-4, 5)
        ])

        proj_label = Text("Giá trị chiếu - Projected value", font_size=22, color=GREY_B)\
                     .next_to(number_line, DOWN, buff=0.18)

        # ── Data dots (2D scatter) ─────────────────────────────────────────────
        blue_dots = VGroup(*[
            Dot(axes.c2p(p[0], p[1]), color=BLUE_C, radius=0.10,
                fill_opacity=0.92)
            for p in blue_pts
        ])
        red_dots = VGroup(*[
            Dot(axes.c2p(p[0], p[1]), color=RED_C,  radius=0.10,
                fill_opacity=0.92)
            for p in red_pts
        ])

        # ── Angle tracker ──────────────────────────────────────────────────────
        ang = ValueTracker(PI / 2.8)    # start ≈ 64°

        # ── Helper functions ───────────────────────────────────────────────────
        def proj2d(pt, a):
            d = np.array([np.cos(a), np.sin(a)])
            return np.dot(pt, d) * d

        def proj1d_scalar(pt, a):
            d = np.array([np.cos(a), np.sin(a)])
            return float(np.dot(pt, d))

        # ── Rotating projection line───────────────────────────
        def make_rot_line():
            a = ang.get_value()
            d = np.array([np.cos(a), np.sin(a)])
            return Line(
                axes.c2p(-4.6 * d[0], -4.6 * d[1]),
                axes.c2p( 4.6 * d[0],  4.6 * d[1]),
                color=LINE_C, stroke_width=2.8,
            )

        rot_line = always_redraw(make_rot_line)

        # ── Perpendicular projection lines (2D → line) ────────────────────────
        def make_proj_seg(pt, color):
            obj = Line(
                axes.c2p(pt[0], pt[1]),
                axes.c2p(pt[0] + 0.01, pt[1]),
                color=color, stroke_width=1.1, stroke_opacity=0.5,
            )

            def upd(m):
                pp = proj2d(pt, ang.get_value())
                s = axes.c2p(pt[0], pt[1])
                e = axes.c2p(pp[0], pp[1])
                if np.linalg.norm(np.array(e) - np.array(s)) > 0.04:
                    try:
                        m.put_start_and_end_on(s, e)
                    except Exception:
                        pass

            obj.add_updater(upd)
            return obj

        # ── Projected dots on 2D line ──────────────────────────────────────────
        def make_dot2d(pt, color):
            obj = Dot(color=color, radius=0.07, fill_opacity=0.8)

            def upd(m):
                pp = proj2d(pt, ang.get_value())
                m.move_to(axes.c2p(pp[0], pp[1]))

            obj.add_updater(upd)
            return obj

        # ── Projected dots on 1D number line ──────────────────────────────────
        def make_dot1d(pt, color):
            obj = Dot(color=color, radius=0.09, fill_opacity=0.95)

            def upd(m):
                s = np.clip(proj1d_scalar(pt, ang.get_value()), -4.9, 4.9)
                m.move_to(number_line.n2p(s))

            obj.add_updater(upd)
            return obj

        b_segs = VGroup(*[make_proj_seg(p, BLUE_C) for p in blue_pts])
        r_segs = VGroup(*[make_proj_seg(p, RED_C)  for p in red_pts])
        b_d2   = VGroup(*[make_dot2d(p, BLUE_C)    for p in blue_pts])
        r_d2   = VGroup(*[make_dot2d(p, RED_C)     for p in red_pts])
        b_d1   = VGroup(*[make_dot1d(p, BLUE_C)    for p in blue_pts])
        r_d1   = VGroup(*[make_dot1d(p, RED_C)     for p in red_pts])

        # ── Labels ────────────────────────────────────────────────────────────
        pca_lbl = VGroup(
            Text("PCA", font_size=34, color=PCA_C, weight=BOLD),
            Text("==> phân tán tốt nhất", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)\
         .to_corner(UL).shift(RIGHT * 0.1 + DOWN * 0.15)

        lda_lbl = VGroup(
            Text("LDA", font_size=34, color=LDA_C, weight=BOLD),
            Text("==> phân nhóm tốt nhất", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)\
         .to_corner(UR).shift(LEFT * 1.6 + DOWN * 0.15)

        # Angle arc + annotation
        def make_angle_arc(a, color, label_str):
            arc = Arc(radius=0.6, angle=a, start_angle=0,
                      color=color, stroke_width=2)
            arc.shift(axes.c2p(0, 0))
            deg_txt = Text(f"{np.degrees(a):.0f}°",
                           font_size=18, color=color)\
                          .next_to(arc, RIGHT, buff=0.05)
            return VGroup(arc, deg_txt)

        pca_arc = make_angle_arc(pca_angle, PCA_C, "PCA")
        lda_arc = make_angle_arc(lda_angle, LDA_C, "LDA")

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text("PCA  vs  LDA", font_size=36, weight=BOLD)\
                    .to_edge(UP, buff=0.15)
        title[0:3].set_color(PCA_C)   # "PCA"
        title[7:10].set_color(LDA_C)  # "LDA"

        # ═════════════════════════════════════════════════════════════════════
        # ANIMATION
        # ═════════════════════════════════════════════════════════════════════
        title_p0 = Text("PHẦN 2: CÁC PHƯƠNG PHÁP GIẢM CHIỀU", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        # 0 – 2s: Title flash
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2 - 5s: Axes + number line
        self.play(
            Create(axes),
            Create(number_line),
            FadeIn(tick_marks),
            Write(proj_label),
            run_time=1.5,
        )
        self.wait(1)

        # 5 - 10s: Data points appear
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in blue_dots], lag_ratio=0.08),
            run_time=1.6,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in red_dots], lag_ratio=0.08),
            run_time=1.6,
        )
        self.wait(1)

        # 10 - 15s: Show rotation line + projections
        self.add(rot_line)
        self.play(
            *[Create(s) for s in [*b_segs, *r_segs]],
            *[GrowFromCenter(d) for d in [*b_d2, *r_d2, *b_d1, *r_d1]],
            run_time=1.6,
        )
        self.wait(3)

        # 15 - 22s: Rotate to PCA direction
        self.play(
            ang.animate.set_value(pca_angle),
            run_time=4.5,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.wait(2.0)

        # 22 - 26s: PCA label + arc
        self.play(
            FadeIn(pca_lbl, shift=RIGHT * 0.25),
            Create(pca_arc),
            run_time=1.0,
        )
        self.wait(3.0)

        # 26 - 34s: Rotate to LDA direction
        self.play(
            FadeOut(pca_arc),
            ang.animate.set_value(lda_angle),
            run_time=4.5,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.wait(3.0)

        # 34 - 45s: LDA label + arc
        self.play(
            FadeIn(lda_lbl, shift=LEFT * 0.25),
            Create(lda_arc),
            run_time=1.0,
        )
        self.wait(10.0)

        self.play(FadeOut(VGroup(axes, number_line, tick_marks, proj_label, blue_dots, red_dots, 
        b_segs, r_segs, b_d2, r_d2, b_d1, r_d1, pca_lbl, lda_lbl, pca_arc, lda_arc, title, rot_line)), run_time=1.5)
