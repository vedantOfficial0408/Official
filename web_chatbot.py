import os
import openai
from dotenv import load_dotenv
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import glob
from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import time

# Load environment variables
load_dotenv()

# Import config as fallback
try:
    from config import OPENAI_API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = None

app = Flask(__name__)

class WebChatBot:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = []
        self.memory_file = "web_chatbot_memory.json"
        self.load_memory()
        
        # System prompt for better behavior
        self.system_prompt = """You are an intelligent and helpful AI assistant with a web interface. You have access to:
1. Web search capabilities for real-time information
2. File reading capabilities to analyze documents
3. Conversation memory to remember previous interactions

Guidelines:
- Provide detailed, accurate, and helpful responses
- Use web search when asked about current events or recent information
- Offer to read files when users mention documents
- Be conversational and engaging
- Remember context from previous messages in the conversation
- If you're unsure about something, say so and offer to search for more information
- Format your responses nicely for web display with proper line breaks"""
        
        # Add system prompt to conversation
        self.add_message("system", self.system_prompt)
    
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def load_memory(self):
        """Load conversation memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    self.conversation_history = memory_data.get('conversations', [])
        except Exception as e:
            print(f"⚠️ Could not load memory: {e}")
            self.conversation_history = []
    
    def save_memory(self):
        """Save conversation memory to file"""
        try:
            memory_data = {
                'conversations': self.conversation_history,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save memory: {e}")
    
    def web_search(self, query):
        """Perform web search and return results"""
        try:
            # Using DuckDuckGo search (no API key required)
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result')[:5]:  # Top 5 results
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    results.append({
                        'title': title_elem.get_text().strip(),
                        'snippet': snippet_elem.get_text().strip(),
                        'url': title_elem.get('href', '')
                    })
            
            return results
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def read_file(self, file_path):
        """Read and analyze a file"""
        try:
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            # Get file extension
            _, ext = os.path.splitext(file_path.lower())
            
            if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"File content ({file_path}):\n{content[:2000]}{'...' if len(content) > 2000 else ''}"
            else:
                return f"Cannot read file type: {ext}. Supported types: .txt, .md, .py, .js, .html, .css, .json, .xml"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def list_files(self):
        """List available files in current directory"""
        try:
            files = []
            for file_path in glob.glob("*"):
                if os.path.isfile(file_path) and not file_path.startswith('.'):
                    files.append(file_path)
            return files
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def get_response(self, user_input):
        """Get response from ChatGPT API with enhanced features"""
        try:
            # Check for special commands
            if user_input.lower().startswith('/search '):
                query = user_input[8:]  # Remove '/search '
                search_results = self.web_search(query)
                if isinstance(search_results, list):
                    search_info = f"Web search results for '{query}':\n"
                    for i, result in enumerate(search_results, 1):
                        search_info += f"{i}. {result['title']}\n   {result['snippet']}\n   {result['url']}\n\n"
                    user_input = f"Based on these search results: {search_info}\nPlease provide a comprehensive answer about: {query}"
                else:
                    user_input = f"Search failed: {search_results}. Please answer: {query}"
            
            elif user_input.lower().startswith('/read '):
                file_path = user_input[6:]  # Remove '/read '
                file_content = self.read_file(file_path)
                user_input = f"Please analyze this file content:\n{file_content}"
            
            elif user_input.lower() == '/files':
                files = self.list_files()
                if isinstance(files, list):
                    files_info = "Available files:\n" + "\n".join(files)
                    user_input = f"Here are the available files:\n{files_info}\n\nYou can use '/read filename' to read any file."
                else:
                    user_input = f"Error listing files: {files}"
            
            # Add user message to conversation
            self.add_message("user", user_input)
            
            # Create completion with enhanced settings
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=2000,  # Increased for more detailed responses
                temperature=0.7
            )
            
            # Extract assistant's response
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation
            self.add_message("assistant", assistant_response)
            
            # Save memory after each interaction
            self.save_memory()
            
            return assistant_response
            
        except Exception as e:
            return f"Error: {str(e)}"

# Initialize chatbot
chatbot = WebChatBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = chatbot.get_response(user_message)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_chat():
    try:
        chatbot.conversation_history = [{"role": "system", "content": chatbot.system_prompt}]
        chatbot.save_memory()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

def main():
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY') or CONFIG_API_KEY
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Please set your API key in one of these ways:")
        print("1. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("2. Set environment variable: export OPENAI_API_KEY=your_key_here")
        print("3. Update the OPENAI_API_KEY in config.py")
        sys.exit(1)
    
    # Set the API key for the OpenAI client
    os.environ['OPENAI_API_KEY'] = api_key
    
    print("🚀 Starting Enhanced Web Chatbot...")
    print("📱 Web interface will open in your browser")
    print("🌐 Server running at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
