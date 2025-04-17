# 🛡️ AI Security Testing Framework

A comprehensive framework for testing AI system security boundaries and responses using dynamic prompt generation and analysis, with full A2A (Agent-to-Agent) compatibility.

## Overview

This framework provides automated testing capabilities for AI systems, focusing on security response testing and boundary analysis. It uses OpenAI's GPT models to generate and analyze responses to potentially malicious prompts while maintaining ethical boundaries. The framework supports both standalone operation and A2A (Agent-to-Agent) communication for integrated testing environments.

## Key Features

- Dynamic prompt generation from multiple sources (MITRE ATT&CK, static files)
- Automated security response testing
- Conversation simulation and analysis
- Detailed logging and result tracking
- JSON and plaintext output formats
- OpenAI API integration
- Ethical boundary testing
- Full A2A (Agent-to-Agent) compatibility
- Docker containerization support

## Prerequisites

- Python 3.10+
- OpenAI API key
- Playwright (for browser automation tests)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-security-framework.git
cd ai-security-framework
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Core Components

### PromptAgent
Manages prompt generation, context handling, and conversation flow:
- Base prompt management
- Context-aware prompt generation
- Conversation history tracking
- Follow-up generation
- A2A message handling

### PromptSourceAgent
Handles prompt sourcing from multiple locations:
- MITRE ATT&CK technique integration
- Static prompt loading
- Dynamic prompt generation
- Source management
- A2A task card processing

### ChatInjectorAgent
Manages chat interactions and security testing:
- Automated chat simulation
- Security boundary testing
- Response analysis
- Logging and reporting
- A2A communication protocols

## Project Structure

```
.
├── agents/                     # Agent implementations
│   ├── __init__.py
│   ├── prompt_agent.py        # Core prompt management
│   ├── prompt_source_agent.py # Prompt source handling
│   ├── chat_injector_agent.py # Chat interaction testing
│   └── recorder_agent.py      # Test recording
├── prompts/                   # Prompt storage
│   └── static_prompts.yaml
├── tests/                     # Test suite
├── output/                    # Test results
├── sources/             # Prompt source implementations
│   └── loader.py
├── logs/                      # Logging directory
└── requirements.txt          # Project dependencies
└── Dockerfile          # Docker configuration
```

## Usage Examples

### Basic Security Test
```python
from agents.prompt_source_agent import PromptSourceAgent
from agents.prompt_agent import PromptAgent

# Initialize agents
source_agent = PromptSourceAgent()
prompt_agent = PromptAgent()

# Generate dynamic prompts
prompts = source_agent.get_dynamic_prompts()

# Run security test
for prompt in prompts:
    response = prompt_agent.generate_prompt(prompt)
    # Analyze response
```

### A2A Mode Operation
```python
# Using Python
python main.py --task-card path/to/task.json

# Using Docker
docker run -it -v $(pwd)/task.json:/app/task.json ai-agent --task-card /app/task.json
```

### Conversation Simulation
```python
# Initialize test
test = test_dynamic_prompt_generation()

# Results are saved in:
# - test_conversation.txt (human-readable format)
# - conversation_dan_roleplay_[timestamp].json (detailed format with metadata)
```

## Deployment Options

### Standalone Mode
Run the framework independently for security testing:
```bash
python main.py
# or with Docker
docker run -it ai-agent
```

### A2A Integration Mode
Run as part of an agent network:
```bash
python main.py --task-card task.json --a2a-mode
# or with Docker
docker run -it -v $(pwd)/task.json:/app/task.json ai-agent --task-card /app/task.json --a2a-mode
```

## Configuration

### A2A Settings
Configure A2A behavior in your .env file:
```bash
A2A_ENABLED=true
A2A_PORT=5000
A2A_HOST=localhost
A2A_PROTOCOL=http
```

## Testing

The framework includes several test types:
- Dynamic prompt generation tests
- Security boundary tests
- Conversation simulation tests
- API integration tests

Run tests:
```bash
python test_dynamic_prompts.py  # For conversation tests
python test_security.py         # For security boundary tests
```

## Security Considerations

- All tests are conducted with ethical boundaries
- Responses maintain security guidelines
- Proper logging of all interactions
- API key security measures
- Rate limiting compliance

## Verified Capabilities

The following features have been tested and verified:
- ✅ OpenAI API integration
- ✅ Dynamic prompt generation
- ✅ Security boundary testing
- ✅ Conversation simulation
- ✅ Result logging and storage
- ✅ Ethical response handling
- ✅ MITRE ATT&CK integration
- ✅ A2A compatibility
- ✅ Docker containerization

## License

MIT License

## Disclaimer

This framework is for authorized security testing and research purposes only. Always follow ethical guidelines and obtain proper authorization before testing any system.

# AI Agent Project

A production-ready AI agent with Docker support and A2A compatibility.

## Features

- Dockerized execution
- Multiple prompt sources (static, file, API)
- A2A (Agent-to-Agent) compatibility
- Local testing support

## Quick Start

### Building the Docker Container

```bash
docker build -t ai-agent .
```

### Running the Agent

#### Standalone Mode

```bash
# Using Docker
docker run -it ai-agent

# Using Python directly
python main.py
```

#### A2A Mode

```bash
# Using Docker
docker run -it -v $(pwd)/task.json:/app/task.json ai-agent --task-card /app/task.json

# Using Python directly
python main.py --task-card path/to/task.json
```

### Switching Prompt Sources

The agent supports multiple prompt sources:

1. Static (default):
```bash
export PROMPT_SOURCE=static
export STATIC_PROMPT="Your prompt here"
```

2. File:
```bash
export PROMPT_SOURCE=file
export PROMPT_FILE_PATH=path/to/prompt.txt
```

3. API:
```bash
export PROMPT_SOURCE=api
export PROMPT_API_URL=http://your-api/prompt
```

You can also use command line arguments:
```bash
python main.py --prompt-source file
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT License 