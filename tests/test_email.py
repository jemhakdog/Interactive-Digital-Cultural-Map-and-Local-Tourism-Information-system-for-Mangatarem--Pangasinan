"""
Sample usage for the email_sender utility.

Before running, set these environment variables:
    - SMTP_EMAIL: Your email address (e.g., your.email@gmail.com)
    - SMTP_PASSWORD: Your app password (for Gmail, use an App Password)

For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate an App Password at https://myaccount.google.com/apppasswords
"""

import os
import sys
from pathlib import Path
import dotenv
dotenv.load_dotenv()
# Add project root to Python path so we can import from utils
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.email_sender import send_email


# ============================================================
# Example 1: Simple Plain Text Email
# ============================================================
def send_simple_email():
    """Send a basic plain text email."""
    success = send_email(
        subject="Hello from Mangatarem Tourism App",
        recipient="recipient@example.com",
        body="This is a simple test email from the tourism app."
    )
    
    if success:
        print("✓ Simple email sent successfully!")
    else:
        print("✗ Failed to send simple email")


# ============================================================
# Example 2: HTML Email with Rich Content
# ============================================================
def send_html_email():
    """Send an email with HTML content."""
    plain_text = "Welcome to Mangatarem Tourism! Visit our cultural sites."
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .btn { background-color: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }
            .footer { background: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Welcome to Mangatarem, Pangasinan!</h1>
        </div>
        <div class="content">
            <h2>Discover Our Rich Cultural Heritage</h2>
            <p>Thank you for your interest in Mangatarem Tourism. Explore our beautiful barangays and cultural landmarks.</p>
            <p><strong>Featured Attractions:</strong></p>
            <ul>
                <li>Historical Churches</li>
                <li>Traditional Festivals</li>
                <li>Local Cuisine</li>
                <li>Natural Wonders</li>
            </ul>
            <p><a href="https://example.com" class="btn">Explore Now</a></p>
        </div>
        <div class="footer">
            <p>Mangatarem Tourism Information System</p>
            <p>© 2026 All rights reserved</p>
        </div>
    </body>
    </html>
    """
    
    success = send_email(
        subject="Welcome to Mangatarem Tourism!",
        recipient="recipient@example.com",
        body=plain_text,
        html_body=html_content
    )
    
    if success:
        print("✓ HTML email sent successfully!")
    else:
        print("✗ Failed to send HTML email")



# ============================================================
# Example 4: Verification Email Template
# ============================================================
def send_verification_email(user_email: str, verification_code: str):
    """Send an account verification email."""
    plain_text = f"Your verification code is: {verification_code}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ background: #2d3436; color: white; padding: 25px; text-align: center; }}
            .content {{ padding: 30px; text-align: center; }}
            .code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .note {{ color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Verify Your Email</h2>
            </div>
            <div class="content">
                <p>Use the code below to verify your email address:</p>
                <div class="code">{verification_code}</div>
                <p class="note">This code expires in 10 minutes. If you didn't request this, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(
        subject="Verify Your Email - Mangatarem Tourism",
        recipient=user_email,
        body=plain_text,
        html_body=html_content
    )


# ============================================================
# Main: Run Examples
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("Email Sender - Sample Usage")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.environ.get('SMTP_EMAIL') or not os.environ.get('SMTP_PASSWORD'):
        print("\n⚠️  Warning: SMTP credentials not set!")
        print("Set these environment variables before running:")
        print("  - SMTP_EMAIL")
        print("  - SMTP_PASSWORD")
        print("\nExample (PowerShell):")
        print('  $env:SMTP_EMAIL = "your.email@gmail.com"')
        print('  $env:SMTP_PASSWORD = "your-app-password"')
        print()
    
    send_verification_email("jemcarlo46@gmail.com", "123456")
    
    # Uncomment the example you want to run:
    # send_simple_email()
    # send_html_email()
    # send_with_custom_smtp()
    # send_verification_email("user@example.com", "123456")
    
    print("\n✨ Uncomment an example function in __main__ to test!")