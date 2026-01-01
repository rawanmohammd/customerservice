from typing import Dict, Any

class EmailService:
    @staticmethod
    def send_notification(to_email: str, subject: str, content: str):
        """
        Simulates sending an email via SMTP.
        In a real app, this would use a provider like SendGrid, AWS SES, or SMTP.
        """
        print(f"\n======== 📧 MOCK EMAIL SENT ========")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print("------------------------------------")
        print(content)
        print("====================================\n")

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
