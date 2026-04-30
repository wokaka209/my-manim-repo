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
    "conv_orange": "#F59E0B",
    "feature_blue": "#58A6FF",
    "pool_green": "#3FB950",
    "relu_red": "#F85149",
    "accent_purple": "#BC8CFF",
    "text_primary": "#E6EDF3",
    "text_secondary": "#8B949E",
    "soft_yellow": "#FFD93D",
}

FONT_CN = "SimSun"
FONT_EN = "Times New Roman"


# ============================================================
# 工具函数
# ============================================================
def gray_to_hex(gray):
    """将 0-1 之间的灰度值转换为十六进制颜色代码"""
    value = int(gray * 255)
    return f"#{value:02X}{value:02X}{value:02X}"


def cn(text, size=36, color=None, weight=NORMAL, **kw):
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_CN, weight=weight, **kw)


def en(text, size=36, color=None, weight=NORMAL, **kw):
    c = color or COLORS["text_primary"]
    return Text(text, font_size=size, color=c, font=FONT_EN, weight=weight, **kw)


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


def matrix_grid(values, cell_size=0.55, color=WHITE, fill="#223042", text_size=20):
    rows = len(values)
    cols = len(values[0])
    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            rect = Square(
                side_length=cell_size,
                stroke_color=color,
                stroke_width=1.6,
                fill_color=fill,
                fill_opacity=0.85,
            )
            rect.move_to(
                np.array(
                    [
                        (j - (cols - 1) / 2) * cell_size,
                        ((rows - 1) / 2 - i) * cell_size,
                        0,
                    ]
                )
            )
            label = Text(
                str(values[i][j]),
                font=FONT_EN,
                font_size=text_size,
                color=COLORS["text_primary"],
            )
            label.move_to(rect.get_center())
            cells.add(rect, label)
    return cells


def image_patch(size=6, cell_size=0.4):
    values = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append((i * 2 + j) % 10)
        values.append(row)

    patch = VGroup()
    for i in range(size):
        for j in range(size):
            gray = 0.18 + 0.1 * ((i + j) % 5)
            rect = Square(
                side_length=cell_size,
                stroke_color=COLORS["border"],
                stroke_width=1,
                fill_color=gray_to_hex(gray),
                fill_opacity=1.0,
            )
            rect.move_to(
                np.array(
                    [
                        (j - (size - 1) / 2) * cell_size,
                        ((size - 1) / 2 - i) * cell_size,
                        0,
                    ]
                )
            )
            patch.add(rect)
    return patch


def stack_block(label_text, color, width=1.6, height=2.6, layers=4):
    blocks = VGroup()
    for idx in range(layers):
        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.14 + idx * 0.05,
        )
        card.shift(RIGHT * idx * 0.08 + UP * idx * 0.06)
        blocks.add(card)
    text = cn(label_text, size=24, color=color, weight=BOLD)
    text.next_to(blocks, DOWN, buff=0.25)
    return VGroup(blocks, text)


# ============================================================
# 主场景
# ============================================================
class CNNPopularizationVideo(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.scene_intro()
        self.scene_image_shape()
        self.scene_why_cnn()
        self.scene_convolution_core()
        self.scene_kernel_shape()
        self.scene_feature_maps()
        self.scene_relu_pooling()
        self.scene_hierarchy()
        self.scene_training_and_apps()
        self.scene_summary()

    # ----------------------------------------------------------
    # 通用清屏
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
                size=22 if idx == 0 else 19,
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

    def _reading_time(
        self, *texts, minimum=2.4, maximum=6.5, units_per_second=11.5, extra=0.55
    ):
        units = 0
        for text in texts:
            units += sum(1 for ch in str(text) if not ch.isspace())
        return min(maximum, max(minimum, units / units_per_second + extra))

    def _hold(
        self, *texts, minimum=2.4, maximum=6.5, units_per_second=11.5, extra=0.55
    ):
        self.wait(
            self._reading_time(
                *texts,
                minimum=minimum,
                maximum=maximum,
                units_per_second=units_per_second,
                extra=extra,
            )
        )

    # ----------------------------------------------------------
    # S1: 开场
    # ----------------------------------------------------------
    def scene_intro(self):
        title = cn("卷积神经网络", size=60, weight=BOLD)
        subtitle = en(
            "Convolutional Neural Network", size=28, color=COLORS["text_secondary"]
        )
        slogan = cn("让计算机逐层看懂图像", size=30, color=COLORS["soft_yellow"])

        title.move_to(UP * 1.6)
        subtitle.next_to(title, DOWN, buff=0.35)
        slogan.next_to(subtitle, DOWN, buff=0.5)

        title.scale(0.4).set_opacity(0)
        subtitle.set_opacity(0)
        slogan.set_opacity(0)

        self.play(
            title.animate.scale(1 / 0.4).set_opacity(1),
            run_time=1.2,
            rate_func=rate_functions.ease_out_elastic,
        )
        self.play(FadeIn(subtitle, shift=UP * 0.2), FadeIn(slogan, shift=UP * 0.2))

        left_card = glass_card(2.2, 2.2)
        left_card.shift(LEFT * 4.2 + DOWN * 0.7)
        left_img = image_patch(size=5, cell_size=0.28).move_to(left_card.get_center())
        left_label = cn("输入图像", size=24, color=COLORS["feature_blue"])
        left_label.next_to(left_card, DOWN, buff=0.2)

        right_card = glass_card(2.2, 2.2)
        right_card.shift(RIGHT * 4.2 + DOWN * 0.7)
        right_text = cn("猫", size=34, color=COLORS["pool_green"], weight=BOLD)
        right_text.move_to(right_card.get_center())
        right_label = cn("分类结果", size=24, color=COLORS["pool_green"])
        right_label.next_to(right_card, DOWN, buff=0.2)

        arrow = Arrow(
            left_card.get_right() + RIGHT * 0.2,
            right_card.get_left() + LEFT * 0.2,
            buff=0.1,
            color=COLORS["conv_orange"],
            stroke_width=5,
        )
        mid_text = cn("CNN", size=32, color=COLORS["conv_orange"], weight=BOLD)
        mid_text.next_to(arrow, UP, buff=0.2)
        caption = self._caption(
            "CNN 的目标，是把像素逐层变成“可以判断类别的证据”。",
            "它不会一口气看完整张图，而是从局部开始，边提特征边压缩信息。",
        )

        self.play(
            FadeIn(left_card),
            FadeIn(left_img),
            FadeIn(left_label),
            GrowArrow(arrow),
            FadeIn(mid_text),
            FadeIn(right_card),
            FadeIn(right_text),
            FadeIn(right_label),
            run_time=1.6,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "CNN 的目标，是把像素逐层变成可以判断类别的证据。",
            "它不会一口气看完整张图，而是从局部开始，边提特征边压缩信息。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S2: 输入图像的 W×H×C
    # ----------------------------------------------------------
    def scene_image_shape(self):
        title = cn("输入图像为什么写成 W×H×C？", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        image_card = glass_card(2.9, 2.9)
        image_card.shift(LEFT * 4.25 + UP * 0.45)
        image_data = image_patch(size=6, cell_size=0.31).move_to(image_card.get_center())
        image_label = cn("一张彩色图片", size=22, color=COLORS["feature_blue"])
        image_label.next_to(image_card, DOWN, buff=0.18)

        formula = MathTex(
            r"32 \times 32 \times 3",
            font_size=44,
            color=COLORS["text_primary"],
        )
        formula.move_to(UP * 1.05 + RIGHT * 1.1)

        dim_specs = [
            ("W", "宽度", "每行有多少列像素", COLORS["conv_orange"]),
            ("H", "高度", "一共有多少行像素", COLORS["pool_green"]),
            ("C", "通道数", "RGB 通常等于 3", COLORS["accent_purple"]),
        ]
        dim_cards = VGroup()
        for idx, (symbol, name, desc, color) in enumerate(dim_specs):
            card = glass_card(2.15, 1.6).move_to(RIGHT * (idx * 2.45 - 0.95) + DOWN * 0.2)
            content = VGroup(
                cn(symbol, size=26, color=color, weight=BOLD),
                cn(name, size=20, color=color),
                cn(desc, size=15, color=COLORS["text_secondary"]),
            ).arrange(DOWN, buff=0.08)
            content.move_to(card.get_center())
            dim_cards.add(VGroup(card, content))

        example_gray = VGroup(
            cn("灰度图：28×28×1", size=18, color=COLORS["text_secondary"]),
            cn("彩色图：32×32×3", size=18, color=COLORS["soft_yellow"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        example_gray.move_to(RIGHT * 1.35 + DOWN * 1.65)

        arrows = VGroup(
            Arrow(formula.get_left() + DOWN * 0.05, dim_cards[0][0].get_top(), buff=0.12, color=COLORS["conv_orange"]),
            Arrow(formula.get_center() + DOWN * 0.05, dim_cards[1][0].get_top(), buff=0.12, color=COLORS["pool_green"]),
            Arrow(formula.get_right() + DOWN * 0.05, dim_cards[2][0].get_top(), buff=0.12, color=COLORS["accent_purple"]),
        )
        caption = self._caption(
            "W×H×C 不是公式技巧，而是图像数据的基本组织方式：宽、高、通道。",
            "前两个维度描述空间位置，最后一个维度描述同一位置上有几路颜色或特征值。",
        )

        self.play(FadeIn(image_card), FadeIn(image_data), FadeIn(image_label), run_time=1.2)
        self.play(Write(formula), run_time=1.0)
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15),
            LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in dim_cards], lag_ratio=0.15),
            FadeIn(example_gray, shift=UP * 0.15),
            run_time=1.8,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "W乘H乘C不是公式技巧，而是图像数据的基本组织方式，宽、高、通道。",
            "前两个维度描述空间位置，最后一个维度描述同一位置上有几路颜色或特征值。",
            minimum=7.2,
        )
        self._clear()

    # ----------------------------------------------------------
    # S2: 为什么需要 CNN
    # ----------------------------------------------------------
    def scene_why_cnn(self):
        title = cn("为什么不用普通全连接网络？", size=42, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        image_card = glass_card(3.2, 3.2)
        patch = image_patch(size=6, cell_size=0.38).move_to(image_card.get_center())
        image_label = cn("一张 32×32×3 的图片", size=24, color=COLORS["feature_blue"])
        image_label.next_to(image_card, DOWN, buff=0.2)
        image_group = VGroup(image_card, patch, image_label)

        fc_card = glass_card(4.8, 4.0)
        fc_title = cn(
            "如果直接拉平成向量", size=24, color=COLORS["relu_red"], weight=BOLD
        )
        fc_formula = MathTex(
            r"32 \times 32 \times 3 = 3072",
            font_size=32,
            color=COLORS["text_primary"],
        )
        fc_params = cn(
            "若接 1000 个神经元，首层参数约 307 万",
            size=20,
            color=COLORS["soft_yellow"],
        )
        fc_breakdown = cn(
            "W、H、C 被压成 1 个长度为 3072 的向量",
            size=18,
            color=COLORS["text_secondary"],
        )
        fc_desc = cn("参数多、忽略空间关系", size=22, color=COLORS["text_secondary"])
        fc_content = VGroup(fc_title, fc_formula, fc_params, fc_breakdown, fc_desc).arrange(
            DOWN, buff=0.24
        )
        fc_content.move_to(fc_card.get_center())
        fc_group = VGroup(fc_card, fc_content)

        top_row = VGroup(image_group, fc_group).arrange(
            RIGHT, buff=1.35, aligned_edge=UP
        )
        top_row.move_to(UP * 0.65)

        arrow = Arrow(
            image_card.get_right() + RIGHT * 0.15,
            fc_card.get_left() + LEFT * 0.15,
            buff=0.1,
            color=COLORS["text_secondary"],
        )
        arrow.put_start_and_end_on(
            image_card.get_right() + RIGHT * 0.12,
            fc_card.get_left() + LEFT * 0.12,
        )
        flatten_label = cn("拉平", size=20, color=COLORS["text_secondary"])
        flatten_label.next_to(arrow, UP, buff=0.12)
        caption = self._caption(
            "一旦把 W×H×C 完全拉平，原来相邻的像素关系就不再显式保留。",
            "但图像理解依赖局部结构：边缘、角点、纹理都来自“附近像素之间如何变化”。",
        )

        self.play(
            FadeIn(image_card),
            FadeIn(patch),
            FadeIn(image_label),
            GrowArrow(arrow),
            FadeIn(flatten_label),
            FadeIn(fc_card),
            FadeIn(fc_title),
            Write(fc_formula),
            FadeIn(fc_params),
            FadeIn(fc_breakdown),
            FadeIn(fc_desc),
            run_time=1.8,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "一旦把W乘H乘C完全拉平，原来相邻的像素关系就不再显式保留。",
            "但图像理解依赖局部结构，边缘角点纹理都来自附近像素之间如何变化。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S3: 卷积的核心动作
    # ----------------------------------------------------------
    def scene_convolution_core(self):
        title = cn("卷积公式到底在算什么？", size=42, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        def row_items(grid, row_idx, cols=3):
            start = row_idx * cols * 2
            end = start + cols * 2
            return VGroup(*grid[start:end])

        image_m = matrix_grid(
            [[5, 2, 1], [4, 3, 1], [1, 2, 5]],
            cell_size=0.56,
            color=COLORS["feature_blue"],
            fill="#17324a",
        )
        kernel_m = matrix_grid(
            [[1, 0, -1], [1, 0, -1], [1, 0, -1]],
            cell_size=0.56,
            color=COLORS["conv_orange"],
            fill="#4a2d12",
        )
        output_box = Square(
            side_length=1.05,
            stroke_color=COLORS["pool_green"],
            stroke_width=2.5,
            fill_color="#173b24",
            fill_opacity=0.9,
        )
        output_num = Text("3", font=FONT_EN, font_size=32, color=COLORS["text_primary"])
        output_num.move_to(output_box.get_center())
        output_group = VGroup(output_box, output_num)

        input_panel = glass_card(2.75, 2.95)
        input_title = cn("1. 输入局部区域", size=22, color=COLORS["feature_blue"], weight=BOLD)
        input_title.move_to(input_panel.get_top() + DOWN * 0.28)
        image_m.move_to(input_panel.get_center() + DOWN * 0.18)
        input_group = VGroup(input_panel, input_title, image_m)

        kernel_panel = glass_card(2.75, 2.95)
        kernel_title = cn("2. 卷积核", size=22, color=COLORS["conv_orange"], weight=BOLD)
        kernel_title.move_to(kernel_panel.get_top() + DOWN * 0.28)
        kernel_m.move_to(kernel_panel.get_center() + DOWN * 0.18)
        kernel_group = VGroup(kernel_panel, kernel_title, kernel_m)

        output_panel = glass_card(2.35, 2.95)
        output_title = cn("3. 输出像素", size=22, color=COLORS["pool_green"], weight=BOLD)
        output_title.move_to(output_panel.get_top() + DOWN * 0.28)
        output_group.move_to(output_panel.get_center() + DOWN * 0.1)
        output_group_all = VGroup(output_panel, output_title, output_group)

        top_row = VGroup(input_group, kernel_group, output_group_all).arrange(RIGHT, buff=0.7)
        top_row.move_to(UP * 1.6)

        arrow1 = Arrow(input_group.get_right(), kernel_group.get_left(), buff=0.12, color=COLORS["text_secondary"])
        arrow2 = Arrow(kernel_group.get_right(), output_group_all.get_left(), buff=0.12, color=COLORS["text_secondary"])
        arrow1_label = cn("逐元素相乘", size=16, color=COLORS["text_secondary"])
        arrow2_label = cn("三行结果求和", size=16, color=COLORS["text_secondary"])
        arrow1_label.next_to(arrow1, UP, buff=0.08)
        arrow2_label.next_to(arrow2, UP, buff=0.08)

        simplification_tag = glass_card(3.0, 0.72, r=0.12)
        simplification_tag.move_to(UP * 2.35 + RIGHT * 4.1)
        simplification_text = cn("先看单通道 3×3 示例", size=18, color=COLORS["soft_yellow"], weight=BOLD)
        simplification_text.move_to(simplification_tag.get_center())

        self.play(FadeIn(simplification_tag), FadeIn(simplification_text), FadeIn(input_group), run_time=1.0)
        self.play(GrowArrow(arrow1), FadeIn(arrow1_label), FadeIn(kernel_group), run_time=1.1)
        self.play(GrowArrow(arrow2), FadeIn(arrow2_label), FadeIn(output_group_all), run_time=1.1)

        formula_card = glass_card(10.8, 0.95)
        formula_card.move_to(DOWN * 0.05)
        formula_title = cn("总公式", size=18, color=COLORS["soft_yellow"], weight=BOLD)
        formula_title.move_to(formula_card.get_left() + RIGHT * 0.9)
        general_formula = MathTex(
            r"y_{i,j}=\sum_{u,v} x_{i+u,j+v}\,k_{u,v}",
            font_size=32,
            color=COLORS["text_primary"],
        )
        general_formula.move_to(formula_card.get_center() + RIGHT * 0.8)

        calc_card = glass_card(10.8, 1.55)
        calc_card.move_to(DOWN * 1.23)
        calc_title = cn("逐行计算过程", size=18, color=COLORS["accent_purple"], weight=BOLD)
        calc_title.move_to(calc_card.get_top() + DOWN * 0.22)
        row_formula = MathTex(
            r"5\cdot1 + 2\cdot0 + 1\cdot(-1) = 4",
            font_size=30,
            color=COLORS["soft_yellow"],
        )
        row_formula.move_to(calc_card.get_center() + UP * 0.22)
        step_label = cn(
            "第一行计算", size=22, color=COLORS["accent_purple"], weight=BOLD
        )
        step_label.move_to(calc_card.get_center() + DOWN * 0.2)

        image_rows = [row_items(image_m, idx) for idx in range(3)]
        kernel_rows = [row_items(kernel_m, idx) for idx in range(3)]
        image_highlights = [
            SurroundingRectangle(group, color=COLORS["accent_purple"], buff=0.05)
            for group in image_rows
        ]
        kernel_highlights = [
            SurroundingRectangle(group, color=COLORS["soft_yellow"], buff=0.05)
            for group in kernel_rows
        ]

        row_formulas = [
            MathTex(
                r"5\cdot1 + 2\cdot0 + 1\cdot(-1) = 4",
                font_size=30,
                color=COLORS["soft_yellow"],
            ),
            MathTex(
                r"4\cdot1 + 3\cdot0 + 1\cdot(-1) = 3",
                font_size=30,
                color=COLORS["soft_yellow"],
            ),
            MathTex(
                r"1\cdot1 + 2\cdot0 + 5\cdot(-1) = -4",
                font_size=30,
                color=COLORS["soft_yellow"],
            ),
        ]
        for formula in row_formulas:
            formula.move_to(row_formula)

        step_labels = [
            cn("第一行计算", size=22, color=COLORS["accent_purple"], weight=BOLD),
            cn("第二行计算", size=22, color=COLORS["accent_purple"], weight=BOLD),
            cn("第三行计算", size=22, color=COLORS["accent_purple"], weight=BOLD),
        ]
        for label in step_labels:
            label.move_to(step_label)

        final_formula = MathTex(
            r"r_1 + r_2 + r_3 = 4 + 3 + (-4) = 3",
            font_size=30,
            color=COLORS["pool_green"],
        )
        final_formula.move_to(row_formula)
        final_label = cn(
            "三行结果求和", size=22, color=COLORS["pool_green"], weight=BOLD
        )
        final_label.move_to(step_label)
        partial_results = [
            MathTex(r"r_1=4,\quad r_2=?,\quad r_3=?", font_size=26, color=COLORS["text_secondary"]),
            MathTex(r"r_1=4,\quad r_2=3,\quad r_3=?", font_size=26, color=COLORS["text_secondary"]),
            MathTex(r"r_1=4,\quad r_2=3,\quad r_3=-4", font_size=26, color=COLORS["text_secondary"]),
        ]
        for result in partial_results:
            result.move_to(calc_card.get_center() + DOWN * 0.58)
        final_results = MathTex(
            r"r_1=4,\quad r_2=3,\quad r_3=-4",
            font_size=26,
            color=COLORS["pool_green"],
        )
        final_results.move_to(partial_results[0])
        caption = self._caption(
            "这里先用单通道示例解释卷积：当前位置的输出，来自局部窗口内像素和卷积核权重的逐元素乘加。",
            "这组 [1,0,-1] 会比较左侧和右侧的数值差异，所以更容易对竖直边缘产生强响应。",
        )

        self.play(
            FadeIn(formula_card),
            FadeIn(formula_title),
            Write(general_formula),
            FadeIn(calc_card),
            FadeIn(calc_title),
            Write(row_formula),
            FadeIn(step_label),
            FadeIn(partial_results[0]),
        )
        self.play(
            Create(image_highlights[0]), Create(kernel_highlights[0]), run_time=0.8
        )
        self._hold(
            "第一行计算", "5乘1加2乘0加1乘负1等于4", minimum=1.3, maximum=2.2, extra=0.2
        )

        for idx in range(1, 3):
            self.play(
                Transform(image_highlights[idx - 1], image_highlights[idx]),
                Transform(kernel_highlights[idx - 1], kernel_highlights[idx]),
                Transform(row_formula, row_formulas[idx]),
                Transform(step_label, step_labels[idx]),
                Transform(partial_results[0], partial_results[idx]),
                run_time=1.0,
            )
            self._hold(
                step_labels[idx].text,
                ["4乘1加3乘0加1乘负1等于3", "1乘1加2乘0加5乘负1等于负4"][idx - 1],
                minimum=1.3,
                maximum=2.2,
                extra=0.2,
            )

        self.play(
            FadeOut(image_highlights[0]),
            FadeOut(kernel_highlights[0]),
            Transform(row_formula, final_formula),
            Transform(step_label, final_label),
            Transform(partial_results[0], final_results),
            Indicate(output_group, color=COLORS["pool_green"]),
            run_time=1.1,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "这里先用单通道示例解释卷积，当前位置的输出，来自局部窗口内像素和卷积核权重的逐元素乘加。",
            "这组一零负一会比较左侧和右侧的数值差异，所以更容易对竖直边缘产生强响应。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S4: 卷积核为什么是这种结构
    # ----------------------------------------------------------
    def scene_kernel_shape(self):
        title = cn("卷积核为什么通常是 3×3×C？", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        input_card = glass_card(2.55, 3.05).shift(LEFT * 4.25 + UP * 0.82)
        input_stack = VGroup(
            RoundedRectangle(
                width=1.55,
                height=2.0,
                corner_radius=0.08,
                stroke_color=COLORS["feature_blue"],
                fill_color=COLORS["feature_blue"],
                fill_opacity=0.12,
            ),
            RoundedRectangle(
                width=1.55,
                height=2.0,
                corner_radius=0.08,
                stroke_color=COLORS["feature_blue"],
                fill_color=COLORS["feature_blue"],
                fill_opacity=0.18,
            ).shift(RIGHT * 0.12 + UP * 0.09),
            RoundedRectangle(
                width=1.55,
                height=2.0,
                corner_radius=0.08,
                stroke_color=COLORS["feature_blue"],
                fill_color=COLORS["feature_blue"],
                fill_opacity=0.24,
            ).shift(RIGHT * 0.24 + UP * 0.18),
        )
        input_stack.move_to(input_card.get_center() + UP * 0.12)
        input_text = VGroup(
            cn("输入体", size=20, color=COLORS["feature_blue"], weight=BOLD),
            MathTex(r"W\times H\times C", font_size=24, color=COLORS["text_primary"]),
        ).arrange(DOWN, buff=0.12)
        input_text.move_to(input_card.get_center() + DOWN * 0.83)

        kernel_card = glass_card(2.6, 3.05).shift(ORIGIN + UP * 0.82)
        kernel_stack = VGroup(
            RoundedRectangle(
                width=1.05,
                height=1.05,
                corner_radius=0.06,
                stroke_color=COLORS["conv_orange"],
                fill_color=COLORS["conv_orange"],
                fill_opacity=0.16,
            ),
            RoundedRectangle(
                width=1.05,
                height=1.05,
                corner_radius=0.06,
                stroke_color=COLORS["conv_orange"],
                fill_color=COLORS["conv_orange"],
                fill_opacity=0.22,
            ).shift(RIGHT * 0.1 + UP * 0.08),
            RoundedRectangle(
                width=1.05,
                height=1.05,
                corner_radius=0.06,
                stroke_color=COLORS["conv_orange"],
                fill_color=COLORS["conv_orange"],
                fill_opacity=0.3,
            ).shift(RIGHT * 0.2 + UP * 0.16),
        )
        kernel_stack.move_to(kernel_card.get_center() + UP * 0.18)
        kernel_text = VGroup(
            cn("卷积核", size=20, color=COLORS["conv_orange"], weight=BOLD),
            MathTex(r"3\times 3\times C", font_size=24, color=COLORS["text_primary"]),
        ).arrange(DOWN, buff=0.12)
        kernel_text.move_to(kernel_card.get_center() + DOWN * 0.83)

        output_card = glass_card(2.2, 3.05).shift(RIGHT * 4.0 + UP * 0.82)
        output_box = Square(
            side_length=1.2,
            stroke_color=COLORS["pool_green"],
            stroke_width=2.5,
            fill_color=COLORS["pool_green"],
            fill_opacity=0.15,
        )
        output_box.move_to(output_card.get_center() + UP * 0.25)
        output_text = VGroup(
            cn("输出", size=20, color=COLORS["pool_green"], weight=BOLD),
            cn("1 个响应值", size=18, color=COLORS["text_primary"]),
        ).arrange(DOWN, buff=0.12)
        output_text.move_to(output_card.get_center() + DOWN * 0.83)

        arrow1 = Arrow(input_card.get_right(), kernel_card.get_left(), buff=0.2, color=COLORS["text_secondary"])
        arrow2 = Arrow(kernel_card.get_right(), output_card.get_left(), buff=0.2, color=COLORS["text_secondary"])

        reason_card = glass_card(10.2, 1.12).move_to(DOWN * 1.24)
        reason_lines = VGroup(
            cn("1. 空间只取 3×3：局部模式来自邻近像素，小窗口更省参数。", size=15, color=COLORS["soft_yellow"]),
            cn("2. 深度等于 C：同一位置的 R、G、B 或多通道特征要一起参与加权。", size=15),
            cn("3. 同一个核反复滑动：同类边缘或纹理会出现在不同位置，规则应共享。", size=15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        reason_lines.move_to(reason_card.get_center())
        reasons = VGroup(reason_card, reason_lines)

        caption = self._caption(
            "卷积核在空间上只看一个小邻域，在通道上却要覆盖全部输入深度，这样才能同时利用位置关系和颜色信息。",
            "所以常见写法是 3×3×C，而不是随便取一个没有结构的一维权重向量。",
        )

        self.play(
            FadeIn(input_card),
            FadeIn(input_stack),
            FadeIn(input_text),
            FadeIn(kernel_card),
            FadeIn(kernel_stack),
            FadeIn(kernel_text),
            FadeIn(output_card),
            FadeIn(output_box),
            FadeIn(output_text),
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            run_time=1.8,
        )
        self.play(FadeIn(reasons, shift=UP * 0.12), run_time=1.2)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "卷积核在空间上只看一个小邻域，在通道上却要覆盖全部输入深度，这样才能同时利用位置关系和颜色信息。",
            "所以常见写法是三乘三乘C，而不是随便取一个没有结构的一维权重向量。",
            minimum=7.4,
        )
        self._clear()

    # ----------------------------------------------------------
    # S5: 多个卷积核生成多个特征图
    # ----------------------------------------------------------
    def scene_feature_maps(self):
        title = cn("为什么会有多个特征图？", size=42, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        image_card = glass_card(2.1, 2.1).shift(LEFT * 5.0 + UP * 0.3)
        image_data = image_patch(size=5, cell_size=0.27).move_to(
            image_card.get_center()
        )
        image_label = cn("原图", size=22, color=COLORS["feature_blue"])
        image_label.next_to(image_card, DOWN, buff=0.18)

        kernel_specs = [
            ("边缘核", "突出轮廓", COLORS["conv_orange"], UP * 1.45),
            ("纹理核", "响应重复纹理", COLORS["accent_purple"], ORIGIN),
            ("角点核", "捕捉交汇处", COLORS["pool_green"], DOWN * 1.45),
        ]
        kernel_cards = VGroup()
        kernel_texts = VGroup()
        fmap_groups = VGroup()
        arrows = VGroup()
        for label, desc, color, offset in kernel_specs:
            kernel_card = glass_card(1.95, 1.05).move_to(
                LEFT * 1.55 + offset + UP * 0.15
            )
            kernel_text = (
                VGroup(
                    cn(label, size=18, color=color, weight=BOLD),
                    cn(desc, size=14, color=COLORS["text_secondary"]),
                )
                .arrange(DOWN, buff=0.08)
                .move_to(kernel_card.get_center())
            )
            fmap = stack_block(
                label.replace("核", "图"), color, width=1.15, height=1.15, layers=3
            ).scale(0.78)
            fmap.move_to(RIGHT * 3.55 + offset + UP * 0.15)
            fmap[1].next_to(fmap[0], RIGHT, buff=0.16)
            arrow = Arrow(
                image_card.get_right() + RIGHT * 0.05 + offset * 0.12,
                fmap.get_left(),
                buff=0.18,
                color=color,
                stroke_width=4,
            )
            kernel_cards.add(kernel_card)
            kernel_texts.add(kernel_text)
            fmap_groups.add(fmap)
            arrows.add(arrow)
        caption = self._caption(
            "一层卷积通常不会只学一个卷积核，而是并行学习多种“看图规则”。",
            "于是同一张输入会被拆成多张特征图，分别记录边缘、纹理、角点等不同证据。",
        )

        self.play(
            FadeIn(image_card),
            FadeIn(image_data),
            FadeIn(image_label),
            LaggedStart(*[FadeIn(card) for card in kernel_cards], lag_ratio=0.15),
            LaggedStart(*[FadeIn(text) for text in kernel_texts], lag_ratio=0.15),
        )
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.12),
            LaggedStart(
                *[FadeIn(fmap, shift=RIGHT * 0.15) for fmap in fmap_groups],
                lag_ratio=0.12,
            ),
            run_time=1.8,
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "一层卷积通常不会只学一个卷积核，而是并行学习多种看图规则。",
            "于是同一张输入会被拆成多张特征图，分别记录边缘、纹理、角点等不同证据。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S5: 激活函数与池化
    # ----------------------------------------------------------
    def scene_relu_pooling(self):
        title = cn("卷积后还会发生什么？", size=42, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        conv_box = glass_card(2.45, 2.15).shift(LEFT * 3.7 + UP * 1.2)
        conv_text = (
            VGroup(
                cn("卷积", size=26, color=COLORS["conv_orange"], weight=BOLD),
                cn("提取局部模式", size=20),
            )
            .arrange(DOWN, buff=0.18)
            .move_to(conv_box.get_center())
        )

        relu_box = glass_card(2.45, 2.15).shift(UP * 1.2)
        relu_text = (
            VGroup(
                cn("ReLU", size=26, color=COLORS["relu_red"], weight=BOLD),
                MathTex(r"f(x)=\max(0, x)", font_size=26, color=COLORS["text_primary"]),
            )
            .arrange(DOWN, buff=0.18)
            .move_to(relu_box.get_center())
        )

        pool_box = glass_card(2.45, 2.15).shift(RIGHT * 3.7 + UP * 1.2)
        pool_text = (
            VGroup(
                cn("池化", size=26, color=COLORS["pool_green"], weight=BOLD),
                cn("压缩尺寸，保留重点", size=20),
            )
            .arrange(DOWN, buff=0.18)
            .move_to(pool_box.get_center())
        )

        arrow1 = Arrow(
            conv_box.get_right(),
            relu_box.get_left(),
            buff=0.2,
            color=COLORS["text_secondary"],
        )
        arrow2 = Arrow(
            relu_box.get_right(),
            pool_box.get_left(),
            buff=0.2,
            color=COLORS["text_secondary"],
        )

        self.play(
            FadeIn(conv_box),
            FadeIn(conv_text),
            GrowArrow(arrow1),
            FadeIn(relu_box),
            FadeIn(relu_text),
            GrowArrow(arrow2),
            FadeIn(pool_box),
            FadeIn(pool_text),
            run_time=1.8,
        )

        relu_example_title = cn("ReLU 示例", size=22, color=COLORS["relu_red"])
        relu_in = MathTex(
            r"[-2,\ 1,\ -3,\ 4]", font_size=28, color=COLORS["text_primary"]
        )
        relu_arrow = MathTex(
            r"\rightarrow", font_size=38, color=COLORS["text_secondary"]
        )
        relu_out = MathTex(r"[0,\ 1,\ 0,\ 4]", font_size=28, color=COLORS["relu_red"])
        relu_demo = VGroup(relu_in, relu_arrow, relu_out).arrange(RIGHT, buff=0.25)
        relu_group = VGroup(relu_example_title, relu_demo).arrange(DOWN, buff=0.18)

        pool_example_title = cn("最大池化示例", size=22, color=COLORS["pool_green"])
        pool_in = matrix_grid(
            [[1, 3], [2, 5]],
            cell_size=0.52,
            color=COLORS["feature_blue"],
            fill="#17324a",
        )
        pool_out = matrix_grid(
            [[5]],
            cell_size=0.68,
            color=COLORS["pool_green"],
            fill="#173b24",
            text_size=24,
        )
        pool_arrow = MathTex(
            r"\rightarrow", font_size=40, color=COLORS["text_secondary"]
        )
        pool_demo = VGroup(pool_in, pool_arrow, pool_out).arrange(RIGHT, buff=0.4)
        pool_group = VGroup(pool_example_title, pool_demo).arrange(DOWN, buff=0.22)
        examples = VGroup(relu_group, pool_group).arrange(
            RIGHT, buff=1.4, aligned_edge=UP
        )
        examples.move_to(DOWN * 0.55)
        caption = self._caption(
            "ReLU 会把负响应截断成 0，只保留真正被“激活”的模式。",
            "池化则用更少的位置概括更大的区域，让后续层看到更稳健、更紧凑的特征。",
        )

        self.play(FadeIn(examples, shift=UP * 0.2))
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "ReLU 会把负响应截断成零，只保留真正被激活的模式。",
            "池化则用更少的位置概括更大的区域，让后续层看到更稳健、更紧凑的特征。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S6: 层级提特征
    # ----------------------------------------------------------
    def scene_hierarchy(self):
        title = cn("CNN 是如何逐层理解图像的？", size=40, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        layers = VGroup(
            stack_block("浅层\n边缘", COLORS["feature_blue"], width=1.4, height=2.4),
            stack_block("中层\n纹理", COLORS["conv_orange"], width=1.4, height=2.4),
            stack_block("深层\n部件", COLORS["accent_purple"], width=1.4, height=2.4),
            stack_block("输出\n类别", COLORS["pool_green"], width=1.4, height=2.4),
        )
        layers.arrange(RIGHT, buff=0.82)
        layers.scale(0.78)
        layers.move_to(UP * 1.15)

        arrows = VGroup()
        for idx in range(len(layers) - 1):
            arrows.add(
                Arrow(
                    layers[idx].get_right(),
                    layers[idx + 1].get_left(),
                    buff=0.18,
                    color=COLORS["text_secondary"],
                    stroke_width=4,
                )
            )

        self.play(
            LaggedStart(
                *[FadeIn(layer, shift=UP * 0.2) for layer in layers], lag_ratio=0.18
            )
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15))

        caption = self._caption(
            "CNN 的强项不只是“找边缘”，而是能把低级特征不断组合成更高级的语义。",
            "浅层先分辨方向和轮廓，中层组合出纹理与形状，深层再拼成耳朵、车轮这类部件。",
            "最后一层根据这些部件证据，输出对类别的整体判断。",
        )
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.9)
        self._hold(
            "CNN 的强项不只是找边缘，而是能把低级特征不断组合成更高级的语义。",
            "浅层先分辨方向和轮廓，中层组合出纹理与形状，深层再拼成耳朵车轮这类部件。",
            "最后一层根据这些部件证据，输出对类别的整体判断。",
            minimum=7,
            maximum=10,
        )
        self._clear()

    # ----------------------------------------------------------
    # S7: 训练与应用
    # ----------------------------------------------------------
    def scene_training_and_apps(self):
        title = cn("CNN 怎么学会识别？又能做什么？", size=38, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title))

        train_card = glass_card(4.25, 3.45)
        train_title = cn("训练过程", size=24, color=COLORS["soft_yellow"], weight=BOLD)
        train_steps = VGroup(
            cn("1. 输入大量已标注图片", size=18),
            cn("2. 前向传播得到预测", size=18),
            cn("3. 用误差反向更新卷积核", size=18),
        )
        train_steps.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        loss_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=1.55,
            y_length=0.9,
            tips=False,
            axis_config={
                "include_numbers": False,
                "stroke_color": COLORS["border"],
                "stroke_width": 1.2,
            },
        )
        loss_curve = loss_axes.plot(
            lambda x: 2.8 * np.exp(-0.75 * x) + 0.35,
            x_range=[0, 4],
            color=COLORS["soft_yellow"],
        )
        loss_label = cn("误差逐步下降", size=16, color=COLORS["soft_yellow"])
        loss_group = VGroup(loss_label, VGroup(loss_axes, loss_curve)).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT
        )
        train_content = VGroup(train_title, train_steps, loss_group).arrange(
            DOWN, aligned_edge=LEFT, buff=0.26
        )
        train_content.move_to(train_card.get_center())
        train_group = VGroup(train_card, train_content)

        app_card = glass_card(4.25, 3.45)
        app_title = cn("典型应用", size=24, color=COLORS["pool_green"], weight=BOLD)
        apps = VGroup(
            cn("图像分类", size=18),
            cn("目标检测", size=18),
            cn("医学影像分析", size=18),
            cn("自动驾驶感知", size=18),
        )
        apps.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        app_content = VGroup(app_title, apps).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )
        app_content.move_to(app_card.get_center())
        app_group = VGroup(app_card, app_content)

        cards = VGroup(train_group, app_group).arrange(RIGHT, buff=2.0)
        cards.move_to(UP * 0.4)
        caption = self._caption(
            "CNN 的卷积核不是人工手写规则，而是在训练中从数据里学出来的。",
            "当误差持续下降，模型就会越来越擅长把图像转换成适合分类、检测和分析的特征。",
        )

        self.play(
            FadeIn(train_card),
            FadeIn(train_title),
            LaggedStart(
                *[FadeIn(item, shift=UP * 0.15) for item in train_steps], lag_ratio=0.15
            ),
            FadeIn(loss_group, shift=UP * 0.15),
            FadeIn(app_card),
            FadeIn(app_title),
            LaggedStart(
                *[FadeIn(item, shift=UP * 0.15) for item in apps], lag_ratio=0.15
            ),
            run_time=1.8,
        )

        connector = Arrow(
            train_card.get_right(),
            app_card.get_left(),
            buff=0.18,
            color=COLORS["conv_orange"],
            stroke_width=4,
        )
        connector_text = cn("学到的卷积核参数", size=19, color=COLORS["conv_orange"])
        connector_text.next_to(connector, UP, buff=0.12)
        self.play(GrowArrow(connector), FadeIn(connector_text))
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self._hold(
            "CNN 的卷积核不是人工手写规则，而是在训练中从数据里学出来的。",
            "当误差持续下降，模型就会越来越擅长把图像转换成适合分类、检测和分析的特征。",
            minimum=7,
        )
        self._clear()

    # ----------------------------------------------------------
    # S8: 总结
    # ----------------------------------------------------------
    def scene_summary(self):
        title = cn("一句话总结 CNN", size=46, weight=BOLD)
        title.move_to(UP * 2.55)
        self.play(Write(title))

        headline_card = glass_card(10.6, 1.05)
        headline_card.move_to(UP * 1.5)
        headline = cn(
            "CNN 用局部卷积、参数共享和层级组合，把像素逐步变成语义判断。",
            size=24,
            color=COLORS["soft_yellow"],
            weight=BOLD,
        )
        headline.move_to(headline_card.get_center())

        input_card = glass_card(1.85, 1.85).move_to(LEFT * 4.7 + DOWN * 0.05)
        input_img = image_patch(size=4, cell_size=0.22).move_to(input_card.get_center())
        input_label = cn("输入图像", size=18, color=COLORS["feature_blue"])
        input_label.next_to(input_card, DOWN, buff=0.14)

        stages = VGroup(
            stack_block("局部\n感知", COLORS["feature_blue"], width=1.0, height=1.45, layers=3).scale(0.72),
            stack_block("共享\n卷积核", COLORS["conv_orange"], width=1.0, height=1.45, layers=3).scale(0.72),
            stack_block("层级\n组合", COLORS["accent_purple"], width=1.0, height=1.45, layers=3).scale(0.72),
        )
        stages.arrange(RIGHT, buff=0.78)
        stages.move_to(DOWN * 0.05)

        output_card = glass_card(1.85, 1.85).move_to(RIGHT * 4.7 + DOWN * 0.05)
        output_text = cn("猫", size=28, color=COLORS["pool_green"], weight=BOLD)
        output_text.move_to(output_card.get_center())
        output_label = cn("语义判断", size=18, color=COLORS["pool_green"])
        output_label.next_to(output_card, DOWN, buff=0.14)

        arrows = VGroup()
        chain = [input_card, *stages, output_card]
        for left, right in zip(chain, chain[1:]):
            arrows.add(
                Arrow(
                    left.get_right(),
                    right.get_left(),
                    buff=0.15,
                    color=COLORS["text_secondary"],
                    stroke_width=3.6,
                )
            )

        principle_cards = VGroup()
        principle_specs = [
            ("局部感受野", "只看邻近区域", COLORS["feature_blue"]),
            ("参数共享", "同一规则反复用", COLORS["conv_orange"]),
            ("层级表示", "从边缘走向语义", COLORS["accent_purple"]),
        ]
        for idx, (head, desc, color) in enumerate(principle_specs):
            card = glass_card(3.15, 0.92).move_to(RIGHT * (idx * 3.4 - 3.4) + DOWN * 1.5)
            dot = Dot(radius=0.06, color=color)
            head_text = cn(head, size=18, color=color, weight=BOLD)
            top = VGroup(dot, head_text).arrange(RIGHT, buff=0.14)
            desc_text = cn(desc, size=15, color=COLORS["text_secondary"])
            content = VGroup(top, desc_text).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            content.move_to(card.get_center())
            principle_cards.add(VGroup(card, content))

        ending = self._caption(
            "CNN 擅长图像处理，不是因为结构复杂，而是因为它的归纳方式刚好贴合图像本身。",
            "局部、共享、层级，这三件事共同决定了它为什么高效。",
        )

        self.play(
            FadeIn(headline_card),
            FadeIn(headline),
            FadeIn(input_card),
            FadeIn(input_img),
            FadeIn(input_label),
            FadeIn(output_card),
            FadeIn(output_text),
            FadeIn(output_label),
            LaggedStart(
                *[FadeIn(stage, shift=UP * 0.15) for stage in stages], lag_ratio=0.18
            ),
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.14),
            run_time=2.0,
        )
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.12) for card in principle_cards], lag_ratio=0.16
            ),
            run_time=1.2,
        )
        self.play(FadeIn(ending, shift=UP * 0.2))
        self._hold(
            "CNN 用局部卷积、参数共享和层级组合，把像素逐步变成语义判断。",
            "局部感受野，只看一小块，抓住邻近关系。",
            "参数共享，同一个卷积核在整张图上重复使用。",
            "层级表示，从边缘到纹理，再到语义目标。",
            "CNN 擅长图像处理，不是因为结构复杂，而是因为它的归纳方式刚好贴合图像本身。",
            "局部共享层级，这三件事共同决定了它为什么高效。",
            minimum=6,
            maximum=9,
        )
