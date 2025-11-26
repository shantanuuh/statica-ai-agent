# Statica.in AI Agent

AI-powered customer support agent for statica.in WordPress site.

## Features

- 🤖 AI-powered customer support
- 💬 Multiple agent types (support, product, general)
- 🆓 Free Hugging Face integration
- 🎯 Intelligent fallback responses
- 🌐 FastAPI backend
- 🔒 CORS enabled for WordPress integration

## Deployment on Render

### 1. One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### 2. Manual Deployment

1. **Fork this repository** to your GitHub account
2. **Create account** on [Render.com](https://render.com)
3. **Connect your GitHub** repository
4. **Create new Web Service** and select this repository
5. **Add environment variable**:
   - `HF_TOKEN`: Your Hugging Face token (get free token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
6. **Deploy** - Render will automatically build and deploy

### 3. Configuration

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

- `POST /chat` - Main chat endpoint
- `GET /health` - Health check
- `GET /test` - Test endpoint
- `GET /test-chat?message=Hello` - Test chat via GET

## WordPress Integration

Update your WordPress plugin with your Render URL:
`https://your-app-name.onrender.com/chat`

## Example Request

```bash
curl -X POST "https://your-app.onrender.com/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What WordPress services do you offer?",
    "agent_type": "support"
  }'