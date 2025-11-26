import smtplib
import os
import logging
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Dict, Any, List
from email_templates import EmailTemplates

logger = logging.getLogger(__name__)

class EmailAutomationAgent:
    def __init__(self):
        self.templates = EmailTemplates()
        self.smtp_config = {
            "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "port": int(os.getenv("SMTP_PORT", 587)),
            "username": os.getenv("SMTP_USERNAME", ""),
            "password": os.getenv("SMTP_PASSWORD", ""),
            "from_email": os.getenv("FROM_EMAIL", "noreply@statica.in"),
            "from_name": os.getenv("FROM_NAME", "Statica Aircraft Models")
        }
    
    async def send_automated_email(self, email_type: str, recipient_email: str, 
                                 custom_message: str = None, user_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send automated email for Statica aircraft models"""
        try:
            if not self._is_valid_email(recipient_email):
                return {"success": False, "message": "Invalid email address", "email_sent": False}
            
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {"success": False, "message": "Email service not configured", "email_sent": False}
            
            template = self.templates.get_template(email_type, custom_message, user_data or {})
            
            msg = MimeMultipart()
            msg['From'] = f"{self.smtp_config['from_name']} <{self.smtp_config['from_email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = template["subject"]
            
            html_part = MimeText(template["html_body"], 'html')
            text_part = MimeText(template["text_body"], 'plain')
            msg.attach(text_part)
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_config["server"], self.smtp_config["port"])
            server.starttls()
            server.login(self.smtp_config["username"], self.smtp_config["password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent: {email_type} to {recipient_email}")
            return {"success": True, "message": f"Email sent to {recipient_email}", "email_sent": True}
            
        except Exception as e:
            logger.error(f"❌ Email sending failed: {str(e)}")
            return {"success": False, "message": f"Failed: {str(e)}", "email_sent": False}
    
    def _is_valid_email(self, email: str) -> bool:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        return [
            {"type": "welcome", "name": "Welcome to Statica", "description": "New customer welcome with kit recommendations"},
            {"type": "ncc_guide", "name": "NCC Competition Guide", "description": "NCC-specific kit recommendations and tips"},
            {"type": "beginner_guide", "name": "Beginner Modeling Guide", "description": "Starter kit recommendations and tips"},
            {"type": "order_confirmation", "name": "Order Confirmation", "description": "Purchase confirmation email"},
            {"type": "shipping_update", "name": "Shipping Update", "description": "Order shipping status"}
        ]
