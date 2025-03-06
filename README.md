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

## License

This project is open-source and available for modification and use under the MIT license.

### MIT License

```
MIT License

Copyright (c) 2024-2025 Ralph King

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```