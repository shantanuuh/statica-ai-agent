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
        
        # Email configuration - Set these in Render environment variables
        self.smtp_config = {
            "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "port": int(os.getenv("SMTP_PORT", 587)),
            "username": os.getenv("SMTP_USERNAME", ""),
            "password": os.getenv("SMTP_PASSWORD", ""),
            "from_email": os.getenv("FROM_EMAIL", "noreply@statica.in"),
            "from_name": os.getenv("FROM_NAME", "Statica Support")
        }
        
        # Test configuration on startup
        self._test_smtp_connection()
    
    def _test_smtp_connection(self):
        """Test SMTP connection on startup"""
        try:
            if self.smtp_config["username"] and self.smtp_config["password"]:
                server = smtplib.SMTP(self.smtp_config["server"], self.smtp_config["port"])
                server.starttls()
                server.login(self.smtp_config["username"], self.smtp_config["password"])
                server.quit()
                logger.info("✅ SMTP connection test successful")
            else:
                logger.warning("⚠️ SMTP credentials not set - email sending disabled")
        except Exception as e:
            logger.error(f"❌ SMTP connection failed: {str(e)}")
    
    async def send_automated_email(self, email_type: str, recipient_email: str, 
                                 custom_message: str = None, user_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send automated email based on type"""
        try:
            # Validate recipient email
            if not self._is_valid_email(recipient_email):
                return {
                    "success": False,
                    "message": "Invalid email address",
                    "email_sent": False
                }
            
            # Check if SMTP is configured
            if not self.smtp_config["username"] or not self.smtp_config["password"]:
                return {
                    "success": False,
                    "message": "Email service not configured",
                    "email_sent": False
                }
            
            # Get email template
            template = self.templates.get_template(email_type, custom_message, user_data or {})
            
            # Create email message
            msg = MimeMultipart()
            msg['From'] = f"{self.smtp_config['from_name']} <{self.smtp_config['from_email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = template["subject"]
            
            # Add HTML and plain text versions
            html_part = MimeText(template["html_body"], 'html')
            text_part = MimeText(template["text_body"], 'plain')
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_config["server"], self.smtp_config["port"])
            server.starttls()
            server.login(self.smtp_config["username"], self.smtp_config["password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"✅ Email sent: {email_type} to {recipient_email}")
            
            return {
                "success": True,
                "message": f"Email sent successfully to {recipient_email}",
                "email_sent": True,
                "email_type": email_type
            }
            
        except Exception as e:
            logger.error(f"❌ Email sending failed: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}",
                "email_sent": False
            }
    
    def _is_valid_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available email templates"""
        return [
            {"type": "welcome", "name": "Welcome Email", "description": "New customer welcome email"},
            {"type": "support", "name": "Support Response", "description": "Customer support follow-up"},
            {"type": "newsletter", "name": "Newsletter", "description": "Monthly newsletter"},
            {"type": "offer", "name": "Special Offer", "description": "Promotional offers and discounts"},
            {"type": "thank_you", "name": "Thank You", "description": "Post-purchase thank you"},
            {"type": "feedback", "name": "Feedback Request", "description": "Customer feedback survey"},
            {"type": "abandoned_cart", "name": "Abandoned Cart", "description": "Follow-up for abandoned carts"},
            {"type": "password_reset", "name": "Password Reset", "description": "Password reset instructions"},
            {"type": "order_confirmation", "name": "Order Confirmation", "description": "Order confirmation email"},
            {"type": "shipping_update", "name": "Shipping Update", "description": "Shipping status updates"}
        ]
    
    async def send_bulk_emails(self, email_type: str, recipient_emails: List[str], 
                              custom_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send bulk emails to multiple recipients"""
        results = {
            "total": len(recipient_emails),
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        for email in recipient_emails:
            result = await self.send_automated_email(
                email_type=email_type,
                recipient_email=email,
                user_data=custom_data
            )
            
            if result["email_sent"]:
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "email": email,
                    "error": result["message"]
                })
        
        return results
