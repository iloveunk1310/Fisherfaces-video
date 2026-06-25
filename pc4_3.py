"""
PC4 – Part 3: FLD Strengths & Weakness 
==============================================
Render:  manim pc4_3.py FLDPart3 -pqh
"""

from manim import *
import numpy as np

Text.set_default(font="Be Vietnam Pro")
class FLDPart3(Scene):

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    FLD_C  = "#FF8C42"
    SW_C   = "#EF9A9A"
    GRID_FILL  = "#0D2137"
    GRID_STK   = "#3A6EA5"
    RANK_FILL  = "#0D47A1"

    def construct(self):
        # ── Dữ liệu ──────────────────────────────────────────────────────────
        np.random.seed(2025)
        n = 15
        a = np.radians(45)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        Cov = R @ np.diag([2.2, 0.12]) @ R.T
        L   = np.linalg.cholesky(Cov)
        bp  = (L @ np.random.randn(2, n)).T + [-2.0, 0.0]
        rp  = (L @ np.random.randn(2, n)).T + [ 2.0, 0.0]
        mu_b, mu_r = bp.mean(0), rp.mean(0)
        Sw_mat = ((bp - mu_b).T @ (bp - mu_b) + (rp - mu_r).T @ (rp - mu_r))
        w = np.linalg.solve(Sw_mat, mu_r - mu_b)
        if w[0] < 0: w = -w
        w /= np.linalg.norm(w)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 1 — Điểm mạnh  (0:00 – 0:12)
        # ══════════════════════════════════════════════════════════════════════
        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=8.5, y_length=4.8,
            axis_config={"color": WHITE, "include_tip": True, "stroke_width": 2},
        ).shift(UP * 0.8)

        bdots = VGroup(*[Dot(axes.c2p(*p), color=self.BLUE_C, radius=0.10) for p in bp])
        rdots = VGroup(*[Dot(axes.c2p(*p), color=self.RED_C,  radius=0.10) for p in rp])
        fld_line = Line(
            axes.c2p(-4.5*w[0], -4.5*w[1]),
            axes.c2p( 4.5*w[0],  4.5*w[1]),
            color=self.FLD_C, stroke_width=2.5,
        )

        self.play(FadeIn(VGroup(axes, bdots, rdots, fld_line)), run_time=0.8)

        # Nhãn điểm mạnh 
        str_badge = VGroup(
            Text("Điểm mạnh:", font_size=20, color=GREEN_B, weight=BOLD),
            Text("Kháng ánh sáng & biểu cảm", font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.25)
        str_badge.next_to(axes, UP, buff=0.15).to_edge(LEFT, buff=0.3)

        

        self.play(Write(str_badge), run_time=0.7)

        # Các chấm đỏ nhấp nháy
        for _ in range(4):
            self.play(
                *[d.animate.set_fill(opacity=0.18) for d in rdots],
                run_time=0.22,
            )
            self.play(
                *[d.animate.set_fill(opacity=1.00) for d in rdots],
                run_time=0.22,
            )

        self.wait(6.0)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 2 — Điểm yếu: Ma trận suy biến  (0:12 – 0:22)
        # ══════════════════════════════════════════════════════════════════════
       
        self.play(
            FadeOut(VGroup(axes, bdots, rdots, fld_line, str_badge)),
            run_time=0.7,
        )

        # ── 2a: Lưới ô vuông N>>M ────────────────────────────────────────────
        # Lưới lớn = Sw: N×N matrix
        str_badge = VGroup(
            Text("Điểm yếu:", font_size=20, color=GREEN_B, weight=BOLD),
            Text("Ma trận suy biến", font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.25)
        str_badge.next_to(axes, UP, buff=0.15).to_edge(LEFT, buff=0.3)
        self.play(Write(str_badge), run_time=0.7)
        CELL = 0.24
        NR, NC = 10, 13
        big_grid = VGroup()
        for r in range(NR):
            for c in range(NC):
                sq = Square(
                    side_length=CELL,
                    fill_color=self.GRID_FILL, fill_opacity=0.88,
                    stroke_color=self.GRID_STK, stroke_width=0.45,
                )
                sq.move_to([
                    (c - NC / 2 + 0.5) * CELL,
                    (NR / 2 - 0.5 - r) * CELL,
                    0,
                ])
                big_grid.add(sq)
        big_grid.move_to(UP * 1.3)

        big_lbl = VGroup(
            Text("Sw :  N x N  ma trận", font_size=18, color=ORANGE, weight=BOLD),
            Text("N x N = 10,000+  chiều  (số pixel)", font_size=14, color=GREY_A),
        ).arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        big_lbl.next_to(big_grid, RIGHT, buff=0.35)

        # Cụm nhỏ = rank(Sw) ≤ M − c
        MR, MC = 2, 5
        small_grid = VGroup()
        for r in range(MR):
            for c in range(MC):
                sq = Square(
                    side_length=CELL * 0.9,
                    fill_color=self.RANK_FILL, fill_opacity=0.92,
                    stroke_color=self.BLUE_C, stroke_width=1.1,
                )
                sq.move_to([
                    (c - MC / 2 + 0.5) * CELL * 0.9,
                    (MR / 2 - 0.5 - r) * CELL * 0.9,
                    0,
                ])
                small_grid.add(sq)
        small_grid.next_to(big_grid, DOWN, buff=0.45)

        small_lbl = VGroup(

            Text("M = 50  ảnh  <<  N", font_size=14, color=GREY_A),
        ).arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        small_lbl.next_to(small_grid, RIGHT, buff=0.35)

        # Hiện lưới lớn
        self.play(
            LaggedStart(Create(big_grid), FadeIn(big_lbl), lag_ratio=0.4),
            run_time=1.1,
        )
        # Hiện cụm nhỏ
        self.play(GrowFromCenter(small_grid), FadeIn(small_lbl), run_time=0.7)

        # Lưới lớn đè xuống cụm nhỏ
        self.play(
            big_grid.animate.shift(DOWN * 0.55).scale(1.10),
            small_grid.animate.scale(0.40),
            run_time=1.3, rate_func=smooth,
        )
        self.wait(1.5)

        # ── 2b: Fade grid, phóng to Sw → Sw^{-1} ─────────────────────────────
        self.play(
            FadeOut(VGroup(big_grid, big_lbl, small_grid, small_lbl, str_badge)),
            run_time=0.6,
        )

        # Mẫu số: |w^T Sw w|
        denominator = MathTex(
            r"|\,\mathbf{w}^\top",
            r"\mathbf{S}_{w}",
            r"\mathbf{w}\,|",
            font_size=62,
        )
        denominator[1].set_color(self.SW_C)
        denominator.move_to(UP * 0.5)

        need_note = Text(
            "Giải FLD cần tính  ...",
            font_size=16, color=GREY_A,
        ).next_to(denominator, DOWN, buff=0.4)

        self.play(Write(denominator), run_time=0.7)
        self.play(FadeIn(need_note), run_time=0.4)
        self.wait(0.4)

        # Transform mẫu số → Sw^{-1} 
        sw_inv = MathTex(r"\mathbf{S}_{w}^{-1}", font_size=82, color=RED)
        sw_inv.move_to(denominator.get_center())

        self.play(
            Transform(denominator, sw_inv),
            FadeOut(need_note),
            run_time=0.85,
        )

        # ── 2c: Rung lắc + Flash ──────────────────────────────────────────────
        self.play(
            Wiggle(
                denominator,
                scale_value=1.28,
                rotation_angle=0.025 * TAU,
                n_wiggles=5,
            ),
            run_time=1.4,
        )
        self.play(
            Flash(
                denominator.get_center(),
                color=RED, flash_radius=0.9, num_lines=10, line_length=0.3,
            ),
            run_time=0.4,
        )

        # ── 2d: "SINGULAR MATRIX!" nhấp nháy ─────────────────────────────────
        warn_text = Text("MA TRẬN SUY BIẾN!", font_size=30, color=RED, weight=BOLD)
        warn_bg   = BackgroundRectangle(warn_text, color=BLACK,
                                        fill_opacity=0.90, buff=0.20)
        warning   = VGroup(warn_bg, warn_text)
        warning.next_to(denominator, DOWN, buff=0.55)

        self.play(FadeIn(warning, scale=1.35), run_time=0.45)

        for _ in range(4):
            self.play(warn_text.animate.set_fill(opacity=0.08), run_time=0.18)
            self.play(warn_text.animate.set_fill(opacity=1.00), run_time=0.18)

        # ══════════════════════════════════════════════════════════════════════
        #  PHASE 3 — gợi mở giải pháp  (0:22 – 0:30)
        # ══════════════════════════════════════════════════════════════════════
        # Giải pháp: Fisherfaces = PCA + FLD
        solution = VGroup(
            Text("Giải pháp:", font_size=19, color=GREEN_B, weight=BOLD),
            Text("Fisherfaces  =  PCA  +  FLD", font_size=19, color=GREEN_B),
        ).arrange(RIGHT, buff=0.22)
        solution.shift(DOWN * 2.0)

        self.wait(3.0)
        self.play(Write(solution), run_time=0.9)
        self.wait(6.0)

        # Fade out toàn bộ
        self.play(
            FadeOut(VGroup(denominator, warning, solution)),
            run_time=1.0,
        )