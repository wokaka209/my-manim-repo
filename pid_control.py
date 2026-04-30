from manim import *
from manim import rate_functions
import numpy as np

config.media_width = "100%"

# ============================================================
# 颜色 & 字体
# ============================================================
COLORS = {
    "bg": "#0d1117",
    "surface": "#161b22",
    "border": "#30363d",
    "p_coral": "#FF6B6B",
    "i_teal": "#4ECDC4",
    "d_amber": "#FFD93D",
    "setpoint_blue": "#58A6FF",
    "output_green": "#3FB950",
    "error_red": "#F85149",
    "disturbance_orange": "#F05032",
    "text_primary": "#E6EDF3",
    "text_secondary": "#8B949E",
    "glow_white": "#FFFFFF",
    "arrow_gray": "#6E7681",
    "warning_yellow": "#D29922",
}

FONT_CN = "SimSun"
FONT_EN = "Times New Roman"
FONT_MONO = "Monaco"

# ============================================================
# 工具函数
# ============================================================


def cn(text, size=36, color=None, weight=NORMAL, **kw):
    """中文文字，默认 36 号（科普大字）"""
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_CN, weight=weight, **kw)


def en(text, size=36, color=None, weight=NORMAL, **kw):
    """英文文字"""
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_EN, weight=weight, **kw)


def glass_card(w, h, r=0.18):
    """毛玻璃卡片"""
    return RoundedRectangle(
        width=w,
        height=h,
        corner_radius=r,
        fill_opacity=0.88,
        fill_color=COLORS["surface"],
        stroke_width=1.5,
        stroke_color=COLORS["border"],
    )


def h_line(axes, y_val, color, width_frac=1.0):
    """坐标系水平参考线"""
    y = axes.y_axis.number_to_point(y_val)[1]
    x0 = axes.x_axis.number_to_point(axes.x_range[0])[0]
    x1 = axes.x_axis.number_to_point(axes.x_range[1])[0]
    if width_frac < 1:
        x1 = x0 + (x1 - x0) * width_frac
    return Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2.5)


def make_axes(
    x_len=8,
    y_len=4,
    x_range=[0, 10, 2],
    y_range=[0, 1.4, 0.2],
    pos=DOWN * 0.5 + RIGHT * 0.3,
):
    """快速创建深色风格坐标轴"""
    return Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_len,
        y_length=y_len,
        axis_config={
            "color": COLORS["text_secondary"],
            "include_numbers": True,
            "font_size": 22,
        },
        tips=False,
    ).move_to(pos)


# ============================================================
# 主场景
# ============================================================
class PIDControlVideo(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.scene_intro()
        # 已删除: self.scene_analogy()  # 场景2：温控类比
        self.scene_block_diagram()
        self.scene_p_control()
        self.scene_i_control()
        self.scene_d_control()
        self.scene_pid_combined()
        self.scene_summary()

    # ----------------------------------------------------------
    # S1: 开场标题
    # ----------------------------------------------------------
    def scene_intro(self):
        # 大标题 —— 缩放弹入
        title = cn("PID 控制算法", size=60, weight=BOLD)
        title.move_to(UP * 1.8)
        title.scale(0.3).set_opacity(0)
        self.play(
            title.animate.scale(1 / 0.3).set_opacity(1),
            run_time=1.4,
            rate_func=rate_functions.ease_out_elastic,
        )

        # P I D 三字母 —— 依次发光进场
        letters_data = [
            ("P", COLORS["p_coral"], LEFT * 1.6),
            ("I", COLORS["i_teal"], ORIGIN),
            ("D", COLORS["d_amber"], RIGHT * 1.6),
        ]
        letter_mobs = []
        for ch, color, shift in letters_data:
            letter = en(ch, size=80, color=color, weight=BOLD)
            letter.move_to(DOWN * 0.6 + shift)
            letter.set_opacity(0).shift(UP * 0.6)
            glow = Dot(radius=0.6, color=color, fill_opacity=0)
            glow.move_to(letter.get_center() + DOWN * 0.6)
            self.play(
                letter.animate.set_opacity(1).shift(DOWN * 0.6),
                glow.animate.set_opacity(0.25),
                run_time=0.7,
                rate_func=rate_functions.ease_out_back,
            )
            self.play(
                glow.animate.scale(1.4).set_opacity(0).shift(DOWN * 0.6), run_time=0.4
            )
            letter_mobs.append(letter)

        # 公式 —— 从下方滑入
        formula = MathTex(
            r"u(t) = K_p{\cdot}e(t) + K_i\!\int\!e(t)\,dt + K_d\frac{de(t)}{dt}",
            font_size=34,
            color=COLORS["text_secondary"],
        )
        formula.move_to(DOWN * 2.5)
        formula.set_opacity(0).shift(DOWN * 0.5)
        self.play(
            formula.animate.set_opacity(1).shift(UP * 0.5),
            run_time=1.2,
        )

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S2: PID 系统框图（横向布局，更大更清晰）
    # ----------------------------------------------------------
    def scene_block_diagram(self):
        title = cn("PID 控制系统框图", size=44, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_opacity(0).shift(DOWN * 0.5)
        self.play(title.animate.set_opacity(1).shift(UP * 0.5), run_time=0.8)

        center_y = DOWN * 0.3  # 整体上移，为反馈回路留空间

        # ── 比较器 ──
        comp = Circle(
            radius=0.35,
            stroke_color=COLORS["setpoint_blue"],
            stroke_width=2.5,
            fill_opacity=0,
        )
        comp_lbl = en("±", size=30, color=COLORS["setpoint_blue"], weight=BOLD)
        comp_g = VGroup(comp, comp_lbl).move_to(LEFT * 5.2 + center_y)

        # ── P / I / D 三个块 ──
        blk = dict(
            width=1.9,
            height=0.95,
            corner_radius=0.14,
            fill_opacity=0.88,
            fill_color=COLORS["surface"],
            stroke_width=2,
        )

        p_blk = RoundedRectangle(color=COLORS["p_coral"], **blk)
        p_lbl = en("Kp", size=30, color=COLORS["p_coral"])
        p_lbl.move_to(p_blk.get_center())
        p_g = VGroup(p_blk, p_lbl)

        i_blk = RoundedRectangle(color=COLORS["i_teal"], **blk)
        i_lbl = en("Ki·∫", size=28, color=COLORS["i_teal"])
        i_lbl.move_to(i_blk.get_center())
        i_g = VGroup(i_blk, i_lbl)

        d_blk = RoundedRectangle(color=COLORS["d_amber"], **blk)
        d_lbl = en("Kd·d/dt", size=26, color=COLORS["d_amber"])
        d_lbl.move_to(d_blk.get_center())
        d_g = VGroup(d_blk, d_lbl)

        pid_blocks = VGroup(p_g, i_g, d_g).arrange(DOWN, buff=0.4)
        pid_blocks.move_to(LEFT * 2.8 + center_y)

        # ── 求和点 ──
        sum_c = Circle(
            radius=0.3, stroke_color=COLORS["text_primary"], stroke_width=2.5
        )
        sum_l = en("Σ", size=28)
        sum_g = VGroup(sum_c, sum_l).move_to(LEFT * 0.3 + center_y)

        # ── 被控对象 ──
        plant = RoundedRectangle(
            width=2.4,
            height=1.3,
            corner_radius=0.14,
            fill_opacity=0.88,
            fill_color=COLORS["surface"],
            stroke_color=COLORS["output_green"],
            stroke_width=2,
        )
        plant_lbl = cn("被控对象", size=30, color=COLORS["output_green"])
        plant_lbl.move_to(plant.get_center())
        plant_g = VGroup(plant, plant_lbl).move_to(RIGHT * 2.5 + center_y)

        # ── 输出点 ──
        out_dot = Dot(radius=0.08, color=COLORS["output_green"]).move_to(
            RIGHT * 4.5 + center_y
        )

        # ── 进场：从左到右，逐模块显现 ──
        for g in [comp_g, pid_blocks, sum_g, plant_g, out_dot]:
            g.set_opacity(0)
        self.play(comp_g.animate.set_opacity(1), run_time=0.5)

        # P/I/D 三个块逐个进场，有教学节奏感
        for block in [p_g, i_g, d_g]:
            block.set_opacity(0)
            self.play(block.animate.set_opacity(1), run_time=0.35)

        self.play(
            sum_g.animate.set_opacity(1), plant_g.animate.set_opacity(1), run_time=0.5
        )
        self.play(out_dot.animate.set_opacity(1), run_time=0.3)

        # ── 连接箭头 & 标签 ──
        arrow_cfg = dict(
            stroke_width=2.5, buff=0.08, max_tip_length_to_length_ratio=0.15
        )

        # 设定值 r(t) — 从上方输入比较器
        r_lbl = cn("r(t) 设定值", size=16, color=COLORS["setpoint_blue"])
        r_lbl.next_to(comp_g, LEFT * 0.5, buff=0.15)
        arr_r = Arrow(
            r_lbl.get_bottom() + DOWN * 0.1,
            comp_g.get_left() + DOWN * 0.2,
            color=COLORS["setpoint_blue"],
            **arrow_cfg,
        )

        # 比较器 → PID：误差 e(t)
        arr_e = Arrow(
            comp_g.get_right(),
            pid_blocks.get_left(),
            color=COLORS["arrow_gray"],
            **arrow_cfg,
        )
        e_lbl = cn("e(t) 误差", size=16, color=COLORS["error_red"])
        e_lbl.next_to(arr_e, DOWN * 0.1, buff=0.12)

        # PID → 求和
        arr_pid_sum = Arrow(
            pid_blocks.get_right(),
            sum_c.get_left(),
            color=COLORS["arrow_gray"],
            **arrow_cfg,
        )

        # 求和 → 被控对象：控制量 u(t)
        arr_sum_plant = Arrow(
            sum_c.get_right(), plant.get_left(), color=COLORS["arrow_gray"], **arrow_cfg
        )
        u_lbl = cn("u(t) 控制量", size=16, color=COLORS["text_primary"])
        u_lbl.next_to(arr_sum_plant, DOWN * 0.1, buff=0.12)

        # 被控对象 → 输出
        arr_out = Arrow(
            plant.get_right(),
            out_dot.get_left(),
            color=COLORS["output_green"],
            **arrow_cfg,
        )
        y_lbl = cn("y(t) 输出", size=24, color=COLORS["output_green"])
        y_lbl.next_to(out_dot, RIGHT, buff=0.15)

        # 沿信号流方向依次显示箭头和标签
        for mob in [
            arr_r,
            r_lbl,
            arr_e,
            e_lbl,
            arr_pid_sum,
            arr_sum_plant,
            u_lbl,
            arr_out,
            y_lbl,
        ]:
            mob.set_opacity(0)
        self.play(
            arr_r.animate.set_opacity(1), r_lbl.animate.set_opacity(1), run_time=0.4
        )
        self.play(
            arr_e.animate.set_opacity(1), e_lbl.animate.set_opacity(1), run_time=0.4
        )
        self.play(arr_pid_sum.animate.set_opacity(1), run_time=0.3)
        self.play(
            arr_sum_plant.animate.set_opacity(1),
            u_lbl.animate.set_opacity(1),
            run_time=0.4,
        )
        self.play(
            arr_out.animate.set_opacity(1), y_lbl.animate.set_opacity(1), run_time=0.4
        )

        # ── 反馈回路（沿路径动画绘制）──
        fb_y = out_dot.get_bottom()[1] - 2.2
        fb_lines = VGroup(
            Line(
                out_dot.get_bottom(),
                [out_dot.get_center()[0], fb_y, 0],
                color=COLORS["error_red"],
                stroke_width=2.5,
            ),
            Line(
                [out_dot.get_center()[0], fb_y, 0],
                [comp_g.get_center()[0], fb_y, 0],
                color=COLORS["error_red"],
                stroke_width=2.5,
            ),
            Line(
                [comp_g.get_center()[0], fb_y, 0],
                comp_g.get_bottom(),
                color=COLORS["error_red"],
                stroke_width=2.5,
            ),
        )
        fb_arrow = Arrow(
            fb_lines[2].get_start(),
            fb_lines[2].get_end(),
            color=COLORS["error_red"],
            buff=0.06,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )
        fb_lbl = cn("反馈回路", size=24, color=COLORS["error_red"])
        fb_lbl.move_to(
            [(out_dot.get_center()[0] + comp_g.get_center()[0]) / 2, fb_y - 0.5, 0]
        )

        # 沿路径逐段绘制，模拟信号流动
        self.play(Create(fb_lines[0]), run_time=0.35)
        self.play(Create(fb_lines[1]), FadeIn(fb_lbl), run_time=0.5)
        self.play(Create(fb_lines[2]), FadeIn(fb_arrow), run_time=0.35)

        # ── 信号流走向总结标注 ──
        flow_hint = cn(
            "信号流：设定值 → 误差 → PID运算 → 控制量 → 输出 → 反馈",
            size=22,
            color=COLORS["text_secondary"],
        )
        flow_hint.to_edge(DOWN, buff=0.25)
        flow_hint.set_opacity(0)
        self.play(flow_hint.animate.set_opacity(1), run_time=0.6)

        self.wait(1.5)
        self._clear()

    # ----------------------------------------------------------
    # S3: P 控制
    # ----------------------------------------------------------
    def scene_p_control(self):
        # 标题 + 公式
        title = cn("比例控制 P", size=44, weight=BOLD, color=COLORS["p_coral"])
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0).shift(LEFT * 3)
        self.play(title.animate.set_opacity(1).shift(RIGHT * 3), run_time=1.0)

        formula = MathTex(
            r"u(t) = K_p \cdot e(t)", font_size=40, color=COLORS["p_coral"]
        )
        formula.next_to(title, DOWN, buff=0.3)
        formula.set_opacity(0).shift(DOWN * 0.4)
        self.play(formula.animate.set_opacity(1).shift(UP * 0.4), run_time=0.8)

        # 直觉说明
        intuition = cn("误差越大 → 输出越强", size=30, color=COLORS["p_coral"])
        intuition.next_to(formula, DOWN, buff=0.25)
        intuition.set_opacity(0)
        self.play(FadeIn(intuition), run_time=0.6)

        # 坐标系 — 左移为右侧标签留空间
        axes = make_axes(x_len=7, y_len=3.5, pos=DOWN * 0.5 + LEFT * 0.3)
        sp = h_line(axes, 1.0, COLORS["setpoint_blue"])
        sp_lbl = cn("设定值", size=24, color=COLORS["setpoint_blue"])
        sp_lbl.next_to(sp, RIGHT, buff=0.15)

        self.play(FadeIn(axes), FadeIn(sp), FadeIn(sp_lbl), run_time=0.6)

        # 三条 P 曲线 — 标签放在曲线末端右侧，垂直错开
        curves_cfg = [
            (0.5, "Kp=0.5", 0.45, UP * 0.1),
            (1.0, "Kp=1.0", 0.72, ORIGIN),
            (2.5, "Kp=2.5", 1.0, DOWN * 0.1),
        ]
        for kp, lbl_txt, opacity, y_shift in curves_cfg:

            def p_resp(x, k=kp):
                if x <= 0:
                    return 0
                ss = k / (1 + k)
                if k < 1.8:
                    return ss * (1 - np.exp(-k * x * 0.55))
                else:
                    return ss * (1 - np.exp(-x * 0.9)) + 0.10 * np.sin(
                        x * 2.8
                    ) * np.exp(-x * 0.35)

            curve = axes.plot(p_resp, x_range=[0, 10], color=COLORS["p_coral"])
            curve.set_stroke(width=3.0, opacity=opacity)
            # 标签放在曲线 x=8 处对应点的右侧
            lbl_x = 8.5
            lbl_y = p_resp(lbl_x)
            lbl = en(lbl_txt, size=24, color=COLORS["p_coral"])
            lbl.set_opacity(opacity)
            lbl.move_to(axes.c2p(lbl_x, lbl_y) + RIGHT * 0.8 + y_shift)
            self.play(
                Create(curve, run_time=1.8),
                FadeIn(lbl, shift=RIGHT * 0.15),
                run_time=1.8,
            )

        # 注释 — 放在坐标轴下方，避免与曲线区域重叠
        notes = VGroup(
            cn("✓ 响应快", size=26, color=COLORS["output_green"]),
            cn("✗ 有稳态误差", size=26, color=COLORS["error_red"]),
            cn("✗ Kp 过大 → 振荡", size=26, color=COLORS["error_red"]),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        notes.next_to(axes, DOWN, buff=0.35)
        notes.set_opacity(0)
        self.play(notes.animate.set_opacity(1), run_time=0.8)

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S4: I 控制
    # ----------------------------------------------------------
    def scene_i_control(self):
        title = cn("积分控制 I", size=44, weight=BOLD, color=COLORS["i_teal"])
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0).shift(DOWN * 0.5)
        self.play(title.animate.set_opacity(1).shift(UP * 0.5), run_time=0.8)

        formula = MathTex(
            r"u_I(t) = K_i \!\int_0^t e(\tau)\,d\tau",
            font_size=40,
            color=COLORS["i_teal"],
        )
        formula.next_to(title, DOWN, buff=0.3)
        formula.set_opacity(0)
        self.play(formula.animate.set_opacity(1), run_time=0.8)

        intuition = cn("误差累积 → 持续补偿", size=30, color=COLORS["i_teal"])
        intuition.next_to(formula, DOWN, buff=0.25)
        intuition.set_opacity(0)
        self.play(FadeIn(intuition), run_time=0.6)

        axes = make_axes(x_len=7, y_len=3.5, pos=DOWN * 0.5 + LEFT * 0.3)
        sp = h_line(axes, 1.0, COLORS["setpoint_blue"])
        sp_lbl = cn("设定值", size=24, color=COLORS["setpoint_blue"])
        sp_lbl.next_to(sp, RIGHT, buff=0.15)
        self.play(FadeIn(axes), FadeIn(sp), FadeIn(sp_lbl), run_time=0.5)

        # 仅 P — 有稳态误差，标签放在曲线末端右侧
        def p_only(x):
            if x <= 0:
                return 0
            return 0.73 * (1 - np.exp(-x * 0.75))

        p_curve = axes.plot(
            p_only, x_range=[0, 10], color=COLORS["p_coral"], stroke_width=3
        )
        p_lbl = cn("仅 P 控制", size=24, color=COLORS["p_coral"])
        p_lbl.move_to(axes.c2p(8.5, p_only(8.5)) + RIGHT * 1.0 + UP * 0.15)
        self.play(Create(p_curve), FadeIn(p_lbl), run_time=2.0)

        # 累积误差标注 — 用填充区域可视化，放在曲线上方
        err_lbl = cn(
            "← 稳态误差（始终到不了设定值）", size=24, color=COLORS["error_red"]
        )
        err_lbl.move_to(axes.get_center() + RIGHT * 2)
        err_lbl.set_opacity(0)
        self.play(FadeIn(err_lbl), run_time=0.6)
        self.play(err_lbl.animate.set_opacity(0.3), run_time=0.25)
        self.play(err_lbl.animate.set_opacity(1), run_time=0.25)

        # PI — 消除稳态误差
        def pi_resp(x):
            if x <= 0:
                return 0
            return 1.0 * (1 - 1.15 * np.exp(-x * 0.42) * np.cos(x * 0.75))

        pi_curve = axes.plot(
            pi_resp, x_range=[0, 10], color=COLORS["i_teal"], stroke_width=3
        )
        pi_lbl = cn("PI 控制", size=24, color=COLORS["i_teal"])
        pi_lbl.move_to(axes.c2p(8.5, pi_resp(8.5)) + RIGHT * 0.8 + DOWN * 0.15)
        self.play(Create(pi_curve), FadeIn(pi_lbl), run_time=2.2)

        # 注释 — 放在坐标轴下方
        notes = VGroup(
            cn("✓ 消除稳态误差", size=26, color=COLORS["output_green"]),
            cn("✗ 可能超调", size=26, color=COLORS["error_red"]),
            cn("✗ 响应较慢", size=26, color=COLORS["warning_yellow"]),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        notes.next_to(axes, DOWN, buff=0.35)
        notes.set_opacity(0)
        self.play(notes.animate.set_opacity(1), run_time=0.8)

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S5: D 控制
    # ----------------------------------------------------------
    def scene_d_control(self):
        title = cn("微分控制 D", size=44, weight=BOLD, color=COLORS["d_amber"])
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0).shift(RIGHT * 3)
        self.play(title.animate.set_opacity(1).shift(LEFT * 3), run_time=0.8)

        formula = MathTex(
            r"u_D(t) = K_d \frac{de(t)}{dt}",
            font_size=40,
            color=COLORS["d_amber"],
        )
        formula.next_to(title, DOWN, buff=0.3)
        formula.set_opacity(0)
        self.play(formula.animate.set_opacity(1), run_time=0.8)

        intuition = cn("变化趋势 → 提前制动", size=30, color=COLORS["d_amber"])
        intuition.next_to(formula, DOWN, buff=0.25)
        intuition.set_opacity(0)
        self.play(FadeIn(intuition), run_time=0.6)

        # 坐标系 — 留出上方和右侧空间给标注
        axes = make_axes(
            x_len=7, y_len=3.5, y_range=[0, 1.5, 0.2], pos=DOWN * 0.5 + LEFT * 0.3
        )
        sp = h_line(axes, 1.0, COLORS["setpoint_blue"])
        sp_lbl = cn("设定值", size=24, color=COLORS["setpoint_blue"])
        sp_lbl.next_to(sp, RIGHT, buff=0.15)
        self.play(FadeIn(axes), FadeIn(sp), FadeIn(sp_lbl), run_time=0.5)

        # 无 D — 大超调
        def no_d(x):
            if x <= 0:
                return 0
            return 1.0 * (1 - 1.45 * np.exp(-x * 0.58) * np.cos(x * 1.15))

        c_no_d = axes.plot(
            no_d, x_range=[0, 10], color=COLORS["error_red"], stroke_width=3
        )
        l_no_d = cn("无D：大超调", size=24, color=COLORS["error_red"])
        l_no_d.move_to(axes.c2p(8.5, no_d(8.5)) + RIGHT * 0.3 + UP * 0.2)
        self.play(Create(c_no_d), FadeIn(l_no_d), run_time=2.2)

        # 超调量标注 — 垂直虚线从峰值到设定值
        peak_x = 1.8
        peak_val = no_d(peak_x)
        peak_point = axes.c2p(peak_x, peak_val)
        setpoint_point = axes.c2p(peak_x, 1.0)
        overshoot_bracket = DashedLine(
            peak_point,
            setpoint_point,
            color=COLORS["warning_yellow"],
            stroke_width=2.5,
        )
        overshoot_lbl = cn("超调量", size=22, color=COLORS["warning_yellow"])
        overshoot_lbl.next_to(overshoot_bracket, LEFT, buff=0.15)
        self.play(Create(overshoot_bracket), FadeIn(overshoot_lbl), run_time=0.6)

        # 有 D — 平滑趋近
        def with_d(x):
            if x <= 0:
                return 0
            return 1.0 * (
                1
                - np.exp(-x * 0.78)
                * (1.04 * np.cos(x * 0.48) + 0.09 * np.sin(x * 0.48))
            )

        c_with_d = axes.plot(
            with_d, x_range=[0, 10], color=COLORS["d_amber"], stroke_width=3
        )
        l_with_d = cn("有D：平滑趋近", size=24, color=COLORS["d_amber"])
        l_with_d.move_to(axes.c2p(8.5, with_d(8.5)) + RIGHT * 0.3 + DOWN * 0.15)
        self.play(Create(c_with_d), FadeIn(l_with_d), run_time=2.2)

        # 切线标注 — 在有D曲线上升段画切线，说明"D感知斜率"
        dx = 0.05
        tx = 0.8
        slope = (with_d(tx + dx) - with_d(tx - dx)) / (2 * dx)
        pt = axes.c2p(tx, with_d(tx))
        # 用场景坐标直接计算切线端点（y方向按像素比例缩放）
        y_scale = axes.y_length / (axes.y_range[1] - axes.y_range[0])
        x_scale = axes.x_length / (axes.x_range[1] - axes.x_range[0])
        tan_half = 0.8  # 半长（场景单位）
        tan_dx = tan_half / np.sqrt(1 + (slope * y_scale / x_scale) ** 2)
        tan_dy = slope * tan_dx * y_scale / x_scale
        tan_start = pt + LEFT * tan_dx + DOWN * tan_dy
        tan_end = pt + RIGHT * tan_dx + UP * tan_dy
        tangent = Line(tan_start, tan_end, color=COLORS["d_amber"], stroke_width=2.5)
        tg_lbl = cn("斜率=变化趋势", size=22, color=COLORS["d_amber"])
        tg_lbl.next_to(tangent.get_top(), UP + RIGHT * 0.5, buff=0.12)
        self.play(Create(tangent), FadeIn(tg_lbl), run_time=0.8)

        # 注释 — 坐标轴下方
        notes = VGroup(
            cn("✓ 抑制超调", size=26, color=COLORS["output_green"]),
            cn("✗ 对噪声敏感", size=26, color=COLORS["error_red"]),
            cn("✗ 不能单独使用", size=26, color=COLORS["warning_yellow"]),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        notes.next_to(axes, DOWN, buff=0.35)
        notes.set_opacity(0)
        self.play(notes.animate.set_opacity(1), run_time=0.8)

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S6: PID 联合 + 参数整定
    # ----------------------------------------------------------
    def scene_pid_combined(self):
        title = cn("PID 三力合一", size=44, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0).shift(UP * 0.5)
        self.play(title.animate.set_opacity(1).shift(DOWN * 0.5), run_time=0.8)

        # 大坐标系 — 稍微上移，为底部总结留空间
        axes = make_axes(x_len=9, y_len=4.0, pos=UP * 0.1)
        sp = h_line(axes, 1.0, COLORS["setpoint_blue"])
        sp_lbl = cn("设定值", size=24, color=COLORS["setpoint_blue"])
        sp_lbl.next_to(sp, RIGHT, buff=0.15)
        self.play(FadeIn(axes), FadeIn(sp), FadeIn(sp_lbl), run_time=0.6)

        # 三条曲线：P → PI → PID 逐步叠加
        def p_curve(x):
            if x <= 0:
                return 0
            return 0.73 * (1 - np.exp(-x * 0.75))

        def pi_curve(x):
            if x <= 0:
                return 0
            return 1.0 * (1 - 1.15 * np.exp(-x * 0.42) * np.cos(x * 0.75))

        def pid_curve(x):
            if x <= 0:
                return 0
            return 1.0 * (1 - np.exp(-x * 1.15) * np.cos(x * 0.28))

        # P — 标签放在曲线末端右侧
        c1 = axes.plot(
            p_curve, x_range=[0, 10], color=COLORS["p_coral"], stroke_width=3
        )
        l1 = cn("仅 P", size=24, color=COLORS["p_coral"])
        l1.move_to(axes.c2p(8.5, p_curve(8.5)) + RIGHT * 0.8 + UP * 0.1)
        self.play(Create(c1), FadeIn(l1), run_time=2.0)

        # PI
        c2 = axes.plot(
            pi_curve, x_range=[0, 10], color=COLORS["i_teal"], stroke_width=3
        )
        l2 = cn("PI", size=24, color=COLORS["i_teal"])
        l2.move_to(axes.c2p(8.5, pi_curve(8.5)) + RIGHT * 0.6 + UP * 0.1)
        self.play(Create(c2), FadeIn(l2), run_time=2.0)

        # PID — 粗线突出
        c3 = axes.plot(
            pid_curve, x_range=[0, 10], color=COLORS["output_green"], stroke_width=4
        )
        l3 = cn("PID ✓", size=26, color=COLORS["output_green"], weight=BOLD)
        l3.move_to(axes.c2p(8.5, pid_curve(8.5)) + RIGHT * 0.5 + UP * 0.2)
        self.play(Create(c3), FadeIn(l3), run_time=2.2)

        # 底部总结条 — 放在坐标轴下方，不与曲线重叠
        summary_bar = glass_card(10, 1.0)
        summary_bar.next_to(axes, DOWN, buff=0.5)
        summary_txt = cn(
            "P 快速响应  +  I 消除误差  +  D 抑制超调  =  最佳控制",
            size=28,
            color=COLORS["text_primary"],
            weight=BOLD,
        )
        summary_txt.move_to(summary_bar.get_center())
        self.play(FadeIn(summary_bar), FadeIn(summary_txt), run_time=0.8)

        self.wait(1.5)
        self._clear()

    # ----------------------------------------------------------
    # S7: 总结 — PID 拼图归位
    # ----------------------------------------------------------
    def scene_summary(self):
        # ── 标题 ──
        title = cn("PID 总结", size=50, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_opacity(0).shift(UP * 0.5)
        self.play(title.animate.set_opacity(1).shift(DOWN * 0.5), run_time=1.0)

        # ── 三块拼图卡片 ──
        cards_info = [
            ("P", "比例", "快速响应，但有稳态误差", COLORS["p_coral"]),
            ("I", "积分", "消除静差，但可能超调", COLORS["i_teal"]),
            ("D", "微分", "抑制超调，但对噪声敏感", COLORS["d_amber"]),
        ]

        cards = VGroup()
        for letter, name, desc, color in cards_info:
            # 大字母（亮色）+ 名称（亮色）+ 描述（白色，克制不花哨）
            big = en(letter, size=52, color=color, weight=BOLD)
            nm = cn(name, size=28, color=color, weight=BOLD)
            ds = cn(desc, size=20, color=COLORS["text_primary"])
            content = VGroup(big, nm, ds).arrange(DOWN, buff=0.15)
            cards.add(content)

        cards.arrange(RIGHT, buff=0.7).move_to(UP * 0.5)

        # P 从左侧飞入
        cards[0].shift(LEFT * 6).set_opacity(0)
        self.play(
            cards[0].animate.shift(RIGHT * 6).set_opacity(1),
            run_time=0.8,
            rate_func=rate_functions.ease_out_back,
        )
        # I 从下方弹入
        cards[1].shift(DOWN * 3).set_opacity(0)
        self.play(
            cards[1].animate.shift(UP * 3).set_opacity(1),
            run_time=0.8,
            rate_func=rate_functions.ease_out_back,
        )
        # D 从右侧飞入
        cards[2].shift(RIGHT * 6).set_opacity(0)
        self.play(
            cards[2].animate.shift(LEFT * 6).set_opacity(1),
            run_time=0.8,
            rate_func=rate_functions.ease_out_back,
        )

        # ── 连接弧线：P → I → D 视觉串联 ──
        arc1 = ArcBetweenPoints(
            cards[0].get_right() + RIGHT * 0.05,
            cards[1].get_left() + LEFT * 0.05,
            angle=-TAU / 8,
            color=COLORS["arrow_gray"],
            stroke_width=2,
        )
        arc2 = ArcBetweenPoints(
            cards[1].get_right() + RIGHT * 0.05,
            cards[2].get_left() + LEFT * 0.05,
            angle=-TAU / 8,
            color=COLORS["arrow_gray"],
            stroke_width=2,
        )
        self.play(Create(arc1), Create(arc2), run_time=0.6)

        # ── 核心公式 — 三项高亮着色 ──
        formula = MathTex(
            r"u(t)",
            r"=",
            r"K_p{\cdot}e(t)",
            r"+",
            r"K_i\!\int\!e(t)\,dt",
            r"+",
            r"K_d\frac{de(t)}{dt}",
            font_size=38,
        )
        formula[0].set_color(COLORS["text_primary"])
        formula[1].set_color(COLORS["text_secondary"])
        formula[2].set_color(COLORS["p_coral"])  # P 项
        formula[3].set_color(COLORS["text_secondary"])
        formula[4].set_color(COLORS["i_teal"])  # I 项
        formula[5].set_color(COLORS["text_secondary"])
        formula[6].set_color(COLORS["d_amber"])  # D 项
        formula.next_to(cards, DOWN, buff=0.6)
        formula.set_opacity(0).shift(DOWN * 0.3)
        self.play(formula.animate.set_opacity(1).shift(UP * 0.3), run_time=1.2)

        # ── 每项闪烁一次，与卡片颜色呼应 ──
        for idx in [2, 4, 6]:
            self.play(
                formula[idx].animate.scale(1.15),
                run_time=0.2,
                rate_func=rate_functions.ease_out_quad,
            )
            self.play(
                formula[idx].animate.scale(1 / 1.15),
                run_time=0.2,
            )

        # ── 一句话总结 ──
        takeaway = cn(
            "P 快速响应  +  I 消除静差  +  D 抑制超调  =  稳准快",
            size=26,
            color=COLORS["text_primary"],
            weight=BOLD,
        )
        takeaway.next_to(formula, DOWN, buff=0.5)
        takeaway.set_opacity(0)
        self.play(takeaway.animate.set_opacity(1), run_time=0.8)

        # ── 分隔线 + 结束语 ──
        deco = Line(LEFT * 2.5, RIGHT * 2.5, color=COLORS["border"], stroke_width=1.5)
        deco.next_to(takeaway, DOWN, buff=0.4)
        thanks = cn("谢谢观看", size=40, weight=BOLD, color=COLORS["text_secondary"])
        thanks.next_to(deco, DOWN, buff=0.25)
        self.play(FadeIn(deco), FadeIn(thanks), run_time=0.8)

        self.wait(2.0)
        self._clear()

    # ----------------------------------------------------------
    # 辅助：清屏
    # ----------------------------------------------------------
    def _clear(self, run_time=0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    config.quality = "fourk_quality"
    config.preview = True
