import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

smtp_server = 'sandbox.smtp.mailtrap.io'
smtp_port = 2525
smtp_username = '4a995e1a083b15'
smtp_password = 'e250b0efe5b93b'
from_email = 'appriemannsystem@gmail.com'

async def send_reset_password_email(to_email: str, token: str):
    subject = "Password Reset"

    html_content = f"""
    <!doctype html>
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      </head>
      <body style="font-family: sans-serif;">
        <div style="display: block; margin: auto; max-width: 600px;" class="main">
          <h1 style="font-size: 18px; text-align: center; font-weight: bold; margin-top: 20px">Password Reset</h1>
          <p style="font-size: 18px; text-align: center;">Here is your password reset token:</p>
          <div style="text-align: center; margin-top: 50px; margin-bottom:25dp">
            <p style="background-color: #f0f0f0; color: #333; padding: 10px 20px; font-size: 24px; border-radius: 5px; display: inline-block;">{token}</p>
          </div>
          <p style="font-size: 18px; text-align: center;">This token will expire in 1 hour.</p>
        </div>
      </body>
    </html>
    """

    # Create MIME objects
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach HTML part
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))
