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
    "text_primary": "#E6EDF3",
    "text_secondary": "#8B949E",
    "soft_yellow": "#FFD93D",
    "input_blue": "#58A6FF",
    "forward_cyan": "#39D2C0",
    "weight_purple": "#BC8CFF",
    "bias_teal": "#4ECDC4",
    "activation_orange": "#F59E0B",
    "output_green": "#3FB950",
    "loss_red": "#F85149",
    "gradient_warm": "#F05032",
    "delta_pink": "#F778BA",
    "update_amber": "#D29922",
    "neuron_fill": "#1C2333",
    "arrow_gray": "#6E7681",
}

FONT_CN = "SimSun"
FONT_EN = "Times New Roman"

# 布局常量：内容区 y ∈ [1.0, 3.2]，字幕区 y ∈ [-3.5, -2.5]
TITLE_Y = 3.2          # 标题
CONTENT_TOP = 2.2       # 内容顶部
CONTENT_BOT = -1.8      # 内容底部（给字幕留空间）
CAPTION_Y = -3.0        # 字幕中心


# ============================================================
# 工具函数
# ============================================================
def cn(text, size=36, color=None, weight=NORMAL, **kw):
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_CN, weight=weight, **kw)


def en(text, size=36, color=None, weight=NORMAL, **kw):
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_EN, weight=weight, **kw)


def glass_card(w, h, r=0.18):
    return RoundedRectangle(
        width=w, height=h, corner_radius=r,
        fill_opacity=0.88, fill_color=COLORS["surface"],
        stroke_width=1.5, stroke_color=COLORS["border"],
    )


def neuron_circle(label_text, color, radius=0.32):
    circle = Circle(
        radius=radius, fill_color=COLORS["neuron_fill"],
        fill_opacity=0.92, stroke_color=color, stroke_width=2.5,
    )
    label = cn(label_text, size=22, color=color, weight=BOLD)
    label.move_to(circle.get_center())
    return VGroup(circle, label)


def nn_layer(neuron_labels, color, x_pos, y_center=0, buff=0.65):
    neurons = VGroup()
    for label in neuron_labels:
        neurons.add(neuron_circle(label, color))
    neurons.arrange(DOWN, buff=buff)
    neurons.move_to(RIGHT * x_pos + UP * y_center)
    return neurons


def connect_layers(layer_left, layer_right, color=None, stroke_width=1.8):
    arrows = VGroup()
    c = color or COLORS["arrow_gray"]
    for n_left in layer_left:
        for n_right in layer_right:
            start = n_left.get_center()
            end = n_right.get_center()
            direction = end - start
            unit = direction / np.linalg.norm(direction)
            arrows.add(Arrow(
                start + unit * 0.36, end - unit * 0.36,
                buff=0, color=c, stroke_width=stroke_width,
                max_tip_length_to_length_ratio=0.15,
            ))
    return arrows


def flow_dot(color, radius=0.06):
    return Dot(radius=radius, color=color)


# ============================================================
# 主场景
# ============================================================
class ForwardBackpropVideo(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.scene_intro()
        self.scene_what_is_nn()
        self.scene_what_is_affine()
        self.scene_neuron_computation()
        self.scene_forward_propagation()
        self.scene_what_is_backprop()
        self.scene_chain_rule()
        self.scene_gradient_descent()
        self.scene_training_loop()
        self.scene_summary()

    # ----------------------------------------------------------
    # 通用工具
    # ----------------------------------------------------------
    def _clear(self):
        self.play(
            *[FadeOut(mob, shift=DOWN * 0.15) for mob in self.mobjects],
            run_time=0.6,
        )

    def _caption(self, *lines, width=11.2):
        text_group = VGroup()
        for idx, line in enumerate(lines):
            item = cn(
                line,
                size=22,
                color=COLORS["soft_yellow"] if idx == 0 else COLORS["text_primary"],
                weight=BOLD if idx == 0 else NORMAL,
            )
            if item.width > width - 0.8:
                item.scale_to_fit_width(width - 0.8)
            text_group.add(item)
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        box = glass_card(width, 0.7 + 0.46 * len(lines), r=0.14)
        text_group.move_to(box.get_center())
        group = VGroup(box, text_group)
        group.to_edge(DOWN, buff=0.22)
        return group

    def _reading_time(self, *texts, minimum=3.0, maximum=8.0,
                      units_per_second=10.0, extra=1.0):
        units = sum(sum(1 for ch in str(t) if not ch.isspace()) for t in texts)
        return min(maximum, max(minimum, units / units_per_second + extra))

    def _hold(self, *texts, **kw):
        self.wait(self._reading_time(*texts, **kw))

    def _build_network(self, y_center=0.0):
        input_layer = nn_layer(["x₁", "x₂"], COLORS["input_blue"], -3.5, y_center)
        hidden_layer = nn_layer(["h₁", "h₂", "h₃"], COLORS["forward_cyan"], 0, y_center)
        output_layer = nn_layer(["ŷ"], COLORS["output_green"], 3.5, y_center)
        arrows_1 = connect_layers(input_layer, hidden_layer)
        arrows_2 = connect_layers(hidden_layer, output_layer)
        return input_layer, hidden_layer, output_layer, arrows_1, arrows_2

    def _layer_labels(self, y_offset=0.35):
        lbl_in = cn("输入层", size=22, color=COLORS["input_blue"])
        lbl_hd = cn("隐藏层", size=22, color=COLORS["forward_cyan"])
        lbl_out = cn("输出层", size=22, color=COLORS["output_green"])
        return lbl_in, lbl_hd, lbl_out

    # ----------------------------------------------------------
    # S1: 开场
    # ----------------------------------------------------------
    def scene_intro(self):
        # ── 标题：双色，弹性缩放 ──
        t_fwd = cn("前向传播", size=56, weight=BOLD, color=COLORS["forward_cyan"])
        t_sep = cn("与", size=40, color=COLORS["text_primary"])
        t_bwd = cn("反向传播", size=56, weight=BOLD, color=COLORS["gradient_warm"])
        title = VGroup(t_fwd, t_sep, t_bwd).arrange(RIGHT, buff=0.2)
        title.move_to(UP * 2.6)

        subtitle = en("Forward & Backpropagation", size=28, color=COLORS["text_secondary"])
        subtitle.next_to(title, DOWN, buff=0.2)

        title.scale(0.3).set_opacity(0)
        subtitle.set_opacity(0)

        self.play(
            title.animate.scale(1 / 0.3).set_opacity(1),
            run_time=1.2, rate_func=rate_functions.ease_out_elastic,
        )
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.5)

        # ── 以 NN 图为中心 ──
        r = 0.2
        # 输入层（2 个神经元 + 特征标签）
        mini_in = VGroup(*[
            Circle(radius=r, fill_color=COLORS["input_blue"],
                   fill_opacity=0.85, stroke_color=COLORS["input_blue"],
                   stroke_width=2.5).shift(UP * (i - 0.5) * 0.65)
            for i in range(2)
        ]).shift(LEFT * 3.0 + UP * 0.0)
        feat1 = cn("学习时间", size=22, color=COLORS["input_blue"])
        feat1.next_to(mini_in[0], LEFT, buff=0.3)
        feat2 = cn("睡眠时间", size=22, color=COLORS["input_blue"])
        feat2.next_to(mini_in[1], LEFT, buff=0.3)

        # 隐藏层（3 个神经元）
        mini_hd = VGroup(*[
            Circle(radius=r, fill_color=COLORS["forward_cyan"],
                   fill_opacity=0.85, stroke_color=COLORS["forward_cyan"],
                   stroke_width=2.5).shift(UP * (i - 1) * 0.65)
            for i in range(3)
        ]).shift(UP * 0.0)

        # 输出层（1 个神经元 + 标签）
        mini_out = VGroup(
            Circle(radius=r, fill_color=COLORS["output_green"],
                   fill_opacity=0.85, stroke_color=COLORS["output_green"],
                   stroke_width=2.5)
        ).shift(RIGHT * 3.0 + UP * 0.0)
        pred = cn("预测分数", size=22, color=COLORS["output_green"])
        pred.next_to(mini_out[0], RIGHT, buff=0.3)

        # 连线
        mini_lines = VGroup()
        for l in mini_in:
            for h in mini_hd:
                mini_lines.add(Line(l.get_center(), h.get_center(),
                                    stroke_width=1.8, color=COLORS["arrow_gray"]))
        for h in mini_hd:
            for o in mini_out:
                mini_lines.add(Line(h.get_center(), o.get_center(),
                                    stroke_width=1.8, color=COLORS["arrow_gray"]))

        # 层标题
        lbl_in = cn("输入层", size=22, color=COLORS["input_blue"], weight=BOLD)
        lbl_in.next_to(mini_in, UP, buff=0.3)
        lbl_hd = cn("隐藏层", size=22, color=COLORS["forward_cyan"], weight=BOLD)
        lbl_hd.next_to(mini_hd, UP, buff=0.3)
        lbl_out = cn("输出层", size=22, color=COLORS["output_green"], weight=BOLD)
        lbl_out.next_to(mini_out, UP, buff=0.3)

        # 绘制网络
        self.play(
            LaggedStart(*[Create(l) for l in mini_lines], lag_ratio=0.03),
            FadeIn(mini_in), FadeIn(mini_hd), FadeIn(mini_out),
            run_time=1.2,
        )
        self.play(FadeIn(feat1), FadeIn(feat2), FadeIn(pred),
                  FadeIn(lbl_in), FadeIn(lbl_hd), FadeIn(lbl_out),
                  run_time=0.6)
        self.wait(0.5)

        # ── 前向传播动画：青色光点从左到右 ──
        fwd_label = cn("前向传播", size=24, color=COLORS["forward_cyan"], weight=BOLD)
        fwd_label.move_to(DOWN * 1.8)
        self.play(FadeIn(fwd_label), run_time=0.4)

        # 光点 input→hidden
        dots_1 = VGroup(*[flow_dot(COLORS["forward_cyan"], 0.08).move_to(l.get_start())
                          for l in mini_lines[:6]])
        self.play(FadeIn(dots_1), run_time=0.2)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_end())
                          for d, l in zip(dots_1, mini_lines[:6])], lag_ratio=0.06),
            run_time=0.8,
        )
        self.play(FadeOut(dots_1), run_time=0.15)

        # 光点 hidden→output
        dots_2 = VGroup(*[flow_dot(COLORS["forward_cyan"], 0.08).move_to(l.get_start())
                          for l in mini_lines[6:]])
        self.play(FadeIn(dots_2), run_time=0.2)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_end())
                          for d, l in zip(dots_2, mini_lines[6:])], lag_ratio=0.06),
            run_time=0.6,
        )
        self.play(FadeOut(dots_2), FadeOut(fwd_label), run_time=0.3)

        # ── 反向传播动画：暖色光点从右到左 ──
        bwd_label = cn("反向传播", size=24, color=COLORS["gradient_warm"], weight=BOLD)
        bwd_label.move_to(DOWN * 1.8)
        self.play(FadeIn(bwd_label), run_time=0.4)

        # 光点 output→hidden
        dots_3 = VGroup(*[flow_dot(COLORS["gradient_warm"], 0.08).move_to(l.get_end())
                          for l in mini_lines[6:]])
        self.play(FadeIn(dots_3), run_time=0.2)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_start())
                          for d, l in zip(dots_3, mini_lines[6:])], lag_ratio=0.06),
            run_time=0.6,
        )
        self.play(FadeOut(dots_3), run_time=0.15)

        # 光点 hidden→input
        dots_4 = VGroup(*[flow_dot(COLORS["gradient_warm"], 0.08).move_to(l.get_end())
                          for l in mini_lines[:6]])
        self.play(FadeIn(dots_4), run_time=0.2)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_start())
                          for d, l in zip(dots_4, mini_lines[:6])], lag_ratio=0.06),
            run_time=0.8,
        )
        self.play(FadeOut(dots_4), FadeOut(bwd_label), run_time=0.3)

        # ── 底部说明 ──
        caption = self._caption(
            "神经网络是如何从数据中学习规律的？",
            "前向做预测，反向算梯度，循环往复，网络学会。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "神经网络是如何从数据中学习规律的？",
            "前向做预测，反向算梯度，循环往复，网络学会。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S2: 什么是神经网络（2层网络 = 输入+隐藏+输出）
    # ----------------------------------------------------------
    def scene_what_is_nn(self):
        title = cn("什么是神经网络？", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        input_layer, hidden_layer, output_layer, arrows_1, arrows_2 = (
            self._build_network(y_center=-0.2)
        )
        lbl_in, lbl_hd, lbl_out = self._layer_labels()
        lbl_in.next_to(input_layer, UP, buff=0.3)
        lbl_hd.next_to(hidden_layer, UP, buff=0.3)
        lbl_out.next_to(output_layer, UP, buff=0.3)

        feat1 = cn("学习时间", size=22, color=COLORS["text_secondary"])
        feat2 = cn("睡眠时间", size=22, color=COLORS["text_secondary"])
        feat1.next_to(input_layer[0], LEFT, buff=0.4)
        feat2.next_to(input_layer[1], LEFT, buff=0.4)
        pred_label = cn("预测分数", size=22, color=COLORS["text_secondary"])
        pred_label.next_to(output_layer[0], RIGHT, buff=0.35)

        self.play(
            LaggedStart(
                FadeIn(input_layer, shift=UP * 0.15), FadeIn(lbl_in),
                FadeIn(feat1), FadeIn(feat2), lag_ratio=0.15,
            ), run_time=1.0,
        )
        self.play(
            LaggedStart(FadeIn(hidden_layer, shift=UP * 0.15), FadeIn(lbl_hd), lag_ratio=0.15),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                FadeIn(output_layer, shift=UP * 0.15), FadeIn(lbl_out),
                FadeIn(pred_label), lag_ratio=0.15,
            ), run_time=0.8,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_1], lag_ratio=0.08), run_time=1.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_2], lag_ratio=0.08), run_time=0.8,
        )

        # 术语标注
        note = cn("通常只计算有权重的层，所以叫「2层网络」",
                  size=22, color=COLORS["soft_yellow"])
        note.next_to(output_layer, DOWN, buff=0.6)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)

        caption = self._caption(
            "输入学习时间和睡眠时间，经过隐藏层处理，",
            "输出预测的考试分数。隐藏层用 ReLU 激活。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "输入学习时间和睡眠时间，经过隐藏层处理，",
            "输出预测的考试分数。隐藏层用 ReLU 激活。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S2.5: 什么是 Affine 层
    # ----------------------------------------------------------
    def scene_what_is_affine(self):
        title = cn("什么是 Affine 层？", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── 核心公式 ──
        f_main = MathTex(r"a = x \cdot W + b", font_size=48)
        f_main[0][0].set_color(COLORS["text_primary"])
        f_main[0][2].set_color(COLORS["input_blue"])
        f_main[0][4].set_color(COLORS["weight_purple"])
        f_main[0][6].set_color(COLORS["bias_teal"])
        f_main.move_to(UP * 1.5)

        card = glass_card(f_main.width + 1.0, f_main.height + 0.5, r=0.14)
        card.move_to(f_main.get_center())

        self.play(FadeIn(card), Write(f_main), run_time=0.8)
        self.wait(0.3)

        # ── 逐项解释（两列布局，更紧凑）──
        x_explain = cn("x = 输入数据", size=22, color=COLORS["input_blue"])
        w_explain = cn("W = 权重", size=22, color=COLORS["weight_purple"])
        b_explain = cn("b = 偏置", size=22, color=COLORS["bias_teal"])
        a_explain = cn("a = 加权求和结果", size=22, color=COLORS["text_primary"])

        col_left = VGroup(x_explain, w_explain).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        col_right = VGroup(b_explain, a_explain).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explains = VGroup(col_left, col_right).arrange(RIGHT, buff=1.5)
        explains.move_to(UP * 0.1)

        for e in col_left:
            self.play(FadeIn(e, shift=RIGHT * 0.1), run_time=0.3)
        for e in col_right:
            self.play(FadeIn(e, shift=RIGHT * 0.1), run_time=0.3)

        # ── 直观例子（紧凑卡片，在字幕上方）──
        example_card = glass_card(10.0, 0.7, r=0.12)
        example_card.shift(DOWN * 1.5)
        example = cn("例：预测分数 = 学习时间 × 0.6 + 睡眠时间 × 0.3 + 偏置",
                     size=22, color=COLORS["soft_yellow"])
        example.move_to(example_card.get_center())

        self.play(FadeIn(example_card), FadeIn(example), run_time=0.6)

        caption = self._caption(
            "Affine 层就是加权求和：把每个输入乘以权重，再加上偏置。",
            "这是神经网络中最基础的计算。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "Affine 层就是加权求和：把每个输入乘以权重，再加上偏置。",
            "这是神经网络中最基础的计算。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S3: 神经元计算（Affine 层 + ReLU 层）
    # ----------------------------------------------------------
    def scene_neuron_computation(self):
        title = cn("Affine 层 + 激活层", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── Phase 1: 结构图 ──
        neuron = neuron_circle("h₁", COLORS["forward_cyan"], radius=0.4)
        neuron.move_to(LEFT * 1.5 + UP * 0.3)

        in1 = Arrow(LEFT * 5.5 + UP * 1.3, neuron.get_left() + UP * 0.12,
                     buff=0.1, color=COLORS["input_blue"], stroke_width=3)
        in2 = Arrow(LEFT * 5.5 + DOWN * 0.7, neuron.get_left() + DOWN * 0.12,
                     buff=0.1, color=COLORS["input_blue"], stroke_width=3)
        w1 = cn("w₁", size=22, color=COLORS["weight_purple"])
        w1.move_to(in1.get_center() + UP * 0.28)
        w2 = cn("w₂", size=22, color=COLORS["weight_purple"])
        w2.move_to(in2.get_center() + DOWN * 0.28)
        x1 = cn("x₁", size=24, color=COLORS["input_blue"])
        x1.move_to(LEFT * 5.5 + UP * 1.3 + LEFT * 0.3)
        x2 = cn("x₂", size=24, color=COLORS["input_blue"])
        x2.move_to(LEFT * 5.5 + DOWN * 0.7 + LEFT * 0.3)

        bias = neuron_circle("b", COLORS["bias_teal"], 0.2)
        bias.move_to(DOWN * 1.3 + LEFT * 1.5)
        bias_arr = Arrow(bias.get_top(), neuron.get_bottom() + DOWN * 0.05,
                         buff=0.1, color=COLORS["bias_teal"], stroke_width=2.5)

        out = Arrow(neuron.get_right() + RIGHT * 0.05, RIGHT * 2.0,
                    buff=0.1, color=COLORS["output_green"], stroke_width=3)
        z_lbl = cn("z", size=24, color=COLORS["output_green"])
        z_lbl.next_to(out, UP, buff=0.2)

        self.play(FadeIn(neuron, scale=0.8), run_time=0.6)
        self.play(GrowArrow(in1), GrowArrow(in2), FadeIn(w1), FadeIn(w2),
                  FadeIn(x1), FadeIn(x2), run_time=0.8)
        self.play(GrowArrow(bias_arr), FadeIn(bias), run_time=0.5)
        self.play(GrowArrow(out), FadeIn(z_lbl), run_time=0.5)
        self.wait(0.8)

        # ── Phase 2: 清掉结构，展示 Affine + ReLU 公式 ──
        struct_group = VGroup(neuron, in1, in2, w1, w2, x1, x2, bias, bias_arr, out, z_lbl)
        self.play(FadeOut(struct_group, shift=LEFT * 0.3), run_time=0.6)

        # Affine 层公式
        f_affine_label = cn("Affine 层", size=22, color=COLORS["weight_purple"], weight=BOLD)
        f1 = MathTex(r"a = x \cdot W + b", font_size=34)
        f1[0][0].set_color(COLORS["text_primary"])
        f1[0][2].set_color(COLORS["input_blue"])
        f1[0][4].set_color(COLORS["weight_purple"])
        f1[0][6].set_color(COLORS["bias_teal"])

        # ReLU 层公式
        f_relu_label = cn("ReLU 层", size=22, color=COLORS["activation_orange"], weight=BOLD)
        f2 = MathTex(r"z = \max(0, a)", font_size=34)
        f2.set_color(COLORS["activation_orange"])

        affine_group = VGroup(f_affine_label, f1).arrange(DOWN, buff=0.15)
        relu_group = VGroup(f_relu_label, f2).arrange(DOWN, buff=0.15)
        formulas = VGroup(affine_group, relu_group).arrange(DOWN, buff=0.5)
        formulas.move_to(UP * 0.5)

        card = glass_card(formulas.width + 0.8, formulas.height + 0.6, r=0.14)
        card.move_to(formulas.get_center())

        self.play(FadeIn(card), FadeIn(f_affine_label), Write(f1), run_time=0.8)
        self.play(FadeIn(f_relu_label), Write(f2), run_time=0.8)

        # ReLU 曲线（右下）
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 3, 1],
            x_length=3.0, y_length=1.4,
            axis_config={"stroke_color": COLORS["text_secondary"], "stroke_width": 1},
        )
        axes.move_to(RIGHT * 4.0 + DOWN * 1.5)
        curve = axes.plot(lambda x: max(0, x),
                          color=COLORS["activation_orange"], stroke_width=2.5)
        relu_lbl = cn("ReLU(a)", size=22, color=COLORS["activation_orange"])
        relu_lbl.next_to(axes, UP, buff=0.15)

        self.play(Create(axes), run_time=0.5)
        self.play(Create(curve), FadeIn(relu_lbl), run_time=0.8)
        self.wait(0.5)

        # 要点
        note = cn("隐藏层常用 ReLU，输出层用 Softmax 或恒等函数",
                  size=22, color=COLORS["soft_yellow"])
        note.move_to(DOWN * 1.8)
        self.play(FadeIn(note), run_time=0.5)

        caption = self._caption(
            "Affine 层做矩阵乘法加偏置，ReLU 层把负值截为零。",
            "这是隐藏层的标准组合，简单却非常有效。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "Affine 层做矩阵乘法加偏置，ReLU 层把负值截为零。",
            "这是隐藏层的标准组合，简单却非常有效。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S4: 前向传播（层的正向传递 forward）
    # ----------------------------------------------------------
    def scene_forward_propagation(self):
        title = cn("前向传播 forward()", size=40, weight=BOLD, color=COLORS["forward_cyan"])
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── 构建网络，增加标注 ──
        input_layer, hidden_layer, output_layer, arrows_1, arrows_2 = (
            self._build_network(y_center=-0.2)
        )
        lbl_in, lbl_hd, lbl_out = self._layer_labels()
        lbl_in.next_to(input_layer, UP, buff=0.25)
        lbl_hd.next_to(hidden_layer, UP, buff=0.25)
        lbl_out.next_to(output_layer, UP, buff=0.25)

        # 特征标签
        feat1 = cn("学习时间", size=22, color=COLORS["input_blue"])
        feat2 = cn("睡眠时间", size=22, color=COLORS["input_blue"])
        feat1.next_to(input_layer[0], LEFT, buff=0.4)
        feat2.next_to(input_layer[1], LEFT, buff=0.4)

        # 输入值
        val_x1 = cn("0.6", size=22, color=COLORS["soft_yellow"])
        val_x2 = cn("0.8", size=22, color=COLORS["soft_yellow"])
        val_x1.next_to(feat1, DOWN, buff=0.15)
        val_x2.next_to(feat2, DOWN, buff=0.15)

        # 权重标签 W1（取几条代表性连线标注）
        w1_lbl = cn("W₁", size=22, color=COLORS["weight_purple"], weight=BOLD)
        w1_lbl.move_to(arrows_1[0].get_center() + UP * 0.28)
        b1_lbl = cn("b₁", size=22, color=COLORS["bias_teal"], weight=BOLD)
        b1_lbl.next_to(hidden_layer[0], LEFT, buff=0.55)

        w2_lbl = cn("W₂", size=22, color=COLORS["weight_purple"], weight=BOLD)
        w2_lbl.move_to(arrows_2[0].get_center() + UP * 0.25)
        b2_lbl = cn("b₂", size=22, color=COLORS["bias_teal"], weight=BOLD)
        b2_lbl.next_to(output_layer[0], LEFT, buff=0.55)

        # 输出标注
        pred_label = cn("预测分数", size=22, color=COLORS["output_green"])
        pred_label.next_to(output_layer[0], RIGHT, buff=0.4)

        # ── 动画：逐层展示 ──
        self.play(
            FadeIn(input_layer), FadeIn(feat1), FadeIn(feat2),
            FadeIn(val_x1), FadeIn(val_x2), FadeIn(lbl_in),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_1], lag_ratio=0.04),
            FadeIn(hidden_layer), FadeIn(lbl_hd),
            FadeIn(w1_lbl), FadeIn(b1_lbl),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_2], lag_ratio=0.04),
            FadeIn(output_layer), FadeIn(lbl_out),
            FadeIn(w2_lbl), FadeIn(b2_lbl), FadeIn(pred_label),
            run_time=1.0,
        )

        # ── 光点流 input→hidden ──
        dots_1 = VGroup(*[flow_dot(COLORS["forward_cyan"]).move_to(a.get_start()) for a in arrows_1])
        self.play(FadeIn(dots_1), run_time=0.3)
        self.play(
            LaggedStart(*[d.animate.move_to(a.get_end()) for d, a in zip(dots_1, arrows_1)],
                        lag_ratio=0.08),
            run_time=1.0,
        )
        self.play(FadeOut(dots_1), run_time=0.2)

        # 隐藏层激活
        self.play(
            LaggedStart(*[Indicate(h, color=COLORS["forward_cyan"], scale_factor=1.12)
                          for h in hidden_layer], lag_ratio=0.1),
            run_time=0.6,
        )

        # ── 光点流 hidden→output ──
        dots_2 = VGroup(*[flow_dot(COLORS["forward_cyan"]).move_to(a.get_start()) for a in arrows_2])
        self.play(FadeIn(dots_2), run_time=0.3)
        self.play(
            LaggedStart(*[d.animate.move_to(a.get_end()) for d, a in zip(dots_2, arrows_2)],
                        lag_ratio=0.08),
            run_time=0.8,
        )
        self.play(FadeOut(dots_2), run_time=0.2)

        # 输出值
        val_y = cn("ŷ = 0.65", size=22, color=COLORS["soft_yellow"], weight=BOLD)
        val_y.next_to(output_layer[0], DOWN, buff=0.25)
        self.play(
            FadeIn(val_y, shift=UP * 0.1),
            Indicate(output_layer[0], color=COLORS["output_green"], scale_factor=1.15),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── 清掉网络，展示层的流向 ──
        net_group = VGroup(
            input_layer, hidden_layer, output_layer,
            arrows_1, arrows_2, lbl_in, lbl_hd, lbl_out,
            feat1, feat2, val_x1, val_x2, val_y,
            w1_lbl, w2_lbl, b1_lbl, b2_lbl, pred_label,
        )
        self.play(FadeOut(net_group, shift=DOWN * 0.2), run_time=0.5)

        # ── forward() 流向图（带中间值标注）──
        layer_names = ["Affine1", "ReLU", "Affine2", "Softmax"]
        layer_colors = [COLORS["weight_purple"], COLORS["activation_orange"],
                        COLORS["weight_purple"], COLORS["output_green"]]
        layer_boxes = VGroup()
        for name, color in zip(layer_names, layer_colors):
            box = glass_card(2.0, 0.7, r=0.1)
            box.set_stroke(color=color, width=2)
            lbl = cn(name, size=22, color=color, weight=BOLD)
            lbl.move_to(box.get_center())
            layer_boxes.add(VGroup(box, lbl))
        layer_boxes.arrange(RIGHT, buff=0.3)
        layer_boxes.move_to(UP * 0.5)

        flow_arrows = VGroup()
        for i in range(3):
            a = Arrow(layer_boxes[i].get_right(), layer_boxes[i + 1].get_left(),
                      buff=0.08, color=COLORS["arrow_gray"], stroke_width=2)
            flow_arrows.add(a)

        # 中间值标注（箭头上方）
        mid_labels = [
            ("x", COLORS["input_blue"]),
            ("a₁", COLORS["weight_purple"]),
            ("z₁", COLORS["activation_orange"]),
            ("ŷ", COLORS["output_green"]),
        ]
        mid_lbls = VGroup()
        for i, (text, color) in enumerate(mid_labels):
            lbl = cn(text, size=22, color=color, weight=BOLD)
            if i == 0:
                lbl.next_to(layer_boxes[0], LEFT, buff=0.3)
            elif i == 3:
                lbl.next_to(layer_boxes[3], RIGHT, buff=0.3)
            else:
                lbl.next_to(flow_arrows[i - 1], UP, buff=0.12)
            mid_lbls.add(lbl)

        # 代码片段
        code_txt = cn("for layer in layers.values():", size=22, color=COLORS["text_secondary"])
        code_txt2 = cn("    x = layer.forward(x)", size=22, color=COLORS["forward_cyan"])
        code_group = VGroup(code_txt, code_txt2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        code_group.next_to(layer_boxes, DOWN, buff=0.6)

        # 动画
        self.play(FadeIn(mid_lbls[0]), run_time=0.3)
        for i in range(4):
            self.play(FadeIn(layer_boxes[i], shift=RIGHT * 0.1), run_time=0.4)
            if i < 3:
                self.play(GrowArrow(flow_arrows[i]), FadeIn(mid_lbls[i + 1]), run_time=0.4)
        self.play(FadeIn(code_group), run_time=0.5)

        caption = self._caption(
            "数据依次经过 Affine1→ReLU→Affine2→Softmax，得到 ŷ。",
            "每一层都调用 forward()，输出传给下一层。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "数据依次经过 Affine1→ReLU→Affine2→Softmax，得到 ŷ。",
            "每一层都调用 forward()，输出传给下一层。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S5: 反向传播 backward() — 与 S1 NN 图照应
    # ----------------------------------------------------------
    def scene_what_is_backprop(self):
        title = cn("反向传播 backward()", size=40, weight=BOLD, color=COLORS["gradient_warm"])
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── 与 S1 相同的 NN 图 ──
        r = 0.2
        mini_in = VGroup(*[
            Circle(radius=r, fill_color=COLORS["input_blue"],
                   fill_opacity=0.85, stroke_color=COLORS["input_blue"],
                   stroke_width=2.5).shift(UP * (i - 0.5) * 0.65)
            for i in range(2)
        ]).shift(LEFT * 3.0 + UP * 0.3)
        mini_hd = VGroup(*[
            Circle(radius=r, fill_color=COLORS["forward_cyan"],
                   fill_opacity=0.85, stroke_color=COLORS["forward_cyan"],
                   stroke_width=2.5).shift(UP * (i - 1) * 0.65)
            for i in range(3)
        ]).shift(UP * 0.3)
        mini_out = VGroup(
            Circle(radius=r, fill_color=COLORS["output_green"],
                   fill_opacity=0.85, stroke_color=COLORS["output_green"],
                   stroke_width=2.5)
        ).shift(RIGHT * 3.0 + UP * 0.3)

        mini_lines = VGroup()
        for l in mini_in:
            for h in mini_hd:
                mini_lines.add(Line(l.get_center(), h.get_center(),
                                    stroke_width=1.8, color=COLORS["arrow_gray"]))
        for h in mini_hd:
            for o in mini_out:
                mini_lines.add(Line(h.get_center(), o.get_center(),
                                    stroke_width=1.8, color=COLORS["arrow_gray"]))

        lbl_in = cn("输入层", size=22, color=COLORS["input_blue"], weight=BOLD)
        lbl_in.next_to(mini_in, UP, buff=0.3)
        lbl_hd = cn("隐藏层", size=22, color=COLORS["forward_cyan"], weight=BOLD)
        lbl_hd.next_to(mini_hd, UP, buff=0.3)
        lbl_out = cn("输出层", size=22, color=COLORS["output_green"], weight=BOLD)
        lbl_out.next_to(mini_out, UP, buff=0.3)

        self.play(
            LaggedStart(*[Create(l) for l in mini_lines], lag_ratio=0.03),
            FadeIn(mini_in), FadeIn(mini_hd), FadeIn(mini_out),
            FadeIn(lbl_in), FadeIn(lbl_hd), FadeIn(lbl_out),
            run_time=1.0,
        )

        # ── 前向（灰暗）+ 反向（暖色高亮）──
        fwd_label = cn("前向传播 →", size=22, color=COLORS["arrow_gray"])
        fwd_label.move_to(DOWN * 1.5)
        fwd_label.set_opacity(0.5)
        self.play(FadeIn(fwd_label), run_time=0.3)

        # 暖色反向光点 output→hidden→input
        bwd_label = cn("← 反向传播", size=24, color=COLORS["gradient_warm"], weight=BOLD)
        bwd_label.move_to(DOWN * 1.5)
        self.play(FadeOut(fwd_label), FadeIn(bwd_label), run_time=0.4)

        # 光点 hidden→output 反向
        dots_b1 = VGroup(*[flow_dot(COLORS["gradient_warm"], 0.09).move_to(l.get_end())
                           for l in mini_lines[6:]])
        self.play(FadeIn(dots_b1), run_time=0.15)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_start())
                          for d, l in zip(dots_b1, mini_lines[6:])], lag_ratio=0.06),
            run_time=0.6,
        )
        self.play(FadeOut(dots_b1), run_time=0.1)

        # 光点 input→hidden 反向
        dots_b2 = VGroup(*[flow_dot(COLORS["gradient_warm"], 0.09).move_to(l.get_end())
                           for l in mini_lines[:6]])
        self.play(FadeIn(dots_b2), run_time=0.15)
        self.play(
            LaggedStart(*[d.animate.move_to(l.get_start())
                          for d, l in zip(dots_b2, mini_lines[:6])], lag_ratio=0.06),
            run_time=0.8,
        )
        self.play(FadeOut(dots_b2), run_time=0.1)
        self.wait(0.5)

        # ── 清掉 NN，展示代码 + 公式 ──
        net_group = VGroup(
            mini_in, mini_hd, mini_out, mini_lines,
            lbl_in, lbl_hd, lbl_out, bwd_label,
        )
        self.play(FadeOut(net_group, shift=DOWN * 0.2), run_time=0.5)

        # 代码片段
        code1 = cn("for layer in reversed(layers):", size=22, color=COLORS["text_secondary"])
        code2 = cn("    dout = layer.backward(dout)", size=22, color=COLORS["gradient_warm"])
        code_group = VGroup(code1, code2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        code_group.move_to(UP * 1.8)

        self.play(FadeIn(code_group), run_time=0.5)
        self.wait(0.8)

        # ── 三张公式卡片（横向并排，不打架）──
        formula_data = [
            ("Softmax", r"\frac{\partial L}{\partial a} = y - t",
             "误差信号", COLORS["delta_pink"]),
            ("Affine", r"\frac{\partial L}{\partial W} = x^\top \cdot \delta",
             "权重梯度", COLORS["weight_purple"]),
            ("ReLU", r"\mathbb{1}(x>0) \cdot \delta",
             "截断传递", COLORS["activation_orange"]),
        ]

        cards = VGroup()
        for name, formula, explain, color in formula_data:
            lbl = cn(name, size=22, color=color, weight=BOLD)
            f = MathTex(formula, font_size=28, color=color)
            exp = cn(explain, size=22, color=COLORS["text_secondary"])
            inner = VGroup(lbl, f, exp).arrange(DOWN, buff=0.1)
            card = glass_card(inner.width + 0.4, inner.height + 0.3, r=0.1)
            card.set_stroke(color=color, width=2)
            inner.move_to(card.get_center())
            cards.add(VGroup(card, inner))

        cards.arrange(RIGHT, buff=0.3)
        cards.move_to(DOWN * 0.5)

        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.1), run_time=0.5)
            self.wait(0.5)

        caption = self._caption(
            "每层实现 backward()，梯度从输出层逐层传回输入层。",
            "就像 S1 的暖色光点，从右到左传递误差信号。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "每层实现 backward()，梯度从输出层逐层传回输入层。",
            "就像 S1 的暖色光点，从右到左传递误差信号。",
            minimum=8,
        )
        self._clear()

    # ----------------------------------------------------------
    # S7: 链式法则（层的反向传播传递链）
    # ----------------------------------------------------------
    def scene_chain_rule(self):
        title = cn("链式法则：梯度如何逐层传递", size=38, weight=BOLD, color=COLORS["delta_pink"])
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── 先解释链式法则的概念 ──
        chain_intro = cn("复合函数的导数 = 各层导数的乘积", size=24, color=COLORS["soft_yellow"])
        chain_intro.next_to(title, DOWN, buff=0.3)
        chain_formula = MathTex(
            r"\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \cdot "
            r"\frac{\partial y}{\partial h} \cdot \frac{\partial h}{\partial w}",
            font_size=30, color=COLORS["text_primary"],
        )
        chain_formula.next_to(chain_intro, DOWN, buff=0.25)

        self.play(FadeIn(chain_intro), run_time=0.5)
        self.play(Write(chain_formula), run_time=1.0)
        self.wait(1.0)

        # 清掉概念，展示具体步骤
        self.play(FadeOut(chain_intro), FadeOut(chain_formula), run_time=0.5)

        step_data = [
            ("① SoftmaxWithLoss", r"\delta_3 = y - t",
             "误差信号 = 预测 - 标签", COLORS["delta_pink"]),
            ("② Affine2 层", r"\frac{\partial L}{\partial W_2} = z_1^\top \cdot \delta_3",
             "用隐藏层输出 × 上游梯度", COLORS["weight_purple"]),
            ("③ ReLU 层", r"\delta_2 = \delta_3 \cdot W_2^\top \cdot \mathbb{1}(z_1 > 0)",
             "正数传梯度，负数截断为 0", COLORS["activation_orange"]),
            ("④ Affine1 层", r"\frac{\partial L}{\partial W_1} = x^\top \cdot \delta_2",
             "用输入 × 上游梯度", COLORS["forward_cyan"]),
        ]

        cards = VGroup()
        y_positions = [1.6, 0.4, -0.8, -2.0]
        for (label, formula, explain, color), y in zip(step_data, y_positions):
            card = glass_card(9.5, 1.2, r=0.12)
            card.shift(UP * y)
            lbl = cn(label, size=22, color=color, weight=BOLD)
            lbl.move_to(card.get_center() + LEFT * 3.0 + UP * 0.2)
            f = MathTex(formula, font_size=28, color=color)
            f.move_to(card.get_center() + RIGHT * 0.5 + UP * 0.2)
            exp = cn(explain, size=22, color=COLORS["text_secondary"])
            exp.move_to(card.get_center() + DOWN * 0.28)
            cards.add(VGroup(card, lbl, f, exp))

        # 逐个出现，每步停顿
        for c in cards:
            self.play(FadeIn(c, shift=UP * 0.1), run_time=0.7)
            self.wait(0.8)

        # 连接箭头
        arrows = VGroup()
        for i in range(3):
            a = Arrow(
                cards[i].get_bottom() + DOWN * 0.03,
                cards[i + 1].get_top() + UP * 0.03,
                buff=0.03, color=COLORS["arrow_gray"], stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(a)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=0.8)

        caption = self._caption(
            "每层用局部导数 × 上游梯度，这就是链式法则。",
            "梯度像接力棒，从输出层逐层传回输入层。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "每层用局部导数 × 上游梯度，这就是链式法则。",
            "梯度像接力棒，从输出层逐层传回输入层。",
            minimum=8,
        )
        self._clear()

    # ----------------------------------------------------------
    # S8: 梯度下降（公式 + 曲线分步展示）
    # ----------------------------------------------------------
    def scene_gradient_descent(self):
        title = cn("梯度下降：更新权重", size=40, weight=BOLD, color=COLORS["update_amber"])
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── Phase 1: 公式 + 直觉解释 ──
        f_update = MathTex(
            r"w^{\text{new}} = w^{\text{old}} - \alpha \frac{\partial L}{\partial w}",
            font_size=38, color=COLORS["soft_yellow"],
        )
        f_update.move_to(UP * 1.8)

        card = glass_card(f_update.width + 0.8, f_update.height + 0.4, r=0.14)
        card.move_to(f_update.get_center())

        self.play(FadeIn(card), Write(f_update), run_time=0.8)

        # 逐项解释
        exp_w = cn("w = 权重参数", size=22, color=COLORS["text_primary"])
        exp_a = cn("α = 学习率（步长）", size=22, color=COLORS["activation_orange"])
        exp_g = cn("∂L/∂w = 梯度（方向）", size=22, color=COLORS["gradient_warm"])
        exps = VGroup(exp_w, exp_a, exp_g).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        exps.move_to(UP * 0.3)

        for e in exps:
            self.play(FadeIn(e, shift=RIGHT * 0.1), run_time=0.35)
        self.wait(0.5)

        # 直觉比喻
        analogy = cn("梯度告诉你「哪边下坡」，学习率决定「走多远」", size=22, color=COLORS["soft_yellow"])
        analogy.move_to(DOWN * 1.0)
        self.play(FadeIn(analogy), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(card), FadeOut(f_update), FadeOut(exps), FadeOut(analogy),
                  run_time=0.5)

        # ── Phase 2: 损失曲线 + 滚动小球 ──
        axes = Axes(
            x_range=[0, 1.5, 0.5], y_range=[0, 1.0, 0.5],
            x_length=5.0, y_length=2.5,
            axis_config={"stroke_color": COLORS["text_secondary"], "stroke_width": 1},
        )
        axes.move_to(LEFT * 1.5 + UP * 0.1)
        loss_curve = axes.plot(lambda x: (x - 0.90) ** 2 * 0.8 + 0.05,
                               color=COLORS["loss_red"], stroke_width=2.5)
        x_lbl = cn("权重 w", size=22, color=COLORS["text_secondary"])
        x_lbl.next_to(axes, DOWN, buff=0.1)
        y_lbl = cn("损失 L", size=22, color=COLORS["loss_red"])
        y_lbl.next_to(axes, LEFT, buff=0.1)

        self.play(Create(axes), Create(loss_curve), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)

        # 小球沿曲线滚动（多步下降）
        ball = Dot(radius=0.12, color=COLORS["update_amber"])
        w_positions = [0.30, 0.45, 0.55, 0.65, 0.75, 0.82, 0.87]
        ball.move_to(axes.c2p(w_positions[0], (w_positions[0] - 0.90) ** 2 * 0.8 + 0.05))
        self.play(FadeIn(ball), run_time=0.3)

        for i in range(1, len(w_positions)):
            w = w_positions[i]
            target = axes.c2p(w, (w - 0.90) ** 2 * 0.8 + 0.05)
            self.play(ball.animate.move_to(target), run_time=0.5)
            self.wait(0.15)

        # 标记最低点
        min_dot = Dot(axes.c2p(0.90, 0.05), color=COLORS["output_green"], radius=0.1)
        min_lbl = cn("最优解", size=22, color=COLORS["output_green"], weight=BOLD)
        min_lbl.next_to(min_dot, UP, buff=0.15)
        self.play(FadeIn(min_dot), FadeIn(min_lbl), run_time=0.5)
        self.wait(0.5)

        # 学习率对比卡片（右侧）
        lr_card = glass_card(3.2, 2.2, r=0.12)
        lr_card.shift(RIGHT * 3.8 + UP * 0.1)
        lr_title = cn("学习率 α 的影响", size=22, color=COLORS["activation_orange"], weight=BOLD)
        lr_title.move_to(lr_card.get_center() + UP * 0.7)

        lr1 = cn("太大 → 来回震荡", size=22, color=COLORS["loss_red"])
        lr2 = cn("太小 → 收敛太慢", size=22, color=COLORS["text_secondary"])
        lr3 = cn("刚好 → 稳定下降", size=22, color=COLORS["output_green"])
        lr_items = VGroup(lr1, lr2, lr3).arrange(DOWN, buff=0.2)
        lr_items.move_to(lr_card.get_center() + DOWN * 0.15)

        self.play(FadeIn(lr_card), FadeIn(lr_title), run_time=0.4)
        for item in [lr1, lr2, lr3]:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.35)
        self.wait(1.0)

        caption = self._caption(
            "梯度告诉你下坡方向，学习率决定每步走多远。",
            "沿损失曲面逐步下降，直到找到最优解。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "梯度告诉你下坡方向，学习率决定每步走多远。",
            "沿损失曲面逐步下降，直到找到最优解。",
            minimum=8,
        )
        self._clear()

    # ----------------------------------------------------------
    # S9: 训练循环（TwoLayerNet + SGD 的完整训练）
    # ----------------------------------------------------------
    def scene_training_loop(self):
        title = cn("完整训练循环", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── Phase 1: 4 步循环 ──
        box_w, box_h = 2.2, 0.85
        positions = [UP * 1.0 + LEFT * 2.5, UP * 1.0 + RIGHT * 2.5,
                     DOWN * 0.5 + RIGHT * 2.5, DOWN * 0.5 + LEFT * 2.5]
        labels = ["① Mini-batch", "② gradient()", "③ 更新参数", "④ 重复"]
        colors = [COLORS["forward_cyan"], COLORS["loss_red"],
                  COLORS["gradient_warm"], COLORS["update_amber"]]

        boxes = VGroup()
        for pos, label, color in zip(positions, labels, colors):
            card = glass_card(box_w, box_h, r=0.1)
            card.set_stroke(color=color, width=2)
            card.move_to(pos)
            lbl = cn(label, size=22, color=color, weight=BOLD)
            lbl.move_to(card.get_center())
            boxes.add(VGroup(card, lbl))

        loop_arrows = VGroup()
        for i in range(4):
            s = boxes[i].get_center()
            e = boxes[(i + 1) % 4].get_center()
            d = e - s; u = d / np.linalg.norm(d)
            loop_arrows.add(Arrow(s + u * 0.5, e - u * 0.5, buff=0,
                                  color=COLORS["arrow_gray"], stroke_width=2.5,
                                  max_tip_length_to_length_ratio=0.12))

        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.15),
                  run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in loop_arrows], lag_ratio=0.12),
                  run_time=0.8)

        # 光点循环
        dot = flow_dot(COLORS["soft_yellow"], 0.09)
        dot.move_to(boxes[0].get_center())
        self.play(FadeIn(dot), run_time=0.2)
        for _ in range(2):
            for i in range(4):
                self.play(dot.animate.move_to(boxes[(i + 1) % 4].get_center()), run_time=0.4)
        self.play(FadeOut(dot), run_time=0.2)

        # ── Phase 2: 清掉循环图，代码（左）+ 曲线（右）──
        self.play(FadeOut(boxes), FadeOut(loop_arrows), run_time=0.5)

        # 代码卡片（左侧）
        code_lines = [
            ("for i in range(10000):", COLORS["text_secondary"]),
            ("    batch = x_train[mask]", COLORS["forward_cyan"]),
            ("    grad = network.gradient(batch)", COLORS["loss_red"]),
            ("    params -= lr * grad  # SGD", COLORS["gradient_warm"]),
        ]
        code_group = VGroup()
        for text, color in code_lines:
            code_group.add(cn(text, size=22, color=color))
        code_group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        code_card = glass_card(code_group.width + 0.5, code_group.height + 0.4, r=0.1)
        code_card.move_to(LEFT * 3.0 + UP * 0.3)
        code_group.move_to(code_card.get_center())

        self.play(FadeIn(code_card), FadeIn(code_group), run_time=0.8)

        # 损失曲线（右侧）
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1, 0.5],
            x_length=4.5, y_length=2.0,
            axis_config={"stroke_color": COLORS["text_secondary"], "stroke_width": 1},
        )
        axes.move_to(RIGHT * 2.8 + UP * 0.3)
        x_label = cn("训练轮数", size=22, color=COLORS["text_secondary"])
        x_label.next_to(axes, DOWN, buff=0.1)
        y_label = cn("损失", size=22, color=COLORS["loss_red"])
        y_label.next_to(axes, LEFT, buff=0.1)
        loss_line = axes.plot(lambda x: 0.8 * np.exp(-0.3 * x) + 0.05,
                              color=COLORS["loss_red"], stroke_width=2.5)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)
        self.play(Create(loss_line), run_time=1.5)

        conv_lbl = cn("损失收敛 → 模型学会", size=22, color=COLORS["output_green"], weight=BOLD)
        conv_lbl.next_to(axes, UP, buff=0.15)
        self.play(FadeIn(conv_lbl), run_time=0.4)
        self.wait(0.5)

        caption = self._caption(
            "取 mini-batch、算梯度、更新参数，循环往复。",
            "上万次迭代，损失逐渐收敛，模型越来越准。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "取 mini-batch、算梯度、更新参数，循环往复。",
            "上万次迭代，损失逐渐收敛，模型越来越准。",
            minimum=8,
        )
        self._clear()

    # ----------------------------------------------------------
    # S10: 总结
    # ----------------------------------------------------------
    def scene_summary(self):
        title = cn("总结：前向传播与反向传播", size=40, weight=BOLD, color=COLORS["soft_yellow"])
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        # ── 中央 NN 图（与 S1 照应，更紧凑）──
        r = 0.15
        mini_in = VGroup(*[
            Circle(radius=r, fill_color=COLORS["input_blue"],
                   fill_opacity=0.85, stroke_color=COLORS["input_blue"],
                   stroke_width=2).shift(UP * (i - 0.5) * 0.45)
            for i in range(2)
        ]).shift(LEFT * 2.0 + UP * 0.8)
        mini_hd = VGroup(*[
            Circle(radius=r, fill_color=COLORS["forward_cyan"],
                   fill_opacity=0.85, stroke_color=COLORS["forward_cyan"],
                   stroke_width=2).shift(UP * (i - 1) * 0.45)
            for i in range(3)
        ]).shift(UP * 0.8)
        mini_out = VGroup(
            Circle(radius=r, fill_color=COLORS["output_green"],
                   fill_opacity=0.85, stroke_color=COLORS["output_green"],
                   stroke_width=2)
        ).shift(RIGHT * 2.0 + UP * 0.8)

        mini_lines = VGroup()
        for l in mini_in:
            for h in mini_hd:
                mini_lines.add(Line(l.get_center(), h.get_center(),
                                    stroke_width=1.5, color=COLORS["arrow_gray"]))
        for h in mini_hd:
            for o in mini_out:
                mini_lines.add(Line(h.get_center(), o.get_center(),
                                    stroke_width=1.5, color=COLORS["arrow_gray"]))

        self.play(
            LaggedStart(*[Create(l) for l in mini_lines], lag_ratio=0.03),
            FadeIn(mini_in), FadeIn(mini_hd), FadeIn(mini_out),
            run_time=1.0,
        )

        # ── 前向传播标注（上方，青色）──
        fwd_arrow = Arrow(
            mini_in.get_top() + UP * 0.1 + LEFT * 0.2,
            mini_out.get_top() + UP * 0.1 + RIGHT * 0.2,
            buff=0.1, color=COLORS["forward_cyan"], stroke_width=3,
            max_tip_length_to_length_ratio=0.06,
        )
        fwd_lbl = cn("前向传播：输入 → 预测", size=22, color=COLORS["forward_cyan"], weight=BOLD)
        fwd_lbl.next_to(fwd_arrow, UP, buff=0.1)
        self.play(GrowArrow(fwd_arrow), FadeIn(fwd_lbl), run_time=0.6)

        # ── 反向传播标注（下方，暖色）──
        bwd_arrow = Arrow(
            mini_out.get_bottom() + DOWN * 0.1 + RIGHT * 0.2,
            mini_in.get_bottom() + DOWN * 0.1 + LEFT * 0.2,
            buff=0.1, color=COLORS["gradient_warm"], stroke_width=3,
            max_tip_length_to_length_ratio=0.06,
        )
        bwd_lbl = cn("反向传播：误差 → 梯度", size=22, color=COLORS["gradient_warm"], weight=BOLD)
        bwd_lbl.next_to(bwd_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(bwd_arrow), FadeIn(bwd_lbl), run_time=0.6)
        self.wait(0.5)

        # ── 三步总结卡片（紧凑排列）──
        step_data = [
            ("① 前向", "Affine→ReLU→Softmax → ŷ", COLORS["forward_cyan"]),
            ("② 反向", "梯度 = y - t，逐层传回", COLORS["gradient_warm"]),
            ("③ 更新", "w = w - α × 梯度，循环学习", COLORS["update_amber"]),
        ]
        step_cards = VGroup()
        for label, desc, color in step_data:
            lbl = cn(label, size=22, color=color, weight=BOLD)
            dsc = cn(desc, size=22, color=COLORS["text_primary"])
            inner = VGroup(lbl, dsc).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            card = glass_card(inner.width + 0.4, inner.height + 0.3, r=0.1)
            card.set_stroke(color=color, width=2)
            inner.move_to(card.get_center())
            step_cards.add(VGroup(card, inner))

        step_cards.arrange(RIGHT, buff=0.25)
        step_cards.move_to(DOWN * 1.3)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in step_cards], lag_ratio=0.15),
                  run_time=1.0)
        self.wait(1.0)

        caption = self._caption(
            "前向做预测，反向算梯度，SGD 更新权重。",
            "循环往复，网络就学会了。这就是深度学习的核心。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "前向做预测，反向算梯度，SGD 更新权重。",
            "循环往复，网络就学会了。这就是深度学习的核心。",
            minimum=8,
        )
        self._clear()


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    config.quality = "fourk_quality"
    config.preview = True
