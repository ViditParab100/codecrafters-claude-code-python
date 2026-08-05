# AI Agent CLI

A Python-based command-line interface that allows an LLM (Large Language Model) to interact directly with your local file system and shell. This script turns a language model into an autonomous agent capable of reading, writing, and executing commands.

## Features

- **Agentic Workflow**: Uses a loop to handle tool calls, allowing the model to "think," act, and then process the results of those actions.
- **Tool Use (Function Calling)**:
  - `Read`: Allows the model to examine the contents of local files.
  - `Write`: Allows the model to create or overwrite files with specific content.
  - `Bash`: Allows the model to run shell commands and see the output/errors.
- **OpenRouter Integration**: Configured to work with various models via OpenRouter (defaults to a Google Gemma model).
- **Environment Aware**: Uses `.env` for secure API key management.

## Prerequisites

- Python 3.x
- An OpenAI-compatible API provider (e.g., OpenRouter)
- An API Key for your provider

## Setup

1. **Clone the repository** (if not already done).
2. **Navigate to the app directory**:
   ```bash
   cd app
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the `app/` directory and add your credentials:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```
4. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv
   ```

## Usage

Run the script by passing a prompt using the `-p` flag. The prompt can include instructions to perform tasks on your local files or run terminal commands.

```bash
python main.py -p "Read the contents of README.md and tell me what it does"
```

**Example Use Cases:**
- "Find all `.py` files in the current directory and list them."
- "Create a new file named `test.txt` with the content 'Hello World'."
- "Check my current directory using `ls` and tell me if there is a folder named `data`."

## How It Works

1. The script initializes the OpenAI client with your API key.
2. It sends your prompt to the model along with definitions of the `Read`, `Write`, and `Bash` tools.
3. If the model decides it needs to use a tool, it returns a `tool_call`.
4. The script executes the requested function locally (e.g., runs the shell command or reads the file).
5. The result of that function is sent back to the model.
6. This continues in a loop until the model provides a final response or reaches a terminal state.

## Warning

**Use with caution.** The `Bash` tool allows the model to execute arbitrary shell commands on your machine. Only run this script in trusted environments and be careful with prompts that might perform destructive operations (like `rm -rf`).
