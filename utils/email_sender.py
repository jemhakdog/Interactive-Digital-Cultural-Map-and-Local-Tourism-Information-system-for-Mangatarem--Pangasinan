"""
Email sending utility with clean function design.

Uses EmailConfig dataclass to avoid excessive parameters.
Separates message building from SMTP transmission.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from typing import Optional
import os

logger = logging.getLogger(__name__)


@dataclass
class EmailConfig:
    """
    Email configuration settings.
    
    Attributes:
        sender_email: Sender's email address
        sender_password: Sender's email password
        smtp_server: SMTP server address
        smtp_port: SMTP server port
    """
    sender_email: str
    sender_password: str
    smtp_server: str = 'smtp.gmail.com'
    smtp_port: int = 587
    
    @classmethod
    def from_env(cls) -> Optional['EmailConfig']:
        """
        Create EmailConfig from environment variables.
        
        Returns:
            EmailConfig if credentials found, None otherwise
        """
        sender = os.environ.get('SMTP_EMAIL')
        password = os.environ.get('SMTP_PASSWORD')
        
        if not sender or not password:
            return None
        
        return cls(
            sender_email=sender,
            sender_password=password,
            smtp_server=os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
            smtp_port=int(os.environ.get('SMTP_PORT', '587'))
        )


def _build_email_message(
    subject: str,
    recipient: str,
    body: str,
    html_body: Optional[str],
    sender_email: str
) -> MIMEMultipart:
    """
    Build MIME email message with text and optional HTML.
    
    Args:
        subject: Email subject line
        recipient: Recipient email address
        body: Plain text email body
        html_body: Optional HTML email body
        sender_email: Sender email address
        
    Returns:
        Constructed MIME message
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)
    
    if html_body:
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
    
    return msg


def _send_via_smtp(msg: MIMEMultipart, config: EmailConfig) -> bool:
    """
    Send email message via SMTP server.
    
    Args:
        msg: Constructed MIME message
        config: SMTP configuration
        
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        server = smtplib.SMTP(config.smtp_server, config.smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config.sender_email, config.sender_password)
        server.sendmail(config.sender_email, msg['To'], msg.as_string())
        server.close()
        
        logger.info(f"Email sent successfully to {msg['To']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def send_email(
    subject: str,
    recipient: str, 
    body: str,
    html_body: Optional[str] = None,
    config: Optional[EmailConfig] = None
) -> bool:
    """
    Send email using SMTP (clean API with 5 parameters).
    
    Args:
        subject: The subject of the email
        recipient: The recipient's email address
        body: The plain text body of the email
        html_body: Optional HTML body of the email
        config: Optional EmailConfig (defaults to env vars)
        
    Returns:
        True if email sent successfully, False otherwise
    """
    if config is None:
        config = EmailConfig.from_env()
    
    if config is None:
        logger.error("SMTP credentials not provided")
        return False
    
    msg = _build_email_message(subject, recipient, body, html_body, config.sender_email)
    return _send_via_smtp(msg, config)


def send_password_reset_email(recipient: str, reset_url: str) -> bool:
    """
    Send a password reset email with a styled HTML template.

    Args:
        recipient: User's email address
        reset_url: Full URL of the password reset page

    Returns:
        True if sent successfully, False otherwise
    """
    plain_text = (
        f"You requested a password reset for your GoMangatarem account.\n\n"
        f"Click the link below to reset your password (expires in 30 minutes):\n"
        f"{reset_url}\n\n"
        f"If you did not request this, please ignore this email."
    )

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0a1a14; margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 520px; margin: 0 auto; }}
            .card {{ background: linear-gradient(135deg, #0d2e1e 0%, #0a1f16 100%); border: 1px solid rgba(52,211,153,0.15); border-radius: 24px; overflow: hidden; box-shadow: 0 25px 60px rgba(0,0,0,0.5); }}
            .header {{ background: linear-gradient(135deg, #065f46 0%, #064e3b 100%); padding: 36px 40px; text-align: center; }}
            .icon {{ font-size: 48px; display: block; margin-bottom: 12px; }}
            .header h1 {{ color: #ecfdf5; font-size: 24px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }}
            .header p {{ color: rgba(167,243,208,0.7); font-size: 14px; margin: 6px 0 0; }}
            .body {{ padding: 36px 40px; }}
            .body p {{ color: rgba(209,250,229,0.75); font-size: 15px; line-height: 1.7; margin: 0 0 24px; }}
            .btn {{ display: block; background: linear-gradient(135deg, #059669 0%, #047857 100%); color: #ecfdf5 !important; text-decoration: none; text-align: center; padding: 16px 32px; border-radius: 14px; font-weight: 700; font-size: 16px; letter-spacing: 0.3px; margin: 0 0 28px; box-shadow: 0 8px 24px rgba(5,150,105,0.35); }}
            .warning {{ background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 12px; padding: 14px 18px; color: rgba(253,230,138,0.75); font-size: 13px; line-height: 1.6; margin: 0 0 24px; }}
            .footer {{ padding: 20px 40px; text-align: center; border-top: 1px solid rgba(52,211,153,0.08); }}
            .footer p {{ color: rgba(167,243,208,0.3); font-size: 12px; margin: 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="header">
                    <span class="icon">🌿</span>
                    <h1>Reset Your Password</h1>
                    <p>GoMangatarem Heritage Portal</p>
                </div>
                <div class="body">
                    <p>We received a request to reset the password for your account. Click the button below to choose a new password.</p>
                    <a href="{reset_url}" class="btn">Reset My Password</a>
                    <div class="warning">
                        ⏱ This link expires in <strong>30 minutes</strong>. If you did not request a password reset, you can safely ignore this email — your account is secure.
                    </div>
                    <p style="font-size:13px; color:rgba(167,243,208,0.4); word-break:break-all;">Or copy this URL: {reset_url}</p>
                </div>
                <div class="footer">
                    <p>© 2026 GoMangatarem · Mangatarem, Pangasinan</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(
        subject="Reset Your Password — GoMangatarem",
        recipient=recipient,
        body=plain_text,
        html_body=html_body,
    )
