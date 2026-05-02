# PID 控制 · Manim 动画场景文档

> **项目**：PID 控制算法可视化动画  
> **引擎**：Manim Community v0.18+  
> **风格**：深色科技风 · 与 `git_version_control.py` 统一视觉语言  
> **总时长**：约 2 分钟（15fps 渲染）

---

## 一、全局规范

### 1.1 字体

| 用途 | 字体 | 常量名 |
|------|------|--------|
| 中文正文 | SimSun（宋体） | `FONT_CN` |
| 英文/公式标注 | Times New Roman | `FONT_EN` |
| 代码/数据 | Monaco | `FONT_MONO` |

### 1.2 配色方案

```python
COLORS = {
    # ── 背景与面板 ──
    "bg":               "#0d1117",   # 深色背景
    "surface":          "#161b22",   # 卡片底色
    "border":           "#30363d",   # 边框

    # ── PID 三通道主色 ──
    "p_coral":          "#FF6B6B",   # P — 珊瑚红
    "i_teal":           "#4ECDC4",   # I — 青绿
    "d_amber":          "#FFD93D",   # D — 琥珀黄

    # ── 信号色 ──
    "setpoint_blue":    "#58A6FF",   # 设定值 — 蓝
    "output_green":     "#3FB950",   # 实际输出 — 绿
    "error_red":        "#F85149",   # 误差 — 红
    "disturbance_orange":"#F05032",  # 扰动 — 橙

    # ── 辅助 ──
    "text_primary":     "#E6EDF3",   # 主文字
    "text_secondary":   "#8B949E",   # 次文字
    "glow_white":       "#FFFFFF",   # 光晕
    "arrow_gray":       "#6E7681",   # 连接箭头
}
```

### 1.3 通用工具函数

```python
def cn_text(text, font_size=24, color=None, **kwargs):
    """中文文字"""
    ...

def en_text(text, font_size=24, color=None, **kwargs):
    """英文文字"""
    ...

def glow_dot(radius=0.08, color=WHITE, glow_radius=0.3):
    """带光晕的圆点"""
    ...

def glass_card(width, height, corner_radius=0.15):
    """毛玻璃卡片"""
    return RoundedRectangle(
        width=width, height=height, corner_radius=corner_radius,
        fill_opacity=0.85, fill_color=COLORS["surface"],
        stroke_width=1.5, stroke_color=COLORS["border"],
    )
```

---

## 二、场景总览

| 场景编号 | 类名 | 内容 | 时长 |
|----------|------|------|------|
| S1 | `SceneIntro` | 开场标题 + PID 三个字母逐个点亮 | 8s |
| S2 | `SceneWhatIsPID` | PID 控制的直觉：开车追目标速度 | 14s |
| S3 | `SceneBlockDiagram` | PID 控制系统框图（信号流） | 16s |
| S4 | `ScenePControl` | 比例控制详解 + 响应曲线动画 | 16s |
| S5 | `SceneIControl` | 积分控制详解 + 消除稳态误差 | 16s |
| S6 | `SceneDControl` | 微分控制详解 + 抑制超调 | 16s |
| S7 | `ScenePIDTuning` | 参数调节效果对比（三曲线同屏） | 18s |
| S8 | `SceneSummary` | 总结收尾 | 10s |

**总时长 ≈ 114s（约 2 分钟）**

---

## 三、场景详细设计

---

### S1 · 开场 `SceneIntro`

**目的**：建立视觉基调，点明主题

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–1s | 背景淡入 | 深色背景 + 网格线（极淡） |
| 1–3s | 标题逐字打出 | `cn_text("PID 控制算法", font_size=48)` 居中上方 |
| 3–6s | P / I / D 三字母逐个点亮 | 三个大号字母，点亮时发出对应色光晕 |
| 6–8s | 副标题 + 公式闪现 | `en_text("u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt")` |

#### 关键实现

```python
class SceneIntro(Scene):
    def construct(self):
        # 网格背景
        grid = NumberPlane(
            background_line_style={"stroke_color": "#1a2030", "stroke_width": 0.5}
        )
        self.add(grid)

        # 标题
        title = cn_text("PID 控制算法", font_size=48, weight=BOLD)
        title.move_to(UP * 1.5)
        self.play(Write(title), run_time=2)

        # P I D 三字母
        p = en_text("P", font_size=72, color=COLORS["p_coral"], weight=BOLD)
        i = en_text("I", font_size=72, color=COLORS["i_teal"], weight=BOLD)
        d = en_text("D", font_size=72, color=COLORS["d_amber"], weight=BOLD)
        letters = VGroup(p, i, d).arrange(RIGHT, buff=1.2)
        letters.move_to(DOWN * 0.5)

        for letter, glow_color in [(p, COLORS["p_coral"]), 
                                    (i, COLORS["i_teal"]), 
                                    (d, COLORS["d_amber"])]:
            glow = Dot(radius=0.5, color=glow_color, fill_opacity=0.2)
            glow.move_to(letter)
            self.play(
                FadeIn(letter, shift=UP * 0.3),
                FadeIn(glow),
                run_time=0.8
            )
            self.play(glow.animate.set_opacity(0), run_time=0.3)

        # 公式
        formula = MathTex(
            r"u(t) = K_p \cdot e(t) + K_i \int e(t)\,dt + K_d \frac{de(t)}{dt}",
            font_size=28, color=COLORS["text_secondary"]
        )
        formula.move_to(DOWN * 2)
        self.play(FadeIn(formula, shift=UP * 0.3), run_time=1)
        self.wait(1)

        # 退场
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S2 · 直觉引入 `SceneWhatIsPID`

**目的**：用生活化场景建立 PID 的直觉理解

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 场景标题淡入 | "从开车说起" |
| 2–8s | 汽车追速动画 | 一辆小车 + 速度表 + 目标线，展示油门控制 |
| 8–12s | 三个卡片依次飞入 | P="踩多深" / I="差多久" / D="变多快" |
| 12–14s | 退场 | 全部淡出 |

#### 关键实现思路

- **汽车**：用 `Rectangle` + 两个 `Circle`（车轮）组合，位于画面下方
- **速度表**：左侧垂直刻度尺，蓝色水平线 = 目标速度，绿色填充 = 当前速度
- **卡片**：`glass_card` + 对应颜色标题 + 中文解释

```python
class SceneWhatIsPID(Scene):
    def construct(self):
        # 标题
        title = cn_text("从开车说起", font_size=40, weight=BOLD)
        title.move_to(UP * 3)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1)

        # ── 速度表 ──
        speed_bg = Rectangle(
            width=0.6, height=4,
            fill_opacity=0.3, fill_color=COLORS["surface"],
            stroke_color=COLORS["border"], stroke_width=1
        ).move_to(LEFT * 5 + UP * 0.5)

        target_line = Line(
            speed_bg.get_bottom() + UP * 3,  # 目标速度位置
            speed_bg.get_right() + LEFT * 0.05,
            color=COLORS["setpoint_blue"], stroke_width=3
        )

        # 当前速度填充条（随动画增长）
        speed_fill = Rectangle(
            width=0.5, height=0.01,
            fill_opacity=0.8, fill_color=COLORS["output_green"],
            stroke_width=0
        ).align_to(speed_bg.get_bottom(), DOWN)

        # ── 小车 ──
        car_body = Rectangle(width=2, height=0.8, fill_opacity=1,
                             fill_color=COLORS["surface"],
                             stroke_color=COLORS["text_secondary"])
        wheel1 = Circle(radius=0.2, fill_opacity=1, fill_color="#333")
        wheel2 = Circle(radius=0.2, fill_opacity=1, fill_color="#333")
        car = VGroup(car_body, wheel1, wheel2)
        wheel1.next_to(car_body, DOWN, buff=0).shift(LEFT * 0.5)
        wheel2.next_to(car_body, DOWN, buff=0).shift(RIGHT * 0.5)
        car.move_to(DOWN * 1.5)

        self.play(
            FadeIn(speed_bg), FadeIn(target_line),
            FadeIn(car), run_time=1
        )

        # 速度逼近动画（简化：手动控制高度）
        self.play(
            speed_fill.animate.stretch_to_fit_height(3).align_to(
                speed_bg.get_bottom(), DOWN
            ),
            car.animate.shift(RIGHT * 2),
            run_time=4, rate_func=rate_functions.ease_out_sine
        )
        self.wait(1)

        # ── 三张直觉卡片 ──
        cards_data = [
            ("P · 比例", "误差大 → 用力踩", COLORS["p_coral"]),
            ("I · 积分", "一直差 → 持续加力", COLORS["i_teal"]),
            ("D · 微分", "变太快 → 提前刹车", COLORS["d_amber"]),
        ]
        cards = VGroup()
        for label, desc, color in cards_data:
            card = glass_card(width=3.2, height=1.5)
            lbl = cn_text(label, font_size=22, color=color, weight=BOLD)
            dsc = cn_text(desc, font_size=18, color=COLORS["text_primary"])
            VGroup(lbl, dsc).arrange(DOWN, buff=0.2).move_to(card)
            VGroup(card, lbl, dsc).move_to(card.get_center())
            cards.add(VGroup(card, lbl, dsc))

        cards.arrange(RIGHT, buff=0.5).move_to(UP * 1.5)
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.6)

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S3 · 框图 `SceneBlockDiagram`

**目的**：展示 PID 控制系统的标准框图与信号流

#### 布局草图（14.2 × 8 标准画幅）

```
                    ┌──────┐    ┌──────┐    ┌──────────┐
 设定值 r(t) ──(+)→│  P   │    │      │    │          │    ┌────────┐
               │   └──────┘    │ 求和 │───→│ 被控对象 │───→│ 输出   │──→ y(t)
               │   ┌──────┐    │      │    │          │    └────────┘
 e(t) ────────┤   │  I   │───→│      │    └──────────┘         │
               │   └──────┘    └──────┘                         │
               │   ┌──────┐                                     │
               │   │  D   │───→┘                                │
               │   └──────┘                                     │
               │                                                │
               └────────────────── e(t) ───────────────────────┘
                                  反馈
```

#### 动画序列

| 时间 | 动作 |
|------|------|
| 0–2s | 框图结构逐块出现（设定值→误差计算→P/I/D→求和→对象→输出→反馈） |
| 2–6s | 信号流动动画（光点沿路径移动） |
| 6–10s | 标注各信号名称 |
| 10–14s | 高亮反馈回路，强调"闭环" |
| 14–16s | 退场 |

#### 关键实现思路

- 各功能块用 `RoundedRectangle` + 标签文字
- 连接线用 `Arrow` / `Line`
- 信号流动用 `glow_dot` 沿 `TracedPath` 移动
- 反馈回路用不同颜色的箭头区分

```python
class SceneBlockDiagram(Scene):
    def construct(self):
        title = cn_text("PID 控制系统框图", font_size=36, weight=BOLD)
        title.move_to(UP * 3.2)
        self.play(Write(title), run_time=1)

        # ── 功能块 ──
        block_style = dict(
            width=1.8, height=0.9, corner_radius=0.12,
            fill_opacity=0.85, fill_color=COLORS["surface"],
            stroke_width=1.5
        )

        # 误差计算（比较器用圆圈）
        comparator = Circle(radius=0.3, stroke_color=COLORS["setpoint_blue"],
                           stroke_width=2)
        comparator_label = en_text("+", font_size=20, color=COLORS["setpoint_blue"])
        comparator_label.move_to(comparator)
        comp_group = VGroup(comparator, comparator_label).move_to(LEFT * 5.5 + UP * 0.5)

        # P / I / D 三个块
        p_block = RoundedRectangle(color=COLORS["p_coral"], **block_style)
        p_label = en_text("Kp", font_size=22, color=COLORS["p_coral"])
        VGroup(p_block, p_label).move_to(p_block.get_center())

        i_block = RoundedRectangle(color=COLORS["i_teal"], **block_style)
        i_label = en_text("Ki·∫", font_size=22, color=COLORS["i_teal"])

        d_block = RoundedRectangle(color=COLORS["d_amber"], **block_style)
        d_label = en_text("Kd·d/dt", font_size=20, color=COLORS["d_amber"])

        # 三个块纵向排列
        pid_blocks = VGroup(
            VGroup(p_block, p_label),
            VGroup(i_block, i_label),
            VGroup(d_block, d_label)
        ).arrange(DOWN, buff=0.4).move_to(LEFT * 2.5 + UP * 0.5)

        # 求和点
        sum_circle = Circle(radius=0.25, stroke_color=COLORS["text_primary"],
                           stroke_width=2)
        sum_label = en_text("Σ", font_size=22)
        VGroup(sum_circle, sum_label).move_to(LEFT * 0.3 + UP * 0.5)

        # 被控对象
        plant_block = RoundedRectangle(
            width=2.2, height=1.2, corner_radius=0.12,
            fill_opacity=0.85, fill_color=COLORS["surface"],
            stroke_color=COLORS["output_green"], stroke_width=1.5
        )
        plant_label = cn_text("被控对象", font_size=20, color=COLORS["output_green"])
        VGroup(plant_block, plant_label).move_to(RIGHT * 2.5 + UP * 0.5)

        # 输出
        output_label = cn_text("y(t)", font_size=22, color=COLORS["output_green"])

        # ── 逐块出现 ──
        elements = [comp_group, pid_blocks, VGroup(sum_circle, sum_label),
                    VGroup(plant_block, plant_label)]
        for elem in elements:
            self.play(FadeIn(elem, shift=RIGHT * 0.3), run_time=0.7)

        # ── 连接线（箭头） ──
        # 设定值 → 比较器
        r_label = cn_text("r(t)", font_size=20, color=COLORS["setpoint_blue"])
        r_label.next_to(comparator, UP)
        arrow_r = Arrow(comparator.get_top() + UP * 0.8, comparator.get_top(),
                       color=COLORS["setpoint_blue"], buff=0.1)
        self.play(FadeIn(arrow_r), FadeIn(r_label), run_time=0.5)

        # 比较器 → PID各块
        # P/I/D → 求和点
        # 求和点 → 被控对象
        # 被控对象 → 输出
        # 输出 → 反馈回路
        # ...（具体坐标需根据实际布局微调）

        # ── 信号流动动画 ──
        signal_dot = glow_dot(color=COLORS["setpoint_blue"])
        # 沿路径追踪...

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S4 · 比例控制 `ScenePControl`

**目的**：直观展示 P 控制的含义与特征

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 标题 + 公式 | `u(t) = Kp · e(t)` 大号居中 |
| 2–5s | P 控制响应曲线绘制 | 坐标系 + 阶跃响应曲线（有稳态误差、超调） |
| 5–10s | Kp 从小→大的对比 | 三条曲线叠加（Kp=0.5 / 1.0 / 3.0） |
| 10–14s | 标注关键特征 | "响应快" / "有稳态误差" / "Kp过大→振荡" |
| 14–16s | 退场 | 淡出 |

#### 关键实现思路

- 用 `Axes` + `plot()` 绘制响应曲线
- 三条曲线同时绘制，用不同透明度/颜色区分
- 标注用 `Brace` + 文字

```python
class ScenePControl(Scene):
    def construct(self):
        title = cn_text("比例控制 P", font_size=36, weight=BOLD,
                        color=COLORS["p_coral"])
        title.move_to(UP * 3.2)
        self.play(Write(title), run_time=1)

        # 公式
        formula = MathTex(r"u(t) = K_p \cdot e(t)",
                         font_size=36, color=COLORS["p_coral"])
        formula.next_to(title, DOWN, buff=0.4)
        self.play(Write(formula), run_time=1.5)

        # ── 坐标系 ──
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.4, 0.2],
            x_length=8, y_length=4,
            axis_config={"color": COLORS["text_secondary"]},
            tips=False
        ).move_to(DOWN * 0.5)

        # 设定值线
        setpoint = axes.get_h_line(1.0, color=COLORS["setpoint_blue"])
        sp_label = cn_text("设定值", font_size=16, color=COLORS["setpoint_blue"])
        sp_label.next_to(setpoint, RIGHT)

        self.play(FadeIn(axes), FadeIn(setpoint), FadeIn(sp_label), run_time=1)

        # ── 三组 Kp 的响应曲线 ──
        # 简化：用指数趋近 + 超调模拟
        curves_data = [
            (0.5, "Kp=0.5", 0.4, COLORS["p_coral"], 0.4),   # 低增益：慢，稳态误差大
            (1.0, "Kp=1.0", 0.7, COLORS["p_coral"], 0.7),   # 中增益
            (3.0, "Kp=3.0", 1.0, COLORS["p_coral"], 1.0),   # 高增益：振荡
        ]

        curves = []
        labels = []
        for kp_val, label_text, opacity, color, final_opacity in curves_data:
            # 用参数方程生成响应曲线
            def p_response(x, k=kp_val):
                if x < 0.5:
                    return 0
                t = x - 0.5
                # 简化模型：一阶系统 + 可调增益
                steady = k / (1 + k)  # 终值
                if k < 2:
                    return steady * (1 - np.exp(-k * t * 0.5))
                else:
                    # 高增益产生振荡
                    return steady * (1 - np.exp(-t)) + 0.15 * np.sin(t * 3) * np.exp(-t * 0.3)

            curve = axes.plot(p_response, x_range=[0, 10], color=color)
            curve.set_stroke(opacity=opacity)
            curves.append(curve)

            lbl = en_text(label_text, font_size=16, color=color)
            lbl.set_opacity(opacity)
            labels.append(lbl)

        # 曲线标签排列
        for idx, lbl in enumerate(labels):
            lbl.next_to(axes, RIGHT).shift(DOWN * (0.8 - idx * 0.6))

        for curve, label in zip(curves, labels):
            self.play(
                Create(curve, run_time=2, rate_func=rate_functions.ease_out_sine),
                FadeIn(label, shift=LEFT * 0.2), run_time=2
            )

        # ── 标注 ──
        annotations = VGroup(
            cn_text("✓ 响应快", font_size=18, color=COLORS["output_green"]),
            cn_text("✗ 存在稳态误差", font_size=18, color=COLORS["error_red"]),
            cn_text("✗ Kp 过大 → 振荡", font_size=18, color=COLORS["error_red"]),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        annotations.move_to(LEFT * 5.5 + DOWN * 1)

        self.play(FadeIn(annotations, shift=RIGHT * 0.3), run_time=1)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S5 · 积分控制 `SceneIControl`

**目的**：展示 I 控制如何消除稳态误差

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 标题 + 公式 | `u(t) = Ki · ∫e(t)dt` |
| 2–6s | 稳态误差可视化 | P 控制曲线（不到位）+ 阴影面积 = 累积误差 |
| 6–10s | I 项加入后曲线动画 | 曲线缓慢上升最终到达设定值 |
| 10–14s | 标注 | "✓ 消除稳态误差" / "✗ 可能超调" / "✗ 响应慢" |
| 14–16s | 退场 | 淡出 |

#### 关键实现思路

- 阴影面积用 `axes.get_area()` 渲染
- I 控制曲线用"缓慢爬升到达目标"的函数模拟

```python
class SceneIControl(Scene):
    def construct(self):
        title = cn_text("积分控制 I", font_size=36, weight=BOLD,
                        color=COLORS["i_teal"])
        title.move_to(UP * 3.2)

        formula = MathTex(r"u_I(t) = K_i \int_0^t e(\tau)\,d\tau",
                         font_size=36, color=COLORS["i_teal"])
        formula.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(formula), run_time=2)

        # 坐标系
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.4, 0.2],
            x_length=8, y_length=4,
            axis_config={"color": COLORS["text_secondary"]},
            tips=False
        ).move_to(DOWN * 0.5)

        setpoint = axes.get_h_line(1.0, color=COLORS["setpoint_blue"])

        # P 控制曲线（有稳态误差）
        def p_only(x):
            steady = 0.75  # 到不了设定值
            return steady * (1 - np.exp(-x * 0.8))

        p_curve = axes.plot(p_only, x_range=[0, 10], color=COLORS["p_coral"])

        # 误差阴影面积
        error_area = axes.get_area(
            p_curve, x_range=[0, 10],
            bounded=axes.get_h_line(1.0),
            color=COLORS["error_red"], opacity=0.15
        )

        self.play(FadeIn(axes), FadeIn(setpoint), run_time=0.5)
        self.play(Create(p_curve), run_time=2)

        # 高亮误差面积
        error_label = cn_text("累积误差 = 阴影面积", font_size=18,
                             color=COLORS["error_red"])
        error_label.move_to(DOWN * 2.5)
        self.play(FadeIn(error_area), Write(error_label), run_time=1.5)
        self.wait(0.5)

        # I 控制加入后的曲线（缓慢到达设定值）
        def pi_response(x):
            # P+I: 最终到达设定值，但有超调
            target = 1.0
            if x < 0.5:
                return 0
            t = x - 0.5
            return target * (1 - 1.2 * np.exp(-t * 0.4) * np.cos(t * 0.8))

        pi_curve = axes.plot(pi_response, x_range=[0, 10], color=COLORS["i_teal"])
        self.play(Create(pi_curve), run_time=2)

        annotations = VGroup(
            cn_text("✓ 消除稳态误差", font_size=18, color=COLORS["output_green"]),
            cn_text("✗ 可能超调", font_size=18, color=COLORS["error_red"]),
            cn_text("✗ 响应较慢", font_size=18, color=COLORS["warning_yellow"]),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        annotations.move_to(LEFT * 5.5 + DOWN * 1)

        self.play(FadeIn(annotations, shift=RIGHT * 0.3), run_time=1)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S6 · 微分控制 `SceneDControl`

**目的**：展示 D 控制如何抑制超调、预测趋势

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 标题 + 公式 | `u(t) = Kd · de(t)/dt` |
| 2–6s | 无 D vs 有 D 对比 | 两条曲线：大超调 vs 平滑趋近 |
| 6–10s | 微分 = 曲线斜率可视化 | 在超调点标注切线 + "预测变化趋势" |
| 10–14s | 标注 | "✓ 抑制超调" / "✗ 对噪声敏感" / "✗ 不能单独使用" |
| 14–16s | 退场 | 淡出 |

#### 关键实现思路

- 超调点用 `TangentLine` 展示斜率
- 对比用动画：先画无D曲线（大超调），再画有D曲线（平滑）

```python
class SceneDControl(Scene):
    def construct(self):
        title = cn_text("微分控制 D", font_size=36, weight=BOLD,
                        color=COLORS["d_amber"])
        title.move_to(UP * 3.2)

        formula = MathTex(r"u_D(t) = K_d \frac{de(t)}{dt}",
                         font_size=36, color=COLORS["d_amber"])
        formula.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), Write(formula), run_time=2)

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.6, 0.2],
            x_length=8, y_length=4,
            axis_config={"color": COLORS["text_secondary"]},
            tips=False
        ).move_to(DOWN * 0.5)

        setpoint = axes.get_h_line(1.0, color=COLORS["setpoint_blue"])
        self.play(FadeIn(axes), FadeIn(setpoint), run_time=0.5)

        # 无 D：大超调
        def pi_no_d(x):
            return 1.0 * (1 - 1.5 * np.exp(-x * 0.6) * np.cos(x * 1.2))

        curve_no_d = axes.plot(pi_no_d, x_range=[0, 10], color=COLORS["error_red"])
        lbl_no_d = cn_text("无D：大超调", font_size=16, color=COLORS["error_red"])
        lbl_no_d.next_to(axes, RIGHT).shift(UP * 0.8)
        self.play(Create(curve_no_d), FadeIn(lbl_no_d), run_time=2)

        # 有 D：平滑
        def pid_with_d(x):
            return 1.0 * (1 - np.exp(-x * 0.8) * (1.05 * np.cos(x * 0.5) + 0.1 * np.sin(x * 0.5)))

        curve_with_d = axes.plot(pid_with_d, x_range=[0, 10], color=COLORS["d_amber"])
        lbl_with_d = cn_text("有D：平滑趋近", font_size=16, color=COLORS["d_amber"])
        lbl_with_d.next_to(axes, RIGHT).shift(DOWN * 0.2)
        self.play(Create(curve_with_d), FadeIn(lbl_with_d), run_time=2)

        # 超调点切线标注
        overshoot_point = axes.c2p(2.5, pi_no_d(2.5))
        tangent = Line(
            overshoot_point + LEFT * 1.2 + DOWN * 0.8,
            overshoot_point + RIGHT * 1.2 + UP * 0.8,
            color=COLORS["warning_yellow"], stroke_width=2
        )
        tangent_label = cn_text("斜率 = 变化趋势", font_size=16,
                               color=COLORS["warning_yellow"])
        tangent_label.next_to(tangent, UP, buff=0.2)

        self.play(Create(tangent), Write(tangent_label), run_time=1)

        annotations = VGroup(
            cn_text("✓ 抑制超调", font_size=18, color=COLORS["output_green"]),
            cn_text("✗ 对噪声敏感", font_size=18, color=COLORS["error_red"]),
            cn_text("✗ 不能单独使用", font_size=18, color=COLORS["warning_yellow"]),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        annotations.move_to(LEFT * 5.5 + DOWN * 1)

        self.play(FadeIn(annotations), run_time=1)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S7 · 参数调节 `ScenePIDTuning`

**目的**：展示 PID 三个参数的调节效果对比

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 标题 | "参数调节效果" |
| 2–5s | Kp 增大动画 | 曲线从慢→快→振荡的渐变 |
| 5–8s | Ki 增大动画 | 稳态误差从大→0，但超调增大 |
| 8–11s | Kd 增大动画 | 超调减小→平缓 |
| 11–16s | 三参数配合：最优曲线 | 最佳整定的曲线 + 满意标记 |
| 16–18s | 退场 | 淡出 |

#### 关键实现思路

- 使用 `ValueTracker` 驱动参数变化
- `always_redraw` 实时更新曲线
- 三行排列，每行一组参数对比

```python
class ScenePIDTuning(Scene):
    def construct(self):
        title = cn_text("参数调节效果", font_size=36, weight=BOLD)
        title.move_to(UP * 3.5)
        self.play(Write(title), run_time=1)

        # ── 三行坐标系 ──
        axes_config = dict(
            x_range=[0, 10, 2], y_range=[0, 1.4, 0.2],
            x_length=5, y_length=1.8,
            axis_config={"color": COLORS["text_secondary"], "stroke_width": 1},
            tips=False
        )

        row_positions = [UP * 1.8, UP * 0, DOWN * 1.8]
        row_labels = [
            ("Kp 增大", COLORS["p_coral"]),
            ("Ki 增大", COLORS["i_teal"]),
            ("Kd 增大", COLORS["d_amber"]),
        ]

        for pos, (label, color) in zip(row_positions, row_labels):
            axes = Axes(**axes_config).move_to(pos + RIGHT * 1)
            sp = axes.get_h_line(1.0, color=COLORS["setpoint_blue"])
            lbl = cn_text(label, font_size=20, color=color, weight=BOLD)
            lbl.next_to(axes, LEFT, buff=0.3)

            self.play(FadeIn(axes), FadeIn(sp), Write(lbl), run_time=0.5)

            # 在每个坐标系中画 2-3 条对比曲线
            # Kp 行：小/中/大 Kp
            # Ki 行：0/小/大 Ki
            # Kd 行：0/中/大 Kd
            # ...具体曲线绘制略

        self.wait(2)

        # ── 最优整定 ──
        best_axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.4, 0.2],
            x_length=10, y_length=5,
            axis_config={"color": COLORS["text_secondary"]},
            tips=False
        ).move_to(DOWN * 0.5)

        best_label = cn_text("最优整定", font_size=28, weight=BOLD,
                            color=COLORS["output_green"])
        best_label.move_to(UP * 3)

        self.play(FadeIn(best_axes), Write(best_label), run_time=1)

        # 最优响应曲线
        def optimal(x):
            return 1.0 * (1 - np.exp(-x * 1.2) * np.cos(x * 0.3))

        best_curve = best_axes.plot(optimal, x_range=[0, 10],
                                    color=COLORS["output_green"])
        self.play(Create(best_curve), run_time=2)

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

### S8 · 总结 `SceneSummary`

**目的**：收尾，强化记忆

#### 动画序列

| 时间 | 动作 | 视觉元素 |
|------|------|----------|
| 0–2s | 标题淡入 | "PID 三位一体" |
| 2–6s | 三张总结卡片飞入 | P / I / D 各一张，含核心关键词 |
| 6–8s | 中心公式出现 | `u(t) = Kp·e + Ki·∫e·dt + Kd·de/dt` 高亮 |
| 8–10s | 感谢语 | "谢谢观看" + 装饰线 |

#### 布局

```
         ┌─────────┐  ┌─────────┐  ┌─────────┐
         │ P 比例  │  │ I 积分  │  │ D 微分  │
         │ 快速响应 │  │ 消除误差 │  │ 抑制超调 │
         └─────────┘  └─────────┘  └─────────┘
              ╲            │            ╱
               ╲           │           ╱
                ───── PID 公式 ─────
              ──────── 谢谢观看 ────────
```

#### 关键实现

```python
class SceneSummary(Scene):
    def construct(self):
        title = cn_text("PID 三位一体", font_size=40, weight=BOLD)
        title.move_to(UP * 2.8)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1)

        # ── 三张卡片 ──
        cards_data = [
            ("P · 比例", "快速响应\n但有稳态误差", COLORS["p_coral"]),
            ("I · 积分", "消除稳态误差\n但可能超调", COLORS["i_teal"]),
            ("D · 微分", "抑制超调\n但对噪声敏感", COLORS["d_amber"]),
        ]

        cards = VGroup()
        for label, desc, color in cards_data:
            card = glass_card(width=3.0, height=2.0)
            lbl = cn_text(label, font_size=22, color=color, weight=BOLD)
            dsc = cn_text(desc, font_size=16, color=COLORS["text_primary"])
            VGroup(lbl, dsc).arrange(DOWN, buff=0.3).move_to(card)
            cards.add(VGroup(card, lbl, dsc))

        cards.arrange(RIGHT, buff=0.6).move_to(UP * 0.5)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.6)

        # ── 中心公式 ──
        formula = MathTex(
            r"u(t) = K_p \cdot e(t) + K_i \int e(t)\,dt + K_d \frac{de(t)}{dt}",
            font_size=28, color=COLORS["text_primary"]
        )
        formula.move_to(DOWN * 1.5)
        self.play(Write(formula), run_time=2)

        # ── 感谢语 ──
        thanks = cn_text("谢谢观看", font_size=32, weight=BOLD,
                        color=COLORS["text_secondary"])
        thanks.move_to(DOWN * 3)
        deco_line = Line(LEFT * 3, RIGHT * 3, color=COLORS["border"])
        deco_line.next_to(thanks, UP, buff=0.2)

        self.play(FadeIn(thanks), Create(deco_line), run_time=1)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
```

---

## 四、主场景类（串联所有子场景）

```python
class PIDControlVideo(Scene):
    """PID 控制算法 · 完整动画"""

    def construct(self):
        # 按顺序播放所有子场景
        SceneIntro.construct(self)
        SceneWhatIsPID.construct(self)
        SceneBlockDiagram.construct(self)
        ScenePControl.construct(self)
        SceneIControl.construct(self)
        SceneDControl.construct(self)
        ScenePIDTuning.construct(self)
        SceneSummary.construct(self)
```

> **注意**：实际渲染时建议每个子场景单独渲染后再拼接，避免内存溢出。也可使用 `-n start,end` 参数分段渲染。

---

## 五、渲染命令

```bash
# 激活 conda 环境
conda activate my-manim

# 渲染完整视频（720p30）
manim -pql git_version_control.py PIDControlVideo

# 单独渲染某个场景（调试用）
manim -pql pid_control.py ScenePControl

# 高质量渲染
manim -pqh pid_control.py PIDControlVideo
```

---

## 六、视觉风格备注

1. **深色背景** `#0d1117` 贯穿始终，与 git_version_control.py 统一
2. **P/I/D 三色**（珊瑚红/青绿/琥珀黄）在所有场景中保持一致，强化色彩映射记忆
3. **毛玻璃卡片**（`glass_card`）用于所有信息面板
4. **光晕效果**（`glow_dot`）用于信号流动和强调点
5. **曲线动画** 使用 `Create()` 而非 `FadeIn()`，模拟实时绘制感
6. **公式** 统一使用 `MathTex`（LaTeX 渲染），字号 ≥ 28 保证可读性
7. **布局边界**：所有元素坐标确保在 x ∈ [-6.5, 6.5]、y ∈ [-3.5, 3.8] 范围内，不超出画幅

---

## 七、扩展方向

- [ ] 加入离散 PID 公式：`u[k] = Kp·e[k] + Ki·Σe + Kd·(e[k]-e[k-1])`
- [ ] 加入 Ziegler-Nichols 整定法动画
- [ ] 加入实际应用场景（无人机/温控/平衡车）
- [ ] 加入抗积分饱和（Anti-windup）说明
- [ ] 支持交互式参数调节（manim 的 `Scene.interactive` 模式）
