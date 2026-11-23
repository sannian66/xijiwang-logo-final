# 西几王传媒 / XIJIWANG MEDIA Logo 动画 — 交接文档

更新：2026-11-23 19:55 (UTC+8)

## 1. 项目目标
用代码（SVG + CSS/JS）做狮子 logo 的品牌开场动画。风格：克制、高级、Apple/Google 感；Material 3 emphasized + ease-out-expo；不要旋转/弹跳/扫光等噱头。
交付规格：2560×1440、60fps、带音效；音频 −16 LUFS，True Peak ≤ −1.5 dBTP；bt709 limited range 编码（纯白解码 255）。
铁律：旧版本文件永不修改，每个新版本都用新文件名。

## 2. 最终版本（deliverables/）
| 版本 | 概念 | 独立审稿分数 | 文件 |
|---|---|---|---|
| **v4.2 光圈** | 8 片光圈叶片打开成狮脸，鼻子 ▶/❚❚ 可切换，下划线 = 进度条 | 5.5 → 7.8 → **8.2** | `xijiwang-logo-v4.2-aperture-intro-2K-60fps.mp4`、`-playpause-demo-2K-60fps.mp4`、`-interactive.html`、`-sfx.wav` |
| **v5.6 XJW** | 字母 X/J/W 变形成五官，▶ 按入左眼，鬃毛生长 | 6.2 → 6.8 → 7.4 → 8.0 → **8.4** | `xijiwang-logo-v5.6-xjw-intro-2K-60fps.mp4`（5.4s）、`-playpause-demo-2K-60fps.mp4`（14.2s）、`-interactive.html`、`-sfx.wav` |
| **v3.x 播放键** | ❚❚ → 光标点击 → 变 ▶ → ▶ 成为狮子鼻子 → 镜头拉远、狮子圆形展开 → 字标 | v3 5.2 → v3.1 7.0 → v3.2 7.8 → v3.3 8.1 → v3.4 **8.2**（无 P1，达标） | `xijiwang-logo-v3.4-play-2K-60fps-{light,dark}.mp4`、`-play.html`、`-sfx.wav`（v3.1–v3.3 也在） |
| 头像 | 1:1 白底，图标约占 66% | — | `xijiwang-avatar-v4.2.svg/-1024.png`、`xijiwang-avatar-v5.6.svg/-1024.png` |

用户已确认最终版只要 v4.2 和 v5.6（v3 系列是后加的迭代任务）。
已弃用：v4.1（径向同步光圈，无旋转）——用户明确否决，不要再用这个方向。

## 3. 进行中的工作：v3 迭代
- 目标：独立审稿 ≥ 8.2 且无 P1。
- v3.2 审稿（reviews/review-v32i/REVIEW.md）剩余问题：
  - P2-1：2.38–2.43s 有约 3 帧只见五官、不见头部 → 揭示圆起始半径 R0≈86 + .reveal 0.1s 淡入。
  - P2-2：揭示太快像"弹出" → 改 cubic(.05,.7,.1,1)，时长约 900ms。
  - P3：2.10–2.37s 空档（G0≈2200，按钮切换≈2.20s，圆环消失≈2.10，thump≈2.21）；亮度超范围（编码加 `lutyuv=y='clip(val,16,235)'`）；❚❚→▶ 变形加长到约 0.6s。
- v3.3 已在构建中（template33.html 等）；若仓库里没有 v3.3 文件，说明构建未完成，请从 template32.html 复制出 v3.3 按上面修复，渲染后再找独立审稿人打分。

## 4. 源码（source/）
- `source/anim/`：
  - 渲染器：`python3 render3.py <html> <帧目录> <"#dark"|""> 60 <时长秒> 2560`（playwright 逐帧 seek）。
  - v3.2：`template32.html` + `build32.py` + `morph32.py`（预计算变形关键帧）+ `sfx32.py`，脚本 `run32.sh` / `enc32.sh`。
  - v4.2：`template42.html` + `build42.py` + `sfx42.py`，`run8.sh`。
  - v5.6：`template56.html` + `build56.py`（读取 `v5src.svg`，N=360）+ `sfx56.py`，`run9.sh`。
  - 旧版本 template2/3/4/5/51… 以及对应 build/sfx 均保留。
- `source/avatar/mk.py`：头像生成。
- `assets/`：用户上传的原始 logo SVG（横版主 logo，#202624；v5 用的新版 #000 墨色）。

环境：`pip install svgpathtools playwright && playwright install chromium`；需要 ffmpeg、ImageMagick。

## 5. 编码命令（标准）
```
ffmpeg -framerate 60 -i 帧/f%04d.png -i sfx.wav \
 -vf scale=out_color_matrix=bt709:out_range=tv,format=yuv420p \
 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
 -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0 \
 -c:v libx264 -preset slow -crf 12 -c:a aac -b:a 320k out.mp4
```
音频验证：`ffmpeg -i x.wav -af ebur128=peak=true -f null -`

## 6. 坑点
- 带 SVG transform 属性的元素需 `transform-box: view-box; transform-origin: 0 0`，否则 Chrome 会偏移。
- 动画时间一改，对应音效事件时间必须同步改。
- CSS `d: path()` Safari 不支持 → v3.2 起用 JS setAttribute('d') 驱动。
- `animation-fill-mode: both` 会回填初始帧，曾导致 v3 入场动画失效，用 `forwards`。
- 结尾把动画元素切换回原始路径，可让最后一帧与源 SVG 像素级一致。
- 用户永远要 60fps；回复用中文。

## 7. 工作流
每版：改新文件 → 渲染亮/暗 → 编码 → 由**未参与制作**的独立审稿人打分（/10，分项：概念、工艺、节奏缓动、品牌还原、声音、明暗一致）→ 按 P1/P2/P3 修 → 新版本，循环至达标。审稿报告在 `reviews/`。

## 8. v3.3 更新（19:21）
- v3.3 已渲染并放入 deliverables/：修复了 2.4s 五官碎片（0 帧）、揭示改为平滑光圈、空档收紧、圆环中心对准 ▶、−16.0 LUFS / −2.3 dBTP，最后一帧与源 SVG 像素一致。
- **尚未独立审稿打分**（v3.2 为 7.8）。下一步：找未参与制作的审稿人给 v3.3 打分。
- 待查：2.425s 有一个未解释的音频起音；解码后边缘少量像素亮度超 16–235（x264 振铃，占比 ≤0.21%）；❚❚→▶ 变形加长到 0.6s 但体感变化不大，可换曲线。

## 9. v3.4 更新（19:55）— 达标 8.2，无 P1
- 审稿：v3.3 = 8.1（reviews/review-v33），v3.4 = **8.2**（reviews/review-v34）。分项：概念 7.7、工艺 8.6、节奏 7.9、品牌 9.0、声音 8.3、明暗 9.0。
- v3.4 改动（template34 / morph34 / sfx34 / build34 / enc34 / run34）：
  - 揭示：遮罩恒 r=128，`.reveal` 以鼻心为原点 scale .72→1（decel .7s，2.20s 起），仅 .05s 淡入；环 2.18s 起 .12s 淡出。
  - ❚❚→▶ 形变改 soft 曲线（morph34 默认 soft；build34 默认 RINGOFF=2.18，可直接复现）。
  - 两半合并成单一 path（同向绕行），f100 起无缝，无双边抗锯齿细缝。
  - 混响前高通 180Hz，2.41s 次低频 flam 消除；滑音改 smoothstep。
  - 去掉无效 lutyuv：超范围像素为 x264 振铃，亮 ≤0.24%、暗 ≤0.17%，在 EBU R103 容差内。
  - −16.0 LUFS / −2.4 dBTP；HTML 末帧与源 SVG 差 0。
- v3.5 候选（审稿预计约 8.5）：
  - P2-1(a) 镜头/环放大延后到 2.4s、时长 1.4s，让狮子先在静止镜头里长出来（现在被 2.8→1 拉远抵消，屏上只长 4%）；可能需把 `.lockup` 推迟到 3.45s。
  - P2-1(b) 环 `off .05s linear 2.2s`，与狮子淡入互补，消除 f134–f136 下巴下灰弧。
  - P2-1(c) 可选：环 2.05–2.20s 放大并上移贴合鬃毛（违背"环心=鼻心"，需拍板）。
  - P3：滑音改用与画面同一 bez(.4,0,.2,1)；▶ 光学偏左 2.2 单位。
- 构建：`cd source/anim && python3 build34.py template34.html v34.html && python3 sfx34.py sfx34.wav 7.5 && bash run34.sh v34.html v34 7.5 && bash enc34.sh v34l sfx34.wav light.mp4 450`
