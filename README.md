# Ollama Chat Interface

A modern graphical user interface for interacting with Ollama language models, built with Python and Tkinter.

## Features

- Clean and intuitive chat interface
- Real-time streaming responses
- Code block support with syntax highlighting
- Copy functionality for code snippets
- Model selection dropdown
- Thinking state indicators
- Keyboard shortcuts for efficient interaction
- Context menu for copy operations

## Requirements

- Python 3.x
- Ollama running locally
- Required Python packages:
  - tkinter
  - requests
  - pyperclip

## Usage

1. Ensure Ollama is running on localhost:11434
2. Run the application:
```bash
python main.py
```

## Key Features

- Model Selection: Choose from available Ollama models via dropdown
- Chat History: Scrollable chat history with distinct user/assistant formatting
- Code Handling: Special formatting for code blocks with copy functionality
- Keyboard Shortcuts:
    - Ctrl+Enter: Send message
    - Shift+Enter: New line in input
- Status Indicators: Shows typing status and operation feedback

## Interface Elements

- Message input area with send/clear buttons
- Model selection dropdown
- Chat history with formatted messages
- Status bar for system feedback
- Context menu for copy operations

