"""
PC4 – Part 1: FLD projection
==========================================
Render:  manim pc4_1.py FLDPart1 -pqh
"""

from manim import *
import numpy as np
Text.set_default(font="Be Vietnam Pro")

class FLDPart1(Scene):

    BLUE_C = "#4FC3F7"
    RED_C  = "#EF5350"
    FLD_C  = "#FF8C42"   # orange: FLD line

    def construct(self):
        # ── Dữ liệu
        np.random.seed(2025)
        n = 15
        a = np.radians(45)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a),  np.cos(a)]])
        Cov = R @ np.diag([2.2, 0.12]) @ R.T
        L   = np.linalg.cholesky(Cov)

        bp = (L @ np.random.randn(2, n)).T + [-2.0, 0.0]   # blue cluster
        rp = (L @ np.random.randn(2, n)).T + [ 2.0, 0.0]   # red  cluster

        # FLD direction: w* = Sw^{-1}(μ₁ − μ₂)
        mu_b, mu_r = bp.mean(0), rp.mean(0)
        Sw_mat = ((bp - mu_b).T @ (bp - mu_b) +
                  (rp - mu_r).T @ (rp - mu_r))
        w = np.linalg.solve(Sw_mat, mu_r - mu_b)
        if w[0] < 0: w = -w
        w /= np.linalg.norm(w)
        fld_angle = float(np.arctan2(w[1], w[0]))   # ≈ −40.3°

        # ── Scalar projections (dùng khi tính vị trí label sau zoom) ──────────
        b_scalars = [float(np.dot(p, w)) for p in bp]
        r_scalars = [float(np.dot(p, w)) for p in rp]

        # ── Layout ─────────────────────────────────────────────────────────────
        NL_CENTER  = DOWN * 2.9    # vị trí trục 1D lúc đầu
        NL_ZOOM_TO = DOWN * 0.4   # vị trí sau zoom
        ZOOM_SCALE = 2.0

        axes = Axes(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            x_length=9, y_length=5,
            axis_config={"color": WHITE, "include_tip": True, "stroke_width": 2},
        ).shift(UP * 0.75)

        bdots = VGroup(*[Dot(axes.c2p(*p), color=self.BLUE_C, radius=0.10) for p in bp])
        rdots = VGroup(*[Dot(axes.c2p(*p), color=self.RED_C,  radius=0.10) for p in rp])

        nl = NumberLine(x_range=[-5, 5, 1], length=9,
                        color=WHITE, stroke_width=2).shift(NL_CENTER)
        ticks = VGroup(*[
            Line(UP*0.10, DOWN*0.10, color=GREY_B, stroke_width=1.5).move_to(nl.n2p(x))
            for x in range(-4, 5)
        ])
        nl_lbl = Text("giá trị chiếu", font_size=18, color=GREY_B)\
                     .next_to(nl, DOWN, buff=0.15)

        # ── ValueTracker điều khiển góc xoay ───────────────────────────────────
        ang_tr = ValueTracker(PI / 2.5)   # bắt đầu ≈ 72°

        # ── Đường thẳng xoay
        def make_line():
            a  = ang_tr.get_value()
            dv = np.array([np.cos(a), np.sin(a)])
            return Line(
                axes.c2p(-4.6*dv[0], -4.6*dv[1]),
                axes.c2p( 4.6*dv[0],  4.6*dv[1]),
                color=self.FLD_C, stroke_width=2.5,
            )
        rot_line = always_redraw(make_line)

        # ── Chấm chiếu trên trục 1D
        def make_dot1d(pt, color):
            dot = Dot(color=color, radius=0.09, fill_opacity=0.9)
            def upd(m):
                a  = ang_tr.get_value()
                dv = np.array([np.cos(a), np.sin(a)])
                s  = np.clip(float(np.dot(pt, dv)), -4.9, 4.9)
                m.move_to(nl.n2p(s))
            dot.add_updater(upd)
            return dot

        b1d = VGroup(*[make_dot1d(p, self.BLUE_C) for p in bp])
        r1d = VGroup(*[make_dot1d(p, self.RED_C)  for p in rp])

        # ── Đoạn chiếu vuông góc từ 2D → trục xoay 
        def make_seg(pt, color):
            seg = Line(axes.c2p(*pt), axes.c2p(*pt),
                       color=color, stroke_width=0.9, stroke_opacity=0.45)
            def upd(m):
                a  = ang_tr.get_value()
                dv = np.array([np.cos(a), np.sin(a)])
                pp = float(np.dot(pt, dv)) * dv
                s  = axes.c2p(*pt)
                e  = axes.c2p(*pp)
                if np.linalg.norm(np.array(e) - np.array(s)) > 0.03:
                    try:
                        m.put_start_and_end_on(s, e)
                    except Exception:
                        pass
            seg.add_updater(upd)
            return seg

        b_segs = VGroup(*[make_seg(p, self.BLUE_C) for p in bp])
        r_segs = VGroup(*[make_seg(p, self.RED_C)  for p in rp])

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 1 (0:00–0:02) — scatter plot + trục 1D
        # ══════════════════════════════════════════════════════════════════════
        title_p0 = Text("PHẦN 4: FLD - Phân tích biệt thức tuyến tính", font_size=32, color=BLUE, weight=BOLD)
        title_p0.shift(ORIGIN)
        self.play(Write(title_p0), run_time = 0.5)
        self.wait(1.5)
        self.play(FadeOut(title_p0), run_time = 0.5)
        self.play(Create(axes), run_time=0.8)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in [*bdots, *rdots]], lag_ratio=0.05),
            run_time=1.2,
        )
        self.play(Create(nl), FadeIn(ticks), Write(nl_lbl), run_time=0.7)

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 2 (0:02–0:04) — đường thẳng xuất hiện + chiếu sống
        # ══════════════════════════════════════════════════════════════════════
        self.add(rot_line)
        self.play(
            *[Create(s) for s in [*b_segs, *r_segs]],
            *[GrowFromCenter(d) for d in [*b1d,  *r1d]],
            run_time=0.9,
        )

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 3 (0:04–0:09) — xoay đến góc FLD tối ưu
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            ang_tr.animate.set_value(fld_angle),
            run_time=4.5,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 4 (0:09–0:13) — dừng + nhãn FLD
        # ══════════════════════════════════════════════════════════════════════
        # Xoá updater — tất cả vị trí đã cố định
        rot_line.clear_updaters()
        for m in [*b1d, *r1d, *b_segs, *r_segs]:
            m.clear_updaters()

        # Đường FLD sáng hơn / dày hơn
        fld_final = Line(
            axes.c2p(-4.6*w[0], -4.6*w[1]),
            axes.c2p( 4.6*w[0],  4.6*w[1]),
            color=self.FLD_C, stroke_width=4.0,
        )
        self.play(Transform(rot_line, fld_final), run_time=0.35)
        self.play(Flash(axes.c2p(0, 0), color=self.FLD_C,
                        flash_radius=0.4, num_lines=8, line_length=0.25),
                  run_time=0.4)

        fld_tag = VGroup(
            Text("FLD", font_size=26, color=self.FLD_C, weight=BOLD),
            Text("Fisher's Linear Discriminant", font_size=16, color=GREY_A),
            
        ).arrange(RIGHT, buff=0.2).next_to(axes, DOWN, buff=0.18)

        self.play(FadeIn(fld_tag, shift=UP * 0.1), run_time=0.7)
        self.wait(1.0)

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 5 (0:13–0:16) — zoom vào trục 1D
        # ══════════════════════════════════════════════════════════════════════
        # nl_group gom tất cả những gì ở vùng 1D
        nl_group = VGroup(nl, ticks, b1d, r1d)

        self.play(
            FadeOut(VGroup(axes, bdots, rdots,
                           rot_line, b_segs, r_segs,
                           fld_tag, nl_lbl)),
            nl_group.animate.scale(ZOOM_SCALE).move_to(NL_ZOOM_TO),
            run_time=1.8,
            rate_func=smooth,
        )

        # ══════════════════════════════════════════════════════════════════════
        #  Phase 6 (0:16–0:20) — hiển thị tách biệt rõ ràng
        # ══════════════════════════════════════════════════════════════════════
        # Sau khi Manim chạy xong animate, get_center() đã cập nhật đúng vị trí
        b_cx  = b1d.get_center()[0]   # tâm ngang cụm xanh
        r_cx  = r1d.get_center()[0]   # tâm ngang cụm đỏ
        nl_y  = nl_group.get_center()[1]   # vị trí y của trục sau zoom

        # Nhãn cụm
        b_lbl = Text("Người B", font_size=18, color=self.BLUE_C, weight=BOLD)\
                    .move_to([b_cx, nl_y + 0.65, 0])
        r_lbl = Text("Người A", font_size=18, color=self.RED_C,  weight=BOLD)\
                    .move_to([r_cx, nl_y + 0.65, 0])

        # Tìm khoảng trống giữa hai cụm
        b_xs    = sorted([d.get_center()[0] for d in b1d])
        r_xs    = sorted([d.get_center()[0] for d in r1d])
        gap_lo  = b_xs[-1]    # chấm xanh ngoài cùng bên phải
        gap_hi  = r_xs[0]     # chấm đỏ ngoài cùng bên trái

        # Thanh khoảng trống  màu xanh lá
        gap_cx  = (gap_lo + gap_hi) / 2
        gap_w   = gap_hi - gap_lo
        gap_bar = Rectangle(
            width=gap_w, height=0.45,
            fill_color=GREEN_B, fill_opacity=0.18,
            stroke_color=GREEN_B, stroke_width=1.8,
        ).move_to([gap_cx, nl_y, 0])
        gap_txt = Text("khoảng trống", font_size=14, color=GREEN_B)\
                      .next_to(gap_bar, DOWN, buff=0.08)

        # Tiêu đề
        title = Text("Tách biệt rõ ràng!", font_size=26, color=GREEN_B, weight=BOLD)\
                    .shift(UP * 2.4)

        self.play(
            Write(title),
            FadeIn(b_lbl, shift=DOWN * 0.1),
            FadeIn(r_lbl, shift=DOWN * 0.1),
            run_time=0.8,
        )
        self.play(
            FadeIn(gap_bar),
            Write(gap_txt),
            run_time=0.6,
        )
        self.wait(4.5)

        # Fade out nhẹ để chuyển sang Part 2
        self.play(
            FadeOut(VGroup(nl_group, title, b_lbl, r_lbl, gap_bar, gap_txt)),
            run_time=1.0,
        )