import requests
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StaticaAIAgent:
    def __init__(self):
        self.huggingface_token = os.getenv("HF_TOKEN", "")
        
        # Complete Statica.in business context
        self.company_context = {
            "name": "Statica",
            "website": "https://statica.in",
            "support_email": "support@statica.in",
            "business_type": "Premium Aircraft Model Kits & Aeromodelling Supplies",
            "description": "India's premier destination for precision aircraft model kits, tools, and aeromodelling supplies",
            "target_audience": "Hobbyists, NCC Cadets, Aviation Students, Collectors, Model Building Enthusiasts",
            "shipping": "Ships across India and internationally",
            "support": "Email and WhatsApp support available"
        }
        
        # Complete Product Catalog based on your website
        self.product_catalog = {
            # Static Model Kits
            "virus_sw_80_30cm": {
                "name": "Virus SW 80 Static Model Balsa Kit (30 cms)",
                "category": "static_models",
                "price": "₹3,499.00",
                "description": "30cm version of the iconic Virus SW 80 jet trainer. Precision CNC laser-cut from imported balsa wood.",
                "features": [
                    "High quality imported Balsa wood",
                    "Precision CNC laser cut",
                    "Includes scale Technical Drawing",
                    "Molded PVC canopy",
                    "Undercarriage detailing",
                    "IAF scheme decals",
                    "Zig-zag puzzle type assembly"
                ],
                "specs": "Length: 30cm, Material: Balsa Wood",
                "ideal_for": "NCC competitions, beginners, hobbyists, educational projects",
                "url": "https://statica.in/balsa-wood-aircraft-model-kits/"
            },
            
            "virus_sw_80_55cm": {
                "name": "Virus SW 80 Static Model Balsa Kit (55 cms)",
                "category": "static_models", 
                "price": "₹4,499.00",
                "description": "55cm larger version of the Virus SW 80. More detailed and impressive display piece.",
                "features": [
                    "High quality imported Balsa wood",
                    "Precision CNC laser cut",
                    "Includes scale Technical Drawing",
                    "Molded PVC canopy", 
                    "Undercarriage detailing",
                    "IAF scheme decals",
                    "Zig-zag puzzle type assembly"
                ],
                "specs": "Length: 55cm, Material: Balsa Wood",
                "ideal_for": "Advanced modelers, display pieces, competitions, collectors",
                "url": "https://statica.in/balsa-wood-aircraft-model-kits/"
            },
            
            "dassault_rafale": {
                "name": "Dassault Rafale Static Model Kit",
                "category": "static_models",
                "price": "₹4,899.00",
                "description": "Detailed model of the French Dassault Rafale multirole fighter aircraft.",
                "features": [
                    "Premium balsa wood construction",
                    "Precision laser-cut parts",
                    "Detailed technical drawings",
                    "Authentic decals and markings"
                ],
                "specs": "Scale model, Material: Balsa Wood",
                "ideal_for": "Advanced modelers, military aircraft enthusiasts",
                "url": "https://statica.in/premium-aircraft-models/"
            },
            
            "sukhoi_su30": {
                "name": "Sukhoi Su-30MKI Static Model Kit", 
                "category": "static_models",
                "price": "₹4,899.00",
                "description": "Scale model of the Indian Air Force's Sukhoi Su-30MKI air superiority fighter.",
                "features": [
                    "Authentic IAF markings",
                    "Precision engineering",
                    "Detailed assembly instructions",
                    "High-quality materials"
                ],
                "specs": "Scale model, Material: Balsa Wood", 
                "ideal_for": "IAF enthusiasts, advanced builders",
                "url": "https://statica.in/premium-aircraft-models/"
            },
            
            # Flying Model Kits
            "skybee_25_cl": {
                "name": "Skybee 25 CL Trainer Kit",
                "category": "flying_models",
                "price": "₹3,994.00",
                "description": "Control Line trainer aircraft perfect for beginners in flying models.",
                "features": [
                    "Ready-to-build control line kit",
                    "Ideal for beginners",
                    "Stable flight characteristics", 
                    "Complete assembly required"
                ],
                "specs": "Control Line, Skill Level: Beginner",
                "ideal_for": "Flying beginners, control line enthusiasts",
                "url": "https://statica.in/flying-model-kits-rc-control-line/"
            },
            
            "ultra_peacemaker": {
                "name": "Ultra Peacemaker Flying Model Kit",
                "category": "flying_models",
                "price": "₹5,166.00", 
                "description": "Advanced flying model kit for experienced hobbyists.",
                "features": [
                    "High-performance design",
                    "Suitable for experienced builders",
                    "Excellent flight characteristics",
                    "Premium construction materials"
                ],
                "specs": "Flying Model, Skill Level: Advanced",
                "ideal_for": "Experienced flyers, hobby competitions",
                "url": "https://statica.in/flying-model-kits-rc-control-line/"
            },
            
            # Tools & Equipment
            "modeling_tools": {
                "name": "Precision Modeling Tools Set",
                "category": "tools",
                "price": "Prices vary",
                "description": "Professional tools for aircraft model assembly and finishing.",
                "features": [
                    "Precision cutters and knives",
                    "Specialized sanding tools",
                    "Assembly jigs and holders",
                    "Finishing supplies"
                ],
                "specs": "Various tools and accessories",
                "ideal_for": "All model builders, serious hobbyists",
                "url": "https://statica.in/precision-modeling-tools-aircraft-assembly/"
            }
        }
        
        self.models = {
            "product": "microsoft/DialoGPT-large",
            "support": "microsoft/DialoGPT-medium", 
            "general": "microsoft/DialoGPT-medium"
        }
    
    async def generate_response(self, prompt: str, agent_type: str = "product") -> str:
        """Generate response with complete Statica product knowledge"""
        try:
            # Build comprehensive product context
            product_context = self._build_product_context()
            system_prompt = self._get_system_prompt(agent_type, product_context)
            
            if self.huggingface_token:
                response = await self._call_huggingface_api(prompt, system_prompt)
                if response and "thank you for your message" not in response.lower():
                    return response
            
            # Fallback to specialized local responses
            return self._get_local_response(prompt, agent_type)
                
        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            return self._get_local_response(prompt, agent_type)
    
    def _build_product_context(self) -> str:
        """Build detailed product context for the AI"""
        catalog_summary = "STatica.in COMPLETE PRODUCT CATALOG:\n\n"
        
        # Group by category
        categories = {
            "static_models": "🎯 STATIC DISPLAY MODEL KITS (Balsa Wood):",
            "flying_models": "✈️ FLYING MODEL KITS (RC & Control Line):", 
            "tools": "🛠️ PRECISION MODELING TOOLS & EQUIPMENT:"
        }
        
        for category_id, category_name in categories.items():
            catalog_summary += f"\n{category_name}\n"
            catalog_summary += "=" * 50 + "\n"
            
            for product_id, product in self.product_catalog.items():
                if product["category"] == category_id:
                    catalog_summary += f"""
Product: {product['name']}
Price: {product['price']}
Description: {product['description']}
Key Features: {', '.join(product['features'][:3])}...
Ideal For: {product['ideal_for']}
Details: {self.company_context['website']}{product['url']}
---
"""
        
        return catalog_summary
    
    def _get_system_prompt(self, agent_type: str, product_context: str) -> str:
        """Get system prompt with complete Statica product knowledge"""
        base_prompts = {
            "product": f"""You are a product expert and aeromodelling specialist for {self.company_context['name']} - India's premier aircraft model kit provider.

COMPANY INFORMATION:
- Business: {self.company_context['business_type']}
- Description: {self.company_context['description']}
- Target Audience: {self.company_context['target_audience']}
- Shipping: {self.company_context['shipping']}
- Support: {self.company_context['support']}
- Website: {self.company_context['website']}
- Email: {self.company_context['support_email']}

COMPLETE PRODUCT CATALOG:
{product_context}

You are an expert in:
1. AIRCRAFT MODEL KITS - Static display models, flying models, balsa wood construction
2. NCC REQUIREMENTS - Which kits are suitable for NCC Air Wing competitions
3. SKILL LEVEL GUIDANCE - Recommending kits based on builder experience
4. TOOLS & EQUIPMENT - Precision modeling tools and their uses
5. AEROMODELLING TECHNIQUES - Assembly, finishing, and display tips

KEY PRODUCT CATEGORIES:
- Static Display Kits: Virus SW 80, Dassault Rafale, Sukhoi Su-30 (Balsa wood)
- Flying Model Kits: Skybee 25 CL, Ultra Peacemaker (Control Line/RC)  
- Modeling Tools: Precision tools for assembly and finishing

PRICING RANGE: ₹3,499 - ₹5,166 (Most kits in ₹3,500-₹5,000 range)

You help customers with:
- Recommending the perfect kit based on their needs and skill level
- Explaining differences between static vs flying models
- NCC competition kit requirements and suitability
- Product features, materials, and construction techniques
- Tool recommendations for different building stages
- Guidance on kit selection for beginners vs advanced builders

Always be:
- Knowledgeable about aeromodelling and aircraft models
- Helpful in guiding customers to the right products
- Specific about product details and specifications
- Encouraging about the hobby and craftsmanship
- Clear about pricing and product availability""",

            "support": f"""You are a customer support specialist for {self.company_context['name']}.

You help with:
- Order status and shipping inquiries across India
- Product questions and specifications
- Assembly guidance and resource direction
- Website navigation and product categories
- General customer service and support

Be supportive and focus on helping modelers with their specific needs.""",

            "general": f"""You are a helpful AI assistant for {self.company_context['name']} website.

Provide friendly, accurate information about our premium aircraft model kits, tools, and aeromodelling supplies."""
        }
        
        return base_prompts.get(agent_type, base_prompts["product"])
    
    def _get_local_response(self, prompt: str, agent_type: str) -> str:
        """Intelligent local responses specific to Statica products"""
        prompt_lower = prompt.lower()
        
        # Product category detection
        if any(word in prompt_lower for word in ['virus', 'sw80', 'static model', 'balsa']):
            return self._get_static_models_response(prompt_lower)
        
        elif any(word in prompt_lower for word in ['flying', 'control line', 'rc', 'skybee', 'peacemaker']):
            return self._get_flying_models_response(prompt_lower)
        
        elif any(word in prompt_lower for word in ['tools', 'equipment', 'cutters', 'sanding']):
            return self._get_tools_response()
        
        elif any(word in prompt_lower for word in ['ncc', 'competition', 'air wing']):
            return self._get_ncc_response()
        
        elif any(word in prompt_lower for word in ['price', 'cost', 'how much']):
            return self._get_pricing_response()
        
        elif any(word in prompt_lower for word in ['difference', 'compare', 'which one']):
            return self._get_comparison_response(prompt_lower)
        
        elif any(word in prompt_lower for word in ['beginner', 'starter', 'first kit']):
            return self._get_beginner_recommendation()
        
        elif any(word in prompt_lower for word in ['hello', 'hi', 'help']):
            return self._get_welcome_response()
        
        else:
            return self._get_general_response(prompt)
    
    def _get_static_models_response(self, prompt: str) -> str:
        """Handle static model kit queries"""
        if '30' in prompt or 'small' in prompt:
            product = self.product_catalog['virus_sw_80_30cm']
        elif '55' in prompt or 'large' in prompt:
            product = self.product_catalog['virus_sw_80_55cm']
        elif 'rafale' in prompt:
            product = self.product_catalog['dassault_rafale']
        elif 'sukhoi' in prompt or 'su30' in prompt:
            product = self.product_catalog['sukhoi_su30']
        else:
            # General static models info
            static_kits = [p for p in self.product_catalog.values() if p['category'] == 'static_models']
            
            response = "**🎯 STATIC DISPLAY MODEL KITS**\n\n"
            response += "We offer premium balsa wood static model kits perfect for display, education, and NCC competitions:\n\n"
            
            for kit in static_kits:
                response += f"✈️ **{kit['name']}** - {kit['price']}\n"
                response += f"   {kit['description'][:100]}...\n"
                response += f"   Ideal for: {kit['ideal_for']}\n\n"
            
            response += f"Browse all static models: {self.company_context['website']}/balsa-wood-aircraft-model-kits/"
            return response

        return f"""**{product['name']}**

💰 **Price:** {product['price']}
📏 **Specs:** {product['specs']}
🎯 **Ideal For:** {product['ideal_for']}

{product['description']}

**Key Features:**
{chr(10).join('• ' + feature for feature in product['features'])}

**Perfect for:** {product['ideal_for']}

🔗 **View Details:** {product['url']}

Ready to build this amazing aircraft model? Visit our website to order!"""
    
    def _get_flying_models_response(self, prompt: str) -> str:
        """Handle flying model kit queries"""
        flying_kits = [p for p in self.product_catalog.values() if p['category'] == 'flying_models']
        
        response = "**✈️ FLYING MODEL KITS**\n\n"
        response += "We offer control line and RC flying model kits for hobbyists who want to fly their creations:\n\n"
        
        for kit in flying_kits:
            response += f"🚀 **{kit['name']}** - {kit['price']}\n"
            response += f"   {kit['description']}\n"
            response += f"   Skill Level: {kit['ideal_for']}\n\n"
        
        response += f"Explore flying models: {self.company_context['website']}/flying-model-kits-rc-control-line/"
        return response
    
    def _get_tools_response(self) -> str:
        """Handle tools and equipment queries"""
        tools = self.product_catalog['modeling_tools']
        
        return f"""**🛠️ PRECISION MODELING TOOLS**

{tools['description']}

**What we offer:**
{chr(10).join('• ' + feature for feature in tools['features'])}

**Essential for:**
• Cutting and shaping balsa wood
• Sanding and finishing surfaces  
• Precise assembly and alignment
• Professional model finishing

**Browse our tools collection:**
{self.company_context['website']}/precision-modeling-tools-aircraft-assembly/

These tools will help you build better, more precise aircraft models!"""
    
    def _get_ncc_response(self) -> str:
        """Handle NCC-specific inquiries"""
        ncc_kits = [
            self.product_catalog['virus_sw_80_30cm'],
            self.product_catalog['virus_sw_80_55cm']
        ]
        
        response = "**Perfect for NCC Air Wing!** 🎖️\n\n"
        response += "Our kits are specifically designed for AIVSC & IGC aeromodelling competitions:\n\n"
        
        for kit in ncc_kits:
            response += f"✅ **{kit['name']}** - {kit['price']}\n"
            response += f"   {kit['specs']}\n"
            response += f"   {kit['ideal_for']}\n\n"
        
        response += "**Why our kits are ideal for NCC:**\n"
        response += "• Precision CNC laser-cut for competition-level accuracy\n"
        response += "• Premium imported balsa wood materials\n"
        response += "• Scale technical drawings included\n"
        response += "• IAF scheme decals for authenticity\n"
        response += "• Meets NCC competition requirements\n\n"
        
        response += "**Recommended for NCC Competitions:**\n"
        response += "• **30cm Virus SW 80** - Standard competition size\n"
        response += "• **55cm Virus SW 80** - For advanced projects\n\n"
        
        response += "Both kits include everything needed for NCC building competitions!"
        return response
    
    def _get_pricing_response(self) -> str:
        """Handle pricing inquiries"""
        return """**💰 PRICING INFORMATION**

Here's our pricing range for Statica aircraft model kits:

**🎯 Static Display Kits:**
• Virus SW 80 (30cm) - ₹3,499.00
• Virus SW 80 (55cm) - ₹4,499.00  
• Dassault Rafale - ₹4,899.00
• Sukhoi Su-30MKI - ₹4,899.00

**✈️ Flying Model Kits:**
• Skybee 25 CL Trainer - ₹3,994.00
• Ultra Peacemaker - ₹5,166.00

**🛠️ Modeling Tools:** Prices vary based on tool sets

**All kits include:**
• Premium imported materials
• Precision laser-cut parts
• Detailed instructions/technical drawings
• Authentic decals and markings

**💡 Budget Tips:**
• Start with Virus SW 80 30cm for beginners (₹3,499)
• Skybee 25 CL is perfect for first flying model (₹3,994)
• Check our website for any active promotions

Which type of model kit interests you?"""
    
    def _get_comparison_response(self, prompt: str) -> str:
        """Handle product comparison queries"""
        if 'static' in prompt and 'flying' in prompt:
            return self._compare_static_vs_flying()
        elif '30' in prompt and '55' in prompt:
            return self._compare_virus_sizes()
        else:
            return self._general_comparison()
    
    def _compare_static_vs_flying(self) -> str:
        """Compare static vs flying models"""
        return """**🆚 STATIC vs FLYING MODELS - Key Differences:**

**🎯 STATIC DISPLAY MODELS:**
• **Purpose:** Display, education, competition
• **Materials:** Balsa wood, detailed finishes  
• **Assembly:** Glue-based, precise construction
• **Result:** Beautiful display piece
• **Price:** ₹3,499 - ₹4,899
• **Best for:** NCC, collectors, home/office decor

**✈️ FLYING MODELS:**
• **Purpose:** Actual flying, hobby flying
• **Materials:** Lighter construction for flight
• **Assembly:** Includes flight controls
• **Result:** Functional flying aircraft
• **Price:** ₹3,994 - ₹5,166  
• **Best for:** Flying enthusiasts, RC hobbyists

**Recommendation:**
- Want a beautiful display piece? → Choose Static Models
- Want to fly your creation? → Choose Flying Models

Which experience are you looking for?"""
    
    def _compare_virus_sizes(self) -> str:
        """Compare Virus SW 80 sizes"""
        kit_30 = self.product_catalog['virus_sw_80_30cm']
        kit_55 = self.product_catalog['virus_sw_80_55cm']
        
        return f"""**🆚 Virus SW 80: 30cm vs 55cm Comparison**

**{kit_30['name']}**
• Price: {kit_30['price']}
• Length: 30cm
• Best for: {kit_30['ideal_for']}
• Portability: Easy to transport
• Detail Level: Standard competition detail

**{kit_55['name']}**  
• Price: {kit_55['price']}
• Length: 55cm  
• Best for: {kit_55['ideal_for']}
• Portability: Larger, more impressive
• Detail Level: Enhanced details and presence

**Key Differences:**
• **Size:** 55cm is 25cm larger (almost double)
• **Price:** 55cm is ₹1,000 more
• **Display Impact:** 55cm makes a bigger statement
• **Portability:** 30cm easier for competitions

**Recommendation:**
- For NCC competitions & beginners: Choose 30cm
- For display pieces & advanced projects: Choose 55cm

Which better fits your needs?"""
    
    def _general_comparison(self) -> str:
        """General comparison guidance"""
        return """**I can help you compare different aircraft model kits!**

Here are common comparisons I can help with:

• **Virus SW 80 - 30cm vs 55cm** (size and purpose)
• **Static Models vs Flying Models** (display vs functional)  
• **Beginner Kits vs Advanced Kits** (skill levels)
• **NCC Competition Kits** (requirements and suitability)
• **Price Ranges** (budget considerations)

What specific comparison are you interested in? For example:
- "Compare Virus 30cm and 55cm"
- "Difference between static and flying models" 
- "Which kit is best for beginners?"
- "NCC competition kit options" """
    
    def _get_beginner_recommendation(self) -> str:
        """Recommend kits for beginners"""
        return """**🚀 PERFECT STARTER KITS FOR BEGINNERS**

Based on your interest in starting aircraft modeling, here are my recommendations:

**🎯 BEST OVERALL BEGINNER KIT:**
• **Virus SW 80 (30cm)** - ₹3,499
  Why: Perfect size, clear instructions, NCC-approved, great learning project

**✈️ BEGINNER FLYING KIT:**
• **Skybee 25 CL Trainer** - ₹3,994  
  Why: Stable flight characteristics, control line system, beginner-friendly

**💡 BEGINNER TIPS:**
1. Start with a smaller kit (30cm) for manageable completion
2. Have basic tools ready (knife, sandpaper, glue)
3. Allow 2-4 weeks for first build
4. Don't rush - enjoy the process!
5. Join online modeling communities for support

**🛠️ ESSENTIAL STARTER TOOLS:**
• Precision knife
• Sanding blocks/files  
• Wood glue
• Cutting mat
• Tweezers for small parts

The **Virus SW 80 (30cm)** is our most popular beginner kit - perfect balance of challenge and achievement!

Ready to start your aeromodelling journey?"""
    
    def _get_welcome_response(self) -> str:
        """Welcome message for Statica"""
        return f"""**Hello! 👋 Welcome to {self.company_context['name']}!**

I'm your AI assistant specializing in premium aircraft model kits and aeromodelling. I can help you with:

• **Aircraft Model Kits** - Static display & flying models
• **NCC Competition Kits** - Virus SW 80 and other approved models  
• **Product Comparisons** - Help choose the right kit for you
• **Beginner Guidance** - Perfect starter kits and tips
• **Tools & Equipment** - Precision modeling tools
• **Pricing & Orders** - Product costs and ordering information

**Quick Navigation:**
🎯 Static Models: Virus SW 80, Rafale, Sukhoi Su-30
✈️ Flying Models: Skybee 25 CL, Ultra Peacemaker  
🛠️ Modeling Tools: Precision tools and equipment

What would you like to know about our premium aircraft model kits?"""

    def _get_general_response(self, prompt: str) -> str:
        """General fallback response"""
        return f"""Thank you for your question about: "{prompt}"

At {self.company_context['name']}, we specialize in premium aircraft model kits including:

• **Static Display Kits** - Virus SW 80, Dassault Rafale, Sukhoi Su-30
• **Flying Model Kits** - Control Line and RC models  
• **Modeling Tools** - Precision tools for perfect builds

I can help you with:
- Kit recommendations based on your experience level
- NCC competition requirements and suitable kits
- Product comparisons and pricing
- Assembly guidance and tool recommendations

For more specific assistance, you can also:
• Browse our website: {self.company_context['website']}
• Email us: {self.company_context['support_email']}

What specific type of aircraft model kit are you interested in?"""

    async def _call_huggingface_api(self, prompt: str, system_prompt: str) -> str:
        """Call Hugging Face API with enhanced context"""
        try:
            model = "microsoft/DialoGPT-large"
            api_url = f"https://api-inference.huggingface.co/models/{model}"
            
            headers = {
                "Authorization": f"Bearer {self.huggingface_token}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
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
                    if "Assistant:" in generated_text:
                        generated_text = generated_text.split("Assistant:")[-1].strip()
                    return generated_text or self._get_local_response(prompt, "product")
            
            return self._get_local_response(prompt, "product")
                
        except Exception as e:
            logger.error(f"Hugging Face API error: {str(e)}")
            return self._get_local_response(prompt, "product")
