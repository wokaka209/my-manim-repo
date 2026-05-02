from manim import *
from manim import rate_functions
import numpy as np

config.media_width = "100%"

# ─── 全局字体规范 ───
FONT_CN = "SimSun"  # 中文：宋体
FONT_EN = "Times New Roman"  # 英文：新罗马
FONT_MONO = "Monaco"  # 终端等宽字体


def cn_text(text, font_size=24, color=None, weight=NORMAL, **kwargs):
    """中文文字（宋体）"""
    c = color or COLORS["text_primary"]
    return Text(
        text, font_size=font_size, color=c, font=FONT_CN, weight=weight, **kwargs
    )


def en_text(text, font_size=24, color=None, weight=NORMAL, **kwargs):
    """英文文字（Times New Roman）"""
    c = color or COLORS["text_primary"]
    return Text(
        text, font_size=font_size, color=c, font=FONT_EN, weight=weight, **kwargs
    )


def mono_text(text, font_size=16, color=None, weight=NORMAL, **kwargs):
    """等宽字体文字（终端/代码）"""
    c = color or COLORS["text_primary"]
    return Text(
        text, font_size=font_size, color=c, font=FONT_MONO, weight=weight, **kwargs
    )


# ─── 全局配色方案 ───
COLORS = {
    "bg": "#0d1117",  # GitHub Dark 深色背景
    "surface": "#161b22",  # 卡片/面板底色
    "border": "#30363d",  # 边框色
    "git_orange": "#F05032",  # Git Logo 橙
    "add_green": "#3FB950",  # git add 绿
    "commit_purple": "#A371F7",  # git commit 紫
    "push_blue": "#58A6FF",  # push 蓝
    "pull_pink": "#F778BA",  # pull 粉
    "main_blue": "#58A6FF",  # main 分支蓝
    "feature_green": "#3FB950",  # feature 分支绿
    "hotfix_red": "#F85149",  # hotfix 分支红
    "warning_yellow": "#D29922",  # 警告黄
    "text_primary": "#E6EDF3",  # 主文字
    "text_secondary": "#8B949E",  # 次文字
    "terminal_bg": "#0d1117",  # 终端背景
    "terminal_border": "#30363d",
}


def glow_dot(radius=0.08, color=WHITE, glow_radius=0.3):
    """创建带发光效果的圆点"""
    core = Dot(radius=radius, color=color)
    glow = Dot(radius=glow_radius, color=color, fill_opacity=0.15)
    return VGroup(glow, core)


def terminal_window(title_text="$ git", width=10, height=5.5, content_lines=None):
    """创建终端风格的窗口"""
    border = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        color=COLORS["terminal_border"],
        fill_opacity=1,
        fill_color=COLORS["terminal_bg"],
        stroke_width=1.5,
    )

    title_bar = Rectangle(
        width=width,
        height=0.45,
        fill_opacity=1,
        fill_color=COLORS["surface"],
        stroke_width=0,
    )
    title_bar.move_to(border.get_top() + DOWN * 0.225)

    dots = VGroup()
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        d = Circle(radius=0.06, color=c, fill_opacity=1, stroke_width=0)
        dots.add(d)
    dots.arrange(RIGHT, buff=0.12)
    dots.move_to(title_bar.get_left() + RIGHT * 0.35)

    t_text = mono_text(title_text, font_size=14, color=COLORS["text_secondary"])
    t_text.move_to(title_bar)

    return VGroup(border, title_bar, dots, t_text)


class GitVersionControlVideo(Scene):
    def construct(self):
        self.setup_background()
        self.scene_title()
        self.scene_what_is_git()
        self.scene_git_three_areas()
        self.scene_basic_commands()
        self.scene_workflow()
        self.scene_branch_management()
        self.scene_remote_repository()
        self.scene_merge_conflict()
        self.scene_end()

    def setup_background(self):
        self.camera.background_color = COLORS["bg"]

    # ═══════════════════════════════════════
    #  场景一：标题
    # ═══════════════════════════════════════
    def scene_title(self):
        git_circle = Circle(
            radius=1.2, color=COLORS["git_orange"], fill_opacity=0.15, stroke_width=3
        )
        git_icon = en_text("Git", font_size=64, weight=BOLD, color=COLORS["git_orange"])
        git_icon.move_to(git_circle)

        title = cn_text(
            "版本管理", font_size=56, weight=BOLD, color=COLORS["text_primary"]
        )
        title.next_to(git_circle, DOWN, buff=0.8)

        subtitle = cn_text(
            "分布式版本控制系统", font_size=28, color=COLORS["text_secondary"]
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(DrawBorderThenFill(git_circle), run_time=1)
        self.play(Write(git_icon), run_time=0.6)

        title.shift(DOWN * 0.5)
        subtitle.shift(DOWN * 0.5)
        self.play(
            title.animate.move_to(git_circle.get_bottom() + DOWN * 0.8),
            FadeIn(subtitle, shift=UP * 0.3),
            run_time=0.8,
        )

        self.wait(2.5)

        all_objs = VGroup(git_circle, git_icon, title, subtitle)
        self.play(all_objs.animate.shift(UP * 1.5).set_opacity(0), run_time=0.8)
        self.remove(all_objs)
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景二：什么是 Git
    # ═══════════════════════════════════════
    def scene_what_is_git(self):
        title = cn_text(
            "什么是 Git？", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        features = [
            ("追踪每一次修改", COLORS["add_green"]),
            ("支持多人协作开发", COLORS["push_blue"]),
            ("回溯任意历史版本", COLORS["commit_purple"]),
            ("高效管理项目分支", COLORS["hotfix_red"]),
        ]

        cards = VGroup()
        for text, color in features:
            card_bg = RoundedRectangle(
                width=7,
                height=0.75,
                corner_radius=0.12,
                fill_opacity=0.12,
                fill_color=color,
                stroke_color=color,
                stroke_width=1,
                stroke_opacity=0.4,
            )
            accent = Rectangle(
                width=0.08,
                height=0.55,
                fill_opacity=0.9,
                fill_color=color,
                stroke_width=0,
            )
            accent.move_to(card_bg.get_left() + RIGHT * 0.15)

            label = cn_text(text, font_size=26, color=COLORS["text_primary"])
            label.move_to(card_bg.get_center() + RIGHT * 0.2)

            cards.add(VGroup(card_bg, accent, label))

        cards.arrange(DOWN, buff=0.25)
        cards.next_to(title, DOWN, buff=0.8)

        for i, card in enumerate(cards):
            card.shift(RIGHT * 1.5)
            self.play(card.animate.shift(LEFT * 1.5), run_time=0.5, rate_func=smooth)
            self.wait(0.2)

        self.wait(2)

        self.play(
            FadeOut(title, shift=UP * 0.3),
            LaggedStart(*[FadeOut(c, shift=RIGHT * 0.5) for c in cards], lag_ratio=0.1),
            run_time=0.8,
        )
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景三：Git 三大区域
    # ═══════════════════════════════════════
    def scene_git_three_areas(self):
        title = cn_text(
            "Git 的三大区域", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        areas = [
            ("工作区", "Working Directory", "修改文件", COLORS["push_blue"]),
            ("暂存区", "Staging Area", "标记变更", COLORS["warning_yellow"]),
            ("本地仓库", "Local Repository", "永久记录", COLORS["add_green"]),
        ]

        boxes, labels, sub_labels, desc_texts, icons, nums = [], [], [], [], [], []

        for i, (cn, en, desc, color) in enumerate(areas):
            x_offset = (i - 1) * 3.8

            box = RoundedRectangle(
                width=3.2,
                height=3.2,
                corner_radius=0.2,
                fill_opacity=0.08,
                fill_color=color,
                stroke_color=color,
                stroke_width=2,
                stroke_opacity=0.6,
            )
            box.shift(RIGHT * x_offset + DOWN * 0.3)

            num = mono_text(f"0{i+1}", font_size=16, color=color, weight=BOLD)
            num.move_to(box.get_top() + DOWN * 0.3 + LEFT * 0.9)

            cn_label = cn_text(cn, font_size=26, weight=BOLD, color=color)
            cn_label.move_to(box.get_top() + DOWN * 0.7)

            en_label = en_text(en, font_size=14, color=COLORS["text_secondary"])
            en_label.move_to(box.get_top() + DOWN * 1.1)

            desc_text = cn_text(desc, font_size=20, color=COLORS["text_primary"])
            desc_text.move_to(box.get_center() + DOWN * 0.3)

            if i == 0:
                icon = self._create_file_icon(color)
            elif i == 1:
                icon = self._create_staging_icon(color)
            else:
                icon = self._create_repo_icon(color)
            icon.move_to(box.get_bottom() + UP * 0.55)
            icon.scale(0.7)

            boxes.append(box)
            nums.append(num)
            labels.append(cn_label)
            sub_labels.append(en_label)
            desc_texts.append(desc_text)
            icons.append(icon)

            self.play(DrawBorderThenFill(box), run_time=0.5)
            self.play(
                FadeIn(num, shift=DOWN * 0.2),
                FadeIn(cn_label, shift=DOWN * 0.2),
                FadeIn(en_label, shift=DOWN * 0.2),
                run_time=0.3,
            )
            self.wait(0.2)
            self.play(FadeIn(desc_text, shift=UP * 0.2), FadeIn(icon), run_time=0.3)

        # 连接箭头 + 数据流动画
        arrows_data = [
            (boxes[0], boxes[1], "git add", COLORS["add_green"]),
            (boxes[1], boxes[2], "git commit", COLORS["commit_purple"]),
        ]

        arrow_objs, arrow_labels = [], []

        for from_box, to_box, cmd, color in arrows_data:
            arrow = Arrow(
                from_box.get_right() + RIGHT * 0.05,
                to_box.get_left() + LEFT * 0.05,
                buff=0.05,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15,
            )
            label = mono_text(cmd, font_size=22, color=color, weight=BOLD)
            label.next_to(arrow, UP, buff=0.15)

            self.play(GrowArrow(arrow), Write(label), run_time=0.6)

            # 数据流动画
            dot = Dot(radius=0.06, color=color)
            dot.move_to(arrow.get_start())
            self.play(
                dot.animate.move_to(arrow.get_end()), run_time=0.5, rate_func=smooth
            )
            self.remove(dot)

            arrow_objs.append(arrow)
            arrow_labels.append(label)

        self.wait(3)

        all_objects = (
            [title]
            + boxes
            + nums
            + labels
            + sub_labels
            + desc_texts
            + icons
            + arrow_objs
            + arrow_labels
        )
        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.03),
            run_time=0.8,
        )
        self.wait(0.3)

    def _create_file_icon(self, color):
        file_rect = Rectangle(width=0.5, height=0.7, color=color, stroke_width=1.5)
        corner = Polygon(
            file_rect.get_corner(UR) + DOWN * 0.2,
            file_rect.get_corner(UR),
            file_rect.get_corner(UR) + LEFT * 0.2,
            color=color,
            fill_opacity=0.3,
            stroke_width=1,
        )
        return VGroup(file_rect, corner)

    def _create_staging_icon(self, color):
        h_line = Line(LEFT * 0.25, RIGHT * 0.25, color=color, stroke_width=3)
        v_line = Line(UP * 0.25, DOWN * 0.25, color=color, stroke_width=3)
        return VGroup(h_line, v_line)

    def _create_repo_icon(self, color):
        ellipses = []
        for y in [0.2, -0.2]:
            e = Ellipse(width=0.6, height=0.2, color=color, stroke_width=1.5)
            e.shift(DOWN * y)
            ellipses.append(e)
        l_line = Line(
            ellipses[0].get_left(),
            ellipses[1].get_left(),
            color=color,
            stroke_width=1.5,
        )
        r_line = Line(
            ellipses[0].get_right(),
            ellipses[1].get_right(),
            color=color,
            stroke_width=1.5,
        )
        return VGroup(*ellipses, l_line, r_line)

    # ═══════════════════════════════════════
    #  场景四：基本命令（终端风格）
    # ═══════════════════════════════════════
    def scene_basic_commands(self):
        title = cn_text(
            "基本 Git 命令", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        term = terminal_window(width=11, height=6.2)
        term.shift(DOWN * 0.1)

        self.play(
            DrawBorderThenFill(term[0]),
            FadeIn(term[1]),
            FadeIn(term[2]),
            FadeIn(term[3]),
            run_time=0.5,
        )

        commands = [
            ("$ git init", "Initialized empty Git repository", COLORS["add_green"]),
            ("$ git add .", "Changes staged for commit", COLORS["add_green"]),
            (
                "$ git commit -m 'feat: init'",
                "[main 1a2b3c4] feat: init",
                COLORS["commit_purple"],
            ),
            (
                "$ git status",
                "On branch main\nnothing to commit",
                COLORS["warning_yellow"],
            ),
            ("$ git log --oneline", "1a2b3c4 feat: init", COLORS["commit_purple"]),
            ("$ git push origin main", "Everything up-to-date", COLORS["push_blue"]),
        ]

        y_start = term[0].get_top()[1] - 0.8
        all_lines = []

        for i, (cmd, output, color) in enumerate(commands):
            y_pos = y_start - i * 0.85

            cmd_text = mono_text(cmd, font_size=18, color=COLORS["add_green"])
            cmd_text.move_to(LEFT * 3.5 + UP * y_pos)
            all_lines.append(cmd_text)

            self.play(Write(cmd_text, run_time=0.4, rate_func=linear), run_time=0.4)
            self.wait(0.15)

            out_text = en_text(output, font_size=14, color=COLORS["text_secondary"])
            out_text.move_to(LEFT * 3.5 + UP * (y_pos - 0.32))
            all_lines.append(out_text)

            self.play(FadeIn(out_text, shift=DOWN * 0.1), run_time=0.3)
            self.wait(0.3)

        self.wait(2)

        all_objects = [title, term] + all_lines
        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.02),
            run_time=0.8,
        )
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景五：工作流程
    # ═══════════════════════════════════════
    def scene_workflow(self):
        title = cn_text(
            "Git 工作流程", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        steps = [
            ("修改文件", "Edit", COLORS["push_blue"]),
            ("git add", "Stage", COLORS["add_green"]),
            ("git commit", "Commit", COLORS["commit_purple"]),
            ("git push", "Push", COLORS["push_blue"]),
        ]

        step_groups = []
        box_objs = []

        for i, (cn, en, color) in enumerate(steps):
            box = RoundedRectangle(
                width=2.4,
                height=1.2,
                corner_radius=0.6,
                fill_opacity=0.15,
                fill_color=color,
                stroke_color=color,
                stroke_width=2,
            )

            step_num = mono_text(f"0{i+1}", font_size=13, color=color, weight=BOLD)
            step_num.move_to(box.get_top() + DOWN * 0.22)

            cn_t = cn_text(cn, font_size=20, weight=BOLD, color=COLORS["text_primary"])
            cn_t.move_to(box.get_center() + DOWN * 0.05)

            en_t = en_text(en, font_size=12, color=COLORS["text_secondary"])
            en_t.move_to(box.get_bottom() + UP * 0.18)

            group = VGroup(box, step_num, cn_t, en_t)
            step_groups.append(group)
            box_objs.append(box)

        step_vgroup = VGroup(*step_groups)
        step_vgroup.arrange(RIGHT, buff=0.8)
        step_vgroup.next_to(title, DOWN, buff=1.2)

        arrows = []
        for i in range(len(box_objs) - 1):
            arrow = Arrow(
                box_objs[i].get_right() + RIGHT * 0.05,
                box_objs[i + 1].get_left() + LEFT * 0.05,
                buff=0.05,
                color=COLORS["text_secondary"],
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.append(arrow)

        for i, group in enumerate(step_groups):
            group.shift(DOWN * 0.5)
            self.play(group.animate.shift(UP * 0.5), run_time=0.5, rate_func=smooth)
            if i > 0:
                self.play(GrowArrow(arrows[i - 1]), run_time=0.3)
            self.wait(0.3)

        # 循环箭头：从 push 顶部回到修改文件顶部（下方弧线，镜像对称）
        loop_arrow = CurvedArrow(
            box_objs[-1].get_bottom() + DOWN * 0.22,
            box_objs[0].get_bottom() + DOWN * 0.22,
            color=COLORS["warning_yellow"],
            stroke_width=2,
            angle=-TAU / 4,
        )
        loop_label = cn_text("持续循环", font_size=16, color=COLORS["warning_yellow"])
        loop_label.next_to(loop_arrow, UP, buff=0.15)

        self.play(Create(loop_arrow), FadeIn(loop_label, shift=UP * 0.2), run_time=0.6)

        self.wait(2.5)

        all_objects = [title] + step_groups + arrows + [loop_arrow, loop_label]
        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.03),
            run_time=0.8,
        )
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景六：分支管理
    # ═══════════════════════════════════════
    def scene_branch_management(self):
        title = cn_text(
            "Git 分支管理", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        main_line = Line(
            LEFT * 5.5, RIGHT * 5.5, color=COLORS["main_blue"], stroke_width=4
        )
        main_line.shift(DOWN * 0.5)
        main_label = en_text(
            "main", font_size=20, color=COLORS["main_blue"], weight=BOLD
        )
        main_label.next_to(main_line, DOWN, buff=0.25)
        main_label.align_to(main_line, LEFT)

        self.play(Create(main_line), Write(main_label), run_time=0.6)

        commit_positions = {
            "C0": LEFT * 4.5 + DOWN * 0.5,
            "C1": LEFT * 2.5 + DOWN * 0.5,
            "C2": LEFT * 0.5 + DOWN * 0.5,
            "C3": UP * 1.2 + LEFT * 1.2,
            "C4": RIGHT * 2 + DOWN * 0.5,
            "C5": RIGHT * 4.5 + DOWN * 0.5,
            "C6": UP * 1.2 + RIGHT * 3,
        }

        commit_colors = {
            "C0": COLORS["main_blue"],
            "C1": COLORS["main_blue"],
            "C2": COLORS["main_blue"],
            "C3": COLORS["feature_green"],
            "C4": COLORS["main_blue"],
            "C5": COLORS["main_blue"],
            "C6": COLORS["hotfix_red"],
        }

        connections = [
            ("C0", "C1", COLORS["main_blue"], False),
            ("C1", "C2", COLORS["main_blue"], False),
            ("C2", "C3", COLORS["feature_green"], True),
            ("C2", "C4", COLORS["main_blue"], False),
            ("C4", "C5", COLORS["main_blue"], False),
            ("C4", "C6", COLORS["hotfix_red"], True),
        ]

        commit_order = ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]
        commit_objs = {}

        for cid in commit_order:
            pos = commit_positions[cid]
            color = commit_colors[cid]
            dot_glow = glow_dot(radius=0.1, color=color, glow_radius=0.35)
            dot_glow.move_to(pos)
            label = mono_text(cid, font_size=13, color=color, weight=BOLD)
            label.next_to(dot_glow, DOWN, buff=0.15)

            commit_objs[cid] = (dot_glow, label)

            self.play(FadeIn(dot_glow, shift=UP * 0.2), Write(label), run_time=0.3)
            self.wait(0.1)

        branch_lines = []
        for from_id, to_id, color, is_curved in connections:
            start = commit_positions[from_id]
            end = commit_positions[to_id]

            if is_curved:
                line = CurvedArrow(
                    start + UP * 0.15,
                    end + DOWN * 0.15,
                    color=color,
                    stroke_width=2.5,
                    angle=-TAU / 6,
                    tip_length=0.15,
                )
            else:
                line = Arrow(
                    start + RIGHT * 0.2,
                    end + LEFT * 0.2,
                    color=color,
                    stroke_width=2.5,
                    buff=0.1,
                    max_tip_length_to_length_ratio=0.15,
                )

            branch_lines.append(line)
            self.play(Create(line), run_time=0.3)

        feature_label = en_text(
            "feature", font_size=16, color=COLORS["feature_green"], weight=BOLD
        )
        feature_label.next_to(commit_positions["C3"], UP, buff=0.3)
        hotfix_label = en_text(
            "hotfix", font_size=16, color=COLORS["hotfix_red"], weight=BOLD
        )
        hotfix_label.next_to(commit_positions["C6"], UP, buff=0.3)

        self.play(Write(feature_label), Write(hotfix_label), run_time=0.4)

        head_arrow = Arrow(
            commit_positions["C5"] + DOWN * 1.2,
            commit_positions["C5"] + DOWN * 0.2,
            color=COLORS["warning_yellow"],
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )
        head_label = en_text(
            "HEAD", font_size=16, color=COLORS["warning_yellow"], weight=BOLD
        )
        head_label.next_to(head_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(head_arrow), Write(head_label), run_time=0.5)

        cmd_texts_data = [
            ("git branch feature", "创建分支", COLORS["feature_green"]),
            ("git checkout feature", "切换分支", COLORS["push_blue"]),
            ("git merge hotfix", "合并分支", COLORS["hotfix_red"]),
        ]

        cmd_group = VGroup()
        for cmd, desc, color in cmd_texts_data:
            cmd_text = mono_text(f"$ {cmd}", font_size=16, color=COLORS["add_green"])
            desc_text = cn_text(
                f"# {desc}", font_size=14, color=COLORS["text_secondary"]
            )
            row = VGroup(cmd_text, desc_text).arrange(RIGHT, buff=0.3)
            cmd_group.add(row)

        cmd_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cmd_group.to_edge(DOWN, buff=0.5)
        cmd_group.align_to(LEFT * 3)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=RIGHT * 0.3) for c in cmd_group], lag_ratio=0.2
            ),
            run_time=0.8,
        )

        self.wait(2.5)

        all_objects = [
            title,
            main_line,
            main_label,
            feature_label,
            hotfix_label,
            head_arrow,
            head_label,
        ]
        all_objects += [obj for cid in commit_objs for obj in commit_objs[cid]]
        all_objects += branch_lines
        all_objects += list(cmd_group)

        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.02),
            run_time=0.8,
        )
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景七：远程仓库
    # ═══════════════════════════════════════
    def scene_remote_repository(self):
        title = cn_text(
            "远程仓库协作", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        local_box = RoundedRectangle(
            width=3.5,
            height=3,
            corner_radius=0.2,
            fill_opacity=0.08,
            fill_color=COLORS["add_green"],
            stroke_color=COLORS["add_green"],
            stroke_width=2,
        )
        local_box.shift(LEFT * 3.5 + DOWN * 0.3)

        local_icon = self._create_computer_icon(COLORS["add_green"])
        local_icon.move_to(local_box.get_top() + DOWN * 0.7)
        local_icon.scale(0.8)

        local_label = cn_text(
            "本地仓库", font_size=24, weight=BOLD, color=COLORS["add_green"]
        )
        local_label.move_to(local_box.get_bottom() + UP * 0.6)

        remote_box = RoundedRectangle(
            width=3.5,
            height=3,
            corner_radius=0.2,
            fill_opacity=0.08,
            fill_color=COLORS["push_blue"],
            stroke_color=COLORS["push_blue"],
            stroke_width=2,
        )
        remote_box.shift(RIGHT * 3.5 + DOWN * 0.3)

        remote_icon = self._create_cloud_icon(COLORS["push_blue"])
        remote_icon.move_to(remote_box.get_top() + DOWN * 0.7)
        remote_icon.scale(0.8)

        remote_label = cn_text(
            "远程仓库", font_size=24, weight=BOLD, color=COLORS["push_blue"]
        )
        remote_label.move_to(remote_box.get_bottom() + UP * 0.6)

        self.play(
            DrawBorderThenFill(local_box),
            FadeIn(local_icon, shift=DOWN * 0.2),
            Write(local_label),
            run_time=0.6,
        )
        self.play(
            DrawBorderThenFill(remote_box),
            FadeIn(remote_icon, shift=DOWN * 0.2),
            Write(remote_label),
            run_time=0.6,
        )

        push_arrow = Arrow(
            local_box.get_right() + UP * 0.4,
            remote_box.get_left() + UP * 0.4,
            buff=0.15,
            color=COLORS["push_blue"],
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        push_label = mono_text(
            "git push", font_size=20, color=COLORS["push_blue"], weight=BOLD
        )
        push_label.next_to(push_arrow, UP, buff=0.15)

        pull_arrow = Arrow(
            remote_box.get_left() + DOWN * 0.4,
            local_box.get_right() + DOWN * 0.4,
            buff=0.15,
            color=COLORS["pull_pink"],
            stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        pull_label = mono_text(
            "git pull", font_size=20, color=COLORS["pull_pink"], weight=BOLD
        )
        pull_label.next_to(pull_arrow, DOWN, buff=0.15)

        self.play(GrowArrow(push_arrow), Write(push_label), run_time=0.5)

        for _ in range(3):
            data_dot = Dot(radius=0.06, color=COLORS["push_blue"])
            data_dot.move_to(push_arrow.get_start())
            self.play(
                data_dot.animate.move_to(push_arrow.get_end()),
                run_time=0.4,
                rate_func=smooth,
            )
            self.remove(data_dot)

        self.play(GrowArrow(pull_arrow), Write(pull_label), run_time=0.5)

        for _ in range(3):
            data_dot = Dot(radius=0.06, color=COLORS["pull_pink"])
            data_dot.move_to(pull_arrow.get_start())
            self.play(
                data_dot.animate.move_to(pull_arrow.get_end()),
                run_time=0.4,
                rate_func=smooth,
            )
            self.remove(data_dot)

        explanation = VGroup(
            cn_text(
                "push: 推送本地提交到远程", font_size=20, color=COLORS["push_blue"]
            ),
            cn_text(
                "pull: 拉取远程更新到本地", font_size=20, color=COLORS["pull_pink"]
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=0.5)

        self.wait(3)

        all_objects = [
            title,
            local_box,
            local_icon,
            local_label,
            remote_box,
            remote_icon,
            remote_label,
            push_arrow,
            push_label,
            pull_arrow,
            pull_label,
            explanation,
        ]
        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.03),
            run_time=0.8,
        )
        self.wait(0.3)

    def _create_computer_icon(self, color):
        screen = Rectangle(width=0.9, height=0.6, color=color, stroke_width=2)
        stand = Line(
            screen.get_bottom(),
            screen.get_bottom() + DOWN * 0.2,
            color=color,
            stroke_width=2,
        )
        base = Line(
            screen.get_bottom() + DOWN * 0.2 + LEFT * 0.25,
            screen.get_bottom() + DOWN * 0.2 + RIGHT * 0.25,
            color=color,
            stroke_width=2,
        )
        return VGroup(screen, stand, base)

    def _create_cloud_icon(self, color):
        circles = VGroup()
        for pos in [LEFT * 0.25, RIGHT * 0.25, UP * 0.15]:
            c = Circle(radius=0.25, color=color, fill_opacity=0.15, stroke_width=1.5)
            c.shift(pos)
            circles.add(c)
        return circles

    # ═══════════════════════════════════════
    #  场景八：合并冲突
    # ═══════════════════════════════════════
    def scene_merge_conflict(self):
        title = cn_text(
            "合并与冲突", font_size=44, weight=BOLD, color=COLORS["text_primary"]
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6)

        branch1 = Line(
            LEFT * 4.5 + UP * 1,
            RIGHT * 0.5 + UP * 1,
            color=COLORS["main_blue"],
            stroke_width=3,
        )
        branch2 = Line(
            LEFT * 4.5 + DOWN * 1,
            RIGHT * 0.5 + DOWN * 1,
            color=COLORS["feature_green"],
            stroke_width=3,
        )

        b1_label = en_text("main", font_size=16, color=COLORS["main_blue"])
        b1_label.next_to(branch1, LEFT, buff=0.2)
        b2_label = en_text("feature", font_size=16, color=COLORS["feature_green"])
        b2_label.next_to(branch2, LEFT, buff=0.2)

        c_main_1 = glow_dot(0.1, COLORS["main_blue"], 0.3).move_to(LEFT * 3 + UP * 1)
        c_main_2 = glow_dot(0.1, COLORS["main_blue"], 0.3).move_to(LEFT * 1 + UP * 1)
        c_feat_1 = glow_dot(0.1, COLORS["feature_green"], 0.3).move_to(
            LEFT * 3 + DOWN * 1
        )
        c_feat_2 = glow_dot(0.1, COLORS["feature_green"], 0.3).move_to(
            LEFT * 1 + DOWN * 1
        )

        merge_pos = RIGHT * 2
        merge_ring = Circle(
            radius=0.22,
            color=COLORS["hotfix_red"],
            stroke_width=3,
            fill_opacity=0.2,
            fill_color=COLORS["hotfix_red"],
        )
        merge_ring.move_to(merge_pos)
        merge_label = en_text(
            "Merge", font_size=14, color=COLORS["hotfix_red"], weight=BOLD
        )
        merge_label.next_to(merge_ring, UP, buff=0.2)

        merge_line1 = CurvedArrow(
            LEFT * 1 + UP * 1,
            merge_pos + LEFT * 0.15,
            color=COLORS["main_blue"],
            stroke_width=2,
            angle=-TAU / 6,
            tip_length=0.12,
        )
        merge_line2 = CurvedArrow(
            LEFT * 1 + DOWN * 1,
            merge_pos + LEFT * 0.15,
            color=COLORS["feature_green"],
            stroke_width=2,
            angle=TAU / 6,
            tip_length=0.12,
        )

        self.play(
            Create(branch1),
            Create(branch2),
            Write(b1_label),
            Write(b2_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(c_main_1),
            FadeIn(c_main_2),
            FadeIn(c_feat_1),
            FadeIn(c_feat_2),
            run_time=0.4,
        )
        self.play(Create(merge_line1), Create(merge_line2), run_time=0.5)
        self.play(DrawBorderThenFill(merge_ring), Write(merge_label), run_time=0.4)

        for _ in range(3):
            self.play(merge_ring.animate.set_fill(opacity=0.5), run_time=0.2)
            self.play(merge_ring.animate.set_fill(opacity=0.15), run_time=0.2)

        conflict_code = VGroup(
            mono_text("<<<<<<< HEAD", font_size=16, color=COLORS["hotfix_red"]),
            en_text(
                'print("Hello from main")', font_size=16, color=COLORS["main_blue"]
            ),
            mono_text("=======", font_size=16, color=COLORS["warning_yellow"]),
            en_text(
                'print("Hello from feature")',
                font_size=16,
                color=COLORS["feature_green"],
            ),
            mono_text(">>>>>>> feature", font_size=16, color=COLORS["hotfix_red"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        code_panel = RoundedRectangle(
            width=5.5,
            height=2.8,
            corner_radius=0.15,
            fill_opacity=0.9,
            fill_color=COLORS["terminal_bg"],
            stroke_color=COLORS["hotfix_red"],
            stroke_width=1.5,
        )
        code_panel.to_edge(DOWN, buff=0.5)
        code_panel.shift(RIGHT * 1.5)
        conflict_code.move_to(code_panel.get_center())

        self.play(DrawBorderThenFill(code_panel), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 0.2) for line in conflict_code],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )

        resolve_text = cn_text(
            "→ 手动解决冲突后 git add + git commit",
            font_size=18,
            color=COLORS["add_green"],
        )
        resolve_text.next_to(code_panel, DOWN, buff=0.2)
        self.play(FadeIn(resolve_text, shift=UP * 0.2), run_time=0.4)

        self.wait(3)

        all_objects = [
            title,
            branch1,
            branch2,
            b1_label,
            b2_label,
            c_main_1,
            c_main_2,
            c_feat_1,
            c_feat_2,
            merge_line1,
            merge_line2,
            merge_ring,
            merge_label,
            code_panel,
            resolve_text,
        ] + list(conflict_code)

        self.play(
            LaggedStart(*[FadeOut(o) for o in all_objects], lag_ratio=0.02),
            run_time=0.8,
        )
        self.wait(0.3)

    # ═══════════════════════════════════════
    #  场景九：优美总结
    # ═══════════════════════════════════════
    def scene_end(self):
        # ── 布局说明 ──
        # Manim 默认画幅 ≈ ±4.0 (高) × ±7.1 (宽)
        # Logo 偏上 (y=1.8)，轨道半径 2.3，卡片 2.2×1.1
        # 最远卡片中心: 1.8+2.3=4.1 → 卡片边缘 4.1+0.55=4.65（超出）
        # 改用椭圆轨道：水平半径 2.8, 垂直半径 1.9，保证所有内容在画幅内

        logo_center = UP * 1.6

        # ── 中心 Git logo（双层光晕） ──
        git_glow = Circle(
            radius=1.15, color=COLORS["git_orange"], fill_opacity=0.03, stroke_width=0
        )
        git_glow.move_to(logo_center)
        git_outer = Circle(
            radius=0.9, color=COLORS["git_orange"], fill_opacity=0.1, stroke_width=2.5
        )
        git_outer.move_to(logo_center)
        git_inner = Circle(
            radius=0.65, color=COLORS["git_orange"], fill_opacity=0.05, stroke_width=1
        )
        git_inner.move_to(logo_center)
        git_text_obj = en_text(
            "Git", font_size=48, weight=BOLD, color=COLORS["git_orange"]
        )
        git_text_obj.move_to(logo_center)

        self.play(
            FadeIn(git_glow),
            DrawBorderThenFill(git_outer),
            DrawBorderThenFill(git_inner),
            run_time=0.6,
        )
        self.play(Write(git_text_obj), run_time=0.4)

        # ── 六角形知识点环绕（椭圆轨道） ──
        summary_items = [
            ("三大区域", "Working → Staging → Repo", COLORS["push_blue"]),
            ("基本命令", "init / add / commit / push", COLORS["add_green"]),
            ("分支管理", "branch / checkout / merge", COLORS["feature_green"]),
            ("远程协作", "push / pull / fetch", COLORS["commit_purple"]),
            ("冲突解决", "resolve conflict", COLORS["hotfix_red"]),
            ("持续循环", "Edit → Stage → Commit → Push", COLORS["warning_yellow"]),
        ]

        n = len(summary_items)
        orbit_rx = 2.8  # 水平轨道半径
        orbit_ry = 1.7  # 垂直轨道半径
        card_w, card_h = 2.2, 1.05

        card_groups = []

        for i, (cn, en, color) in enumerate(summary_items):
            angle = -PI / 2 + i * TAU / n  # 从顶部开始顺时针
            pos = np.array(
                [
                    orbit_rx * np.cos(angle),
                    orbit_ry * np.sin(angle) + logo_center[1],
                    0,
                ]
            )

            # 连接线：从 logo 外缘到卡片内侧
            line_start = logo_center + np.array(
                [0.95 * np.cos(angle), 0.95 * np.sin(angle), 0]
            )
            card_inner_offset = np.array(
                [
                    -(card_w / 2 + 0.15) * np.cos(angle),
                    -(card_h / 2 + 0.15) * np.sin(angle),
                    0,
                ]
            )
            line_end = pos + card_inner_offset
            line = Line(
                line_start, line_end, color=color, stroke_width=1.5, stroke_opacity=0.35
            )

            # 小卡片
            card = RoundedRectangle(
                width=card_w,
                height=card_h,
                corner_radius=0.12,
                fill_opacity=0.12,
                fill_color=color,
                stroke_color=color,
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            card.move_to(pos)

            cn_t = cn_text(cn, font_size=18, weight=BOLD, color=color)
            cn_t.move_to(card.get_center() + UP * 0.15)

            en_t = en_text(en, font_size=10, color=COLORS["text_secondary"])
            en_t.move_to(card.get_center() + DOWN * 0.22)

            group = VGroup(line, card, cn_t, en_t)
            card_groups.append(group)

        # 逐个入场：从中心方向滑入
        for i, group in enumerate(card_groups):
            angle = -PI / 2 + i * TAU / n
            slide_dir = np.array([np.cos(angle), np.sin(angle), 0])
            group.shift(-slide_dir * 0.8)
            self.play(
                group.animate.shift(slide_dir * 0.8),
                FadeIn(group, shift=slide_dir * 0.3),
                run_time=0.5,
                rate_func=smooth,
            )
            self.wait(0.1)

        self.wait(1.2)

        # ── 底部感谢语 ──
        thank_y = DOWN * 3.0
        left_line = Line(
            LEFT * 5.0,
            LEFT * 1.8,
            color=COLORS["git_orange"],
            stroke_width=1.5,
            stroke_opacity=0.4,
        )
        right_line = Line(
            RIGHT * 1.8,
            RIGHT * 5.0,
            color=COLORS["git_orange"],
            stroke_width=1.5,
            stroke_opacity=0.4,
        )
        left_line.move_to(thank_y)
        right_line.move_to(thank_y)

        self.play(Create(left_line), Create(right_line), run_time=0.5)

        # 中文感谢语：弹性缩放入场
        thank_cn = cn_text(
            "感谢观看", font_size=36, weight=BOLD, color=COLORS["git_orange"]
        )
        thank_cn.move_to(thank_y)
        thank_cn_saved_center = thank_cn.get_center()
        thank_cn.scale(0).move_to(thank_cn_saved_center)
        self.play(
            thank_cn.animate.scale(1).move_to(thank_cn_saved_center),
            run_time=0.6,
            rate_func=smooth,
        )

        # 英文感谢语：淡入
        thank_en = en_text("Thank You", font_size=18, color=COLORS["text_secondary"])
        thank_en.next_to(thank_cn, DOWN, buff=0.15)
        self.play(FadeIn(thank_en, shift=UP * 0.2), run_time=0.3)

        self.wait(4)

        # ── 整体优雅退场 ──
        all_end = [
            git_glow,
            git_outer,
            git_inner,
            git_text_obj,
            left_line,
            right_line,
            thank_cn,
            thank_en,
        ] + card_groups
        self.play(
            LaggedStart(*[FadeOut(o) for o in all_end], lag_ratio=0.05),
            run_time=1.2,
        )


if __name__ == "__main__":
    from manim import *

    config.quality = "fourk_quality"  # 最高画质：3840x2160 (4K)
    config.preview = True
