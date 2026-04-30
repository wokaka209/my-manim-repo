from manim import *

config.pixel_width = 1600
config.pixel_height = 1200
config.frame_width = 12
config.frame_height = 9

COLORS = {
    "bg": "#0d1117",
    "surface": "#161b22",
    "border": "#30363d",
    "text_primary": "#E6EDF3",
    "text_secondary": "#8B949E",
    "input_blue": "#58A6FF",
    "forward_cyan": "#39D2C0",
    "gradient_warm": "#F05032",
    "output_green": "#3FB950",
    "arrow_gray": "#6E7681",
    "neuron_fill": "#1C2333",
}

FONT_CN = "SimSun"
FONT_EN = "Times New Roman"


def cn(text, size=36, color=None, weight=NORMAL, **kwargs):
    return Text(
        text,
        font=FONT_CN,
        font_size=size,
        color=color or COLORS["text_primary"],
        weight=weight,
        **kwargs,
    )


def en(text, size=24, color=None, weight=NORMAL, **kwargs):
    return Text(
        text,
        font=FONT_EN,
        font_size=size,
        color=color or COLORS["text_secondary"],
        weight=weight,
        **kwargs,
    )


def glass_card(width, height, radius=0.18):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=radius,
        fill_color=COLORS["surface"],
        fill_opacity=0.92,
        stroke_color=COLORS["border"],
        stroke_width=1.5,
    )


def neuron(color, radius=0.22):
    return Circle(
        radius=radius,
        fill_color=COLORS["neuron_fill"],
        fill_opacity=0.95,
        stroke_color=color,
        stroke_width=2.5,
    )


def layer(count, color, x_pos, y_offsets):
    nodes = VGroup(*[neuron(color).shift(RIGHT * x_pos + UP * y) for y in y_offsets[:count]])
    return nodes


def connect_layers(left_layer, right_layer):
    lines = VGroup()
    for left in left_layer:
        for right in right_layer:
            lines.add(
                Line(
                    left.get_center(),
                    right.get_center(),
                    stroke_color=COLORS["arrow_gray"],
                    stroke_width=1.6,
                )
            )
    return lines


class BackpropCover(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]

        badge = glass_card(2.9, 0.55, radius=0.14)
        badge_text = cn("神经网络科普", size=22, color=COLORS["text_secondary"])
        badge_group = VGroup(badge, badge_text)
        badge_text.move_to(badge.get_center())
        badge_group.move_to(UP * 3.45)

        title_left = cn("前向传播", size=44, color=COLORS["forward_cyan"], weight=BOLD)
        title_mid = cn("与", size=34, color=COLORS["text_primary"])
        title_right = cn("反向传播", size=44, color=COLORS["gradient_warm"], weight=BOLD)
        title = VGroup(title_left, title_mid, title_right).arrange(RIGHT, buff=0.18)
        title.next_to(badge_group, DOWN, buff=0.28)

        subtitle = cn("神经网络如何学习", size=24, color=COLORS["text_secondary"])
        subtitle.next_to(title, DOWN, buff=0.18)

        input_layer = layer(2, COLORS["input_blue"], -3.25, [0.55, -0.55])
        hidden_layer = layer(3, COLORS["forward_cyan"], 0, [1.0, 0, -1.0])
        output_layer = layer(1, COLORS["output_green"], 3.25, [0])
        links = VGroup(
            connect_layers(input_layer, hidden_layer),
            connect_layers(hidden_layer, output_layer),
        )
        network = VGroup(links, input_layer, hidden_layer, output_layer)
        network.move_to(DOWN * 0.55)

        forward_arrow = Arrow(
            start=LEFT * 4.2 + UP * 0.95,
            end=RIGHT * 4.2 + UP * 0.95,
            buff=0,
            color=COLORS["forward_cyan"],
            stroke_width=4,
            max_tip_length_to_length_ratio=0.06,
        )
        forward_label = cn("前向传播", size=24, color=COLORS["forward_cyan"], weight=BOLD)
        forward_label.next_to(forward_arrow, UP, buff=0.12)

        backprop_arrow = Arrow(
            start=RIGHT * 4.2 + DOWN * 2.55,
            end=LEFT * 4.2 + DOWN * 2.55,
            buff=0,
            color=COLORS["gradient_warm"],
            stroke_width=4,
            max_tip_length_to_length_ratio=0.06,
        )
        backprop_label = cn("反向传播", size=24, color=COLORS["gradient_warm"], weight=BOLD)
        backprop_label.next_to(backprop_arrow, UP, buff=0.12)

        footer_card = glass_card(4.5, 0.8, radius=0.16)
        footer_text = cn("预测  ->  误差  ->  更新权重", size=24, color=COLORS["text_primary"])
        footer = VGroup(footer_card, footer_text)
        footer_text.move_to(footer_card.get_center())
        footer.move_to(DOWN * 3.45)

        self.add(
            badge_group,
            title,
            subtitle,
            network,
            forward_arrow,
            forward_label,
            backprop_arrow,
            backprop_label,
            footer,
        )
