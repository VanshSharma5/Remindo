from datetime import datetime
import smtplib
from email.message import EmailMessage
from zoneinfo import ZoneInfo

from app.core.config import settings

IST = ZoneInfo("Asia/Kolkata")


def format_ist_time(dt: datetime) -> str:
    """
    Convert datetime to Indian Standard Time and format it nicely.

    Handles:
    - naive datetime (assumes UTC)
    - timezone-aware datetime
    """

    # If datetime is naive, assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to IST
    ist_dt = dt.astimezone(IST)

    # Format nicely
    return ist_dt.strftime("%I:%M %p, %d %b %Y")

def build_email_html2(tasks):
    task_html = ""

    for task in tasks:
        task_html += f"""
        <div style="background:#f9fafc; border-left:5px solid #4CAF50; 
                    padding:12px; margin-bottom:10px; border-radius:6px;">
            
            <div style="font-size:16px; font-weight:bold; color:#2c3e50;">
                {task.title}
            </div>
            
            <div style="margin:6px 0; color:#555;">
                {task.description}
            </div>
            
            <div style="font-size:12px; color:#fff; background:#3498db; 
                        display:inline-block; padding:4px 8px; border-radius:4px;">
                ⏰ {format_ist_time(task.scheduled_at)}
            </div>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:Arial; background:linear-gradient(135deg,#74ebd5,#ACB6E5); padding:20px;">
        
        <div style="max-width:500px; margin:auto; background:#ffffff; 
                    padding:20px; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            
            <h2 style="text-align:center; color:#4CAF50;">
                📋 Task Reminder
            </h2>
            
            {task_html}
            
        </div>
        
    </body>
    </html>
    """

def build_email_html(tasks):
    task_items = "".join([
        f"""
        <tr>
            <td style="padding:10px 0; border-bottom:1px solid #eee;">
                <strong style="font-size:16px; color:#333;">{t.title}</strong><br/>
                <span style="color:#777; font-size:13px;">
                    {t.description}
                </span><br/>
                <span style="color:#4CAF50; font-size:12px;">
                    ⏰ {format_ist_time(t.scheduled_at)}
                </span>
            </td>
        </tr>
        """
        for t in tasks
    ])

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">
        
        <table width="100%" cellspacing="0" cellpadding="0" style="background-color:#f4f6f8; padding:20px;">
            <tr>
                <td align="center">

                    <!-- Card -->
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.08);">

                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#4CAF50,#2E7D32); padding:20px; text-align:center; color:white;">
                                <h2 style="margin:0;">📅 Your Tasks for Tomorrow</h2>
                                <p style="margin:5px 0 0; font-size:13px; opacity:0.9;">
                                    Stay organized. Stay ahead.
                                </p>
                            </td>
                        </tr>

                        <!-- Body -->
                        <tr>
                            <td style="padding:20px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    {task_items}
                                </table>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background:#fafafa; padding:15px; text-align:center; font-size:12px; color:#999;">
                                You are receiving this because you scheduled tasks.<br/>
                                Keep building consistency 🚀
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """


def send_email(to_email: str, subject: str, tasks):
    message = EmailMessage()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject

    # Plain fallback (important for email clients)
    # plain_text = "\n".join([
    #     f"- {t.title} at {t.scheduled_at}"
    #     for t in tasks
    # ])

    # message.set_content(plain_text)

    # HTML version
    html_content = build_email_html2(tasks)
    message.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(message)