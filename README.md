# Harmonica Jianpu

Convert single-line sheet music into jianpu and playing guidance for 12-hole C chromatic harmonica.

Harmonica Jianpu is a learning-oriented web tool for chromatic harmonica beginners. It converts staff notation into beginner-friendly numbered musical notation and adds 12-hole C chromatic harmonica guidance, including hole number, breath direction, and slide usage.

## Project Scope

The first version focuses on a reliable core workflow:

- Import MusicXML or compressed MusicXML (`.musicxml`, `.xml`, `.mxl`).
- Convert single-line melodies only.
- Render output as `1=C` jianpu for C chromatic harmonica practice.
- Add 12-hole C chromatic harmonica hole, breath, and slide hints.
- Preview the original score beside the generated jianpu for checking.
- Treat PDF/image optical music recognition as an optional later workflow.

Out of scope for the first version:

- Piano scores, accompaniment, chords, or multi-voice counterpoint.
- Fully automatic correction of OMR mistakes.
- Advanced fingering optimization across complex passages.
- Commercial deployment or paid usage.

## Planned Architecture

- Frontend: React + TypeScript.
- Backend: FastAPI + Python.
- Score parsing: MusicXML via `music21` first, with `partitura` as a possible alternative.
- Score preview: OpenSheetMusicDisplay.
- Optional OMR: Audiveris as the primary candidate, with oemer as an experimental alternative.
- Core project logic: normalized note events, jianpu rendering, and 12-hole C chromatic harmonica mapping.

## Chinese Summary

Harmonica Jianpu 是一个面向 12 孔 C 调半音阶口琴初学者的五线谱转简谱工具。项目第一版会优先支持 MusicXML/MXL 单旋律乐谱，并生成固定 `1=C` 的简谱，同时提供孔位、吹吸和按键提示。PDF/图片五线谱会作为后续可选 OMR 流程接入，并保留人工校对环节。

## Development

Prerequisites:

- Python 3.11+
- Node.js 20+

Backend setup:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The backend API runs at `http://127.0.0.1:8000` by default.

Frontend setup:

```powershell
cd frontend
npm install
npm run dev
```

The frontend app runs at `http://127.0.0.1:5173` by default.
On Windows PowerShell, use `npm.cmd` instead of `npm` if script execution policy blocks npm commands.

Verification:

```powershell
cd backend
python -m pytest -q
```

```powershell
cd frontend
npm run test
npm run build
```

Manual smoke test:

1. Start the backend and frontend in two terminals.
2. Open `http://127.0.0.1:5173`.
3. Upload `backend/tests/fixtures/c_major_scale.musicxml`.
4. Confirm that the score preview renders, the jianpu starts with `1 2 3 4`, harmonica hints start with `1吹 1吸 2吹 2吸`, and no warnings are shown.

## License

This project is licensed under the Apache License 2.0.

Optional OMR tools such as Audiveris or homr may use different licenses, including AGPL-3.0. If those tools are enabled, their license requirements must be followed separately.
