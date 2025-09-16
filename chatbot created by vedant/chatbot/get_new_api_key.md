# How to Get a New OpenAI API Key

## Step-by-Step Guide:

### 1. Go to OpenAI Platform
- Visit: https://platform.openai.com/
- Click "Sign Up" or "Log In"

### 2. Create Account (if new)
- Use your email
- Verify your email address
- Complete the signup process

### 3. Generate API Key
- Go to: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Give it a name (e.g., "My Chatbot")
- Copy the key immediately (you won't see it again!)

### 4. Update Your Config
- Open `config.py` in your project
- Replace the old key with your new key:
```python
OPENAI_API_KEY = "your_new_api_key_here"
```

### 5. Test the Connection
- Run: `py test_api.py`
- Should show "API connection successful!"

## Important Notes:
- **Free Tier**: $5 free credit for new accounts
- **Usage Limits**: Check your usage dashboard
- **Billing**: Add payment method for more quota
- **Security**: Never share your API key publicly

## Troubleshooting:
- **"Invalid key"**: Make sure you copied the full key
- **"Quota exceeded"**: Add payment method or wait for reset
- **"Connection error"**: Check your internet connection


