# Harmonica Jianpu

[English](README.md) | **简体中文**

将单旋律五线谱转换为简谱，并生成适用于 12 孔 C 调半音阶口琴的演奏提示。

Harmonica Jianpu 是一款面向半音阶口琴初学者的网页工具。它可以将五线谱转换为易读的简谱，并标注 12 孔 C 调半音阶口琴的孔位、吹吸方式及按键提示。

## 项目范围

首个版本先实现一套可靠的基础流程：

- 导入 MusicXML 或压缩后的 MusicXML 文件（`.musicxml`、`.xml`、`.mxl`）。
- 安装本地 Audiveris OMR 后，可选择导入 PDF 或图片（`.pdf`、`.jpg`、`.jpeg`、`.png`）。
- 只转换单旋律乐谱。
- 输出固定为 `1=C` 的简谱，供 C 调半音阶口琴练习使用。
- 标注 12 孔 C 调半音阶口琴的孔位、吹吸方式和按键提示。
- 在生成的简谱旁预览 MusicXML 原谱，方便对照检查。

以下内容暂不纳入首个版本：

- 钢琴谱、伴奏、和弦或多声部复调。
- 全自动修正 OMR 识别错误。
- 为复杂乐段自动选择更合适的孔位。
- 商业部署或付费使用场景。

## 规划中的技术架构

- 前端：React + TypeScript。
- 后端：FastAPI + Python。
- 乐谱解析：先使用 `music21` 处理 MusicXML，后续可能考虑 `partitura`。
- 乐谱预览：OpenSheetMusicDisplay。
- 可选的 OMR：调用本地 Audiveris 命令行工具，将输入文件预处理为 MusicXML。
- 项目核心逻辑：统一音符事件格式、生成简谱，并映射 12 孔 C 调半音阶口琴孔位。

## 项目简介

Harmonica Jianpu 是一款为 12 孔 C 调半音阶口琴初学者准备的五线谱转简谱工具。现阶段优先支持 MusicXML/MXL 格式的单旋律乐谱，生成固定为 `1=C` 的简谱，同时给出孔位、吹吸和按键提示。PDF 和图片五线谱可通过后续接入的 OMR 流程处理，但识别结果仍需人工校对。

## 开发环境

运行项目需要：

- Python 3.11 或更高版本
- Node.js 20 或更高版本

配置并启动后端：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

后端 API 默认运行在 `http://127.0.0.1:8000`。

配置并启动前端：

```powershell
cd frontend
npm install
npm run dev
```

前端页面默认运行在 `http://127.0.0.1:5173`。
如果 Windows PowerShell 的脚本执行策略阻止运行 npm，请将命令中的 `npm` 换成 `npm.cmd`。

## 可选的 PDF/图片 OMR

上传 PDF 和图片需要本地安装 Audiveris。Harmonica Jianpu 不附带或重新分发 Audiveris。

第一版 OMR 有以下限制：

- 只适合清晰的印刷版单旋律乐谱。
- PDF 最多 3 页。
- 上传文件不能超过 15 MB。
- OMR 默认超时时间为 120 秒。
- 即使没有安装 Audiveris，仍然可以正常上传 MusicXML/MXL 文件。

环境变量：

```powershell
$env:AUDIVERIS_CMD = "C:\Path\To\Audiveris\bin\Audiveris.bat"
$env:OMR_MAX_FILE_MB = "15"
$env:OMR_MAX_PDF_PAGES = "3"
$env:OMR_TIMEOUT_SECONDS = "120"
```

如果 OMR 识别失败，可以直接用 Audiveris 打开乐谱，检查或修改识别结果。导出 MusicXML 后，再将文件上传到本工具。

运行测试：

```powershell
cd backend
python -m pytest -q
```

```powershell
cd frontend
npm run test
npm run build
```

手动检查基本功能：

1. 分别启动后端和前端。
2. 打开 `http://127.0.0.1:5173`。
3. 上传 `backend/tests/fixtures/c_major_scale.musicxml`。
4. 确认左侧能显示原谱；右侧简谱以 `1 2 3 4` 开头，口琴提示以 `1吹 1吸 2吹 2吸` 开头，并且没有出现警告。

## 许可证

本项目采用 Apache License 2.0 许可证。

Audiveris、homr 等可选 OMR 工具可能采用其他许可证，其中包括 AGPL-3.0。启用这些工具时，请另行遵守相应的许可证要求。
