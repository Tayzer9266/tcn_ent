import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List, Optional

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        """
        DNS Records to add for www.tcnentertainment.com to authorize Amazon SES:
        Type	Name	Value
        CNAME	qk2yac66fiurbwfmsbvq4wjvh3hd6x6g._domainkey.www.tcnentertainment.com	qk2yac66fiurbwfmsbvq4wjvh3hd6x6g.dkim.amazonses.com
        CNAME	zk3ge7dgqs5ydvs5j7ynuvypeiewpgx2._domainkey.www.tcnentertainment.com	zk3ge7dgqs5ydvs5j7ynuvypeiewpgx2.dkim.amazonses.com
        CNAME	idbju2z342kseeb4c5foqme67xukwtej._domainkey.www.tcnentertainment.com	idbju2z342kseeb4c5foqme67xukwtej.dkim.amazonses.com
        TXT	_dmarc.www.tcnentertainment.com	v=DMARC1; p=none;
        """

        """
        Initialize the email sender with SMTP server details
        
        Args:
            smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
            smtp_port: SMTP port (e.g., 587 for TLS, 465 for SSL)
            username: Email account username
            password: Email account password or app password
            use_tls: Whether to use TLS encryption (default: True)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        html_body: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email with optional attachments
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            from_email: Sender email address (defaults to username)
            cc_emails: List of CC email addresses
            bcc_emails: List of BCC email addresses
            html_body: HTML version of email body (optional)
            attachments: List of file paths to attach
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            from_email = from_email or self.username
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            
            # Add CC and BCC if provided
            if cc_emails:
                message["Cc"] = ", ".join(cc_emails)
            if bcc_emails:
                message["Bcc"] = ", ".join(bcc_emails)
            
            # Add email body
            if html_body:
                # Create alternative parts for both text and HTML
                message.attach(MIMEText(body, "plain"))
                message.attach(MIMEText(html_body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))
            
            # Add attachments if any
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        self._add_attachment(message, attachment_path)
                    else:
                        print(f"Warning: Attachment file not found: {attachment_path}")
            
            # Connect to SMTP server and send email
            context = ssl.create_default_context()
            
            if self.use_tls:
                # Use TLS
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.username, self.password)
                    
                    # Combine all recipients
                    all_recipients = [to_email]
                    if cc_emails:
                        all_recipients.extend(cc_emails)
                    if bcc_emails:
                        all_recipients.extend(bcc_emails)
                    
                    server.sendmail(from_email, all_recipients, message.as_string())
            else:
                # Use SSL
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.username, self.password)
                    
                    # Combine all recipients
                    all_recipients = [to_email]
                    if cc_emails:
                        all_recipients.extend(cc_emails)
                    if bcc_emails:
                        all_recipients.extend(bcc_emails)
                    
                    server.sendmail(from_email, all_recipients, message.as_string())
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def _add_attachment(self, message: MIMEMultipart, file_path: str):
        """Add an attachment to the email message"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Add header with the filename
            filename = os.path.basename(file_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            
            message.attach(part)
            
        except Exception as e:
            print(f"Failed to add attachment {file_path}: {e}")
            raise

# Example usage and helper function
def send_simple_email(
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    to_email: str,
    subject: str,
    body: str,
    use_tls: bool = True
) -> bool:
    """
    Simple function to send an email without attachments
    
    Args:
        smtp_server: SMTP server address
        smtp_port: SMTP port
        username: Email username
        password: Email password
        to_email: Recipient email
        subject: Email subject
        body: Email body
        use_tls: Use TLS encryption
    
    Returns:
        bool: Success status
    """
    sender = EmailSender(smtp_server, smtp_port, username, password, use_tls)
    return sender.send_email(to_email, subject, body)

# Example usage
if __name__ == "__main__":
    # Example configuration (replace with your actual email settings)
    SMTP_SERVER = "smtp.gmail.com"  # For Gmail
    SMTP_PORT = 587  # For Gmail with TLS
    EMAIL_USERNAME = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_app_password"  # Use app password for Gmail
    
    # Create email sender instance
    email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD)
    
    # Send a simple email
    success = email_sender.send_email(
        to_email="recipient@example.com",
        subject="Test Email from Python",
        body="This is a test email sent using Python!",
        html_body="<h1>Test Email</h1><p>This is a <strong>test email</strong> sent using Python!</p>"
    )
    
    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
