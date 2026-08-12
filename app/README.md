# CodeCrafters Claude Code Python

A Python application that demonstrates integration with OpenAI and SarvamAI APIs for interactive chat and tool usage.

## Features

- Interactive chat mode
- Tool support for file operations (Read, Write, Bash)
- Integration with OpenAI and SarvamAI models
- Environment variable configuration

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `app` directory with the following variables:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   SARVAM_API_KEY=your_sarvam_api_key
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

## Usage

### Interactive Mode

Run the script without arguments to start an interactive session:

```bash
python main.py
```

### One-shot Prompt

Provide a prompt directly via command line:

```bash
python main.py -p "Explain the concept of recursion"
```

## Tools

The application supports the following built-in tools:

- **Read**: Read the contents of a file.
- **Write**: Write content to a file.
- **Bash**: Execute shell commands.

## License

This project is licensed under the MIT License.