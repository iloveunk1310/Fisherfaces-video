"""
PC4 – Part 2: FLD Formula
======================================================
Render:  manim pc4_2.py FLDPart2 -pqh
"""

from manim import *
import numpy as np
Text.set_default(font="Be Vietnam Pro")

class FLDPart2(Scene):

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    FLD_C  = "#FF8C42"
    SB_C   = "#66BB6A"   # xanh lá: between-class scatter
    SW_C   = "#EF9A9A"   # hồng: within-class scatter 

    def construct(self):
        # ── Dữ liệu ──────────────────────────────────────────────────────────
        np.random.seed(2025)
        n = 15
        a = np.radians(45)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        Cov = R @ np.diag([2.2, 0.12]) @ R.T
        L   = np.linalg.cholesky(Cov)

        bp = (L @ np.random.randn(2, n)).T + [-2.0, 0.0]
        rp = (L @ np.random.randn(2, n)).T + [ 2.0, 0.0]

        mu_b, mu_r = bp.mean(0), rp.mean(0)
        Sw_mat = ((bp - mu_b).T @ (bp - mu_b) + (rp - mu_r).T @ (rp - mu_r))
        w = np.linalg.solve(Sw_mat, mu_r - mu_b)
        if w[0] < 0: w = -w
        w /= np.linalg.norm(w)

        # ── Scatter plot nhỏ bên trái ─────────────────────────────────────────
        axes_sm = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=4.6, y_length=3.3,
            axis_config={"color": WHITE, "include_tip": True, "stroke_width": 1.5},
        ).shift(LEFT * 3.5 + UP * 0.3)

        bdots = VGroup(*[Dot(axes_sm.c2p(*p), color=self.BLUE_C, radius=0.08) for p in bp])
        rdots = VGroup(*[Dot(axes_sm.c2p(*p), color=self.RED_C,  radius=0.08) for p in rp])

        fld_sm = Line(
            axes_sm.c2p(-4.5*w[0], -4.5*w[1]),
            axes_sm.c2p( 4.5*w[0],  4.5*w[1]),
            color=self.FLD_C, stroke_width=2.2,
        )
        plot_tag = Text("FLD — hướng tối ưu", font_size=12, color=self.FLD_C)\
                       .next_to(axes_sm, DOWN, buff=0.1)

        # Tâm cụm trên màn hình 
        MU_B_SCR = np.array(axes_sm.c2p(*mu_b))
        MU_R_SCR = np.array(axes_sm.c2p(*mu_r))

        # ── Phase 1 (0:00–0:02): scatter plot xuất hiện ───────────────────────
        self.play(
            FadeIn(VGroup(axes_sm, bdots, rdots, fld_sm, plot_tag)),
            run_time=1.2,
        )

        # ─────────────────────────────────────────────────────────────────────
        #  Bảng công thức bên phải
        # ─────────────────────────────────────────────────────────────────────
        RX = RIGHT * 2.3   # trung tâm ngang panel phải

        panel_title = Text("Mục tiêu FLD", font_size=22, color=self.FLD_C, weight=BOLD)\
                          .shift(RX + UP * 3.35)

        # Công thức J(w) — tách Sb và Sw thành arg riêng để tô màu chính xác
        J_eq = MathTex(
            r"J(\mathbf{w}) = \frac{",      # [0]
            r"| \mathbf{w}^\top ",          # [1]
            r"\mathbf{S}_b",                # [2]  <-- Cần tô màu
            r" \mathbf{w} |",               # [3]
            r"}{",                          # [4]
            r"| \mathbf{w}^\top ",          # [5]
            r"\mathbf{S}_w",                # [6]  <-- Cần tô màu
            r" \mathbf{w} |",               # [7]
            r"}",                           # [8]
            font_size=38
        )
        
        # Gán màu dựa trên đúng index
        J_eq[2].set_color(self.SB_C)
        J_eq[6].set_color(self.SW_C)
        J_eq.next_to(panel_title, DOWN, buff=0.3)

        # Định nghĩa Sb
        Sb_title = VGroup(
            Text("Phân tán giữa các lớp:", font_size=15, color=self.SB_C, weight=BOLD),
        )
        Sb_formula = MathTex(
            r"\mathbf{S}_b",
            r"= \textstyle\sum_i N_i\,",
            r"(\boldsymbol{\mu}_i - \boldsymbol{\mu})",
            r"(\boldsymbol{\mu}_i - \boldsymbol{\mu})^\top",
            font_size=20, color=self.SB_C,
        )
        Sb_note = Text("Sb lớn  =  tâm cụm xa nhau  ==>  tốt!",
                       font_size=13, color=self.SB_C)
        Sb_block = VGroup(Sb_title, Sb_formula, Sb_note)\
                       .arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        Sb_block.next_to(J_eq, DOWN, buff=0.38)

        # Định nghĩa Sw
        Sw_title = VGroup(
            Text("Phân tán trong cùng một lớp:", font_size=15, color=self.SW_C, weight=BOLD),
        )
        Sw_formula = MathTex(
            r"\mathbf{S}_w",
            r"= \textstyle\sum_{i}\sum_{\mathbf{x}\in X_i}",
            r"(\mathbf{x} - \boldsymbol{\mu}_i)",
            r"(\mathbf{x} - \boldsymbol{\mu}_i)^\top",
            font_size=20, color=self.SW_C,
        )
        Sw_note = Text("Sw nhỏ  =  cùng lớp compact  ==>  tốt!",
                       font_size=13, color=self.SW_C)
        Sw_block = VGroup(Sw_title, Sw_formula, Sw_note)\
                       .arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        Sw_block.next_to(Sb_block, DOWN, buff=0.28)

        # Công thức nghiệm w*
        w_star = MathTex(
            r"\mathbf{w}^* =",
            r"\mathbf{S}_w^{-1}",
            r"(\boldsymbol{\mu}_1 - \boldsymbol{\mu}_2)",
            font_size=30,
        )
        w_star[1].set_color(self.SW_C)
        w_star[2].set_color(self.SB_C)
        w_star.next_to(Sw_block, DOWN, buff=0.35)

        w_note = Text("==> maximize J: khoảng cách lớn, cùng lớp compact",
                      font_size=13, color=self.FLD_C)\
                     .next_to(w_star, DOWN, buff=0.14)

        # ── Phase 2 (0:02–0:05): tiêu đề + J(w) xuất hiện ────────────────────
        self.play(Write(panel_title), run_time=0.5)
        self.play(Write(J_eq), run_time=1.2)
        self.wait(0.8)

        # ── Phase 3 (0:05–0:14): giải thích Sb ───────────────────────────────
        # 3a: khoanh vùng Sb trong công thức
        sb_rect = SurroundingRectangle(J_eq[2], color=self.SB_C,
                                       buff=0.07, corner_radius=0.05, stroke_width=1.8)
        self.play(Create(sb_rect), run_time=0.45)

        # 3b: hiện Sb formula + note
        self.play(
            LaggedStart(
                Write(Sb_title),
                Write(Sb_formula),
                FadeIn(Sb_note, shift=UP * 0.06),
                lag_ratio=0.4,
            ),
            run_time=1.4,
        )

        # 3c: center markers + mũi tên always_redraw
        mu_b_dot = Dot(MU_B_SCR, color=self.BLUE_C, radius=0.14)
        mu_r_dot = Dot(MU_R_SCR, color=self.RED_C,  radius=0.14)
        mu_b_tex = MathTex(r"\boldsymbol{\mu}_B", font_size=17, color=self.BLUE_C)\
                       .next_to(mu_b_dot, UP, buff=0.06)
        mu_r_tex = MathTex(r"\boldsymbol{\mu}_R", font_size=17, color=self.RED_C)\
                       .next_to(mu_r_dot, UP, buff=0.06)

        def get_sb_arrow():
            """Mũi tên hai chiều luôn nối hai tâm cụm."""
            s, e = mu_b_dot.get_center(), mu_r_dot.get_center()
            if np.linalg.norm(e - s) < 0.15:
                return VMobject()
            try:
                return DoubleArrow(
                    s, e,
                    color=self.SB_C, buff=0.13, stroke_width=2.2,
                    tip_length=0.13, max_tip_length_to_length_ratio=0.15,
                )
            except Exception:
                return VMobject()

        sb_arrow = always_redraw(get_sb_arrow)
        self.add(sb_arrow)

        self.play(
            GrowFromCenter(mu_b_dot), GrowFromCenter(mu_r_dot),
            Write(mu_b_tex), Write(mu_r_tex),
            run_time=1.0,
        )

        # 3d: tâm cụm xa ra → mũi tên dài ra
        SPREAD = 0.58
        self.play(
            mu_b_dot.animate.shift(LEFT  * SPREAD),
            mu_r_dot.animate.shift(RIGHT * SPREAD),
            mu_b_tex.animate.shift(LEFT  * SPREAD),
            mu_r_tex.animate.shift(RIGHT * SPREAD),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(2.5)

        # Xoá visual Sb, mở đường cho Sw
        sb_arrow.clear_updaters()
        self.play(
            FadeOut(VGroup(mu_b_dot, mu_r_dot, mu_b_tex, mu_r_tex,
                           sb_arrow, sb_rect)),
            run_time=0.5,
        )

        # ── Phase 4 (0:14–0:25): giải thích Sw ───────────────────────────────
        # 4a: khoanh vùng Sw trong công thức
        sw_rect = SurroundingRectangle(J_eq[6], color=self.SW_C,
                                       buff=0.07, corner_radius=0.05, stroke_width=1.8)
        self.play(Create(sw_rect), run_time=0.45)

        # 4b: hiện Sw formula + note
        self.play(
            LaggedStart(
                Write(Sw_title),
                Write(Sw_formula),
                FadeIn(Sw_note, shift=UP * 0.06),
                lag_ratio=0.4,
            ),
            run_time=1.4,
        )

        # 4c: tất cả chấm ép sát vào tâm cụm mình
        COMPRESS = 0.25   

        comp_b = VGroup(*[
            Dot(
                MU_B_SCR + COMPRESS * (np.array(axes_sm.c2p(*p)) - MU_B_SCR),
                color=self.BLUE_C, radius=0.08,
            )
            for p in bp
        ])
        comp_r = VGroup(*[
            Dot(
                MU_R_SCR + COMPRESS * (np.array(axes_sm.c2p(*p)) - MU_R_SCR),
                color=self.RED_C, radius=0.08,
            )
            for p in rp
        ])

        # Center markers hiện để thấy điểm hội tụ
        mu_b_center = Dot(MU_B_SCR, color=self.BLUE_C, radius=0.12, fill_opacity=0.9)
        mu_r_center = Dot(MU_R_SCR, color=self.RED_C,  radius=0.12, fill_opacity=0.9)

        self.play(
            GrowFromCenter(mu_b_center),
            GrowFromCenter(mu_r_center),
            run_time=0.4,
        )
        self.play(
            Transform(bdots, comp_b),
            Transform(rdots, comp_r),
            run_time=2.5, rate_func=smooth,
        )
        self.wait(2.5)

        # 4d: khôi phục chấm gốc
        orig_b = VGroup(*[Dot(axes_sm.c2p(*p), color=self.BLUE_C, radius=0.08) for p in bp])
        orig_r = VGroup(*[Dot(axes_sm.c2p(*p), color=self.RED_C,  radius=0.08) for p in rp])
        self.play(
            Transform(bdots, orig_b),
            Transform(rdots, orig_r),
            FadeOut(VGroup(mu_b_center, mu_r_center, sw_rect)),
            run_time=1.0,
        )

        # ── Phase 5 (0:25–0:30): nghiệm w* + kết luận ────────────────────────
        self.play(Write(w_star), run_time=1.0)
        self.play(FadeIn(w_note, shift=UP * 0.08), run_time=0.5)
        self.wait(5.0)

        # Fade out tất cả
        self.play(
            FadeOut(VGroup(
                axes_sm, bdots, rdots, fld_sm, plot_tag,
                panel_title, J_eq,
                Sb_block, Sw_block,
                w_star, w_note,
            )),
            run_time=1.0,
        )