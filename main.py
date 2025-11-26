from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import requests
import json
import logging
import os
from email_agent import EmailAutomationAgent  # Add this import

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Statica.in AI Agent",
    description="AI-powered customer support and email automation for statica.in",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    agent_type: str = "support"
    user_data: Optional[Dict[str, Any]] = None

class EmailRequest(BaseModel):
    email_type: str  # welcome, support, newsletter, offer, etc.
    recipient_email: str
    subject: Optional[str] = None
    custom_message: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None

class EmailResponse(BaseModel):
    success: bool
    message: str
    email_sent: bool
    recipient: str

class ChatResponse(BaseModel):
    response: str
    success: bool = True
    agent_used: str = "huggingface"

# Initialize agents
from agents.statica_ai_agent import StaticaAIAgent  # Your existing agent
chat_agent = StaticaAIAgent()
email_agent = EmailAutomationAgent()  # New email agent

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint"""
    try:
        logger.info(f"Chat request: {request.message}, Agent: {request.agent_type}")
        
        response = await chat_agent.generate_response(
            prompt=request.message,
            agent_type=request.agent_type
        )
        
        return ChatResponse(
            response=response,
            success=True,
            agent_used="huggingface"
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return ChatResponse(
            response="I apologize, but I'm currently experiencing technical difficulties.",
            success=False,
            agent_used="fallback"
        )

@app.post("/send-email", response_model=EmailResponse)
async def send_email_endpoint(request: EmailRequest):
    """Send automated emails"""
    try:
        logger.info(f"Email request: {request.email_type} to {request.recipient_email}")
        
        result = await email_agent.send_automated_email(
            email_type=request.email_type,
            recipient_email=request.recipient_email,
            custom_message=request.custom_message,
            user_data=request.user_data or {}
        )
        
        return EmailResponse(
            success=result["success"],
            message=result["message"],
            email_sent=result["email_sent"],
            recipient=request.recipient_email
        )
        
    except Exception as e:
        logger.error(f"Email endpoint error: {str(e)}")
        return EmailResponse(
            success=False,
            message=f"Failed to send email: {str(e)}",
            email_sent=False,
            recipient=request.recipient_email
        )

@app.get("/email-templates")
async def get_email_templates():
    """Get available email templates"""
    templates = email_agent.get_available_templates()
    return {"templates": templates}

@app.get("/")
async def root():
    return {
        "message": "Statica.in AI Agent + Email Automation", 
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "send_email": "POST /send-email",
            "templates": "GET /email-templates",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Statica AI Agent + Email Automation",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, access_log=False)
