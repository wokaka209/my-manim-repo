中文 | **[English](README.md)**

# Manim 教学动画

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=fff)
![Manim](https://img.shields.io/badge/Manim_CE-0.20.1-0A0A0A?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

课程作业动画合集。PID 控制、Git 工作流、CNN、反向传播——全部 Manim CE 渲染，统一深色科技风。

## 目录

- [这是什么](#这是什么)
- [文件结构](#文件结构)
- [跑起来](#跑起来)
- [风格规范](#风格规范)
- [用到的东西](#用到的东西)
- [许可协议](#许可协议)

## 这是什么

课程作业和演示用的 Manim 动画脚本。每个 `.py` 文件完全独立，不依赖其他模块，跑一个文件出一个视频。

内容覆盖控制理论（模拟和数字 PID）、版本控制（Git add/commit/push/branch）、深度学习（CNN、反向传播）、图像融合（方向感知梯度损失）。

## 文件结构

```
manim/
├── pid_control.py              # 模拟 PID 控制，从 P 到 PD 到完整 PID
├── digital_pid_control.py      # 数字 PID：采样、保持、离散化
├── git_version_control.py      # Git 工作流可视化
├── gradient_loss_animation.py  # 红外-可见光图像融合的梯度损失
├── CNN/
│   └── cnn_pop_video.py        # 卷积神经网络科普，从卷积核到全连接
├── backpropagation/
│   ├── backprop_pop_video.py   # 前向传播 + 反向传播完整推导
│   └── backprop_cover.py       # 封面图渲染
├── media/                      # Manim 自动生成，不用管
└── output_video/               # 最终成品 MP4
```

每个脚本内部结构都一样：顶部 `COLORS` 字典定义配色，中间 `cn()`/`en()`/`mono()` 是文字快捷函数，底部一个或多个 `Scene` 类是实际画面。

## 跑起来

```bash
# 低质量快速预览（几秒出结果）
manim -pql pid_control.py PIDScene

# 高质量渲染（慢，适合最终输出）
manim -pqh pid_control.py PIDScene

# 只渲染前 3 秒，调试用
manim -pql pid_control.py PIDScene -n 0,3
```

需要 Python 3.x 和 [Manim CE](https://docs.manim.community/en/stable/installation.html)。装好 manim 就行，没有额外依赖。

## 风格规范

所有动画统一用深色科技风，别乱改配色：

| 元素 | 颜色 | 用途 |
|------|------|------|
| 背景 | `#0d1117` | 画布底色 |
| 表面 | `#161b22` | 卡片、面板 |
| 边框 | `#30363d` | 分隔线、描边 |

字体：中文用 SimSun，英文用 Times New Roman，代码用 Monaco。布局不要超出 x ∈ [-6.5, 6.5]、y ∈ [-3.5, 3.8]。

## 用到的东西

- [Manim Community Edition](https://www.manim.community/) — 动画引擎
- Python 3.x
- conda 环境管理

## 许可协议

MIT
