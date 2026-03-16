<p align="center">
  <h1 align="center">Liquid</h1>
  <p align="center">
    Voice-first AI agent platform powered by DigitalOcean Gradient™ AI
    <br />
    <em>Speak naturally. Get real-time spoken responses. Text always available.</em>
  </p>
  <p align="center">
    <a href="https://github.com/Agentscreator/Liquid-AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License"></a>
    <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python 3.11+">
    <img src="https://img.shields.io/badge/node-20%2B-339933?logo=node.js&logoColor=white" alt="Node 20+">
    <img src="https://img.shields.io/badge/DigitalOcean-Gradient_AI-0080FF?logo=digitalocean&logoColor=white" alt="DigitalOcean Gradient AI">
    <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black" alt="React 18">
  </p>
</p>

<br />

## Overview

Liquid is a voice-first AI agent platform built on [DigitalOcean Gradient™ AI Platform](https://www.digitalocean.com/products/gradient/platform). Instead of typing commands and reading text, you speak — and Liquid speaks back in real time. A full text interface is always available alongside voice.

Under the hood, Liquid runs a session-based multi-agent framework with a real-time graph executor, encrypted credential management, and live observability via Server-Sent Events — all powered by DigitalOcean's Gradient Serverless Inference and Agent Inference APIs.

<br />

## 🌊 DigitalOcean Gradient™ AI Integration

Liquid is deeply integrated with DigitalOcean's Gradient AI Platform across the full stack:

| Integration Point | How Liquid Uses It |
|:---|:---|
| **Serverless Inference** | All LLM calls route through Gradient's serverless endpoint (`inference.do-ai.run/v1`) using models like `llama3.3-70b-instruct`, `deepseek-r1`, and others — no GPU provisioning needed |
| **Agent Inference** | Managed agents with knowledge bases, guardrails, and multi-agent routing via the Gradient Agent API |
| **Gradient Python SDK** | Native `gradient` SDK integration (`pip install gradient`) for both sync and async inference with streaming SSE support |
| **App Platform Deployment** | One-click deploy to DigitalOcean App Platform with auto-build from GitHub, health checks, and secret management |
| **Single API Key** | One `GRADIENT_MODEL_ACCESS_KEY` accesses all supported models (OpenAI, Anthropic, Meta, Mistral, DeepSeek) through a unified endpoint |
| **Data Privacy** | When using open-source models, data stays within DigitalOcean infrastructure — never used for training |

### How It Works with Gradient

```
User speaks → Browser captures audio → WebSocket streams to backend
           → Backend calls Gradient Serverless Inference API
           → Model returns response via streaming SSE
           → Audio plays back in real time + transcript in chat
           → Queen agent orchestrates workers via Gradient Agent Inference
```

The Gradient Python SDK (`from gradient import Gradient`) powers all LLM interactions:
- **Serverless Inference** for direct model calls with `GRADIENT_MODEL_ACCESS_KEY`
- **Agent Inference** for managed agent workflows with `GRADIENT_AGENT_ACCESS_KEY`
- **Streaming** via SSE for real-time token delivery to the frontend

<br />

## ✨ Features

<table>
  <tr>
    <td>🎙️&nbsp;&nbsp;<strong>Voice-First Interaction</strong></td>
    <td>Click the mic, speak, and hear real-time spoken responses powered by Gradient AI inference</td>
  </tr>
  <tr>
    <td>⌨️&nbsp;&nbsp;<strong>Text Always Available</strong></td>
    <td>Type in the chat input at any time — voice and text work side by side</td>
  </tr>
  <tr>
    <td>⚡&nbsp;&nbsp;<strong>Low-Latency Streaming</strong></td>
    <td>Bidirectional audio via WebSocket with Gradient SSE streaming for token delivery</td>
  </tr>
  <tr>
    <td>🤖&nbsp;&nbsp;<strong>Multi-Agent Graphs</strong></td>
    <td>Define goal-driven agents as node graphs; a Queen agent orchestrates workers via Gradient Agent Inference</td>
  </tr>
  <tr>
    <td>🔄&nbsp;&nbsp;<strong>Self-Improving Agents</strong></td>
    <td>On failure, the framework captures data, evolves the graph, and redeploys</td>
  </tr>
  <tr>
    <td>📡&nbsp;&nbsp;<strong>Real-Time Observability</strong></td>
    <td>Live SSE streaming of agent execution, node states, and decisions</td>
  </tr>
  <tr>
    <td>🧑‍💻&nbsp;&nbsp;<strong>Human-in-the-Loop</strong></td>
    <td>Intervention nodes pause execution for human input with configurable timeouts</td>
  </tr>
  <tr>
    <td>🔐&nbsp;&nbsp;<strong>Credential Management</strong></td>
    <td>Encrypted API key storage — add once, available everywhere</td>
  </tr>
  <tr>
    <td>🌊&nbsp;&nbsp;<strong>DigitalOcean Native</strong></td>
    <td>Deploy to App Platform, inference via Gradient, secrets managed by DO — fully integrated</td>
  </tr>
</table>

<br />

## 🛠 Tech Stack

| Layer | Technology |
|:------|:-----------|
| AI Inference | [DigitalOcean Gradient™ AI](https://www.digitalocean.com/products/gradient/platform) — Serverless Inference + Agent Inference |
| Gradient SDK | `pip install gradient` / `npm install @digitalocean/gradient` |
| Agent Runtime | Python 3.11 · aiohttp · async graph executor |
| Frontend | React 18 · TypeScript · Tailwind CSS · Vite |
| Streaming | WebSocket (voice) · Server-Sent Events (agent events) |
| LLM Models | Llama 3.3, DeepSeek, Mistral, GPT-4o, Claude — all via single Gradient endpoint |
| Deployment | DigitalOcean App Platform · Docker |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

<br />

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- A DigitalOcean account with Gradient AI access — [sign up here](https://cloud.digitalocean.com/registrations/new)
- A Gradient Model Access Key — [create one here](https://cloud.digitalocean.com/gradient-ai/serverless-inference)

### 1. Clone and install

```bash
git clone https://github.com/Agentscreator/Liquid-AI.git
cd Liquid-AI
./quickstart.sh
```

The quickstart script sets up:
- Agent runtime and graph executor (`core/.venv`)
- MCP tools for agent capabilities (`tools/.venv`)
- Encrypted credential store (`~/.hive/credentials`)
- All Python dependencies via `uv`

### 2. Add your Gradient API key

Create a `.env` file in the project root:

```bash
# Required: Gradient Serverless Inference key
echo "GRADIENT_MODEL_ACCESS_KEY=your_key_here" > .env

# Optional: Gradient Agent Inference (for managed agents)
echo "GRADIENT_AGENT_ACCESS_KEY=your_agent_key" >> .env
echo "GRADIENT_AGENT_ENDPOINT=your_agent_endpoint" >> .env
```

Or add it through the UI after starting: **Settings → Credentials → Add GRADIENT_MODEL_ACCESS_KEY**

### 3. Configure Gradient as your LLM provider

Create or edit `~/.hive/configuration.json`:

```json
{
  "llm": {
    "provider": "gradient",
    "model": "llama3.3-70b-instruct",
    "api_key_env_var": "GRADIENT_MODEL_ACCESS_KEY"
  }
}
```

Available Gradient models include: `llama3.3-70b-instruct`, `deepseek-r1`, `mistral-small-3.1-24b-instruct`, and [many more](https://docs.digitalocean.com/products/gradient-ai-platform/how-to/use-serverless-inference/).

### 4. Start the server

```bash
cd core
uv sync
uv run hive server
```

Open [http://localhost:8000](http://localhost:8000) and you're ready to go.

<br />

## 🎙️ Voice

1. Open a session in the workspace
2. Click the mic button next to the text input
3. Speak — the mic pulses red while listening
4. Liquid responds with audio; the speaker icon shows while it speaks
5. Click the mic again (or the stop button) to end the voice session

Voice transcripts appear in the chat alongside text messages, so you always have a full written record.

<br />

## 🌊 Deploy to DigitalOcean

### Option A: App Platform (recommended)

```bash
# Install doctl CLI
brew install doctl    # macOS
doctl auth init       # authenticate

# Deploy with the included app spec
doctl apps create --spec do-app-spec.yaml
```

Or use the deploy script:

```bash
GRADIENT_MODEL_ACCESS_KEY=your_key ./deploy-digitalocean.sh
```

### Option B: Docker on a Droplet

```bash
docker build -t liquid .
docker run -p 8787:8787 \
  -e GRADIENT_MODEL_ACCESS_KEY=your_key \
  liquid
```

<br />

## 🏗 Architecture

Liquid uses a **Queen + Worker** agent pattern, with all inference routed through DigitalOcean Gradient:

| Component | Role |
|:----------|:-----|
| Queen | Orchestrates conversation, delegates tasks, monitors worker output via Gradient Agent Inference |
| Workers | Execute specific goals as node graphs with tools, memory, and LLM access via Gradient Serverless Inference |
| Judge | Evaluates worker output against defined criteria and escalates failures |
| Event Bus | Pub/sub system streaming 25+ event types to the frontend in real time |
| Gradient Provider | Custom LLM provider (`framework/llm/gradient.py`) wrapping the official Gradient Python SDK |

<br />

## 📁 Project Structure

```
Liquid-AI/
├── core/
│   ├── framework/            # Agent runtime, graph executor, API server
│   │   ├── server/           # aiohttp routes (REST + SSE + WebSocket)
│   │   ├── llm/              # LLM providers (Gradient, LiteLLM, Anthropic)
│   │   │   └── gradient.py   # DigitalOcean Gradient™ AI provider
│   │   └── runtime/          # Graph executor, event bus, session management
│   └── frontend/             # React + TypeScript UI
│       └── src/
│           ├── components/   # ChatPanel, VoiceButton, AgentGraph, TopBar…
│           ├── hooks/        # useVoice, useSSE, useMultiSSE
│           └── pages/        # Home, Workspace, My Agents
├── tools/                    # MCP tool server
├── exports/                  # Your saved agents
├── examples/                 # Template agents
├── deploy-digitalocean.sh    # DigitalOcean App Platform deploy script
├── do-app-spec.yaml          # App Platform specification
├── docs/                     # Architecture docs and guides
└── .env                      # Your API keys (gitignored)
```

<br />

## ⚙️ Configuration

| Variable | Required | Description |
|:---------|:---------|:------------|
| `GRADIENT_MODEL_ACCESS_KEY` | Yes | DigitalOcean Gradient Serverless Inference key |
| `GRADIENT_AGENT_ACCESS_KEY` | No | Gradient Agent Inference key (for managed agents) |
| `GRADIENT_AGENT_ENDPOINT` | No | Gradient Agent endpoint URL |
| `GOOGLE_API_KEY` | No | Gemini Live API access for voice features |
| `ANTHROPIC_API_KEY` | No | Enables Claude models (also available via Gradient) |
| `OPENAI_API_KEY` | No | Enables GPT models (also available via Gradient) |
| `HIVE_CREDENTIAL_KEY` | Auto | Auto-generated key that encrypts the credential store |

<br />

## 🧩 Building Agents

Agents live in `exports/` as Python packages. Each agent defines a node graph in `graph_spec.py`:

```python
graph = GraphSpec(
    nodes=[
        Node(id="my_node", system_prompt="You are a helpful assistant."),
    ]
)
```

Or describe the agent you want in the home input — the Queen agent generates the graph and wiring automatically, using Gradient inference to power every step.

<br />

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push and open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

<br />

## 🔒 Security

For security concerns, see [SECURITY.md](SECURITY.md).

> Never commit your `.env` file or API keys. The `.env` file is gitignored by default.

<br />

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
