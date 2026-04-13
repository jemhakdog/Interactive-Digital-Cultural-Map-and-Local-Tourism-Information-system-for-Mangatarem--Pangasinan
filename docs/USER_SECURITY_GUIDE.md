# User Security Guide

## Overview

This guide explains the security features of the GoMangatarem platform from a user's perspective. Learn how your data is protected and what you can do to keep your account secure.

**Target Audience**: End Users, Contributors, Administrators  
**Last Updated**: April 12, 2026  
**Version**: 1.0.0

---

## Table of Contents

1. [How We Protect Your Data](#how-we-protect-your-data)
2. [Account Security](#account-security)
3. [Safe Browsing Tips](#safe-browsing-tips)
4. [Privacy and Data Collection](#privacy-and-data-collection)
5. [Reporting Security Issues](#reporting-security-issues)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## How We Protect Your Data

### Secure Connections

✅ **HTTPS Encryption**: All connections to GoMangatarem use HTTPS encryption. This means:
- Your login credentials are encrypted during transmission
- Your browsing activity cannot be intercepted by third parties
- Data you submit (photos, reviews, profile information) is encrypted in transit

**How to verify**: Look for the padlock icon 🔒 in your browser's address bar.

### Content Security

✅ **Cross-Site Scripting (XSS) Protection**: We implement multiple layers of protection against malicious code injection:
- All user-submitted content is sanitized before display
- Dangerous scripts are automatically removed
- Content is encoded to prevent unauthorized code execution

**What this means for you**: You can safely view user-generated content (reviews, photos, comments) without risk of malicious scripts running in your browser.

### Session Security

✅ **Protected Sessions**: Your login session is secured with industry-standard protections:
- Session cookies cannot be accessed by JavaScript
- Sessions automatically expire after 7 days of inactivity
- Sessions are protected against cross-site request forgery (CSRF)

**What this means for you**: Your account is protected from unauthorized access, even if you use a shared computer.

### File Upload Safety

✅ **Secure File Uploads**: When you upload photos or videos:
- Filenames are sanitized to remove potentially harmful characters
- Only safe file types are accepted (PNG, JPG, JPEG, GIF, MP4)
- Files are scanned for malicious content

**What this means for you**: You can safely upload photos and videos, and view uploads from other users without security risks.

---

## Account Security

### Creating a Strong Password

Your password must meet these requirements:
- **Minimum 8 characters** in length
- **Maximum 128 characters** allowed
- Can include letters, numbers, and special characters

**Tips for a strong password**:
✅ Use a mix of uppercase, lowercase, numbers, and symbols  
✅ Use a unique password not used on other websites  
✅ Consider using a passphrase (e.g., "Mangatarem2026!CulturalMap")  
✅ Use a password manager to generate and store passwords  

**Avoid these weak passwords**:
❌ "password123"  
❌ "12345678"  
❌ Your username or email  
❌ Common words or phrases  

### Password Reset

If you forget your password:

1. Click **"Forgot Password?"** on the login page
2. Enter your email address
3. Check your email for a password reset link
4. Click the link and create a new password

**Important notes**:
- Reset links expire after **30 minutes**
- Reset links can only be used **once**
- If you don't receive the email, check your spam/junk folder
- Reset links are sent from our secure email system

### Google Sign-In

We offer Google Sign-In as a convenient login option:

**How it works**:
- Click "Sign in with Google" on the login page
- Authenticate with your Google account
- You'll be automatically logged in to GoMangatarem

**What we access from Google**:
- ✅ Your email address
- ✅ Your display name

**What we DON'T access**:
- ❌ Your Google password
- ❌ Your other Google services (Gmail, Drive, etc.)
- ❌ Permission to make changes to your Google account

**Note**: Google Sign-In is only available for regular visitor accounts. Admin and contributor accounts must use traditional username/password login for additional security.

### Session Management

**Automatic Logout**:
- You will be automatically logged out after **7 days** of inactivity
- Closing your browser does guaranteed to end your session
- Use the **"Logout"** button to manually end your session

**Stay Logged In** (Remember Me):
- If you check "Remember Me" during login, your session lasts **30 days**
- This is convenient for personal devices
- **Do not** use "Remember Me" on shared or public computers

**Best Practice**: Always click "Logout" when using a shared computer.

---

## Safe Browsing Tips

### Protecting Your Account

✅ **DO**:
- Use a strong, unique password
- Log out when using shared computers
- Keep your browser up to date
- Use two-factor authentication on your email account
- Report suspicious activity immediately

❌ **DON'T**:
- Share your password with anyone
- Use the same password on multiple websites
- Leave your account logged in on shared computers
- Click on suspicious links claiming to be from GoMangatarem
- Enter your password on any site other than the official GoMangatarem URL

### Recognizing Phishing Attempts

**What is phishing?**: Phishing is when attackers try to trick you into revealing your password by pretending to be GoMangatarem.

**How to recognize phishing emails**:

| Legitimate Email | Phishing Email |
|------------------|----------------|
| Comes from official domain (e.g., @gomangatarem.com) | Comes from suspicious domain |
| Addresses you by username | Uses generic greeting like "Dear User" |
| Contains correct spelling and grammar | Contains spelling mistakes or poor grammar |
| Links go to official GoMangatarem URL | Links go to unfamiliar websites |
| Never asks for your password | Asks you to "verify" or "confirm" your password |

**If you receive a suspicious email**:
1. **Do not** click any links
2. **Do not** download any attachments
3. Check the sender's email address carefully
4. When in doubt, contact us through the official website
5. Report the email to your email provider as phishing

### Browser Security

**Keep Your Browser Updated**:
- Modern browsers include security features that protect you online
- Enable automatic updates in your browser settings
- Supported browsers: Chrome, Firefox, Safari, Edge (latest versions)

**Browser Extensions**:
- Only install extensions from trusted sources
- Be cautious of extensions that request access to "all website data"
- Regularly review and remove unused extensions

**Public Wi-Fi**:
- Avoid logging into sensitive accounts on public Wi-Fi
- If you must use public Wi-Fi, consider using a VPN (Virtual Private Network)
- Look for the padlock icon (🔒) to ensure HTTPS is active

---

## Privacy and Data Collection

### What Data We Collect

**Account Information**:
- Username
- Email address
- Password (encrypted, we cannot read it)
- Account creation date
- User role (visitor, contributor, admin)

**Content You Create**:
- Reviews and comments
- Uploaded photos and videos
- Cultural heritage submissions
- Profile information

**Usage Data**:
- Pages you visit (for analytics)
- Browser type and device information (anonymous)
- IP address (for security and rate limiting)

### How We Use Your Data

| Data Type | Purpose | Shared With? |
|-----------|---------|--------------|
| Username | Display on your content | ✅ Public (on your content) |
| Email | Account recovery, notifications | ❌ Never shared |
| Password | Authentication (encrypted) | ❌ Never shared, never visible |
| Reviews/Comments | Display on platform | ✅ Public (approved content) |
| Photos/Videos | Gallery and cultural documentation | ✅ Public (approved content) |
| IP Address | Security, rate limiting | ❌ Internal use only |
| Page Views | Analytics and improvement | ❌ Aggregated, anonymous |

### Data Retention

**Account Data**: Retained as long as your account is active.

**Content Data**: 
- Approved content is retained indefinitely for cultural preservation
- Rejected or pending content is reviewed and deleted if not approved
- You can request deletion of your content at any time

**Analytics Data**: 
- Aggregated and anonymized for reporting
- Individual session data deleted after 90 days

### Your Rights

You have the right to:
- ✅ Access your personal data
- ✅ Correct inaccurate data
- ✅ Request deletion of your account and content
- ✅ Export your data in a machine-readable format
- ✅ Opt out of non-essential data collection

**To exercise these rights**: Contact us through the official website or email.

---

## Reporting Security Issues

### Found a Security Vulnerability?

If you discover a security issue on the GoMangatarem platform, please follow our **responsible disclosure** process:

1. **Do not** exploit the vulnerability or access other users' data
2. **Do not** publicly disclose the issue before we have a chance to fix it
3. **Contact us immediately** through:
   - Email: [security contact email]
   - Contact form: [website contact page]
4. **Provide details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any relevant screenshots or logs

### What Happens Next?

1. **Acknowledgment** (within 48 hours): We'll confirm receipt of your report
2. **Assessment** (within 7 days): We'll investigate and assess the vulnerability
3. **Fix Development** (within 30 days): We'll develop and test a fix
4. **Deployment**: The fix will be deployed to production
5. **Notification**: We'll notify you when the issue is resolved

### Responsible Disclosure

We appreciate security researchers and users who report vulnerabilities responsibly. We commit to:
- Responding promptly to your report
- Not taking legal action against good-faith researchers
- Giving credit (if desired) in our security acknowledgments
- Keeping you informed of our progress

---

## Frequently Asked Questions

### Q: Is my password stored securely?

**A**: Yes! Your password is:
- **Encrypted** using industry-standard hashing algorithms (bcrypt/PBKDF2)
- **Never stored in plain text** - we cannot read your password
- **Verified** by comparing encrypted values, not by decrypting
- **Protected** against rainbow table attacks with unique salts

Even if our database were compromised, attackers could not easily recover passwords.

### Q: Can other users see my email address?

**A**: No. Your email address is:
- Only visible to you and system administrators
- Never displayed on your profile or content
- Only used for account recovery and system notifications
- Never shared with third parties

### Q: What happens to my data if I delete my account?

**A**: When you request account deletion:
- ✅ Your username, email, and password are permanently deleted
- ✅ Your session tokens are invalidated
- ⚠️ Content you created may remain if already approved (for cultural preservation)
- ⚠️ Anonymous analytics data is retained (not linked to you)

**To request full content deletion**: Contact us specifying which content should be removed.

### Q: Is it safe to upload photos of my family or community events?

**A**: Yes, with these considerations:
- Photos are reviewed before public display
- You retain copyright ownership
- Photos are used only for cultural documentation and tourism promotion
- You can request removal of uploaded photos at any time

**Best practice**: Only upload photos you have permission to share.

### Q: Why does the site ask for my location?

**A**: Location access is optional and used only for:
- Showing attractions near you on the map
- Calculating distances to points of interest
- Improving your browsing experience

**You can deny location access** and still use all features. You can also manually enter a location instead.

### Q: How does the "Remember Me" feature work?

**A**: When you check "Remember Me":
- A secure, encrypted token is stored in your browser
- The token is valid for 30 days
- The token cannot be used to reconstruct your password
- The token is automatically invalidated when you log out

**Security**: The token is protected with the same security as your session cookie (HttpOnly, Secure, SameSite).

### Q: Can I use GoMangatarem on my phone?

**A**: Yes! The platform is fully responsive and works on:
- Smartphones (iOS Safari, Android Chrome)
- Tablets (iPad, Android tablets)
- Desktop computers (Windows, macOS, Linux)

The same security protections apply across all devices.

### Q: What should I do if I suspect my account has been compromised?

**A**: Take these steps immediately:

1. **Change your password**:
   - Log in (if you still can) and change your password
   - Or use "Forgot Password" to reset via email

2. **Review your content**:
   - Check for any changes you didn't make
   - Review uploaded photos and reviews

3. **Contact us**:
   - Report the suspected compromise
   - We can review account activity logs
   - We can temporarily lock your account if needed

4. **Secure your email**:
   - Change your email password
   - Enable two-factor authentication on your email
   - Check for unauthorized access

---

## Security Features Summary

| Feature | What It Does | How It Protects You |
|---------|--------------|---------------------|
| **HTTPS Encryption** | Encrypts all data in transit | Prevents eavesdropping |
| **Content Security Policy** | Restricts what scripts can run | Blocks malicious code |
| **HttpOnly Cookies** | Prevents JavaScript cookie access | Protects session from XSS |
| **SameSite Cookies** | Restricts cross-site cookie sending | Prevents CSRF attacks |
| **Input Sanitization** | Removes dangerous scripts from user input | Prevents stored XSS |
| **Output Encoding** | Converts special characters to HTML entities | Prevents script execution |
| **Rate Limiting** | Limits requests per minute | Prevents brute-force attacks |
| **Password Encryption** | Hashes passwords with salt | Protects passwords if breached |
| **File Upload Scanning** | Validates filenames and extensions | Prevents malicious file uploads |
| **CSRF Tokens** | Unique tokens on all forms | Prevents unauthorized actions |

---

## Additional Resources

### Learn More About Online Security

- [Stay Safe Online - National Cybersecurity Alliance](https://staysafeonline.org/)
- [OnGuardOnline - FTC Security Tips](https://www.consumer.ftc.gov/features/feature-0014-identity-theft)
- [Have I Been Pwned? - Check if your email was in a breach](https://haveibeenpwned.com/)

### Browser Security Settings

- [Chrome Security Settings](https://support.google.com/chrome/answer/95647)
- [Firefox Privacy and Security](https://support.mozilla.org/en-US/products/firefox/privacy-and-security)
- [Safari Privacy Report](https://support.apple.com/en-us/HT211081)
- [Edge Security Features](https://support.microsoft.com/en-us/microsoft-edge)

---

**Document Version**: 1.0.0  
**Last Updated**: April 12, 2026  
**Next Review**: October 12, 2026  
**Questions?**: Contact us through the official GoMangatarem website
