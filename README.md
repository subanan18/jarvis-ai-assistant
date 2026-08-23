<div align="center">

# 🤖 JARVIS AI Desktop Assistant

### Voice-Activated • Agentic AI • Python • Real-Time Assistant

A personal AI desktop assistant built to explore **voice interfaces, AI agents, tool use and intelligent automation**.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-Realtime-000000?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Agentic_Systems-6C63FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In_Development-orange?style=for-the-badge)

</div>

---

## 🧠 Overview

JARVIS is an experimental **voice-first AI assistant for Windows** designed to behave more like a persistent desktop assistant than a traditional chatbot.

The project combines wake-word detection, real-time voice interaction and agent-style tooling so the assistant can listen for activation, respond naturally and eventually perform useful actions on the computer.

> 🚧 **Active project:** The system is under development. This repository will be updated as features are stabilised and prepared for public release.

---

## ✨ Current Features

- 🎙️ Voice-first interaction
- 🗣️ **"Hey Jarvis"** wake-word activation
- ⚡ Real-time conversational agent architecture
- 🧠 AI assistant reasoning/conversation layer
- 💤 Sleep / wake workflow experimentation
- 🖥️ Windows desktop integration
- 🔇 Background operation experiments
- 🛠️ Foundation for tool calling and desktop actions

---

## 🏗️ Architecture

```text
              ┌──────────────────────┐
              │      Microphone      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Wake Word Detection  │
              │     "Hey Jarvis"     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Realtime AI Agent  │
              │      LiveKit         │
              └──────────┬───────────┘
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
      ┌─────────────────┐  ┌─────────────────┐
      │ Voice Response  │  │  Agent Tools    │
      └─────────────────┘  └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Desktop Actions │
                           └─────────────────┘
```

---

## 🛠️ Technology

| Area | Technology |
|---|---|
| Language | Python |
| Realtime agent framework | LiveKit Agents |
| Wake word | OpenWakeWord |
| Audio | 16 kHz mono voice pipeline |
| Platform | Windows |
| Architecture | Event-driven / agent-based |

---

## 🎯 Project Goals

The long-term goal is to build a desktop AI system that can:

- Stay available in the background
- Activate naturally through voice
- Understand conversational requests
- Use tools instead of only generating text
- Assist with coding and productivity workflows
- Interact with desktop applications safely
- Maintain a modular architecture for new capabilities

---

## 🗺️ Roadmap

- [x] Basic real-time AI agent
- [x] Wake-word detection
- [x] Voice activation workflow
- [ ] Reliable sleep / wake state management
- [ ] Background startup on Windows
- [ ] Desktop application controls
- [ ] Coding assistant tools
- [ ] Context and memory layer
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] More agent tools and automations
- [ ] Security and permission controls
- [ ] Public installation guide

---

## 🔐 Security

API credentials and service secrets should **never be committed to this repository**.

When source code is published, configuration will use environment variables and an example environment file rather than real credentials.

```text
.env
*.key
credentials.json
```

These files should remain excluded through `.gitignore`.

---

## 💡 What This Project Demonstrates

This project is an opportunity to work with concepts beyond standard web CRUD development, including:

`Agentic AI` • `Realtime Systems` • `Voice AI` • `Event-Driven Programming` • `Tool Calling` • `Python` • `Desktop Automation`

---

## 👨‍💻 Author

**Subanan Subathevan**

[![GitHub](https://img.shields.io/badge/GitHub-subanan18-181717?style=for-the-badge&logo=github)](https://github.com/subanan18)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-000000?style=for-the-badge&logo=vercel)](https://subanan18.github.io/)

---

<div align="center">

### ⭐ Follow the project as JARVIS evolves into a more capable agentic desktop assistant.

</div>
