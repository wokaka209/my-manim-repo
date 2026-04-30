
# CNN 科普视频工程

## 文件说明

- `cnn_pop_video.py`：基于 manim 社区库的卷积神经网络科普视频实现
- `cnn_voiceover_template.py`：带 AI 自动配音的最小模板，适合直接替换旁白和场景
- `video_script.md`：中文分镜与旁白脚本

## 渲染命令

```powershell
manim -pqh CNN/cnn_pop_video.py CNNPopularizationVideo
```

## 自动配音模板

先安装语音依赖：

```powershell
pip install manim-voiceover gTTS
```

渲染模板场景：

```powershell
manim -pqh CNN/cnn_voiceover_template.py CNNVoiceoverTemplate
```

说明：

- 模板默认使用 `GTTSService(lang="zh-CN")` 生成中文配音。
- 每段动画都绑定到 `tracker.duration`，修改旁白后时长会自动重算。
- 如果你后面要换更自然的配音，只需要替换 `set_speech_service(...)`，不用重写整套场景结构。

## 说明

- 实现不依赖外部图片素材，全部使用 manim 原生图形构建。
- 代码组织方式参考了当前工作区已有 `.py` 文件的风格：统一配色、工具函数、`scene_xxx()` 串联主视频。
