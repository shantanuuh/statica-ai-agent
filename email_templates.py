from typing import Dict, Any
import datetime

class EmailTemplates:
    def __init__(self):
        self.company_info = {
            "name": "Statica",
            "website": "https://statica.in",
            "support_email": "support@statica.in",
            "phone": "+1 (555) 123-4567",
            "address": "123 Web Street, Digital City, DC 12345"
        }
    
    def get_template(self, template_type: str, custom_message: str = None, user_data: Dict[str, Any] = None) -> Dict[str, str]:
        """Get email template by type"""
        user_data = user_data or {}
        
        templates = {
            "welcome": self._welcome_template(custom_message, user_data),
            "support": self._support_template(custom_message, user_data),
            "newsletter": self._newsletter_template(custom_message, user_data),
            "offer": self._offer_template(custom_message, user_data),
            "thank_you": self._thank_you_template(custom_message, user_data),
            "feedback": self._feedback_template(custom_message, user_data),
            "abandoned_cart": self._abandoned_cart_template(custom_message, user_data),
            "password_reset": self._password_reset_template(custom_message, user_data),
            "order_confirmation": self._order_confirmation_template(custom_message, user_data),
            "shipping_update": self._shipping_update_template(custom_message, user_data)
        }
        
        return templates.get(template_type, self._default_template(custom_message, user_data))
    
    def _welcome_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        subject = f"Welcome to {self.company_info['name']}! 🎉"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ padding: 30px; background: #f9f9f9; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to {self.company_info['name']}! 🎉</h1>
                    <p>We're thrilled to have you on board</p>
                </div>
                <div class="content">
                    <h2>Hello {user_data.get('name', 'there')},</h2>
                    <p>Thank you for choosing {self.company_info['name']} for your WordPress needs!</p>
                    
                    {custom_message if custom_message else """
                    <p>Here's what you can expect from us:</p>
                    <ul>
                        <li>🚀 Professional WordPress development</li>
                        <li>🎨 Custom website design</li>
                        <li>⚡ Performance optimization</li>
                        <li>🔧 Ongoing support and maintenance</li>
                    </ul>
                    """}
                    
                    <p><strong>Ready to get started?</strong></p>
                    <a href="{self.company_info['website']}/dashboard" class="btn">Access Your Dashboard</a>
                    
                    <p>If you have any questions, don't hesitate to reach out!</p>
                </div>
                <div class="footer">
                    <p>{self.company_info['name']} | {self.company_info['address']}</p>
                    <p>Email: {self.company_info['support_email']} | Web: {self.company_info['website']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Welcome to {self.company_info['name']}!
        
        Hello {user_data.get('name', 'there')},
        
        Thank you for choosing {self.company_info['name']} for your WordPress needs!
        
        {custom_message if custom_message else "We offer professional WordPress development, custom design, and ongoing support."}
        
        Get started: {self.company_info['website']}/dashboard
        
        Contact us: {self.company_info['support_email']}
        
        Best regards,
        The {self.company_info['name']} Team
        """
        
        return {"subject": subject, "html_body": html_body, "text_body": text_body}
    
    def _support_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        subject = f"Re: Your Support Request - {self.company_info['name']}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>/* Same styling as welcome template */</style>
        </head>
        <body>
            <div class="container">
                <div class="header" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);">
                    <h1>Support Request Update</h1>
                    <p>We're here to help! 🤝</p>
                </div>
                <div class="content">
                    <h2>Hello {user_data.get('name', 'there')},</h2>
                    
                    {custom_message if custom_message else """
                    <p>Thank you for contacting {self.company_info['name']} support. We've received your request and our team is looking into it.</p>
                    
                    <p><strong>What to expect next:</strong></p>
                    <ul>
                        <li>Initial response within 2-4 hours</li>
                        <li>Regular updates on progress</li>
                        <li>Solution implementation</li>
                    </ul>
                    """}
                    
                    <p><strong>Need immediate help?</strong></p>
                    <p>Email: {self.company_info['support_email']}<br>
                    Phone: {self.company_info['phone']}</p>
                </div>
                <div class="footer">
                    <p>{self.company_info['name']} Support Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Support Request Update
        
        Hello {user_data.get('name', 'there')},
        
        {custom_message if custom_message else "We've received your support request and are working on it."}
        
        Contact: {self.company_info['support_email']}
        Phone: {self.company_info['phone']}
        
        {self.company_info['name']} Support Team
        """
        
        return {"subject": subject, "html_body": html_body, "text_body": text_body}
    
    def _newsletter_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        current_month = datetime.datetime.now().strftime("%B %Y")
        subject = f"📰 {self.company_info['name']} Newsletter - {current_month}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>/* Newsletter specific styling */</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📰 {self.company_info['name']} Newsletter</h1>
                    <p>{current_month} Edition</p>
                </div>
                <div class="content">
                    <h2>Hello {user_data.get('name', 'there')},</h2>
                    
                    {custom_message if custom_message else """
                    <h3>🚀 This Month's Highlights</h3>
                    <ul>
                        <li><strong>WordPress 6.3 Update:</strong> New features and improvements</li>
                        <li><strong>Performance Tips:</strong> Speed up your website by 50%</li>
                        <li><strong>Security Update:</strong> Essential plugins to protect your site</li>
                    </ul>
                    
                    <h3>🎯 Pro Tip of the Month</h3>
                    <p>Did you know? Implementing lazy loading can improve your site's loading time by up to 30%!</p>
                    """}
                    
                    <a href="{self.company_info['website']}/blog" class="btn">Read Our Blog</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html_body": html_body, "text_body": text_body}
    
    def _offer_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        subject = "🎁 Special Offer Just For You!"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head><style>/* Offer styling */</style></head>
        <body>
            <div class="container">
                <div class="header" style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);">
                    <h1>🎁 Special Offer!</h1>
                    <p>Exclusive deal for our valued customers</p>
                </div>
                <div class="content">
                    <h2>Hello {user_data.get('name', 'there')},</h2>
                    
                    {custom_message if custom_message else """
                    <p>As a valued member of our community, we're offering you:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <h1 style="color: #FF6B6B; font-size: 48px; margin: 0;">20% OFF</h1>
                        <p style="font-size: 18px;">All WordPress Services</p>
                        <p><strong>Use code: STATICA20</strong></p>
                    </div>
                    
                    <p>This offer includes:</p>
                    <ul>
                        <li>Website development</li>
                        <li>Performance optimization</li>
                        <li>Security upgrades</li>
                        <li>Ongoing maintenance</li>
                    </ul>
                    """}
                    
                    <p><strong>Offer expires in 7 days!</strong></p>
                    <a href="{self.company_info['website']}/contact" class="btn">Claim Your Discount</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return {"subject": subject, "html_body": html_body, "text_body": text_body}
    
    # Additional template methods for other email types...
    def _thank_you_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        subject = "Thank You for Your Business! 🙏"
        # Implementation similar to above...
        return self._default_template(custom_message, user_data)
    
    def _feedback_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        subject = "We'd Love Your Feedback! ⭐"
        # Implementation similar to above...
        return self._default_template(custom_message, user_data)
    
    def _default_template(self, custom_message: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Default template fallback"""
        subject = f"Message from {self.company_info['name']}"
        
        html_body = f"""
        <div class="container">
            <div class="header">
                <h1>{self.company_info['name']}</h1>
            </div>
            <div class="content">
                {custom_message if custom_message else "<p>Thank you for your message.</p>"}
            </div>
        </div>
        """
        
        return {"subject": subject, "html_body": html_body, "text_body": custom_message or "Thank you for your message."}
