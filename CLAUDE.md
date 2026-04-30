# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 **Manim CE 0.20.1** 的教学科普动画项目，在 Python 3.x + conda 环境下运行，无依赖文件。

## 常用命令

```bash
# 低质量快速预览
manim -pql path/to/file.py ClassName

# 高质量渲染（慢）
manim -pqh path/to/file.py ClassName

# 渲染指定帧范围
manim -pql path/to/file.py ClassName -n 0,3
```

## 架构约定

每个 `.py` 文件是**完全自包含**的视频脚本，各自独立渲染，不共享模块。文件内结构：

1. `COLORS` 字典 — 深色科技风配色（背景 `#0d1117`，表面 `#161b22`，边框 `#30363d`）
2. 工具函数 — `cn()`/`en()`/`mono()` 快捷创建中/英/等宽字体文字，`glass_card()` 创建毛玻璃卡片
3. 一个或多个继承 `Scene` 的类作为视频场景

### 两种场景组织方式

| 模式 | 示例 | 说明 |
|------|------|------|
| 单类多子场景 | `pid_control.py`, `digital_pid_control.py`, `git_version_control.py`, `CNN/cnn_pop_video.py`, `backpropagation/backprop_pop_video.py` | 一个 Scene 类按时间轴依次构建所有画面 |
| 多类多场景 | `gradient_loss_animation.py` | 10+ 个独立 Scene 类，每个是一个独立章节 |

`gradient_loss_animation.py` 使用多 Scene 模式时，需逐个渲染每个类，或用脚本串联。

### 主题文件

| 文件 | 主题 |
|------|------|
| `pid_control.py` | 模拟 PID 控制算法 |
| `digital_pid_control.py` | 数字 PID 控制（采样/保持/离散化） |
| `git_version_control.py` | Git 工作流程（add/commit/push/branch） |
| `gradient_loss_animation.py` | 红外-可见光图像融合方向感知梯度损失 |
| `CNN/cnn_pop_video.py` | 卷积神经网络科普 |
| `backpropagation/backprop_pop_video.py` | 反向传播算法科普 |
| `backpropagation/backprop_cover.py` | 反向传播视频封面 |

## 全局规范

- **字体**：中文 `SimSun`，英文 `Times New Roman`，代码 `Monaco`
- **布局边界**：x ∈ [-6.5, 6.5]，y ∈ [-3.5, 3.8]
- **输出**：`media/` 为 Manim 自动输出，`output_video/` 存放最终成品 MP4
- **编码原则**（来自 `.trae/Rules/行为指南.md`）：简单优先，只碰必须改的代码，不添加超出需求的内容
