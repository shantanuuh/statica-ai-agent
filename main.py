from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import requests
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Statica.in AI Agent",
    description="AI-powered customer support for statica.in",
    version="1.0.0"
)

# CORS middleware - allow your WordPress site and all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with ["https://statica.in"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    agent_type: str = "support"
    user_data: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    success: bool = True
    agent_used: str = "huggingface"

class StaticaAIAgent:
    def __init__(self):
        self.huggingface_token = os.getenv("HF_TOKEN", "")
        self.company_context = {
            "name": "Statica",
            "website": "statica.in", 
            "support_email": "support@statica.in",
            "business_type": "WordPress Development & Services",
            "services": "WordPress development, website design, hosting solutions, plugin development, theme customization",
            "pricing": "Basic website: $99 | Business website: $299 | Custom development: Custom pricing",
            "support_hours": "24/7 email support | Response within 2-4 hours"
        }
        
        # Free Hugging Face models
        self.models = {
            "support": "microsoft/DialoGPT-medium",
            "creative": "microsoft/DialoGPT-large", 
            "general": "microsoft/DialoGPT-medium"
        }
    
    async def generate_response(self, prompt: str, agent_type: str = "support") -> str:
        """Generate response using free Hugging Face API with fallback to local responses"""
        try:
            # Try Hugging Face API first
            if self.huggingface_token:
                response = await self._call_huggingface_api(prompt, agent_type)
                if response and response != "Thank you for your message! How can I assist you today?":
                    return response
            
            # Fallback to local responses if Hugging Face fails or no token
            return self._get_local_response(prompt, agent_type)
                
        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            return self._get_local_response(prompt, agent_type)
    
    async def _call_huggingface_api(self, prompt: str, agent_type: str) -> str:
        """Call Hugging Face Inference API"""
        model = self.models.get(agent_type, "microsoft/DialoGPT-medium")
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        headers = {
            "Authorization": f"Bearer {self.huggingface_token}",
            "Content-Type": "application/json"
        }
        
        # Build context-aware prompt
        system_prompt = self._get_system_prompt(agent_type)
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False,
                "repetition_penalty": 1.1
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Clean up the response
                    if "Assistant:" in generated_text:
                        generated_text = generated_text.split("Assistant:")[-1].strip()
                    return generated_text or self._get_local_response(prompt, agent_type)
            else:
                logger.warning(f"Hugging Face API error: {response.status_code} - {response.text}")
                return self._get_local_response(prompt, agent_type)
                
        except requests.exceptions.Timeout:
            logger.error("Hugging Face API timeout")
            return self._get_local_response(prompt, agent_type)
        
        except Exception as e:
            logger.error(f"Hugging Face API exception: {str(e)}")
            return self._get_local_response(prompt, agent_type)
        
        return self._get_local_response(prompt, agent_type)
    
    def _get_system_prompt(self, agent_type: str) -> str:
        """Get system prompt based on agent type"""
        base_prompts = {
            "support": f"""You are a helpful, friendly customer support agent for {self.company_context['name']} ({self.company_context['website']}).

Company Information:
- Business: {self.company_context['business_type']}
- Services: {self.company_context['services']}
- Pricing: {self.company_context['pricing']}
- Support: {self.company_context['support_hours']}
- Email: {self.company_context['support_email']}

You help with:
- Answering questions about WordPress services
- Technical support and troubleshooting
- Pricing and package information
- Website development inquiries
- General customer service

Always be:
- Professional but friendly and warm
- Helpful and solution-oriented
- Clear in your explanations
- Honest about what you can and cannot do

If you don't know something, suggest contacting {self.company_context['support_email']} for detailed assistance.""",

            "product": f"""You are a service expert for {self.company_context['name']}.

Services we offer:
{self.company_context['services']}

Pricing: {self.company_context['pricing']}

You help with:
- Service recommendations based on client needs
- Feature explanations and benefits
- Pricing plan comparisons
- Technical specifications
- Project timelines

Focus on understanding client needs and recommending the best solutions.""",

            "email": """You are an email automation specialist. Create professional, engaging email content.

Focus on:
- Clear, concise communication
- Professional but friendly tone
- Customer engagement and relationship building
- Appropriate call-to-action when relevant
- Proper email formatting

Create emails that build trust and encourage response.""",

            "general": f"""You are a helpful AI assistant for {self.company_context['name']} website.

Provide friendly, accurate, and helpful responses to user inquiries about our WordPress services and website development offerings."""
        }
        
        return base_prompts.get(agent_type, base_prompts["support"])
    
    def _get_local_response(self, prompt: str, agent_type: str) -> str:
        """Fallback to intelligent local responses"""
        prompt_lower = prompt.lower()
        
        # Handle common questions with predefined responses
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'help']):
            return self._get_welcome_response()
        
        elif any(word in prompt_lower for word in ['price', 'cost', 'how much', 'pricing']):
            return self._get_pricing_response()
        
        elif any(word in prompt_lower for word in ['wordpress', 'website', 'site', 'web']):
            return self._get_services_response()
        
        elif any(word in prompt_lower for word in ['contact', 'email', 'phone', 'call', 'reach']):
            return self._get_contact_response()
        
        elif any(word in prompt_lower for word in ['service', 'what do you do', 'offer', 'provide']):
            return self._get_services_response()
        
        elif any(word in prompt_lower for word in ['time', 'hours', 'available', 'support']):
            return self._get_support_response()
        
        elif any(word in prompt_lower for word in ['portfolio', 'work', 'examples', 'projects']):
            return self._get_portfolio_response()
        
        elif any(word in prompt_lower for word in ['thank', 'thanks', 'appreciate']):
            return self._get_thankyou_response()
        
        elif any(word in prompt_lower for word in ['blog', 'content', 'writing']):
            return self._get_blog_response()
        
        elif any(word in prompt_lower for word in ['ecommerce', 'shop', 'store', 'woocommerce']):
            return self._get_ecommerce_response()
        
        else:
            return self._get_general_response(prompt)
    
    def _get_welcome_response(self) -> str:
        return f"""Hello! 👋 Welcome to {self.company_context['name']}!

I'm your AI assistant. I can help you with:

• WordPress website development
• Pricing and package information  
• Technical support
• Service recommendations
• Project consultations

What would you like to know about our services?"""

    def _get_pricing_response(self) -> str:
        return f"""Here's our pricing for WordPress services:

🚀 **Basic Website Package - $99**
- 5 pages custom design
- Mobile responsive
- Basic SEO setup
- Contact form
- 1 month support

💼 **Business Website Package - $299**  
- Up to 10 pages
- E-commerce functionality
- Advanced SEO optimization
- Custom features
- 3 months support

🎨 **Custom Development - Custom Pricing**
- Complex functionality
- Custom plugins/themes
- Ongoing maintenance
- Priority support

Which type of project are you planning? I can help you choose the right package!"""

    def _get_services_response(self) -> str:
        return f"""At {self.company_context['name']}, we specialize in:

🛠️ **WordPress Development**
- Custom theme development
- Plugin customization
- WooCommerce setup
- Website maintenance

🎨 **Website Design**
- Responsive design
- UI/UX optimization
- Brand consistency
- Mobile-first approach

⚡ **Performance & SEO**
- Speed optimization
- SEO setup
- Security hardening
- Performance monitoring

🔧 **Support & Maintenance**
- Regular updates
- Security monitoring
- Backup solutions
- Technical support

What specific service are you interested in?"""

    def _get_contact_response(self) -> str:
        return f"""You can reach us at:

📧 Email: {self.company_context['support_email']}
🌐 Website: {self.company_context['website']}

We typically respond within 2-4 hours during business days.

Would you like to schedule a free consultation call to discuss your project?"""

    def _get_support_response(self) -> str:
        return f"""Our support details:

🕒 Support Hours: {self.company_context['support_hours']}
📧 Primary Contact: {self.company_context['support_email']}

For urgent matters, we prioritize quick responses. For complex issues, we may need 24-48 hours for thorough solutions.

What specific help do you need with your WordPress site?"""

    def _get_portfolio_response(self) -> str:
        return """I'd love to show you our work! 

While I can't display images here, we've worked on various WordPress projects including:

• E-commerce stores with WooCommerce
• Business websites with custom functionality
• Membership sites with user portals
• Blog and content-focused sites
• Custom web applications

You can visit our website to see our portfolio, or tell me about your project and I can share relevant examples!

What type of website are you looking to build?"""

    def _get_thankyou_response(self) -> str:
        return """You're very welcome! 😊

I'm glad I could help. If you have any more questions about WordPress development, pricing, or our services, don't hesitate to ask.

Is there anything else you'd like to know about our offerings?"""

    def _get_blog_response(self) -> str:
        return """We offer comprehensive blog and content services:

📝 **Content Writing & Blogging**
- SEO-optimized blog posts
- Content strategy development
- Article writing and editing
- Content management

📊 **Content Marketing**
- Blog setup and optimization
- Content calendar planning
- Reader engagement strategies
- Social media integration

Would you like help with starting a blog or improving your existing content strategy?"""

    def _get_ecommerce_response(self) -> str:
        return """We specialize in WordPress e-commerce solutions:

🛒 **WooCommerce Development**
- Online store setup
- Product catalog management
- Payment gateway integration
- Shipping configuration

📱 **E-commerce Features**
- Mobile-responsive shopping
- Inventory management
- Order processing systems
- Customer account portals

Are you looking to build a new online store or improve an existing one?"""

    def _get_general_response(self, prompt: str) -> str:
        return f"""Thank you for your question about: "{prompt}"

At {self.company_context['name']}, we specialize in WordPress development and website services. 

Based on your query, I recommend:
- Checking our detailed service descriptions
- Looking at our pricing packages  
- Scheduling a free consultation for specific requirements

You can also email us directly at {self.company_context['support_email']} for personalized assistance.

Could you tell me more about what you're looking to build? I can provide more specific guidance!"""

# Initialize the agent
agent = StaticaAIAgent()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for Statica.in"""
    try:
        logger.info(f"Received message: {request.message}, Agent: {request.agent_type}")
        
        response = await agent.generate_response(
            prompt=request.message,
            agent_type=request.agent_type
        )
        
        return ChatResponse(
            response=response,
            success=True,
            agent_used="huggingface" if agent.huggingface_token else "local"
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return ChatResponse(
            response="I apologize, but I'm currently experiencing technical difficulties. Please try again later or email support@statica.in for immediate assistance.",
            success=False,
            agent_used="fallback"
        )

@app.get("/")
async def root():
    return {
        "message": "Statica.in AI Agent API", 
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "test": "GET /test"
        },
        "agent_status": "huggingface" if agent.huggingface_token else "local_fallback"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Statica AI Agent",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "environment": "production"
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify the API is working"""
    test_response = await agent.generate_response("Hello, test message", "support")
    return {
        "status": "success",
        "message": "API is working correctly!",
        "test_response": test_response,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

@app.get("/test-chat")
async def test_chat_get(message: str = "Hello"):
    """Test chat via GET parameters (for browser testing)"""
    response = await agent.generate_response(message, "support")
    return {
        "your_message": message,
        "ai_response": response,
        "success": True,
        "agent_used": "huggingface" if agent.huggingface_token else "local"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Render sets this)
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting Statica AI Agent")
    print(f"📡 Server running on port: {port}")
    print(f"🔗 Health check: /health")
    print(f"💬 Chat endpoint: POST /chat")
    print(f"🤖 Agent mode: {'Hugging Face' if agent.huggingface_token else 'Local Fallback'}")
    print("=" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        access_log=False,
        log_level="info"
    )