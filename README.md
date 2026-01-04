# 🚀 InfraGenius

**AI-Powered Infrastructure Automation Agent**

InfraGenius is an intelligent infrastructure automation agent that lets you deploy applications to cloud environments using natural language. Simply tell it what you want to deploy, and it handles the entire process - provisioning servers, cloning repos, installing dependencies, building, and serving your app.

## 🎯 Why InfraGenius?

**The Problem:** Deploying applications to cloud infrastructure requires multiple manual steps - spinning up servers, SSH access, running commands, configuring services. This is time-consuming and error-prone.

**The Solution:** InfraGenius acts as your DevOps assistant. Just tell it:
> "Deploy https://github.com/myapp/repo to 2 sandboxes and verify they're live"

And it will:
1. Provision cloud sandboxes
2. Clone your repository
3. Install dependencies
4. Build the application
5. Start the server
6. Verify the URLs are accessible
7. Report back with live URLs

## 🏆 Holiday AI Build-Off 2025 - OpenAgents Track

This project is built for the [Holiday AI Build-Off 2025](https://holiday-ai-buildoff.devpost.com/) hackathon, specifically the **OpenAgents Track**.

**Track Requirements:**
- Build an agent using the OpenAgents framework
- Demonstrate multi-agent capabilities
- Show real-world utility

**What InfraGenius Demonstrates:**
- Natural language to infrastructure automation
- Tool-calling with real cloud APIs (E2B)
- Multi-step orchestration (provision → deploy → verify)
- Real deployments with live URLs

## ✨ Features

- **Natural Language Interface** - No CLI commands to memorize, just describe what you want
- **Cloud Sandboxes** - Uses E2B for instant, isolated cloud environments
- **Full Deploy Pipeline** - Clone, install, build, serve - all automated
- **Multi-Sandbox Support** - Deploy to multiple environments simultaneously
- **Health Verification** - Automatically checks if deployments are live
- **Latency Monitoring** - Measure response times across deployments

## 🛠️ How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenAgents Studio                         │
│                   (Chat UI @ :8700)                          │
│                                                              │
│  User: "Deploy my-app to 2 sandboxes"                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  InfraGenius Agent                           │
│              (CollaboratorAgent)                             │
│                                                              │
│  • Understands natural language requests                     │
│  • Plans deployment steps                                    │
│  • Orchestrates tool execution                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Provider                              │
│           (Nebius / Llama-3.3-70B-Instruct)                 │
│                                                              │
│  • Interprets user intent                                    │
│  • Generates tool calls                                      │
│  • Produces human-readable responses                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Tools                         │
│                  (tools/infra.py)                            │
│                                                              │
│  provision_sandbox() ──► E2B API ──► Cloud VM               │
│  run_command()       ──► Execute shell commands              │
│  deploy_app()        ──► Full deployment pipeline            │
│  verify_url()        ──► HTTP health checks                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   E2B Sandboxes                              │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ sandbox-1│  │ sandbox-2│  │ sandbox-3│                   │
│  │ :8000    │  │ :8000    │  │ :8000    │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │             │             │                          │
│       ▼             ▼             ▼                          │
│   Live URL      Live URL      Live URL                       │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `provision_sandbox` | Create a new E2B cloud sandbox | `name` - friendly name |
| `list_sandboxes` | Show all active sandboxes | none |
| `run_command` | Execute shell command in sandbox | `sandbox_name`, `command` |
| `deploy_app` | Full deploy: clone → install → build → serve | `sandbox_name`, `repo_url` |
| `verify_url` | Check if URL returns HTTP 200 | `url` |
| `check_latency` | Measure response time | `url`, `samples` (optional) |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [OpenAgents](https://github.com/bestagents/openagents) 0.8.5
- [E2B](https://e2b.dev) API key (for cloud sandboxes)
- LLM API key (Nebius, OpenAI, or Groq)

### Installation

```bash
pip install openagents==0.8.5 e2b-code-interpreter requests
```

### Configuration

1. Copy `.env.example` to `.env` and add your API keys:
```bash
E2B_API_KEY=your-e2b-key
CUSTOM_API_KEY=your-llm-api-key
```

2. The agent is configured in `agents/deployer.yaml`

### Running

**Terminal 1 - Start the OpenAgents Network:**
```bash
openagents network start .
```

**Terminal 2 - Start the InfraGenius Agent:**
```bash
# Windows PowerShell
.\start_agent.ps1

# Or manually:
$env:E2B_API_KEY = "your-key"
$env:CUSTOM_API_KEY = "your-key"
openagents agent start ./agents/deployer.yaml
```

**Open the Studio UI:** http://localhost:8700/studio

### Example Commands

```
"Provision a sandbox called my-app"

"Deploy https://github.com/user/repo to sandbox my-app"

"Check if https://8000-xyz.e2b.app is live"

"Deploy my app to 3 sandboxes and verify all URLs"
```

## 📁 Project Structure

```
infra-genius/
├── agents/
│   └── deployer.yaml       # Agent configuration (model, tools, prompts)
├── tools/
│   └── infra.py            # E2B deployment tools
├── network.yaml            # OpenAgents network config
├── start_agent.ps1         # Windows startup script
├── .env.example            # Environment variables template
└── README.md
```

## 🔧 Configuration

### Agent Config (`agents/deployer.yaml`)

```yaml
config:
  model_name: "meta-llama/Llama-3.3-70B-Instruct"
  provider: "custom"
  api_base: "https://api.tokenfactory.nebius.com/v1/"
```

### Supported LLM Providers

| Provider | Config |
|----------|--------|
| Nebius | `provider: "custom"`, `api_base: "https://api.tokenfactory.nebius.com/v1/"` |
| OpenAI | `provider: "openai"` |
| Groq | `provider: "custom"`, `api_base: "https://api.groq.com/openai/v1"` |

## 🐛 Known Issue

**UI Response Bug:** The agent executes tools successfully (visible in terminal), but responses don't appear in the OpenAgents Studio UI.

- Tools execute correctly ✅
- Terminal shows all activity ✅
- UI shows no response ❌

This appears to be related to how `CollaboratorAgent` handles responses after `run_agent()` completes. Working with the OpenAgents team to resolve.

## 🛠️ Tech Stack

- **[OpenAgents](https://github.com/bestagents/openagents)** - Multi-agent framework
- **[E2B](https://e2b.dev)** - Cloud sandbox infrastructure
- **[Nebius AI](https://nebius.com)** - LLM inference (Llama-3.3-70B)

## 📄 License

MIT

---

Built with ❤️ for the Holiday AI Build-Off 2025
