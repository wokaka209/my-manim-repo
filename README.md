# Manim Teaching Animations

A collection of educational and science-popularization animations built with [Manim Community Edition](https://www.manim.community/) 0.20.1.

## Topics

| File | Topic |
|------|-------|
| `pid_control.py` | Analog PID Control Algorithm |
| `digital_pid_control.py` | Digital PID Control (Sampling / Hold / Discretization) |
| `git_version_control.py` | Git Workflow (add / commit / push / branch) |
| `gradient_loss_animation.py` | Direction-Aware Gradient Loss for Infrared-Visible Image Fusion |
| `CNN/cnn_pop_video.py` | Convolutional Neural Network Explained |
| `backpropagation/backprop_pop_video.py` | Backpropagation Algorithm Explained |
| `backpropagation/backprop_cover.py` | Backpropagation Video Cover |

## Quick Start

```bash
# Low quality preview (fast)
manim -pql path/to/file.py ClassName

# High quality render (slow)
manim -pqh path/to/file.py ClassName

# Render specific frame range
manim -pql path/to/file.py ClassName -n 0,3
```

## Environment

- Python 3.x + conda
- Manim CE 0.20.1

## Style Guide

- Dark tech theme: background `#0d1117`, surface `#161b22`, border `#30363d`
- Chinese font: SimSun
- English font: Times New Roman
- Code font: Monaco
- Layout bounds: x in [-6.5, 6.5], y in [-3.5, 3.8]
