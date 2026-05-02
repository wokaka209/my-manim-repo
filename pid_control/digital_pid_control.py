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
    "sample_purple": "#BC8CFF",
    "hold_cyan": "#39D2C0",
    "code_lime": "#7EE787",
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
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_CN, weight=weight, **kw)


def en(text, size=36, color=None, weight=NORMAL, **kw):
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_EN, weight=weight, **kw)


def mono(text, size=28, color=None, **kw):
    c = color or COLORS["code_lime"]
    return Text(text, font_size=size, color=c, font=FONT_MONO, **kw)


def glass_card(w, h, r=0.18):
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
class DigitalPIDVideo(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.scene_intro()
        self.scene_sampling()
        self.scene_position_pid()
        self.scene_incremental_pid()
        self.scene_position_vs_incremental()
        self.scene_code_implementation()
        self.scene_summary()

    # ----------------------------------------------------------
    # S1: 开场标题 — 模拟→数字过渡
    # ----------------------------------------------------------
    def scene_intro(self):
        # 大标题
        title = cn("数字 PID 控制", size=60, weight=BOLD)
        title.move_to(UP * 1.8)
        title.scale(0.3).set_opacity(0)
        self.play(
            title.animate.scale(1 / 0.3).set_opacity(1),
            run_time=1.4,
            rate_func=rate_functions.ease_out_elastic,
        )

        # P I D 三字母
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
                glow.animate.scale(1.4).set_opacity(0).shift(DOWN * 0.6),
                run_time=0.4,
            )
            letter_mobs.append(letter)

        # 连续→离散过渡动画
        axes = Axes(
            x_range=[0, 4 * np.pi, np.pi],
            y_range=[-1.3, 1.3, 0.5],
            x_length=7,
            y_length=2.5,
            axis_config={"color": COLORS["text_secondary"], "font_size": 18},
            tips=False,
        ).move_to(DOWN * 2.0)

        def sine_func(x):
            return np.sin(x)

        # 连续曲线
        cont_curve = axes.plot(
            sine_func,
            x_range=[0, 4 * np.pi],
            color=COLORS["output_green"],
            stroke_width=3,
        )
        cont_lbl = cn("连续", size=22, color=COLORS["output_green"])
        cont_lbl.next_to(axes, RIGHT, buff=0.15)

        self.play(FadeIn(axes), Create(cont_curve), FadeIn(cont_lbl), run_time=1.5)

        # 离散化：零阶保持阶梯线
        num_samples = 20
        ts = 4 * np.pi / num_samples
        steps = []
        for i in range(num_samples):
            x_start = i * ts
            x_end = (i + 1) * ts
            y_val = sine_func(x_start)
            p1 = axes.c2p(x_start, y_val)
            p2 = axes.c2p(x_end, y_val)
            p3 = axes.c2p(x_end, sine_func(x_end))
            steps.append(Line(p1, p2, color=COLORS["hold_cyan"], stroke_width=2.5))
            if i < num_samples - 1:
                steps.append(
                    Line(
                        p2,
                        p3,
                        color=COLORS["hold_cyan"],
                        stroke_width=1.5,
                        stroke_opacity=0.5,
                    )
                )

        step_lines = VGroup(*steps)
        disc_lbl = cn("离散（零阶保持）", size=22, color=COLORS["hold_cyan"])
        disc_lbl.next_to(axes, LEFT, buff=0.15).shift(DOWN * 0.3)

        # 采样点
        sample_dots = VGroup()
        for i in range(num_samples + 1):
            x_val = i * ts
            y_val = sine_func(x_val)
            dot = Dot(
                axes.c2p(x_val, y_val), radius=0.06, color=COLORS["sample_purple"]
            )
            sample_dots.add(dot)

        self.play(
            cont_curve.animate.set_stroke(opacity=0.3),
            FadeIn(step_lines, run_time=2.0),
            FadeIn(sample_dots),
            FadeIn(disc_lbl),
            run_time=2.5,
        )

        # 离散公式
        formula = MathTex(
            r"u[k] = K_p e[k] + K_i T_s \textstyle\sum e[j] + K_d \frac{e[k]-e[k-1]}{T_s}",
            font_size=30,
            color=COLORS["text_secondary"],
        )
        formula.next_to(axes, DOWN, buff=0.3)
        formula.set_opacity(0).shift(DOWN * 0.3)
        self.play(formula.animate.set_opacity(1).shift(UP * 0.3), run_time=1.0)

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S2: 采样与保持（延续S1连续→离散演变风格）
    # ----------------------------------------------------------
    def scene_sampling(self):
        title = cn("从连续到离散：采样与保持", size=44, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_opacity(0).shift(DOWN * 0.5)
        self.play(title.animate.set_opacity(1).shift(UP * 0.5), run_time=0.8)

        # ── Phase 1: 坐标系 + 设定值线 ──
        axes = make_axes(
            x_len=9,
            y_len=3.5,
            x_range=[0, 8, 1],
            y_range=[0, 1.4, 0.2],
            pos=UP * 0.1 + LEFT * 0.5,
        )
        sp = h_line(axes, 1.0, COLORS["setpoint_blue"])
        sp_lbl = cn("设定值", size=22, color=COLORS["setpoint_blue"])
        sp_lbl.next_to(sp, RIGHT, buff=0.15)
        self.play(FadeIn(axes), FadeIn(sp), FadeIn(sp_lbl), run_time=0.6)

        # ── Phase 2: 连续响应曲线实时绘制（与S1风格统一） ──
        def cont_response(x):
            if x <= 0:
                return 0
            return 1.0 * (
                1 - np.exp(-x * 0.8) * (1.05 * np.cos(x * 0.5) + 0.08 * np.sin(x * 0.5))
            )

        cont_curve = axes.plot(
            cont_response, x_range=[0, 8], color=COLORS["output_green"], stroke_width=3
        )
        cont_label = cn("连续信号", size=22, color=COLORS["output_green"])
        cont_label.move_to(axes.c2p(6.5, cont_response(6.5)) + RIGHT * 1.2 + UP * 0.2)
        self.play(Create(cont_curve), FadeIn(cont_label), run_time=2.0)

        # ── Phase 3: 采样点沿曲线依次点亮（与S1正弦波采样呼应） ──
        Ts = 0.5
        num_samples = int(8 / Ts)
        sample_dots = VGroup()
        sample_vlines = VGroup()
        for i in range(num_samples + 1):
            x_val = i * Ts
            if x_val > 8:
                break
            y_val = cont_response(x_val)
            dot = Dot(
                axes.c2p(x_val, y_val), radius=0.08, color=COLORS["sample_purple"]
            )
            sample_dots.add(dot)
            vline = DashedLine(
                axes.c2p(x_val, 0),
                axes.c2p(x_val, y_val),
                color=COLORS["sample_purple"],
                stroke_width=1,
                stroke_opacity=0.4,
            )
            sample_vlines.add(vline)

        # 分3批波浪式进场，模拟信号流方向
        n = len(sample_dots)
        batch_size = (n + 2) // 3
        batches = [
            sample_dots[:batch_size],
            sample_dots[batch_size : 2 * batch_size],
            sample_dots[2 * batch_size :],
        ]
        vline_batches = [
            sample_vlines[:batch_size],
            sample_vlines[batch_size : 2 * batch_size],
            sample_vlines[2 * batch_size :],
        ]
        for dot_batch, vline_batch in zip(batches, vline_batches):
            self.play(
                LaggedStart(
                    *[FadeIn(dot, scale=1.5) for dot in dot_batch],
                    lag_ratio=0.08,
                ),
                LaggedStart(
                    *[FadeIn(vl) for vl in vline_batch],
                    lag_ratio=0.08,
                ),
                run_time=0.6,
            )

        sample_lbl = cn("采样点", size=22, color=COLORS["sample_purple"])
        sample_lbl.next_to(sample_dots[len(sample_dots) // 2], UP, buff=0.3)
        self.play(FadeIn(sample_lbl, shift=UP * 0.15), run_time=0.35)

        # ── Phase 4: 连续曲线→阶梯线演变动画（与S1正弦→锯齿演变呼应） ──
        # 构建零阶保持阶梯线
        zoh_lines = VGroup()
        for i in range(num_samples):
            x_start = i * Ts
            x_end = (i + 1) * Ts
            if x_end > 8:
                x_end = 8
            y_val = cont_response(x_start)
            p1 = axes.c2p(x_start, y_val)
            p2 = axes.c2p(x_end, y_val)
            zoh_lines.add(Line(p1, p2, color=COLORS["hold_cyan"], stroke_width=2.5))

        # 同时构建竖向连接线（阶梯的"跳变"边）
        zoh_vlines = VGroup()
        for i in range(num_samples - 1):
            x_end = (i + 1) * Ts
            if x_end > 8:
                break
            y_bottom = cont_response(i * Ts)
            y_top = cont_response(x_end)
            p1 = axes.c2p(x_end, y_bottom)
            p2 = axes.c2p(x_end, y_top)
            zoh_vlines.add(
                Line(
                    p1,
                    p2,
                    color=COLORS["hold_cyan"],
                    stroke_width=1.5,
                    stroke_opacity=0.5,
                )
            )

        # 演变动画：连续曲线淡出 + 阶梯线逐段从左到右绘制
        # 先将连续曲线变淡
        self.play(cont_curve.animate.set_stroke(opacity=0.25), run_time=0.3)

        # 阶梯线分3段逐段绘制（信号流方向），同时逐段出现竖向跳变线
        seg_size = (len(zoh_lines) + 2) // 3
        vseg_size = (len(zoh_vlines) + 2) // 3
        segs = [
            zoh_lines[:seg_size],
            zoh_lines[seg_size : 2 * seg_size],
            zoh_lines[2 * seg_size :],
        ]
        vsegs = [
            zoh_vlines[:vseg_size],
            zoh_vlines[vseg_size : 2 * vseg_size],
            zoh_vlines[2 * vseg_size :],
        ]
        for hseg, vseg in zip(segs, vsegs):
            self.play(
                LaggedStart(*[Create(line) for line in hseg], lag_ratio=0.06),
                LaggedStart(*[FadeIn(line) for line in vseg], lag_ratio=0.06),
                run_time=0.7,
            )

        # 更新标签：连续→离散
        cont_label_new = cn("离散信号（零阶保持）", size=22, color=COLORS["hold_cyan"])
        cont_label_new.move_to(cont_label.get_center())
        self.play(
            FadeOut(cont_label, shift=UP * 0.15),
            FadeIn(cont_label_new, shift=DOWN * 0.15),
            run_time=0.5,
        )

        # ── Phase 5: 采样周期标注 ──
        idx = 4
        x1 = idx * Ts
        x2 = (idx + 1) * Ts
        y_pos = -0.15
        ts_arrow = DoubleArrow(
            axes.c2p(x1, y_pos),
            axes.c2p(x2, y_pos),
            color=COLORS["sample_purple"],
            stroke_width=2.5,
            buff=0.02,
        )
        ts_lbl = MathTex(r"T_s", font_size=28, color=COLORS["sample_purple"])
        ts_lbl.next_to(ts_arrow, DOWN, buff=0.12)
        self.play(
            GrowFromCenter(ts_arrow),
            FadeIn(ts_lbl, shift=DOWN * 0.1),
            run_time=0.6,
        )

        # ── Phase 6: 提示 — 呼应S1的连续→离散主题 ──
        hint = cn(
            "采样频率越高 → 阶梯越接近原曲线", size=24, color=COLORS["text_secondary"]
        )
        hint.next_to(axes, DOWN, buff=0.6)
        hint.set_opacity(0)
        self.play(hint.animate.set_opacity(1), run_time=0.5)

        self.wait(0.8)
        self._clear()

    # ----------------------------------------------------------
    # S3: 位置式 PID（一步到位 · 彩色公式 + 离散化标注 + 要点）
    # ----------------------------------------------------------
    def scene_position_pid(self):
        # ── 标题 ──
        title = cn("位置式 PID", size=44, weight=BOLD, color=COLORS["p_coral"])
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1), run_time=0.6)

        subtitle = cn("输出 = 绝对位置 u[k]", size=26, color=COLORS["text_secondary"])
        subtitle.next_to(title, DOWN, buff=0.12)
        subtitle.set_opacity(0)
        self.play(FadeIn(subtitle), run_time=0.5)

        # ── 核心公式（彩色 + 下括号标注 P/I/D）──
        pos_formula = MathTex(
            r"u[k]",
            r"=",
            r"\underbrace{K_p \cdot e[k]}_{\mathrm{P}}",
            r"+",
            r"\underbrace{K_i T_s \sum_{j=0}^{k} e[j]}_{\mathrm{I}}",
            r"+",
            r"\underbrace{K_d \frac{e[k]-e[k-1]}{T_s}}_{\mathrm{D}}",
            font_size=36,
        )
        pos_formula[0].set_color(COLORS["text_primary"])
        pos_formula[1].set_color(COLORS["text_secondary"])
        pos_formula[2].set_color(COLORS["p_coral"])
        pos_formula[3].set_color(COLORS["text_secondary"])
        pos_formula[4].set_color(COLORS["i_teal"])
        pos_formula[5].set_color(COLORS["text_secondary"])
        pos_formula[6].set_color(COLORS["d_amber"])
        pos_formula.move_to(UP * 1.0)

        # 三项逐个亮起
        pos_formula.set_opacity(0)
        self.play(pos_formula.animate.set_opacity(1), run_time=0.8)

        # P 项闪烁强调
        self.play(
            pos_formula[2].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(pos_formula[2].animate.scale(1 / 1.08), run_time=0.15)
        self.wait(0.3)
        # I 项闪烁
        self.play(
            pos_formula[4].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(pos_formula[4].animate.scale(1 / 1.08), run_time=0.15)
        self.wait(0.3)
        # D 项闪烁
        self.play(
            pos_formula[6].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(pos_formula[6].animate.scale(1 / 1.08), run_time=0.15)

        # ── 离散化核心替换（紧凑两行） ──
        disc_title = cn(
            "连续 → 离散", size=24, weight=BOLD, color=COLORS["sample_purple"]
        )
        disc_title.move_to(DOWN * 0.4)
        disc_title.set_opacity(0)

        rep_data = [
            (r"\int", r"\longrightarrow", r"\sum", COLORS["i_teal"], "积分→求和"),
            (
                r"\frac{d}{dt}",
                r"\longrightarrow",
                r"\frac{\Delta}{T_s}",
                COLORS["d_amber"],
                "微分→差分",
            ),
        ]

        rep_rows = VGroup()
        for left_tex, arrow_tex, right_tex, color, desc_text in rep_data:
            left_m = MathTex(left_tex, font_size=28, color=COLORS["text_secondary"])
            arrow_m = MathTex(arrow_tex, font_size=24, color=COLORS["sample_purple"])
            right_m = MathTex(right_tex, font_size=28, color=color)
            desc_m = cn(desc_text, size=20, color=color)
            row = VGroup(left_m, arrow_m, right_m, desc_m).arrange(RIGHT, buff=0.4)
            rep_rows.add(row)

        rep_rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rep_rows.next_to(disc_title, DOWN, buff=0.25)
        rep_rows.set_opacity(0)

        self.play(FadeIn(disc_title, shift=DOWN * 0.15), run_time=0.4)
        self.play(rep_rows.animate.set_opacity(1), run_time=0.6)

        self.wait(0.6)

        # ── 三要点（图标 + 文字） ──
        notes_data = [
            (COLORS["output_green"], "✓", "输出是全量位置 u[k]"),
            (COLORS["warning_yellow"], "⚠", "需存储全部历史误差"),
            (COLORS["warning_yellow"], "⚠", "积分饱和需限幅"),
        ]

        notes = VGroup()
        for color, icon, text in notes_data:
            icon_mob = cn(icon, size=24, color=color)
            text_mob = cn(text, size=22, color=COLORS["text_primary"])
            note = VGroup(icon_mob, text_mob).arrange(RIGHT, buff=0.2)
            notes.add(note)
        notes.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        notes.next_to(rep_rows, DOWN, buff=0.4)
        notes.set_opacity(0)

        self.play(
            LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.2),
            run_time=0.7,
        )

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S4: 增量式 PID（一页式 · 彩色公式 + 递推 + 要点）
    # ----------------------------------------------------------
    def scene_incremental_pid(self):
        # ── 标题 ──
        title = cn("增量式 PID", size=44, weight=BOLD, color=COLORS["hold_cyan"])
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1), run_time=0.6)

        subtitle = cn("输出 = 变化量 Δu[k]", size=26, color=COLORS["text_secondary"])
        subtitle.next_to(title, DOWN, buff=0.12)
        subtitle.set_opacity(0)
        self.play(FadeIn(subtitle), run_time=0.5)

        # ── 核心公式（彩色 + 下括号标注 P/I/D）──
        inc_formula = MathTex(
            r"\Delta u[k]",
            r"=",
            r"\underbrace{K_p(e[k]-e[k-1])}_{\mathrm{P}}",
            r"+",
            r"\underbrace{K_i T_s \cdot e[k]}_{\mathrm{I}}",
            r"+",
            r"\underbrace{\frac{K_d}{T_s}(e[k]-2e[k-1]+e[k-2])}_{\mathrm{D}}",
            font_size=34,
        )
        inc_formula[0].set_color(COLORS["hold_cyan"])
        inc_formula[1].set_color(COLORS["text_secondary"])
        inc_formula[2].set_color(COLORS["p_coral"])
        inc_formula[3].set_color(COLORS["text_secondary"])
        inc_formula[4].set_color(COLORS["i_teal"])
        inc_formula[5].set_color(COLORS["text_secondary"])
        inc_formula[6].set_color(COLORS["d_amber"])
        inc_formula.move_to(UP * 1.0)

        # 三项逐个亮起（与S3节奏统一）
        inc_formula.set_opacity(0)
        self.play(inc_formula.animate.set_opacity(1), run_time=0.8)

        # P 项闪烁强调
        self.play(
            inc_formula[2].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(inc_formula[2].animate.scale(1 / 1.08), run_time=0.15)
        self.wait(0.3)
        # I 项闪烁
        self.play(
            inc_formula[4].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(inc_formula[4].animate.scale(1 / 1.08), run_time=0.15)
        self.wait(0.3)
        # D 项闪烁
        self.play(
            inc_formula[6].animate.scale(1.08),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(inc_formula[6].animate.scale(1 / 1.08), run_time=0.15)

        # ── 递推公式 ──
        recur = MathTex(
            r"u[k]",
            r"=",
            r"u[k-1]",
            r"+",
            r"\Delta u[k]",
            font_size=36,
        )
        recur[0].set_color(COLORS["text_primary"])
        recur[1].set_color(COLORS["text_secondary"])
        recur[2].set_color(COLORS["text_primary"])
        recur[3].set_color(COLORS["text_secondary"])
        recur[4].set_color(COLORS["hold_cyan"])
        recur.next_to(inc_formula, DOWN, buff=0.5)
        recur.set_opacity(0).shift(DOWN * 0.2)

        self.play(recur.animate.set_opacity(1).shift(UP * 0.2), run_time=0.6)

        # Δu[k] 闪烁强调
        self.play(
            recur[4].animate.scale(1.15),
            run_time=0.2,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(recur[4].animate.scale(1 / 1.15), run_time=0.15)

        # ── 四要点（图标 + 文字，与S3风格统一） ──
        notes_data = [
            (COLORS["output_green"], "✓", "只输出增量 Δu，无需存储全量"),
            (COLORS["output_green"], "✓", "只存3个误差值 e[k], e[k-1], e[k-2]"),
            (COLORS["output_green"], "✓", "天然无积分饱和风险"),
            (COLORS["output_green"], "✓", "手动/自动切换平滑无冲击"),
        ]

        notes = VGroup()
        for color, icon, text in notes_data:
            icon_mob = cn(icon, size=22, color=color)
            text_mob = cn(text, size=20, color=COLORS["text_primary"])
            note = VGroup(icon_mob, text_mob).arrange(RIGHT, buff=0.2)
            notes.add(note)
        notes.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        notes.next_to(recur, DOWN, buff=0.4)
        notes.set_opacity(0)

        self.play(
            LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.15),
            run_time=0.7,
        )

        self.wait(1.0)
        self._clear()

    # ----------------------------------------------------------
    # S5: 位置式 vs 增量式（左右双栏对比 + 同异点）
    # ----------------------------------------------------------
    def scene_position_vs_incremental(self):
        # ── 标题 ──
        title = cn("位置式 vs 增量式", size=44, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1), run_time=0.6)

        # ── 左右双栏玻璃卡片 ──
        card_w, card_h = 5.2, 3.6
        left_card = glass_card(card_w, card_h)
        left_card.move_to(LEFT * 3.3 + UP * 0.2)

        right_card = glass_card(card_w, card_h)
        right_card.move_to(RIGHT * 3.3 + UP * 0.2)

        # 卡片标题
        pos_header = cn("位置式", size=30, weight=BOLD, color=COLORS["p_coral"])
        pos_header.move_to(left_card.get_top() + DOWN * 0.35)

        inc_header = cn("增量式", size=30, weight=BOLD, color=COLORS["hold_cyan"])
        inc_header.move_to(right_card.get_top() + DOWN * 0.35)

        # 中间 VS
        vs_text = en("VS", size=36, weight=BOLD, color=COLORS["warning_yellow"])
        vs_text.move_to(UP * 0.2)

        # 卡片入场
        self.play(
            FadeIn(left_card),
            FadeIn(pos_header),
            FadeIn(right_card),
            FadeIn(inc_header),
            run_time=0.5,
        )
        self.play(
            vs_text.animate.scale(1.3),
            run_time=0.2,
            rate_func=rate_functions.ease_out_back,
        )
        self.play(vs_text.animate.scale(1 / 1.3), run_time=0.15)

        # ── 对比项（4行，左右卡片内各2行） ──
        # 数据：(维度标签, 位置式值, 增量式值, 增量式是否更优)
        rows_data = [
            ("输出", "全量 u[k]", "增量 Δu[k]", True),
            ("存储", "全部历史误差", "最近3个误差", True),
            ("饱和", "有风险，需限幅", "天然无", True),
            ("切换", "有冲击", "平滑无冲击", True),
        ]

        # 构建左卡片内容（位置式）
        pos_items = VGroup()
        for dim, pos_val, _, _ in rows_data:
            dim_label = cn(dim, size=18, color=COLORS["text_secondary"])
            val_text = cn(pos_val, size=20, color=COLORS["text_primary"])
            item = VGroup(dim_label, val_text).arrange(
                DOWN, buff=0.05, aligned_edge=LEFT
            )
            pos_items.add(item)
        pos_items.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        pos_items.move_to(left_card.get_center() + DOWN * 0.25 + LEFT * 0.4)

        # 构建右卡片内容（增量式）
        inc_items = VGroup()
        for dim, _, inc_val, inc_better in rows_data:
            dim_label = cn(dim, size=18, color=COLORS["text_secondary"])
            val_color = COLORS["output_green"] if inc_better else COLORS["text_primary"]
            suffix = " ✓" if inc_better else ""
            val_text = cn(inc_val + suffix, size=20, color=val_color)
            item = VGroup(dim_label, val_text).arrange(
                DOWN, buff=0.05, aligned_edge=LEFT
            )
            inc_items.add(item)
        inc_items.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        inc_items.move_to(right_card.get_center() + DOWN * 0.25 + LEFT * 0.4)

        # 逐对出现
        pos_items.set_opacity(0)
        inc_items.set_opacity(0)
        for i in range(len(rows_data)):
            self.play(
                pos_items[i].animate.set_opacity(1),
                inc_items[i].animate.set_opacity(1),
                run_time=0.35,
            )

        # ── 分隔线 ──
        sep = Line(LEFT * 5.5, RIGHT * 5.5, color=COLORS["border"], stroke_width=1)
        sep.next_to(VGroup(left_card, right_card), DOWN, buff=0.3)
        self.play(Create(sep), run_time=0.3)

        # ── 底部：相同点 + 核心差异 ──
        same_title = cn("相同点", size=22, weight=BOLD, color=COLORS["output_green"])
        same_items = VGroup(
            cn(
                "同一套 PID 参数  ·  同一离散化原理  ·  本质等价",
                size=18,
                color=COLORS["text_primary"],
            ),
        )
        same_group = VGroup(same_title, same_items).arrange(
            DOWN, buff=0.08, aligned_edge=LEFT
        )
        same_group.next_to(sep, DOWN, buff=0.2)
        same_group.set_opacity(0)
        self.play(FadeIn(same_group), run_time=0.5)

        # ── 核心差异 ──
        core_diff = cn(
            '核心差异：位置式算"在哪"，增量式算"走多少"',
            size=22,
            color=COLORS["warning_yellow"],
            weight=BOLD,
        )
        core_diff.next_to(same_group, DOWN, buff=0.25)
        core_diff.set_opacity(0)
        self.play(core_diff.animate.set_opacity(1), run_time=0.5)

        self.wait(1.5)
        self._clear()

    # ----------------------------------------------------------
    # S6: 代码实现（紧凑终端 · 分组揭示 · 关键行脉冲）
    # ----------------------------------------------------------
    def scene_code_implementation(self):
        title = cn("代码实现", size=44, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1), run_time=0.6)

        CODE_FONT = "Consolas"

        def code_line(text, size=15, color=None):
            c = color or COLORS["code_lime"]
            return Text(text, font_size=size, color=c, font=CODE_FONT)

        # ── 终端创建辅助 ──
        def make_terminal(filename, center_pos):
            tw, th = 5.8, 4.2
            body = RoundedRectangle(
                width=tw,
                height=th,
                fill_opacity=0.95,
                fill_color="#0d1117",
                stroke_width=1.5,
                stroke_color=COLORS["border"],
                corner_radius=0.08,
            )
            body.move_to(center_pos)
            bar_h = 0.3
            bar = Rectangle(
                width=tw,
                height=bar_h,
                fill_opacity=0.7,
                fill_color="#1c2028",
                stroke_width=0,
            )
            bar.move_to(body.get_top() + DOWN * bar_h / 2)
            dots = VGroup(
                Dot(radius=0.045, color="#FF5F57"),
                Dot(radius=0.045, color="#FEBC2E"),
                Dot(radius=0.045, color="#28C840"),
            ).arrange(RIGHT, buff=0.09)
            dots.move_to(bar.get_left() + RIGHT * 0.3)
            bar_title = Text(
                filename,
                font_size=11,
                color=COLORS["text_secondary"],
                font=CODE_FONT,
            )
            bar_title.move_to(bar.get_center())
            code_center = body.get_center() + DOWN * bar_h * 0.25
            group = VGroup(body, bar, dots, bar_title)
            return group, code_center

        # ── 创建终端 ──
        left_term, left_center = make_terminal("pos_pid.c", LEFT * 3.2 + DOWN * 0.2)
        right_term, right_center = make_terminal("inc_pid.c", RIGHT * 3.2 + DOWN * 0.2)
        self.play(FadeIn(left_term), FadeIn(right_term), run_time=0.5)

        # ── 位置式代码 ──
        # 分组: 0=声明, 1=计算, 2=输出
        pos_lines = [
            ("// Position PID", COLORS["text_secondary"], 0),
            ("float integral=0, prev_e=0;", COLORS["text_primary"], 0),
            ("error = sp - pv;", COLORS["output_green"], 1),
            ("integral += error * Ts;", COLORS["i_teal"], 1),
            ("deriv=(error-prev_e)/Ts;", COLORS["d_amber"], 1),
            ("out=Kp*error+Ki*integral", COLORS["p_coral"], 2),
            ("    +Kd*deriv;", COLORS["p_coral"], 2),
            ("prev_e = error;", COLORS["text_secondary"], 2),
        ]

        pos_code = VGroup()
        for text, color, _ in pos_lines:
            pos_code.add(code_line(text, size=14, color=color))
        pos_code.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        pos_code.move_to(left_center + LEFT * 0.3)

        # ── 增量式代码 ──
        inc_lines = [
            ("// Incremental PID", COLORS["text_secondary"], 0),
            ("float e, e1=0, e2=0;", COLORS["text_primary"], 0),
            ("e = sp - pv;", COLORS["output_green"], 1),
            ("dP = Kp*(e-e1);", COLORS["p_coral"], 1),
            ("dI = Ki*Ts*e;", COLORS["i_teal"], 1),
            ("dD=Kd/Ts*(e-2*e1+e2);", COLORS["d_amber"], 1),
            ("out += dP+dI+dD;", COLORS["hold_cyan"], 2),
            ("e2=e1; e1=e;", COLORS["text_secondary"], 2),
        ]

        inc_code = VGroup()
        for text, color, _ in inc_lines:
            inc_code.add(code_line(text, size=14, color=color))
        inc_code.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        inc_code.move_to(right_center + LEFT * 0.3)

        # 关键行索引
        POS_KEY = 5  # "out=Kp*error+Ki*integral"
        INC_KEY = 6  # "out += dP+dI+dD;"

        # ── 分组揭示 ──
        pos_code.set_opacity(0)
        inc_code.set_opacity(0)

        for g in range(3):
            anims = []
            for i, (_, _, grp) in enumerate(pos_lines):
                if grp == g:
                    anims.append(pos_code[i].animate.set_opacity(1))
            for i, (_, _, grp) in enumerate(inc_lines):
                if grp == g:
                    anims.append(inc_code[i].animate.set_opacity(1))
            if anims:
                rt = 0.3 if g < 2 else 0.5
                self.play(*anims, run_time=rt)

        # ── 关键行脉冲聚焦 ──
        # 直接加框 + 脉冲闪烁，不做dim/restore
        pos_box = SurroundingRectangle(
            VGroup(pos_code[POS_KEY], pos_code[POS_KEY + 1]),
            color=COLORS["p_coral"],
            buff=0.06,
            stroke_width=2.5,
        )
        inc_box = SurroundingRectangle(
            inc_code[INC_KEY],
            color=COLORS["hold_cyan"],
            buff=0.06,
            stroke_width=2.5,
        )
        self.play(Create(pos_box), Create(inc_box), run_time=0.4)

        # 脉冲：框放大再收回
        self.play(
            pos_box.animate.scale(1.03),
            inc_box.animate.scale(1.03),
            run_time=0.15,
            rate_func=rate_functions.ease_out_quad,
        )
        self.play(
            pos_box.animate.scale(1 / 1.03),
            inc_box.animate.scale(1 / 1.03),
            run_time=0.15,
        )
        self.wait(0.8)

        # ── 底部一句话提示（替代冗余差异框） ──
        hint = cn(
            "out = 全量   vs   out += 增量",
            size=20,
            color=COLORS["warning_yellow"],
        )
        hint.next_to(VGroup(left_term, right_term), DOWN, buff=0.25)
        hint.set_opacity(0)
        self.play(hint.animate.set_opacity(1), run_time=0.4)

        self.wait(1.2)
        self._clear()

    # ----------------------------------------------------------
    # S7: 总结（简洁三层 · 公式→要点→核心差异）
    # ----------------------------------------------------------
    def scene_summary(self):
        # ── 标题 ──
        title = cn("数字 PID 核心要点", size=46, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        title.set_opacity(0)
        self.play(title.animate.set_opacity(1), run_time=0.6)

        # ── 第一层：离散化核心替换（大号公式，直观展示） ──
        rep1 = VGroup(
            MathTex(r"\int", font_size=40, color=COLORS["text_secondary"]),
            MathTex(r"\longrightarrow", font_size=30, color=COLORS["sample_purple"]),
            MathTex(r"\sum", font_size=40, color=COLORS["i_teal"]),
            cn("积分→求和", size=20, color=COLORS["i_teal"]),
        ).arrange(RIGHT, buff=0.3)

        rep2 = VGroup(
            MathTex(r"\frac{d}{dt}", font_size=40, color=COLORS["text_secondary"]),
            MathTex(r"\longrightarrow", font_size=30, color=COLORS["sample_purple"]),
            MathTex(r"\frac{\Delta}{T_s}", font_size=40, color=COLORS["d_amber"]),
            cn("微分→差分", size=20, color=COLORS["d_amber"]),
        ).arrange(RIGHT, buff=0.3)

        formulas = VGroup(rep1, rep2).arrange(RIGHT, buff=1.5)
        formulas.next_to(title, DOWN, buff=0.5)
        formulas.set_opacity(0)

        self.play(
            formulas.animate.set_opacity(1),
            run_time=0.6,
        )

        # ── 分隔线 ──
        sep1 = Line(LEFT * 5, RIGHT * 5, color=COLORS["border"], stroke_width=1)
        sep1.next_to(formulas, DOWN, buff=0.3)
        self.play(Create(sep1), run_time=0.25)

        # ── 第二层：两条要点（简洁清单） ──
        pt1 = VGroup(
            cn("✓", size=24, color=COLORS["output_green"]),
            cn(
                "工程首选增量式 — 平滑切换·抗饱和·省内存",
                size=24,
                color=COLORS["text_primary"],
            ),
        ).arrange(RIGHT, buff=0.2)

        pt2 = VGroup(
            cn("✓", size=24, color=COLORS["sample_purple"]),
            cn(
                "采样周期：流量 1~5s · 温度 10~30s · 伺服 0.5~2ms",
                size=24,
                color=COLORS["text_primary"],
            ),
        ).arrange(RIGHT, buff=0.2)

        points = VGroup(pt1, pt2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        points.next_to(sep1, DOWN, buff=0.3)
        points.set_opacity(0)

        self.play(
            points.animate.set_opacity(1),
            run_time=0.6,
        )

        # ── 分隔线 ──
        sep2 = Line(LEFT * 5, RIGHT * 5, color=COLORS["border"], stroke_width=1)
        sep2.next_to(points, DOWN, buff=0.3)
        self.play(Create(sep2), run_time=0.25)

        # ── 第三层：核心差异（高亮弹出，最终记忆点） ──
        core = cn(
            '位置式算"在哪"    增量式算"走多少"',
            size=28,
            color=COLORS["warning_yellow"],
            weight=BOLD,
        )
        core.next_to(sep2, DOWN, buff=0.45)
        core.scale(0.85)
        core.set_opacity(0)

        self.play(
            core.animate.set_opacity(1).scale(1 / 0.85),
            run_time=0.6,
            rate_func=rate_functions.ease_out_back,
        )

        # 脉冲强调
        self.play(core.animate.scale(1.05), run_time=0.15)
        self.play(core.animate.scale(1 / 1.05), run_time=0.15)

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
