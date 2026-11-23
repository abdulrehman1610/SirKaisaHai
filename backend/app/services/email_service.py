import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from app.config import settings
from app.services.identity import mask_email


def _get_alias_email(tag: Optional[str] = None) -> str:
    """
    Generates dynamic Gmail plus-aliases (e.g., sirkaisahai+otp@gmail.com)
    while keeping the main SMTP login untouched.
    """
    base_email = settings.SMTP_USER or settings.SMTP_SENDER_EMAIL or "sirkaisahai@gmail.com"
    if not tag or "@" not in base_email:
        return base_email

    user_part, domain = base_email.split("@", 1)
    user_clean = user_part.split("+")[0]
    return f"{user_clean}+{tag}@{domain}"


def _send_smtp_email(
    to_email: str,
    subject: str,
    html_body: str,
    sender_display_name: str,
    alias_tag: Optional[str] = None,
) -> bool:
    """Core SMTP dispatcher using TLS. Never logs plaintext recipient email in production."""
    if not settings.SMTP_SERVER or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        if not settings.is_production:
            print("[Email Service] SMTP not configured in .env. Skipping email dispatch.")
        return False

    sender_address = _get_alias_email(alias_tag)
    safe_target = mask_email(to_email) if settings.is_production else to_email

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{sender_display_name} <{sender_address}>"
        msg["To"] = to_email
        msg["Reply-To"] = settings.SMTP_USER

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, [to_email], msg.as_string())

        if not settings.is_production:
            print(f"[Email Service] Successfully sent email to {safe_target} from {msg['From']}")
        return True
    except Exception as e:
        print(f"[Email Service Error] Failed to send email to {safe_target}: {type(e).__name__}")
        return False


def send_otp_email(to_email: str, otp_code: str) -> bool:
    subject = f"SirKaisaHai - Your Verification Code is {otp_code}"
    html = f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 28px; border: 1px solid #E1E2E4; border-radius: 16px; background-color: #FFFFFF;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="color: #501243; font-size: 24px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">SirKaisaHai</h1>
            <p style="color: #82737B; font-size: 13px; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px;">Anonymous Student Feedback</p>
        </div>

        <div style="background-color: #F8F9FB; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <p style="color: #191C1E; font-size: 15px; line-height: 1.5; margin: 0 0 12px 0;">
                Hello Student,
            </p>
            <p style="color: #50434B; font-size: 14px; line-height: 1.5; margin: 0;">
                Use the verification code below to verify your student status and post anonymous reviews:
            </p>

            <div style="background-color: #EFE5FA; padding: 18px; text-align: center; border-radius: 10px; font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #6B2FA0; margin: 18px 0; border: 1px dashed #6B2FA0;">
                {otp_code}
            </div>

            <p style="color: #82737B; font-size: 12px; line-height: 1.4; margin: 0;">
                This code will expire in <strong>10 minutes</strong>. For privacy, your email is never linked to the review text you post.
            </p>
        </div>

        <p style="color: #9CA3AF; font-size: 11px; text-align: center; margin: 0;">
            If you did not request this verification, you can safely ignore this email.
        </p>
    </div>
    """
    return _send_smtp_email(
        to_email=to_email,
        subject=subject,
        html_body=html,
        sender_display_name="SirKaisaHai Verification",
        alias_tag="otp",
    )


def send_update_email(to_email: str, update_title: str, update_content: str) -> bool:
    subject = f"SirKaisaHai Update: {update_title}"
    html = f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 28px; border: 1px solid #E1E2E4; border-radius: 16px; background-color: #FFFFFF;">
        <div style="border-bottom: 2px solid #F3F4F6; padding-bottom: 16px; margin-bottom: 20px;">
            <span style="background-color: #E8F0FC; color: #2D6FD1; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">System Update</span>
            <h2 style="color: #501243; font-size: 20px; margin: 12px 0 0 0;">{update_title}</h2>
        </div>

        <div style="color: #191C1E; font-size: 14px; line-height: 1.6; margin-bottom: 24px;">
            {update_content}
        </div>

        <div style="background-color: #F8F9FB; border-radius: 8px; padding: 14px; text-align: center;">
            <a href="https://sirkaisahai.vercel.app" style="color: #6B2A5B; font-weight: bold; text-decoration: none; font-size: 13px;">Visit SirKaisaHai Portal &rarr;</a>
        </div>
    </div>
    """
    return _send_smtp_email(
        to_email=to_email,
        subject=subject,
        html_body=html,
        sender_display_name="SirKaisaHai Updates",
        alias_tag="updates",
    )


def send_news_email(to_email: str, headline: str, news_html: str) -> bool:
    subject = f"Campus Bulletin: {headline}"
    html = f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 520px; margin: 0 auto; padding: 28px; border: 1px solid #E1E2E4; border-radius: 16px; background-color: #FFFFFF;">
        <div style="border-bottom: 2px solid #F3F4F6; padding-bottom: 16px; margin-bottom: 20px;">
            <span style="background-color: #E7F6EC; color: #2E9E4F; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">Campus News</span>
            <h2 style="color: #501243; font-size: 20px; margin: 12px 0 0 0;">{headline}</h2>
        </div>

        <div style="color: #191C1E; font-size: 14px; line-height: 1.6; margin-bottom: 24px;">
            {news_html}
        </div>

        <p style="color: #82737B; font-size: 12px; text-align: center; margin: 0;">
            Sent by SirKaisaHai Student Community
        </p>
    </div>
    """
    return _send_smtp_email(
        to_email=to_email,
        subject=subject,
        html_body=html,
        sender_display_name="SirKaisaHai News",
        alias_tag="news",
    )
