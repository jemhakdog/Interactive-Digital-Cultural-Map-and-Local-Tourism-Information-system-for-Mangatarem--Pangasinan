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
