# Statica.in AI Agent

AI-powered customer support agent for statica.in WordPress site.

## 🚀 Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🔑 Getting Your Hugging Face Token

### Step 1: Create Account
1. Go to [Hugging Face](https://huggingface.co)
2. Sign up for free account
3. Verify your email

### Step 2: Generate Token
1. Go to [Settings → Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Set:
   - Name: `statica-ai-agent`
   - Type: `Read`
   - Expires: `Never`
4. Click "Generate"
5. **Copy your token** (starts with `hf_`)

### Step 3: Deploy to Render
1. Click the "Deploy to Render" button above
2. Connect your GitHub account
3. Set environment variable:
   - **Key:** `HF_TOKEN`
   - **Value:** `your_copied_token_here`
4. Click "Create Web Service"

## 📁 Project Structure
- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment config

## 🌐 API Endpoints
- `POST /chat` - Main chat endpoint
- `GET /health` - Health check
- `GET /test` - Test the AI

## 💬 Example Usage
```bash
curl -X POST "https://your-app.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent_type": "support"}'
