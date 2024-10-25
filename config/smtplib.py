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

async def send_notification_email(
    to_email: str,
    first_name: str,
    last_name: str,
    phone: str,
    email: str,
    address: str,
    age: int,
    education: str,
    gender: str,
    hobby: str,
    degree_year: int,
    bio: str,
    experience: float,
    skills: str,
    teacher_id: int
):
    subject = "New Teacher Job Application"
    html_content = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; padding: 0; }}
          .container {{ max-width: 600px; margin: 20px auto; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; text-align: center; }}
          .header {{ background: #4CAF50; color: #fff; padding: 15px; font-size: 24px; border-radius: 8px 8px 0 0; }}
          .form {{ width: 100%; padding: 20px; color: #444; text-align: left; }}
          .form p {{ font-size: 16px; margin: 8px 0; }}
          .form label {{ font-weight: bold; display: inline-block; min-width: 120px; color: #555; }}
          .form .value {{ color: #333; }}
          .button-container {{ margin-top: 20px; text-align: center; }}
          .button {{ font-size: 16px; padding: 10px 20px; color: #fff; border-radius: 5px; margin: 5px; border: none; cursor: pointer; }}
          .approve {{ background-color: #4CAF50; }}
          .decline {{ background-color: #f44336; }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">New Job Application from a Teacher</div>
          <div class="form">
            <p><label>First Name:</label> <span class="value">{first_name}</span></p>
            <p><label>Last Name:</label> <span class="value">{last_name}</span></p>
            <p><label>Phone:</label> <span class="value">{phone}</span></p>
            <p><label>Email:</label> <span class="value">{email}</span></p>
            <p><label>Address:</label> <span class="value">{address}</span></p>
            <p><label>Age:</label> <span class="value">{age}</span></p>
            <p><label>Education:</label> <span class="value">{education}</span></p>
            <p><label>Gender:</label> <span class="value">{gender}</span></p>
            <p><label>Hobby:</label> <span class="value">{hobby}</span></p>
            <p><label>Degree Year:</label> <span class="value">{degree_year}</span></p>
            <p><label>Bio:</label> <span class="value">{bio}</span></p>
            <p><label>Experience:</label> <span class="value">{experience} years</span></p>
            <p><label>Skills:</label> <span class="value">{skills}</span></p>
          </div>
          <div class="button-container">
            <form action="http://localhost:8090/api/job/approve/{teacher_id}" method="get" style="display:inline;">
              <button type="submit" class="button approve">Approve</button>
          </form>
          <form action="http://localhost:8090/api/job/decline/{teacher_id}" method="get" style="display:inline;">
              <button type="submit" class="button decline">Decline</button>
          </form>
          </div>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Notification email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))


async def send_teacher_email(to_email: str, subject: str, message: str):
    html_content = f"""
    <!doctype html>
    <html>
      <body style="font-family: Arial, sans-serif; text-align: center;">
        <h1>{subject}</h1>
        <p>{message}</p>
      </body>
    </html>
    """
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending email:", str(e))
