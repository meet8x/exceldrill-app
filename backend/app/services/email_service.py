import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME

    def send_email(self, to_email: str, subject: str, html_content: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(html_content, 'html'))

            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False

    def send_welcome_premium_email(self, to_email: str, user_name: str = "Valued User"):
        subject = "Welcome to Exceldrill AI Premium! 🚀"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                    <h2 style="color: #4F46E5;">Welcome to Premium!</h2>
                    <p>Hi {user_name},</p>
                    <p>Thank you for upgrading to <strong>Exceldrill AI Premium</strong>. We're thrilled to have you on board!</p>
                    <p>You now have unlimited access to:</p>
                    <ul>
                        <li>✨ Advanced HTML Dashboards</li>
                        <li>📊 Unlimited Report Downloads (Word, PPT, Excel)</li>
                        <li>🎨 Custom Color Schemes</li>
                        <li>🚀 Priority Processing</li>
                    </ul>
                    <p>To get started, simply log in to your dashboard and start analyzing your data like a pro.</p>
                    <br>
                    <a href="http://localhost:3000" style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to Dashboard</a>
                    <br><br>
                    <p>If you have any questions, feel free to reply to this email.</p>
                    <p>Happy Analyzing,<br>The Exceldrill AI Team</p>
                </div>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, html_content)
