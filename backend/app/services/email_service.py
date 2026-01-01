import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

class EmailService:
    @staticmethod
    def send_notification(to_email: str, subject: str, content: str):
        """
        Sends real emails via Gmail SMTP.
        For production, use environment variables for credentials.
        """
        # Use environment variables for Gmail credentials
        sender_email = os.getenv("SMTP_EMAIL", "your-email@gmail.com")
        sender_password = os.getenv("SMTP_PASSWORD", "your-app-password")
        
        # If no credentials, fall back to mock
        if sender_email == "your-email@gmail.com" or not sender_password:
            print(f"\n======== 📧 MOCK EMAIL (No SMTP Configured) ========")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("------------------------------------")
            print(content)
            print("====================================\n")
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain'))
            
            # Send via Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Real email sent to {to_email}")
        except Exception as e:
            print(f"❌ Email failed: {e}")
            # Fallback to console print
            print(f"\n======== 📧 EMAIL (Sent Failed, Printed) ========")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(content)

    @staticmethod
    def generate_html_report(issue_data: Dict[str, Any]) -> str:
        """
        Creates a formatted email body from the Issue data.
        """
        return f"""
        Dear Team,
        
        A new HIGH PRIORITY issue has been escalated by the AI System.
        
        Summary: {issue_data['summary']}
        Department: {issue_data['department'].upper()}
        Priority: {issue_data['priority'].upper()}
        
        Detailed Analysis:
        {issue_data.get('extracted_info', [])}
        
        Please check your dashboard: https://dashboard.zedny.com/issues/
        
        Best,
        ZEdny AI Agent
        """

