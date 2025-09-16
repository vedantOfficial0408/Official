## Enhanced ChatBot created by Vedant

A powerful Python chatbot that uses the OpenAI ChatGPT API with advanced features for intelligent conversations.

## 🚀 Enhanced Features

- **Interactive command-line interface** with rich conversation experience
- **Web search capabilities** - Get real-time information from the internet
- **File reading and analysis** - Read and analyze documents, code, and text files
- **Memory persistence** - Remembers conversations between sessions
- **Enhanced responses** - More detailed and informative answers
- **System prompts** - Intelligent behavior and context awareness
- **Error handling** - Robust error management and user feedback

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   Create a `.env` file in the project directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the chatbot:**
   ```bash
   python chatbot.py
   ```

## Usage

### 🌐 Web Interface (Recommended)
- Start the web chatbot by running `py web_chatbot.py`
- The chatbot will automatically open in your Chrome browser
- Enjoy a beautiful, modern chat interface
- All features available: web search, file reading, memory persistence

### 💻 Command Line Interface
- Start the chatbot by running `py chatbot.py`
- Type your messages and press Enter
- Type `quit`, `exit`, or `bye` to end the conversation
- Press `Ctrl+C` to force quit

### Advanced Commands
- **`/search <query>`** - Search the web for real-time information
  - Example: `/search latest AI news`
- **`/read <filename>`** - Read and analyze files
  - Example: `/read document.txt`
- **`/files`** - List all available files in the current directory

### Examples
```
You: /search Python programming trends 2024
Bot: [Searches web and provides comprehensive answer]

You: /files
Bot: [Lists all available files]

You: /read my_code.py
Bot: [Reads and analyzes the Python file]
```

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## Dependencies

- `openai`: Official OpenAI Python library
- `python-dotenv`: For loading environment variables
- `requests`: For web search functionality
- `beautifulsoup4`: For parsing web search results
- `lxml`: For efficient HTML parsing
- `flask`: For web interface
- `webbrowser`: For auto-opening browser (built-in)

## Customization

You can modify the chatbot behavior by editing `chatbot.py`:

- **Model**: Change the model (currently using `gpt-3.5-turbo`)
- **Response length**: Adjust `max_tokens` (currently 2000 for detailed responses)
- **Creativity**: Modify `temperature` for response creativity (0.0 to 1.0)
- **System prompts**: Customize the AI's behavior and personality
- **File types**: Add support for more file formats in `read_file()` method
- **Search engine**: Modify web search functionality in `web_search()` method
- **Memory**: Customize conversation memory storage and retrieval

## Security Note

Never commit your `.env` file to version control. Your API key should remain private.
