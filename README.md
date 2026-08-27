<div align="center">

# 🤖 JARVIS AI Desktop Assistant

### Wake-word activated • Realtime voice AI • Safe desktop tools • Python

A Windows desktop assistant built around a **Hey Jarvis** wake-word loop, LiveKit realtime voice agents, persistent local memory, controlled desktop actions, weather/search tools, and a lightweight animated UI.

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-Realtime-000000?style=for-the-badge)
![CI](https://img.shields.io/github/actions/workflow/status/subanan18/jarvis-ai-assistant/ci.yml?branch=main&style=for-the-badge&label=CI)
![Status](https://img.shields.io/badge/Status-Active_Development-orange?style=for-the-badge)

</div>

## Why this project

JARVIS explores how a voice assistant can move beyond chat and behave like a small desktop agent. The project focuses on realtime interaction, process lifecycle management, tool safety, local memory, and Windows integration.

## Architecture

```text
Microphone
   │
   ▼
OpenWakeWord ("Hey Jarvis")
   │
   ▼
LiveKit realtime agent
   │
   ├── local JSON memory
   ├── weather (Open-Meteo)
   ├── browser/search
   ├── allow-listed Windows apps
   └── controlled Python-file creation
   │
   ▼
"Go to sleep"
   │
   └── session closes → wake listener resumes
```

## Current features

- 🎙️ Continuous **Hey Jarvis** wake-word detection using OpenWakeWord
- ⚡ Realtime conversational agent using LiveKit Agents + Google realtime model
- 🧠 Persistent local key/value memory with remember, recall and forget tools
- 💤 Explicit sleep command that returns control to the wake-word listener
- 🌦️ Current weather lookup using Open-Meteo
- 🌐 Website opening and Google search
- 🖥️ Controlled Windows application launching through an explicit allow-list
- 💻 Python-file creation restricted to `generated_projects/`
- ✨ PySide6 animated JARVIS orb UI
- 🪟 Visible and hidden Windows launch scripts

## Security decisions

The assistant does **not** execute arbitrary shell commands from model output. Desktop application launching is restricted to an allow-list, and generated Python files are constrained to a dedicated workspace. Credentials are read from `.env.local`, which is excluded from Git.

## Project structure

```text
app/
├── agent.py          # LiveKit agent and tool definitions
├── memory_store.py   # JSON-backed local memory
├── ui.py             # PySide6 animated orb
└── wake_listener.py  # OpenWakeWord lifecycle loop
scripts/
└── download_wake_models.py
tests/
generated_projects/
.github/workflows/ci.yml
```

## Setup

### 1. Create a virtual environment

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env.local` and add your own LiveKit and Google credentials.

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
GOOGLE_API_KEY=your_google_api_key
```

Never commit `.env.local`.

### 3. Download wake-word models

```powershell
python scripts/download_wake_models.py
```

### 4. Run JARVIS

```powershell
python -m app.wake_listener
```

Or use `start_jarvis.bat`. `start_jarvis_hidden.vbs` launches the listener without a console window.

## Example interaction

```text
User:   Hey Jarvis
Jarvis: Hello. How can I help?

User:   What's the weather in London?
Jarvis: [uses weather tool]

User:   Open VS Code
Jarvis: [uses approved application launcher]

User:   Remember that my project deadline is Friday
Jarvis: [stores local memory]

User:   Go to sleep
Jarvis: Going to sleep.
         → realtime session closes
         → wake-word listener resumes
```

## Engineering highlights

`Realtime voice systems` • `Agent tool calling` • `Wake-word detection` • `Async Python` • `Process lifecycle management` • `Security boundaries` • `Persistent state` • `Windows automation`

## Roadmap

- [x] Realtime voice agent
- [x] Wake-word detection
- [x] Sleep → wake-listener lifecycle
- [x] Local persistent memory
- [x] Safe desktop application allow-list
- [x] Weather/search tools
- [x] Controlled Python-file generation
- [ ] Connect the animated UI to realtime agent state
- [ ] Add richer permission controls for desktop actions
- [ ] Add RAG/context sources
- [ ] Add more unit/integration coverage
- [ ] Package as an installable Windows app
- [ ] Add demo GIF/video and screenshots

## Author

**Subanan Subathevan** — Computer Science graduate focused on Python, backend engineering, realtime systems and applied AI.

[Portfolio](https://subanan18.github.io/) · [GitHub](https://github.com/subanan18)
