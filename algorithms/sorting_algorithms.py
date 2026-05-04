from manim import *
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
    "bar_default": "#58A6FF",
    "compare": "#F0883E",
    "swap": "#F85149",
    "sorted": "#3FB950",
    "pivot": "#BC8CFF",
    "minimum": "#FF7B72",
    "caption_yellow": "#FFD93D",
    "code_lime": "#7EE787",
}

FONT_CN = "SimSun"
FONT_EN = "Times New Roman"

INITIAL_ARRAY = [8, 3, 7, 1, 5, 10, 2, 9, 4, 6]


# ============================================================
# 工具函数
# ============================================================
def cn(text, size=36, color=None, weight=NORMAL, **kw):
    return Text(text, font_size=size, color=color or COLORS["text_primary"],
                font=FONT_CN, weight=weight, **kw)


def en(text, size=36, color=None, weight=NORMAL, **kw):
    return Text(text, font_size=size, color=color or COLORS["text_primary"],
                font=FONT_EN, weight=weight, **kw)


def mono(text, size=28, color=None, weight=NORMAL, **kw):
    return Text(text, font_size=size, color=color or COLORS["code_lime"],
                font=FONT_EN, weight=weight, **kw)


def glass_card(w, h, r=0.18):
    return RoundedRectangle(
        width=w, height=h, corner_radius=r,
        fill_opacity=0.88, fill_color=COLORS["surface"],
        stroke_width=1.5, stroke_color=COLORS["border"],
    )


def make_bars(arr, bar_width=0.42, height_scale=0.3):
    bars = VGroup()
    for val in arr:
        bar = Rectangle(
            width=bar_width, height=val * height_scale,
            fill_color=COLORS["bar_default"], fill_opacity=0.9,
            stroke_color=COLORS["border"], stroke_width=1,
        )
        label = en(str(val), size=19, color=COLORS["text_primary"])
        label.next_to(bar, UP, buff=0.08)
        bars.add(VGroup(bar, label))
    bars.arrange(RIGHT, buff=0.1)
    return bars


# ============================================================
# 主场景
# ============================================================
class SortingVideo(Scene):
    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.scene_intro()
        self.scene_bubble_sort()
        self.scene_selection_sort()
        self.scene_insertion_sort()
        self.scene_merge_sort()
        self.scene_quick_sort()
        self.scene_race()
        self.scene_summary()

    # ----------------------------------------------------------
    # 通用辅助
    # ----------------------------------------------------------
    def _clear(self):
        anims = [FadeOut(m, shift=DOWN * 0.15) for m in self.mobjects]
        if anims:
            self.play(*anims, run_time=0.5)

    def _caption(self, text, width=11.2):
        t = cn(text, size=24, color=COLORS["caption_yellow"])
        if t.width > width - 0.6:
            t.scale_to_fit_width(width - 0.6)
        box = glass_card(width, 0.65, r=0.12)
        t.move_to(box.get_center())
        g = VGroup(box, t).to_edge(DOWN, buff=0.2)
        return g

    def _header(self, title_text, subtitle="", complexity=""):
        title = cn(title_text, size=42, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        grp = VGroup(title)
        if subtitle:
            sub = cn(subtitle, size=24, color=COLORS["text_secondary"])
            sub.next_to(title, DOWN, buff=0.1)
            grp.add(sub)
        self.play(FadeIn(grp, shift=DOWN * 0.15), run_time=0.5)
        if complexity:
            tag = mono(complexity, size=26, color=COLORS["code_lime"])
            tag.to_corner(UR, buff=0.4)
            self.play(FadeIn(tag, shift=LEFT * 0.2), run_time=0.3)
            grp.add(tag)
        return grp

    def _color(self, bars, indices, color, rt=0.15):
        anims = [bars[i][0].animate.set_color(color) for i in indices]
        if anims:
            self.play(*anims, run_time=rt)

    def _swap(self, bars, i, j, rt=0.25):
        pi, pj = bars[i].get_center().copy(), bars[j].get_center().copy()
        self.play(bars[i].animate.move_to(pj), bars[j].animate.move_to(pi), run_time=rt)
        bars[i], bars[j] = bars[j], bars[i]

    def _init_bars(self, header_grp):
        bars = make_bars(INITIAL_ARRAY)
        bars.next_to(header_grp, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in bars],
                               lag_ratio=0.04), run_time=0.5)
        return bars

    # ==========================================================
    # S1: 开场
    # ==========================================================
    def scene_intro(self):
        title = cn("排序算法可视化", size=50, weight=BOLD)
        sub = cn("六大经典排序 · 柱状图动画 · 速度竞赛", size=24,
                 color=COLORS["text_secondary"])
        grp = VGroup(title, sub).arrange(DOWN, buff=0.2)
        card = glass_card(grp.width + 1.0, grp.height + 0.7)
        grp.move_to(card.get_center())
        self.play(FadeIn(VGroup(card, grp), scale=0.9), run_time=0.8)
        self.wait(1.5)
        self._clear()

        bars = make_bars(INITIAL_ARRAY)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars],
                               lag_ratio=0.06), run_time=0.8)
        # 颜色图例
        items = [("默认", "bar_default"), ("比较", "compare"),
                 ("交换", "swap"), ("已排好", "sorted"), ("枢轴", "pivot")]
        legend = VGroup(*[
            VGroup(Dot(radius=0.08, color=COLORS[k]),
                   cn(n, size=17)).arrange(RIGHT, buff=0.1)
            for n, k in items
        ]).arrange(RIGHT, buff=0.35)
        legend.next_to(bars, DOWN, buff=0.5)
        self.play(FadeIn(legend, shift=UP * 0.1), run_time=0.4)
        self.wait(1.5)
        self._clear()

    # ==========================================================
    # S2: 冒泡排序 — 每步一个 play，干净利落
    # ==========================================================
    def scene_bubble_sort(self):
        hdr = self._header("冒泡排序", "相邻比较 · 大的往后冒", "O(n²)")
        bars = self._init_bars(hdr)
        cap = self._caption("每轮从左到右比较相邻元素，大的往后交换")
        self.play(FadeIn(cap), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        arr = list(INITIAL_ARRAY)
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                # 比较：两个柱子变橙
                self.play(
                    bars[j][0].animate.set_color(COLORS["compare"]),
                    bars[j + 1][0].animate.set_color(COLORS["compare"]),
                    run_time=0.12,
                )
                if arr[j] > arr[j + 1]:
                    # 交换：红色 + 位置互换
                    self.play(
                        bars[j][0].animate.set_color(COLORS["swap"]),
                        bars[j + 1][0].animate.set_color(COLORS["swap"]),
                        run_time=0.08,
                    )
                    self._swap(bars, j, j + 1, rt=0.18)
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                # 恢复默认色
                self.play(
                    bars[j][0].animate.set_color(COLORS["bar_default"]),
                    bars[j + 1][0].animate.set_color(COLORS["bar_default"]),
                    run_time=0.06,
                )
            # 每轮末尾标绿
            self._color(bars, [n - 1 - i], COLORS["sorted"], rt=0.15)
        self._color(bars, [0], COLORS["sorted"], rt=0.15)
        self.wait(1.0)
        self._clear()

    # ==========================================================
    # S3: 选择排序 — 最小值标记清晰移动
    # ==========================================================
    def scene_selection_sort(self):
        hdr = self._header("选择排序", "每轮选最小放到前面", "O(n²)")
        bars = self._init_bars(hdr)
        cap = self._caption("扫描未排序部分，找到最小值，放到已排序末尾")
        self.play(FadeIn(cap), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        arr = list(INITIAL_ARRAY)
        n = len(arr)
        for i in range(n - 1):
            min_idx = i
            self._color(bars, [min_idx], COLORS["minimum"], rt=0.12)
            for j in range(i + 1, n):
                # 比较当前最小值和新元素
                self.play(
                    bars[min_idx][0].animate.set_color(COLORS["minimum"]),
                    bars[j][0].animate.set_color(COLORS["compare"]),
                    run_time=0.08,
                )
                if arr[j] < arr[min_idx]:
                    self._color(bars, [min_idx], COLORS["bar_default"], rt=0.06)
                    min_idx = j
                    self._color(bars, [min_idx], COLORS["minimum"], rt=0.08)
                else:
                    self._color(bars, [j], COLORS["bar_default"], rt=0.06)
            if min_idx != i:
                self._color(bars, [i], COLORS["swap"], rt=0.08)
                self._swap(bars, i, min_idx, rt=0.2)
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self._color(bars, [i], COLORS["sorted"], rt=0.12)
        self._color(bars, [n - 1], COLORS["sorted"], rt=0.12)
        self.wait(1.0)
        self._clear()

    # ==========================================================
    # S4: 插入排序 — 逐个交换左移，简洁可靠
    # ==========================================================
    def scene_insertion_sort(self):
        hdr = self._header("插入排序", "像整理手中的扑克牌", "O(n²)")
        bars = self._init_bars(hdr)
        cap = self._caption("取出当前元素，向左找到正确位置，插入")
        self.play(FadeIn(cap), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        arr = list(INITIAL_ARRAY)
        n = len(arr)
        self._color(bars, [0], COLORS["sorted"], rt=0.1)

        for i in range(1, n):
            key_val = arr[i]
            # 高亮当前要插入的元素
            self._color(bars, [i], COLORS["compare"], rt=0.12)
            j = i
            # 向左逐个交换，直到找到正确位置
            while j > 0 and arr[j - 1] > key_val:
                self.play(
                    bars[j - 1][0].animate.set_color(COLORS["compare"]),
                    run_time=0.06,
                )
                self._swap(bars, j - 1, j, rt=0.15)
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                self._color(bars, [j], COLORS["sorted"], rt=0.04)
                j -= 1
            self._color(bars, [j], COLORS["sorted"], rt=0.08)

        self.wait(1.0)
        self._clear()

    # ==========================================================
    # S5: 归并排序 — 清晰的分治可视化
    # ==========================================================
    def scene_merge_sort(self):
        hdr = self._header("归并排序", "分治法 · 先拆分再合并", "O(n log n)")
        bars = self._init_bars(hdr)
        cap = self._caption("递归拆分到单个元素，再两两合并成有序序列")
        self.play(FadeIn(cap), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        arr = list(INITIAL_ARRAY)
        n = len(arr)

        # 拆分动画：柱子分组，视觉上展示"拆"
        # 先把所有柱子变色表示"正在处理"
        self._color(bars, list(range(n)), COLORS["compare"], rt=0.2)
        # 分成左右两半
        left_g = VGroup(*[bars[i] for i in range(n // 2)])
        right_g = VGroup(*[bars[i] for i in range(n // 2, n)])
        self.play(
            left_g.animate.shift(LEFT * 0.5 + DOWN * 0.4),
            right_g.animate.shift(RIGHT * 0.5 + DOWN * 0.4),
            run_time=0.4,
        )
        self.wait(0.3)
        # 复原
        self.play(
            left_g.animate.shift(RIGHT * 0.5 + UP * 0.4),
            right_g.animate.shift(LEFT * 0.5 + UP * 0.4),
            run_time=0.4,
        )
        self._color(bars, list(range(n)), COLORS["bar_default"], rt=0.15)

        # 合并阶段：递归执行
        self._merge_sort_anim(bars, arr, 0, n - 1)
        self._color(bars, list(range(n)), COLORS["sorted"], rt=0.2)
        self.wait(1.0)
        self._clear()

    def _merge_sort_anim(self, bars, arr, lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        self._merge_sort_anim(bars, arr, lo, mid)
        self._merge_sort_anim(bars, arr, mid + 1, hi)
        self._merge_anim(bars, arr, lo, mid, hi)

    def _merge_anim(self, bars, arr, lo, mid, hi):
        # 高亮两个子数组
        self._color(bars, list(range(lo, mid + 1)), COLORS["compare"], rt=0.08)
        self._color(bars, list(range(mid + 1, hi + 1)), COLORS["pivot"], rt=0.08)

        L, R = arr[lo:mid + 1], arr[mid + 1:hi + 1]
        i = j = 0
        k = lo
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1

        # 直接更新柱子高度和标签，保持 bars 引用不变
        anims = []
        for idx in range(lo, hi + 1):
            val = arr[idx]
            bar = bars[idx][0]
            lbl = bars[idx][1]
            # 新柱子：高度 = val * 0.3（与 make_bars 的 height_scale 一致）
            new_h = val * 0.3
            old_h = bar.height
            # 缩放高度（锚定底部）
            bottom = bar.get_bottom()
            bar.stretch_to_fit_height(new_h)
            bar.move_to(bottom + UP * new_h / 2)
            bar.set_color(COLORS["sorted"])
            # 更新标签位置
            lbl.next_to(bar, UP, buff=0.08)
            new_lbl = en(str(val), size=19, color=COLORS["text_primary"])
            new_lbl.move_to(lbl)
            anims.append(Transform(lbl, new_lbl))

        self.play(*anims, run_time=0.12)
        self.wait(0.05)
        self._color(bars, list(range(lo, hi + 1)), COLORS["bar_default"], rt=0.05)

    # ==========================================================
    # S6: 快速排序 — 枢轴 + 分区 + 递归
    # ==========================================================
    def scene_quick_sort(self):
        hdr = self._header("快速排序", "选枢轴 · 分区 · 递归", "O(n log n)")
        bars = self._init_bars(hdr)
        cap = self._caption("选一个枢轴，比它小的放左边，大的放右边")
        self.play(FadeIn(cap), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(cap), run_time=0.3)

        arr = list(INITIAL_ARRAY)
        n = len(arr)
        self._quick_sort_anim(bars, arr, 0, n - 1)
        self._color(bars, list(range(n)), COLORS["sorted"], rt=0.2)
        self.wait(1.0)
        self._clear()

    def _quick_sort_anim(self, bars, arr, lo, hi):
        if lo >= hi:
            if lo == hi:
                self._color(bars, [lo], COLORS["sorted"], rt=0.08)
            return
        pivot_idx = self._partition_anim(bars, arr, lo, hi)
        self._quick_sort_anim(bars, arr, lo, pivot_idx - 1)
        self._quick_sort_anim(bars, arr, pivot_idx + 1, hi)

    def _partition_anim(self, bars, arr, lo, hi):
        pivot_val = arr[hi]
        self._color(bars, [hi], COLORS["pivot"], rt=0.1)
        i = lo - 1
        for j in range(lo, hi):
            self.play(bars[j][0].animate.set_color(COLORS["compare"]), run_time=0.06)
            if arr[j] <= pivot_val:
                i += 1
                if i != j:
                    self.play(
                        bars[i][0].animate.set_color(COLORS["swap"]),
                        bars[j][0].animate.set_color(COLORS["swap"]),
                        run_time=0.05,
                    )
                    self._swap(bars, i, j, rt=0.15)
                    arr[i], arr[j] = arr[j], arr[i]
                self._color(bars, [i], COLORS["bar_default"], rt=0.04)
            else:
                self._color(bars, [j], COLORS["bar_default"], rt=0.04)
        i += 1
        if i != hi:
            self.play(
                bars[i][0].animate.set_color(COLORS["swap"]),
                bars[hi][0].animate.set_color(COLORS["swap"]),
                run_time=0.05,
            )
            self._swap(bars, i, hi, rt=0.15)
            arr[i], arr[hi] = arr[hi], arr[i]
        self._color(bars, [i], COLORS["sorted"], rt=0.1)
        return i

    # ==========================================================
    # S7: 竞赛 — 6 算法同步对比
    # ==========================================================
    def scene_race(self):
        self._clear()
        title = cn("排序算法竞赛", size=42, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        self.play(FadeIn(title), run_time=0.4)

        algo_names = ["冒泡", "选择", "插入", "归并", "快排", "堆排"]
        algo_fns = [
            self._bubble_steps, self._selection_steps,
            self._insertion_steps, self._merge_steps,
            self._quick_steps, self._heap_steps,
        ]

        mini_bars = []
        counters = []
        cards = VGroup()
        positions = [
            [-3.5, 0.8, 0], [0, 0.8, 0], [3.5, 0.8, 0],
            [-3.5, -1.8, 0], [0, -1.8, 0], [3.5, -1.8, 0],
        ]

        for idx in range(6):
            b = make_bars(list(INITIAL_ARRAY), bar_width=0.14, height_scale=0.08)
            b.scale(0.45).move_to(positions[idx] + DOWN * 0.1)
            name = cn(algo_names[idx], size=18, weight=BOLD)
            cnt = cn("0", size=15, color=COLORS["text_secondary"])
            hdr = VGroup(name, cnt).arrange(RIGHT, buff=0.15)
            hdr.next_to(b, UP, buff=0.2)
            card = glass_card(b.width + 0.5, b.height + 0.9, r=0.08)
            card.move_to(b.get_center() + UP * 0.1)
            cards.add(VGroup(card, hdr, b))
            mini_bars.append(b)
            counters.append(cnt)

        self.play(FadeIn(cards, lag_ratio=0.08), run_time=0.6)
        self.wait(1.0)

        # 预计算步骤
        all_steps = [fn(list(INITIAL_ARRAY)) for fn in algo_fns]
        max_steps = max(len(s) for s in all_steps)
        step_counts = [0] * 6

        for si in range(max_steps):
            anims = []
            for ai in range(6):
                if si >= len(all_steps[ai]):
                    continue
                step = all_steps[ai][si]
                step_counts[ai] += 1
                b = mini_bars[ai]
                act = step[0]

                if act == "compare":
                    anims += [b[step[1]][0].animate.set_color(COLORS["compare"]),
                              b[step[2]][0].animate.set_color(COLORS["compare"])]
                elif act == "swap":
                    pi = b[step[1]].get_center().copy()
                    pj = b[step[2]].get_center().copy()
                    anims += [b[step[1]].animate.move_to(pj),
                              b[step[2]].animate.move_to(pi)]
                    b[step[1]], b[step[2]] = b[step[2]], b[step[1]]
                elif act == "sorted":
                    for k in step[1]:
                        anims.append(b[k][0].animate.set_color(COLORS["sorted"]))
                elif act == "reset":
                    for k in step[1]:
                        anims.append(b[k][0].animate.set_color(COLORS["bar_default"]))

            if anims:
                self.play(*anims, run_time=0.08)

            # 更新计数器
            for ai in range(6):
                if si < len(all_steps[ai]):
                    new_cnt = cn(str(step_counts[ai]), size=15,
                                 color=COLORS["text_secondary"])
                    new_cnt.move_to(counters[ai])
                    counters[ai].become(new_cnt)

        self.wait(1.5)
        self._clear()

    # --- 步骤记录 ---
    def _bubble_steps(self, arr):
        s = []
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                s.append(("compare", j, j + 1))
                if arr[j] > arr[j + 1]:
                    s.append(("swap", j, j + 1))
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                s.append(("reset", [j, j + 1]))
            s.append(("sorted", [n - 1 - i]))
        s.append(("sorted", [0]))
        return s

    def _selection_steps(self, arr):
        s = []
        n = len(arr)
        for i in range(n - 1):
            m = i
            for j in range(i + 1, n):
                s.append(("compare", m, j))
                if arr[j] < arr[m]:
                    s.append(("reset", [m]))
                    m = j
                else:
                    s.append(("reset", [m, j]))
            if m != i:
                s.append(("swap", i, m))
                arr[i], arr[m] = arr[m], arr[i]
            s.append(("sorted", [i]))
        s.append(("sorted", [n - 1]))
        return s

    def _insertion_steps(self, arr):
        s = []
        n = len(arr)
        s.append(("sorted", [0]))
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                s.append(("compare", j, j + 1))
                s.append(("swap", j, j + 1))
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            s.append(("sorted", list(range(i + 1))))
        return s

    def _merge_steps(self, arr):
        s = []
        self._ms_helper(arr, 0, len(arr) - 1, s)
        s.append(("sorted", list(range(len(arr)))))
        return s

    def _ms_helper(self, arr, lo, hi, s):
        if lo >= hi:
            return
        mid = (lo + hi) // 2
        self._ms_helper(arr, lo, mid, s)
        self._ms_helper(arr, mid + 1, hi, s)
        L, R = arr[lo:mid + 1], arr[mid + 1:hi + 1]
        i = j = 0; k = lo
        while i < len(L) and j < len(R):
            s.append(("compare", lo + i, mid + 1 + j))
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1
        s.append(("sorted", list(range(lo, hi + 1))))

    def _quick_steps(self, arr):
        s = []
        self._qs_helper(arr, 0, len(arr) - 1, s)
        s.append(("sorted", list(range(len(arr)))))
        return s

    def _qs_helper(self, arr, lo, hi, s):
        if lo >= hi:
            if lo == hi:
                s.append(("sorted", [lo]))
            return
        pv = arr[hi]; i = lo - 1
        for j in range(lo, hi):
            s.append(("compare", j, hi))
            if arr[j] <= pv:
                i += 1
                if i != j:
                    s.append(("swap", i, j))
                    arr[i], arr[j] = arr[j], arr[i]
        i += 1
        if i != hi:
            s.append(("swap", i, hi))
            arr[i], arr[hi] = arr[hi], arr[i]
        s.append(("sorted", [i]))
        self._qs_helper(arr, lo, i - 1, s)
        self._qs_helper(arr, i + 1, hi, s)

    def _heap_steps(self, arr):
        s = []; n = len(arr)
        def heapify(sz, r):
            lg = r; l = 2 * r + 1; rt = 2 * r + 2
            if l < sz:
                s.append(("compare", lg, l))
                if arr[l] > arr[lg]: lg = l
            if rt < sz:
                s.append(("compare", lg, rt))
                if arr[rt] > arr[lg]: lg = rt
            if lg != r:
                s.append(("swap", r, lg))
                arr[r], arr[lg] = arr[lg], arr[r]
                heapify(sz, lg)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
        for i in range(n - 1, 0, -1):
            s.append(("swap", 0, i))
            arr[0], arr[i] = arr[i], arr[0]
            s.append(("sorted", [i]))
            heapify(i, 0)
        s.append(("sorted", [0]))
        return s

    # ==========================================================
    # S8: 总结
    # ==========================================================
    def scene_summary(self):
        title = cn("排序算法复杂度对比", size=38, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.4)

        headers = ["算法", "平均", "最坏", "空间", "稳定性"]
        data = [
            ["冒泡排序", "O(n²)", "O(n²)", "O(1)", "稳定"],
            ["选择排序", "O(n²)", "O(n²)", "O(1)", "不稳定"],
            ["插入排序", "O(n²)", "O(n²)", "O(1)", "稳定"],
            ["归并排序", "O(n log n)", "O(n log n)", "O(n)", "稳定"],
            ["快速排序", "O(n log n)", "O(n²)", "O(log n)", "不稳定"],
            ["堆排序", "O(n log n)", "O(n log n)", "O(1)", "不稳定"],
        ]

        cw = [1.8, 1.8, 1.8, 1.5, 1.3]
        rh = 0.52
        total_w = sum(cw)
        x0 = -total_w / 2

        # 表头
        hx = x0
        hcells = VGroup()
        for i, h in enumerate(headers):
            c = cn(h, size=19, color=COLORS["caption_yellow"], weight=BOLD)
            c.move_to([hx + cw[i] / 2, 0, 0])
            hcells.add(c)
            hx += cw[i]
        hbg = glass_card(total_w + 0.15, rh, r=0.05)
        hbg.move_to(hcells.get_center())
        hbg.set_fill(COLORS["border"], opacity=0.5)
        table = VGroup(VGroup(hbg, hcells))

        # 数据行
        for r, row_data in enumerate(data):
            rx = x0
            rcells = VGroup()
            for c, txt in enumerate(row_data):
                color = COLORS["text_primary"]
                if txt == "O(n²)":
                    color = COLORS["swap"]
                elif "n log n" in txt:
                    color = COLORS["sorted"]
                elif txt == "稳定":
                    color = COLORS["sorted"]
                elif txt == "不稳定":
                    color = COLORS["compare"]
                cell = cn(txt, size=17, color=color)
                cell.move_to([rx + cw[c] / 2, 0, 0])
                rcells.add(cell)
                rx += cw[c]
            rbg = glass_card(total_w + 0.15, rh, r=0.05)
            rbg.set_fill(COLORS["surface"], opacity=0.4)
            row_grp = VGroup(rbg, rcells)
            rbg.move_to(rcells.get_center())
            row_grp.shift(DOWN * (r + 1) * rh)
            table.add(row_grp)

        table.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(table), run_time=0.8)
        self.wait(2.0)

        end = cn("感谢观看", size=32, weight=BOLD)
        card = glass_card(end.width + 0.8, 0.7, r=0.1)
        end.move_to(card.get_center())
        g = VGroup(card, end).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(g, scale=0.9), run_time=0.6)
        self.wait(1.5)
