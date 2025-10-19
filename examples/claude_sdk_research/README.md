# Claude Agent SDK + browser-use Integration Examples

This directory contains examples of using Claude Agent SDK with browser-use for automated web research and data extraction.

## 🌟 Overview

The integration combines:
- **Claude Agent SDK**: Advanced AI agent framework with subagents, hooks, and commands
- **browser-use**: Browser automation library for AI agents
- **Specialized Agents**: IEEE researcher, web researcher, data extractor

## 📋 Requirements

1. **Python 3.11+** with uv package manager
2. **ANTHROPIC_API_KEY** environment variable set
3. **Dependencies installed**:
   ```bash
   uv sync
   ```

## 🚀 Quick Start

### 1. Simple Demo

Basic browser automation with Claude:

```bash
uv run python examples/claude_sdk_research/simple_demo.py
```

This demo shows:
- Navigating to websites
- Extracting page information
- Interactive chat mode with browser tools

### 2. IEEE Research Assistant

Search and extract papers from IEEE Xplore:

```bash
# Basic search
uv run python examples/claude_sdk_research/ieee_research.py "machine learning"

# With options
uv run python examples/claude_sdk_research/ieee_research.py \
  "deep learning robotics" \
  --limit 20 \
  --save results.json
```

**Options:**
- `--limit N`: Extract up to N papers (default: 10)
- `--save FILE`: Save results to JSON file

## 📁 Project Structure

```
browser-use-automation/
├── .claude/                          # Claude Agent SDK configuration
│   ├── agents/                       # Specialized subagents
│   │   ├── ieee-researcher.md       # IEEE Xplore specialist
│   │   ├── web-researcher.md        # General web research
│   │   └── data-extractor.md        # Data extraction specialist
│   ├── commands/                     # Slash commands
│   │   └── research-ieee.md         # /research-ieee command
│   └── settings.json                 # Hooks and permissions
├── browser_use/
│   └── claude_sdk_integration/      # Integration layer
│       ├── __init__.py
│       └── tools.py                  # Browser tools for SDK
└── examples/claude_sdk_research/    # This directory
    ├── README.md                     # This file
    ├── simple_demo.py                # Basic demo
    └── ieee_research.py              # Research assistant
```

## 🛠️ Available Browser Tools

The integration exposes these browser-use actions as Claude Agent SDK tools:

| Tool | Description |
|------|-------------|
| `browser_navigate` | Navigate to a URL |
| `browser_click` | Click an element (CSS selector) |
| `browser_type` | Type text into an input field |
| `browser_extract` | Extract text content from page |
| `browser_get_state` | Get current page state (URL, title, tabs) |
| `browser_scroll` | Scroll the page up/down |
| `browser_go_back` | Navigate back in history |

## 🤖 Specialized Subagents

### IEEE Researcher (`ieee-researcher`)

Expert in searching and extracting papers from IEEE Xplore.

**Capabilities:**
- Navigate IEEE Xplore
- Construct effective search queries
- Extract paper metadata (title, authors, DOI, abstract)
- Handle pagination and filters

**Usage in code:**
```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    agents={'ieee-researcher': 'path/to/.claude/agents/ieee-researcher.md'},
    # ... other options
)
```

### Web Researcher (`web-researcher`)

General-purpose web research agent.

**Capabilities:**
- Search engines (Google, Bing, DuckDuckGo)
- Navigate complex websites
- Extract relevant information
- Cross-reference multiple sources

### Data Extractor (`data-extractor`)

Specialist in extracting structured data from web pages.

**Capabilities:**
- Parse tables, lists, complex layouts
- Extract metadata
- Clean and normalize data
- Convert to structured JSON

## 📜 Slash Commands

### `/research-ieee`

Quick command to search IEEE Xplore:

```
/research-ieee machine learning robotics --limit 20 --save results.json
```

## 🔧 Configuration

### Browser Settings (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  },
  "permissions": {
    "mode": "acceptEdits",
    "allowedTools": ["browser_*"]
  },
  "browser": {
    "headless": false,
    "keepOpen": true
  }
}
```

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="your-api-key"

# Optional
export BROWSER_USE_HEADLESS=false
export BROWSER_USE_KEEP_OPEN=true
```

## 💡 Usage Examples

### Example 1: Simple Web Navigation

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from browser_use.claude_sdk_integration import create_browser_mcp_server

options = ClaudeAgentOptions(
    mcp_servers=create_browser_mcp_server('browser-use'),
    permission_mode='bypassPermissions',
)

async for msg in query("Go to python.org and tell me the latest version", options):
    print(msg)
```

### Example 2: Research with Subagent

```python
options = ClaudeAgentOptions(
    system_prompt="You are a research coordinator.",
    mcp_servers=create_browser_mcp_server('browser-use'),
    agents={
        'ieee-researcher': '.claude/agents/ieee-researcher.md'
    },
    setting_sources=['project'],
)

prompt = "Use the ieee-researcher agent to find papers on neural networks"
async for msg in query(prompt, options):
    print(msg)
```

### Example 3: Extract Structured Data

```python
prompt = """Navigate to https://example-research-site.com/papers
Extract all paper titles, authors, and publication years.
Return as JSON array."""

async for msg in query(prompt, options):
    # Process structured results
    print(msg)
```

## 🧪 Testing

Run the integration tests:

```bash
uv run pytest tests/ci/test_claude_sdk_tools.py -v
```

## 📚 Further Reading

- [Claude Agent SDK Documentation](https://docs.claude.com/ja/api/agent-sdk/)
- [browser-use Documentation](../../README.md)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 🐛 Troubleshooting

### "No module named 'claude_agent_sdk'"

Install dependencies:
```bash
uv sync
```

### "ANTHROPIC_API_KEY not set"

Set your API key:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### Browser doesn't open

Check headless setting in `.claude/settings.json`:
```json
{"browser": {"headless": false}}
```

### Rate limiting on IEEE Xplore

Add delays between requests or reduce `--limit`.

## 📝 License

Same as browser-use (MIT License)

## 🤝 Contributing

Contributions welcome! See main project CONTRIBUTING.md for guidelines.
