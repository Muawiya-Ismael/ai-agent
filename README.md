# 🤖 AI Agent Project

An autonomous CLI-based AI Coding Agent built in Python using the OpenAI SDK and OpenRouter API. The agent can inspect directory structures, read source files, create or edit code, and execute Python scripts within a sandboxed target environment (`calculator/`).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Directory & File Description](#directory--file-description)
  - [Core Agent Logic](#core-agent-logic)
  - [Agent Tool Functions (`functions/`)](#agent-tool-functions-functions)
  - [Test Suite](#test-suite)
  - [Target Sandbox Application (`calculator/`)](#target-sandbox-application-calculator)
  - [Project Configuration & Environment](#project-configuration--environment)
- [Getting Started](#getting-started)
- [Usage](#usage)

---

## 🌟 Overview

This project implements an AI Coding Agent that accepts natural language prompts from the user, formulates execution plans using OpenAI tool/function schemas, and iteratively executes workspace actions up to a maximum loop limit (20 iterations).

### Key Features:
- **Autonomous Tool Dispatch**: Interacts with OpenRouter LLMs to select and call appropriate tools dynamically.
- **Sandbox Boundary Enforcement**: All file operations check path validity to prevent directory traversal outside the target workspace directory.
- **Rich Functionality**: Tooling for file discovery, content reading (with truncation limits), file writing, and command-line Python script execution.

---

## 🗂 Directory & File Description

### Core Agent Logic

| File | Description & Purpose |
| --- | --- |
| **`main.py`** | **CLI Entry Point & Agent Execution Loop**: Parses command-line arguments (`user_prompt`, `--verbose`), initializes the OpenAI client with OpenRouter API, sets up conversation messages with system prompt instructions, and manages the main agent loop (up to 20 iterations) executing tool calls and feeding responses back to the model. |
| **`prompts.py`** | **System Instructions**: Defines `system_prompt`, setting the AI agent role (helpful AI coding agent), available tool capabilities, and constraints regarding relative path usage. |
| **`config.py`** | **Global Configuration**: Stores constants used across the application, such as `MAX_CHARS = 10000` to limit file content output size and protect context window limits. |

---

### Agent Tool Functions (`functions/`)

The `functions/` directory contains the actual tool logic and corresponding OpenAI JSON schema definitions that are passed to the model.

| File | Description & Purpose |
| --- | --- |
| **`functions/call_function.py`** | **Tool Dispatcher**: Contains `call_function()` and `available_functions`. Parses tool call requests from the API response, maps the requested function name to Python implementations in `function_map`, injects `working_directory="./calculator"`, executes the function, handles errors, and returns formatted tool response dictionaries. |
| **`functions/get_files_info.py`** | **Directory Listing Tool**: Contains `get_files_info()` and `schema_get_files_info`. Scans and lists files inside a target directory relative to the working directory, returning file sizes (in bytes) and directory status while blocking path traversal. |
| **`functions/get_file_content.py`** | **File Reading Tool**: Contains `get_file_content()` and `schema_get_file_content`. Reads text from a file up to `MAX_CHARS` (10,000 characters). Appends a truncation message if the file exceeds the limit and prevents access outside the working directory. |
| **`functions/write_file.py`** | **File Writing Tool**: Contains `write_file()` and `schema_write_file`. Creates or overwrites files with provided text content, automatically creating missing parent directories while enforcing working directory boundaries. |
| **`functions/run_python_file.py`** | **Python Execution Tool**: Contains `run_python_file()` and `schema_run_python_file`. Runs a Python script using `subprocess.run` inside the sandboxed environment with optional CLI arguments, returning `STDOUT`, `STDERR`, and exit codes. |

---

### Test Suite

Unit test scripts used to independently verify tool function functionality and security path enforcement.

| File | Description & Purpose |
| --- | --- |
| **`test_get_files_info.py`** | Tests `get_files_info` directory listing, verifying listing output for valid subdirectories as well as blocking forbidden path traversals (`/bin`, `../`). |
| **`test_get_file_content.py`** | Tests `get_file_content` by reading valid files, verifying character truncation logic, handling missing files, and validating security boundary checks. |
| **`test_write_file.py`** | Tests `write_file` by writing new files, overwriting existing files, auto-creating directory structures, and ensuring write attempts outside the working directory (e.g. `/tmp/temp.txt`) fail. |
| **`test_run_python_file.py`** | Tests `run_python_file` execution with and without command-line arguments, executing unit test suites, and handling error/non-Python file cases. |

---

### Target Sandbox Application (`calculator/`)

A sample Python project located in `calculator/` which serves as the sandbox target environment (`working_directory`) that the AI agent operates on.

| File / Directory | Description & Purpose |
| --- | --- |
| **`calculator/main.py`** | CLI interface for the calculator application. Takes mathematical expressions as command-line arguments, evaluates them, and displays JSON-formatted results. |
| **`calculator/tests.py`** | Unit test suite (`unittest`) covering arithmetic operations (addition, subtraction, multiplication, division), nested expressions, precedence, empty input, and invalid syntax. |
| **`calculator/pkg/calculator.py`** | Core `Calculator` class implementing infix arithmetic evaluation and operator precedence parsing. |
| **`calculator/pkg/render.py`** | Formatting module providing `format_json_output()` to output calculator results in a clean JSON format. |
| **`calculator/lorem.txt`** & **`calculator/pkg/morelorem.txt`** | Text files used for testing file reading, writing, and truncation logic. |
| **`calculator/README.md`** | Placeholder documentation for the target calculator application. |

---

### Project Configuration & Environment

| File | Description & Purpose |
| --- | --- |
| **`pyproject.toml`** | Project configuration file specifying project metadata, Python version requirement (`>=3.14`), and dependencies (`openai`, `python-dotenv`). |
| **`uv.lock`** | Lockfile automatically generated by `uv` to pin exact dependency versions. |
| **`.python-version`** | Specifies the target Python runtime version (`3.14`). |
| **`.env`** | Environment file containing `OPENROUTER_API_KEY` credential (excluded from version control). |
| **`.gitignore`** | Specifies files and patterns to ignore in Git (e.g., `.venv`, `.env`, `__pycache__`). |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- Package manager (`uv` or `pip`)
- OpenRouter API key

### Environment Setup

1. Create a `.env` file in the root folder:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

2. Install dependencies:
   ```bash
   uv sync
   # or with pip
   pip install -r pyproject.toml
   ```

---

## 💻 Usage

Run the agent by executing `main.py` with a prompt:

```bash
python main.py "Run the calculator tests and tell me if they pass" --verbose
```

### Command Line Arguments

- `user_prompt`: The task or request for the AI agent.
- `--verbose`: Displays detailed step-by-step function calling logs during execution.