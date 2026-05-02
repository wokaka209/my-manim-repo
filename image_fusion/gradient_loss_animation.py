from manim import *



config.background_color = "#1a1a2e"

config.quality = "medium_quality"

config.pixel_height = 720

config.pixel_width = 1280



class TitleScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("方向感知的多尺度梯度损失", font_size=44, color=WHITE)
        subtitle = Text("Direction-aware Multi-scale Gradient Loss", font_size=22, color=LIGHT_GRAY)
        author = Text("红外-可见光图像融合", font_size=20, color=BLUE_B)

        title.move_to(UP * 1.0)
        subtitle.next_to(title, DOWN, buff=0.8)
        author.next_to(subtitle, DOWN, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.wait(0.3)
        self.play(Write(subtitle), run_time=1)
        self.wait(0.3)
        self.play(Write(author), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(author))



class ProblemScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("核心问题", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        defect1 = Text("缺陷1: 只关注梯度幅值，忽略方向信息", font_size=22, color=WHITE, font="Microsoft YaHei UI")
        defect1.next_to(title, DOWN, buff=0.5)

        defect2 = Text("缺陷2: 梯度方向冲突导致相互削弱", font_size=22, color=WHITE, font="Microsoft YaHei UI")
        defect2.next_to(defect1, DOWN, buff=0.25)

        self.play(Write(defect1), run_time=0.8)
        self.play(Write(defect2), run_time=0.8)
        self.wait(0.5)

        traditional_label = Text("传统方法:", font_size=22, color=YELLOW, font="Microsoft YaHei UI")
        traditional_label.move_to(LEFT * 1.5 + DOWN * 1.5)

        formula = MathTex(r"\nabla I = |\nabla_x I| + |\nabla_y I|", font_size=26, color=YELLOW)
        formula.next_to(traditional_label, RIGHT, buff=0.15)

        self.play(Write(traditional_label), Write(formula))
        self.wait(0.5)

        example_text = Text("当两个方向符号相反时发生破坏性干扰", font_size=20, color=ORANGE, font="Microsoft YaHei UI")
        example_text.move_to(DOWN * 2.5)
        self.play(Write(example_text))
        self.wait(2)

        all_elements = [title, defect1, defect2, traditional_label, formula, example_text]
        self.play(FadeOut(*all_elements))



class InnovationScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("核心创新", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        innovation_text = Text("方向感知的多尺度梯度损失", font_size=28, color=GREEN, font="Microsoft YaHei UI")
        innovation_text.move_to(UP * 2.2)
        self.play(Write(innovation_text))
        self.wait(0.5)

        points = VGroup()

        point1 = Text("✓ 分别独立监督水平和垂直分量", font_size=20, color=WHITE, font="Microsoft YaHei UI")
        point2 = Text("✓ 保持梯度的符号 (±)", font_size=20, color=WHITE, font="Microsoft YaHei UI")
        point3 = Text("✓ 多尺度聚合 (细粒度 + 粗粒度)", font_size=20, color=WHITE, font="Microsoft YaHei UI")

        points.add(point1, point2, point3)
        points.arrange(DOWN, buff=0.35)
        points.move_to(UP * 0.8)
        self.play(Write(points), run_time=1.5)
        self.wait(0.5)

        formula = MathTex(r"(\nabla_x, \nabla_y)", font_size=30, color=BLUE_B)
        supervise = Text("分别监督", font_size=20, color=BLUE_B, font="Microsoft YaHei UI")

        formula_group = VGroup(formula, supervise)
        formula_group.arrange(RIGHT, buff=0.3)
        formula_group.move_to(DOWN * 2.2)
        self.play(Write(formula_group))
        self.wait(2)

        all_elements = [title, innovation_text, points, formula_group]
        self.play(FadeOut(*all_elements))



class SobelOperatorScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("Sobel算子", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        kx_label = Text("水平梯度核 Kx", font_size=20, color=BLUE_B, font="Microsoft YaHei UI")
        kx_label.move_to(LEFT * 2 + UP * 1.8)

        kx_matrix = Matrix([["-1", "0", "+1"], ["-2", "0", "+2"], ["-1", "0", "+1"]],
                           element_alignment_corner=LEFT)
        kx_matrix.scale(0.65)
        kx_matrix.next_to(kx_label, DOWN, buff=0.2)

        ky_label = Text("垂直梯度核 Ky", font_size=20, color=ORANGE, font="Microsoft YaHei UI")
        ky_label.move_to(RIGHT * 2 + UP * 1.8)

        ky_matrix = Matrix([["-1", "-2", "-1"], ["0", "0", "0"], ["+1", "+2", "+1"]],
                          element_alignment_corner=LEFT)
        ky_matrix.scale(0.65)
        ky_matrix.next_to(ky_label, DOWN, buff=0.2)

        self.play(Write(kx_label), Write(kx_matrix), Write(ky_label), Write(ky_matrix))
        self.wait(0.5)

        result_label = Text("计算示例: 3×3像素区域", font_size=18, color=YELLOW, font="Microsoft YaHei UI")
        result_label.move_to(LEFT * 2 + DOWN * 1.5)
        self.play(Write(result_label))

        pixel_grid = VGroup()
        for i in range(3):
            for j in range(3):
                rect = Square(side_length=0.5, color=WHITE, fill_opacity=0.3)
                x_pos = -2 + i * 0.6 - 0.6
                y_pos = -1.5 + (2-j) * 0.6
                rect.move_to(np.array([x_pos, y_pos, 0]))
                if j == 0:
                    num = Text("0", font_size=16, color=WHITE)
                elif j == 1:
                    num = Text("10", font_size=16, color=WHITE)
                else:
                    num = Text("20", font_size=16, color=WHITE)
                num.move_to(rect.get_center())
                pixel_grid.add(rect, num)
        self.play(Create(pixel_grid))
        self.wait(0.5)

        result_x = MathTex(r"G_x = 80", font_size=26, color=BLUE_B)
        result_x.move_to(RIGHT * 2 + UP * 1.5)

        result_y = MathTex(r"G_y = 80", font_size=26, color=ORANGE)
        result_y.next_to(result_x, DOWN, buff=0.25)
        self.play(Write(result_x), Write(result_y))
        self.wait(2)

        all_elements = [title, kx_label, kx_matrix, ky_label, ky_matrix, result_label, pixel_grid, result_x, result_y]
        self.play(FadeOut(*all_elements))



class MultiScaleScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("多尺度图像采样", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        scales = [1.0, 0.5, 0.25]
        scale_names = ["尺度 1.0", "尺度 0.5", "尺度 0.25"]
        scale_colors = [BLUE_B, GREEN, ORANGE]
        scale_positions = [LEFT * 2.8, ORIGIN, RIGHT * 2.8]

        scale_images = []
        for i, (scale, name, color, pos) in enumerate(zip(scales, scale_names, scale_colors, scale_positions)):

            box = RoundedRectangle(width=1.8 * 1.2, height=1.2 * 1.2,
                                corner_radius=0.1, color=color, stroke_width=2)
            box.move_to(pos)

            label = Text(name, font_size=18, color=color, font="Microsoft YaHei UI")
            label.next_to(box, DOWN, buff=0.12)

            scale_text = Text(f"{int(480*scale)}×{int(640*scale)}", font_size=12, color=LIGHT_GRAY, font="Microsoft YaHei UI")
            scale_text.next_to(label, DOWN, buff=0.05)

            if scale == 1.0:
                desc = "边缘锐利"
            elif scale == 0.5:
                desc = "中等结构"
            else:
                desc = "整体结构"

            desc_text = Text(desc, font_size=12, color=LIGHT_GRAY, font="Microsoft YaHei UI")
            desc_text.next_to(scale_text, DOWN, buff=0.05)

            self.play(Create(box), Write(label), Write(scale_text), Write(desc_text), run_time=0.4)
            scale_images.extend([box, label, scale_text, desc_text])
            self.wait(0.2)

        self.wait(0.5)

        formula = MathTex(r"I_f^s = R_s(I_f)", font_size=26, color=YELLOW)
        formula.move_to(DOWN * 2.5)
        self.play(Write(formula))
        self.wait(2)

        all_elements = [title] + scale_images + [formula]
        self.play(FadeOut(*all_elements))



class AxisWiseGatingScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("轴向独立选择主导模态", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        vis_label = Text("可见光梯度", font_size=22, color=BLUE_B, font="Microsoft YaHei UI")
        vis_label.move_to(LEFT * 1.5 + UP * 1.8)

        ir_label = Text("红外梯度", font_size=22, color=RED_C, font="Microsoft YaHei UI")
        ir_label.move_to(RIGHT * 1.5 + UP * 1.8)

        self.play(Write(vis_label), Write(ir_label))
        self.wait(0.3)

        vis_grad_x = MathTex(r"\nabla vis_x", font_size=22, color=BLUE_B)
        vis_grad_x.move_to(LEFT * 1.5 + UP * 1.2)

        vis_grad_y = MathTex(r"\nabla vis_y", font_size=22, color=BLUE_B)
        vis_grad_y.next_to(vis_grad_x, DOWN, buff=0.2)

        ir_grad_x = MathTex(r"\nabla ir_x", font_size=22, color=RED_C)
        ir_grad_x.move_to(RIGHT * 1.5 + UP * 1.2)

        ir_grad_y = MathTex(r"\nabla ir_y", font_size=22, color=RED_C)
        ir_grad_y.next_to(ir_grad_x, DOWN, buff=0.2)

        self.play(Write(vis_grad_x), Write(vis_grad_y), Write(ir_grad_x), Write(ir_grad_y))
        self.wait(0.5)

        gating_x = MathTex(r"M_x", font_size=22, color=YELLOW)
        gating_x.move_to(ORIGIN + UP * 1.2)

        gating_y = MathTex(r"M_y", font_size=22, color=YELLOW)
        gating_y.next_to(gating_x, DOWN, buff=0.2)

        gating_desc = Text("选择门控", font_size=16, color=YELLOW, font="Microsoft YaHei UI")
        gating_desc.next_to(gating_x, RIGHT, buff=0.4)

        self.play(Write(gating_x), Write(gating_y), Write(gating_desc))
        self.wait(0.5)

        sel_x = MathTex(r"\nabla sel_x", font_size=20, color=GREEN)
        sel_x.move_to(DOWN * 0.8)

        sel_y = MathTex(r"\nabla sel_y", font_size=20, color=GREEN)
        sel_y.next_to(sel_x, DOWN, buff=0.2)

        sel_label = Text("选择结果", font_size=16, color=GREEN, font="Microsoft YaHei UI")
        sel_label.next_to(sel_x, RIGHT, buff=0.4)

        self.play(Write(sel_x), Write(sel_y), Write(sel_label))
        self.wait(2)

        note = Text("关键: x和y方向可独立选择不同模态", font_size=18, color=ORANGE, font="Microsoft YaHei UI")
        note.move_to(DOWN * 2.8)
        self.play(Write(note))
        self.wait(2)

        all_elements = [title, vis_label, ir_label, vis_grad_x, vis_grad_y, ir_grad_x, ir_grad_y,
                       gating_x, gating_y, gating_desc, sel_x, sel_y, sel_label, note]
        self.play(FadeOut(*all_elements))



class L1LossScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("L1距离损失", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        l1_formula = MathTex(r"L_1(a, b) = |a - b|", font_size=34, color=YELLOW)
        l1_formula.move_to(UP * 2.2)
        self.play(Write(l1_formula))
        self.wait(0.5)

        example_label = Text("计算示例", font_size=20, color=BLUE_B, font="Microsoft YaHei UI")
        example_label.next_to(l1_formula, DOWN, buff=0.5)

        pred_label = Text("预测: [1, 2, -3]", font_size=18, color=WHITE, font="Microsoft YaHei UI")
        pred_label.next_to(example_label, DOWN, buff=0.2)

        target_label = Text("目标: [2, 1, -2]", font_size=18, color=WHITE, font="Microsoft YaHei UI")
        target_label.next_to(pred_label, DOWN, buff=0.15)

        self.play(Write(example_label), Write(pred_label), Write(target_label))
        self.wait(0.3)

        diff_label = Text("差值绝对值: [1, 1, 1]", font_size=18, color=ORANGE, font="Microsoft YaHei UI")
        diff_label.next_to(target_label, DOWN, buff=0.2)
        self.play(Write(diff_label))
        self.wait(0.3)

        mae_text = Text("MAE = (1+1+1) / 3 = 1.0", font_size=22, color=GREEN, font="Microsoft YaHei UI")
        mae_text.next_to(diff_label, DOWN, buff=0.3)
        self.play(Write(mae_text))
        self.wait(1)

        reason_title = Text("为什么用L1而非L2?", font_size=20, color=RED_C, font="Microsoft YaHei UI")
        reason_title.next_to(mae_text, DOWN, buff=0.3)

        reasons = VGroup()
        reason1 = Text("• 减少对偶发大误差的过度惩罚", font_size=16, color=WHITE, font="Microsoft YaHei UI")
        reason2 = Text("• 稳定训练 (处理异常值)", font_size=16, color=WHITE, font="Microsoft YaHei UI")
        reasons.add(reason1, reason2)
        reasons.arrange(DOWN, buff=0.18)
        reasons.next_to(reason_title, DOWN, buff=0.15)
        self.play(Write(reasons))
        self.wait(2)

        all_elements = [title, l1_formula, example_label, pred_label, target_label, diff_label,
                       mae_text, reason_title, reasons]
        self.play(FadeOut(*all_elements))



class L1vsL2Scene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("L1 vs L2 损失对比", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 25, 5],
            x_length=5,
            y_length=2.5,
            axis_config={"color": LIGHT_GRAY},
        )
        axes.move_to(UP * 1.5)
        self.play(Create(axes))
        self.wait(0.3)

        l1_label = Text("L1: 线性", font_size=18, color=BLUE_B, font="Microsoft YaHei UI")
        l1_label.next_to(axes, LEFT, buff=0.25).shift(UP * 0.6)

        l2_label = Text("L2: 二次", font_size=18, color=RED_C, font="Microsoft YaHei UI")
        l2_label.next_to(axes, RIGHT, buff=0.25).shift(UP * 0.6)

        self.play(Write(l1_label), Write(l2_label))

        l1_graph = axes.plot(lambda x: x, x_range=[0, 4.5], color=BLUE_B, stroke_width=3)
        l2_graph = axes.plot(lambda x: x**2, x_range=[0, 4.5], color=RED_C, stroke_width=3)
        self.play(Create(l1_graph), Create(l2_graph), run_time=1.5)
        self.wait(0.5)

        table_data = [
            ["特性", "L1", "L2"],
            ["大误差惩罚", "线性", "二次"],
            ["收敛速度", "快", "慢"],
        ]

        table = Table(table_data, col_labels=[Text(t, font_size=14, color=YELLOW, font="Microsoft YaHei UI") for t in table_data[0]])
        table.scale(0.45)
        table.move_to(DOWN * 1.8)
        self.play(Create(table))
        self.wait(2)

        all_elements = [title, axes, l1_label, l2_label, l1_graph, l2_graph, table]
        self.play(FadeOut(*all_elements))



class EqualWeightingScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("等权重聚合", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        scale_formula = MathTex(r"S = \{1.0, 0.5, 0.25\}", font_size=30, color=YELLOW)
        scale_formula.move_to(UP * 2.2)
        self.play(Write(scale_formula))
        self.wait(0.3)

        weight_formula = MathTex(r"w_s = \frac{1}{|S|} = \frac{1}{3}", font_size=34, color=BLUE_B)
        weight_formula.next_to(scale_formula, DOWN, buff=0.4)
        self.play(Write(weight_formula))
        self.wait(0.5)

        scale_boxes = []
        box_positions = [LEFT * 2.5, ORIGIN, RIGHT * 2.5]

        for i, (scale, w) in enumerate([("1.0", "w1=1/3"), ("0.5", "w2=1/3"), ("0.25", "w3=1/3")]):
            box = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.1,
                                  color=[BLUE_B, GREEN, ORANGE][i], stroke_width=2)
            box.move_to(box_positions[i])

            label = Text(f"尺度 {scale}", font_size=16, color=[BLUE_B, GREEN, ORANGE][i], font="Microsoft YaHei UI")
            label.move_to(box.get_center() + UP * 0.12)

            weight_label = Text(w, font_size=14, color=WHITE, font="Microsoft YaHei UI")
            weight_label.move_to(box.get_center() + DOWN * 0.2)

            self.play(Create(box), Write(label), Write(weight_label), run_time=0.4)
            scale_boxes.extend([box, label, weight_label])

        self.wait(0.5)

        final_formula = MathTex(r"L_{grad} = \frac{1}{3}L_1 + \frac{1}{3}L_2 + \frac{1}{3}L_3", font_size=24, color=GREEN)
        final_formula.move_to(DOWN * 2.5)
        self.play(Write(final_formula))
        self.wait(2)

        all_elements = [title, scale_formula, weight_formula] + scale_boxes + [final_formula]
        self.play(FadeOut(*all_elements))



class LossFunctionScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("完整损失函数", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        total_loss = MathTex(r"L_{total} = \lambda_{SSIM} L_{SSIM} + \lambda_{intensity} L_{intensity} + \lambda_{gradient} L_{gradient}", font_size=20, color=YELLOW)
        total_loss.move_to(UP * 2.2)
        self.play(Write(total_loss))
        self.wait(0.5)

        weight_box = RoundedRectangle(width=3.5, height=1.0, corner_radius=0.1, color=GREEN, stroke_width=2)
        weight_text = Text("论文权重配置", font_size=18, color=GREEN, font="Microsoft YaHei UI")
        weight_text.move_to(weight_box.get_center() + UP * 0.15)

        weights = Text("λ = [1.5, 7, 1.5]", font_size=24, color=WHITE, font="Microsoft YaHei UI")
        weights.move_to(weight_box.get_center() + DOWN * 0.15)

        self.play(Create(weight_box), Write(weight_text), Write(weights))
        self.wait(0.5)

        breakdown = VGroup()

        bar_data = [
            ("SSIM", 1.5, BLUE_B),
            ("Intensity", 7, GREEN),
            ("Gradient", 1.5, ORANGE)
        ]

        current_y = DOWN * 1.8

        for name, weight, color in bar_data:

            bar_width = max(0.5, weight * 0.4)

            bar = Rectangle(width=bar_width, height=0.35, color=color, fill_opacity=0.8)

            bar.move_to(LEFT * (2.5 - bar_width/2) + current_y)

            label = Text(f"{name}: {weight}", font_size=14, color=WHITE, font="Microsoft YaHei UI")

            label.next_to(bar, LEFT, buff=0.25)

            breakdown.add(label, bar)

            current_y += DOWN * 0.5

        breakdown.move_to(DOWN * 1.5)

        self.play(Write(breakdown))
        self.wait(2)

        all_elements = [title, total_loss, weight_box, weight_text, weights, breakdown]
        self.play(FadeOut(*all_elements))



class SummaryScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        title = Text("方法优势总结", font_size=38, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        advantages = [
            ("方向保真", "边缘方向在至少一个轴向上被惩罚"),
            ("消除方向偏差", "对称处理两轴"),
            ("细粒度门控", "像素级独立选择模态"),
            ("多尺度监督", "捕获细粒度和粗粒度结构"),
        ]

        colors = [BLUE_B, GREEN, ORANGE, RED_C]

        boxes = []

        for i, (title_text, desc_text) in enumerate(advantages):

            box = RoundedRectangle(width=5.5, height=0.65, corner_radius=0.1,
                                  color=colors[i], stroke_width=2)

            box.move_to(UP * (2 - i * 0.85))

            check = Text("✓", font_size=20, color=colors[i])

            check.move_to(box.get_center() + LEFT * 2.2)

            title_t = Text(title_text, font_size=18, color=colors[i], font="Microsoft YaHei UI")

            title_t.move_to(box.get_center() + LEFT * 0.6)

            desc = Text(desc_text, font_size=14, color=WHITE, font="Microsoft YaHei UI")

            desc.move_to(box.get_center() + RIGHT * 1.0)

            self.play(Create(box), Write(check), Write(title_t), Write(desc), run_time=0.4)

            boxes.extend([box, check, title_t, desc])

            self.wait(0.2)

        self.wait(2)

        all_elements = [title] + boxes

        self.play(FadeOut(*all_elements))



class EndScene(Scene):

    def construct(self):

        self.camera.background_color = "#1a1a2e"

        thanks = Text("谢谢观看", font_size=52, color=WHITE)

        self.play(Write(thanks), run_time=1.5)

        self.wait(2)

        self.play(FadeOut(thanks))