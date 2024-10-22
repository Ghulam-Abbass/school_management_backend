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

async def send_reset_password_email(to_email: str, code: str):
    subject = "Password Reset"

    html_content = f"""
    <!doctype html>
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <style>
          body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f7f9fc;
          }}
          .main {{
            display: block;
            margin: auto;
            max-width: 600px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
          }}
          h1 {{
            font-size: 24px;
            color: #333;
            text-align: center;
            margin-bottom: 10px;
          }}
          p {{
            font-size: 16px;
            color: #555;
            text-align: center;
          }}
          .token-container {{
            display: flex;
            justify-content: center; /* Center the token horizontally */
            margin: 20px 0; /* Add some margin for spacing */
          }}
          .token {{
            background-color: #e0e7ff;
            color: #1e40af;
            padding: 15px 25px;
            font-size: 20px;
            border-radius: 5px;
            display: inline-block;
          }}
          .footer {{
            text-align: center;
            font-size: 14px;
            color: #888;
            margin-top: 20px;
          }}
        </style>
      </head>
      <body>
        <div class="main">
          <h1>Password Reset</h1>
          <p>Here is your password reset Code:</p>
          <div class="token-container">
            <div class="token">{code}</div>
          </div>
          <p>This token will expire in 1 hour.</p>
          <div class="footer">
            <p>If you did not request a password reset, please ignore this email.</p>
          </div>
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
