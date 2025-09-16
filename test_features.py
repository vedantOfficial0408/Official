#!/usr/bin/env python3
"""
Test script to verify enhanced chatbot features
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import openai
        print("✅ OpenAI package available")
    except ImportError:
        print("❌ OpenAI package not found - run: pip install openai")
    
    try:
        import requests
        print("✅ Requests package available")
    except ImportError:
        print("❌ Requests package not found - run: pip install requests")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup package available")
    except ImportError:
        print("❌ BeautifulSoup package not found - run: pip install beautifulsoup4")
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv package available")
    except ImportError:
        print("❌ Python-dotenv package not found - run: pip install python-dotenv")

def test_file_operations():
    """Test file reading capabilities"""
    import os
    import glob
    
    print("\n📁 Testing file operations:")
    
    # List files
    files = []
    for file_path in glob.glob("*"):
        if os.path.isfile(file_path) and not file_path.startswith('.'):
            files.append(file_path)
    
    print(f"Found {len(files)} files:")
    for file in files:
        print(f"  - {file}")
    
    # Test reading a text file
    if 'README.md' in files:
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Successfully read README.md ({len(content)} characters)")
        except Exception as e:
            print(f"❌ Error reading README.md: {e}")

def main():
    print("🧪 Testing Enhanced Chatbot Features")
    print("=" * 50)
    
    test_imports()
    test_file_operations()
    
    print("\n🚀 To install missing packages, run:")
    print("pip install -r requirements.txt")
    
    print("\n🤖 To start the enhanced chatbot, run:")
    print("python chatbot.py")

if __name__ == "__main__":
    main()
