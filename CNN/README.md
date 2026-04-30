
# CNN 科普视频工程

## 文件说明

- `cnn_pop_video.py`：基于 manim 社区库的卷积神经网络科普视频实现
- `video_script.md`：中文分镜与旁白脚本

## 渲染命令

```powershell
manim -pqh CNN/cnn_pop_video.py CNNPopularizationVideo
```

## 说明

- 实现不依赖外部图片素材，全部使用 manim 原生图形构建。
- 代码组织方式参考了当前工作区已有 `.py` 文件的风格：统一配色、工具函数、`scene_xxx()` 串联主视频。
