import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.services.email_service import EmailService

def test_email_sending():
    print("Testing Email Service...")
    
    # Use the sender email as the recipient for testing
    to_email = "meettheanalyst@gmail.com" 
    
    email_service = EmailService()
    
    print(f"Attempting to send test email to {to_email}...")
    success = email_service.send_welcome_premium_email(to_email, "Test User")
    
    if success:
        print("✅ Email sent successfully!")
        return True
    else:
        print("❌ Failed to send email.")
        return False

if __name__ == "__main__":
    if test_email_sending():
        sys.exit(0)
    else:
        sys.exit(1)
