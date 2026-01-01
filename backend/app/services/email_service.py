import os
import resend

class EmailService:
    @staticmethod
    def send_notification(to_email: str, subject: str, content: str):
        """
        Sends emails via Resend API (works on Hugging Face!)
        """
        print(f"📧 Attempting to send email via Resend to {to_email}")
        
        # Get Resend API Key from environment
        api_key = os.getenv("RESEND_API_KEY")
        
        if not api_key:
            print(f"\n======== 📧 MOCK EMAIL (No Resend API Key) ========")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content:\n{content}")
            print("====================================\n")
            return
        
        try:
            # Set Resend API key
            resend.api_key = api_key
            
            # Send email via Resend
            params = {
                "from": "ZEdny AI <notifications@resend.dev>",
                "to": [to_email],
                "subject": subject,
                "html": content
            }
            
            email_response = resend.Emails.send(params)
            print(f"✅ Email sent successfully via Resend! ID: {email_response['id']}")
            
        except Exception as e:
            print(f"❌ Resend email failed: {e}")
            # Fallback to printing
            print(f"\n======== 📧 EMAIL (Sent Failed, Printed) ========")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content:\n{content}")
            print("====================================\n")

    @staticmethod
    def generate_html_report(report: dict) -> str:
        """Generate HTML email content from issue report."""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #1f2937;">🚨 New Issue Escalated</h2>
            
            <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Summary:</strong> {report.get('description', 'N/A')}</p>
                <p><strong>Department:</strong> {report.get('department', 'General').upper()}</p>
                <p><strong>Priority:</strong> <span style="color: #dc2626; font-weight: bold;">{report.get('priority', 'medium').upper()}</span></p>
            </div>
            
            <h3>Detailed Analysis:</h3>
            <ul>
                {''.join([f'<li>{point}</li>' for point in report.get('points', [])])}
            </ul>
            
            <p style="margin-top: 30px;">
                <a href="https://dashboard.zedny.com/issues/" 
                   style="background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                    View Dashboard
                </a>
            </p>
            
            <p style="color: #6b7280; font-size: 0.875rem; margin-top: 40px;">
                Best regards,<br>
                ZEdny AI System
            </p>
        </body>
        </html>
        """
