**[中文版](README_cn.md)** | English

# Manim Teaching Animations

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=fff)
![Manim](https://img.shields.io/badge/Manim_CE-0.20.1-0A0A0A?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Course assignment animations. PID control, Git workflows, CNN, backpropagation, sorting algorithms — all rendered with Manim CE, all in a dark tech theme.

## Table of Contents

- [What is this](#what-is-this)
- [File structure](#file-structure)
- [Getting started](#getting-started)
- [Style guide](#style-guide)
- [Built with](#built-with)
- [License](#license)

## What is this

A bunch of self-contained Manim scripts I made for coursework and presentations. Each `.py` file is a standalone video — no shared modules, no dependency headaches. Run one file, get one video.

Topics cover control theory (analog and digital PID), version control (Git), deep learning (CNN, backpropagation), image fusion (direction-aware gradient loss), and sorting algorithms (bubble, selection, insertion, merge, quick, heap sort with race comparison).

## File structure

```
manim/
├── pid_control/                # PID control series
│   ├── pid_control.py
│   ├── digital_pid_control.py
│   └── docs/
├── image_fusion/               # Image fusion (graduation project)
│   ├── gradient_loss_animation.py
│   └── docs/
├── git/                        # Git workflow
│   └── git_version_control.py
├── CNN/                        # Convolutional neural networks
│   ├── cnn_pop_video.py
│   └── video_script.md
├── backpropagation/            # Backpropagation
│   ├── backprop_pop_video.py
│   └── backprop_cover.py
├── algorithms/                 # Algorithm visualizations
│   └── sorting_algorithms.py   # 6 sorting algorithms + race
├── media/                      # Manim auto-generated cache
└── output_video/               # Final rendered MP4s
```

每个脚本内部结构都一样：顶部 `COLORS` 字典定义配色，中间 `cn()`/`en()`/`mono()` 是文字快捷函数，底部一个或多个 `Scene` 类是实际画面。

## Getting started

```bash
# Low quality preview (fast)
manim -pql pid_control/pid_control.py PIDControlVideo

# High quality render (slow)
manim -pqh pid_control/pid_control.py PIDControlVideo

# Render first 3 seconds only
manim -pql CNN/cnn_pop_video.py CNNPopularizationVideo -n 0,3
```

需要 Python 3.x 和 [Manim CE](https://docs.manim.community/en/stable/installation.html)。装好 manim 就行，没有额外依赖。

## Style guide

所有动画统一用深色科技风，别乱改配色：

| 元素 | 颜色 | 用途 |
|------|------|------|
| 背景 | `#0d1117` | 画布底色 |
| 表面 | `#161b22` | 卡片、面板 |
| 边框 | `#30363d` | 分隔线、描边 |

字体：中文用 SimSun，英文用 Times New Roman，代码用 Monaco。布局不要超出 x ∈ [-6.5, 6.5]、y ∈ [-3.5, 3.8]。

## Built with

- [Manim Community Edition](https://www.manim.community/) — 动画引擎
- Python 3.x
- conda 环境管理

## License

MIT
