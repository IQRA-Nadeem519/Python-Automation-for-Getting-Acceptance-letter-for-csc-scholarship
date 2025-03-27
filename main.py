
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from email_dats import Email, password  


file_path = 'Dalian-University.csv'


if not os.path.exists(file_path):
    print(f"Error: CSV file '{file_path}' not found.")
    exit()

# Read CSV
df = pd.read_csv(file_path, encoding='utf-8-sig')
print("CSV File Loaded Successfully!")
print(df.head())


expected_columns = ["university", "field", "professor", "email", "research"]

if not all(col in df.columns for col in expected_columns):
    print("Error: CSV file does not contain the expected columns.")
    print(f"Expected: {expected_columns}")
    print(f"Found: {df.columns.tolist()}")
    exit()

df = df.dropna(subset=["professor", "email"])


sender_email = Email
sender_password = password
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Attachment
pdf_filename = 'c:/Users/Dell/OneDrive/Desktop/61-70/63 m/cv.pdf'  

try:
   
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, sender_password)

    for _, row in df.iterrows():
        recipient_name = row['professor'].strip()
        recipient_email = row['email'].strip()
        research_interest = row['research'].strip()

        # Email Content
        subject = "Acceptance Letter for CSC Scholarship"
        body = f"""Dear Professor {recipient_name},

I hope this message finds you well. My name is Muneeb Ahmed, a final-year Mechanical Engineering student at Air University, Pakistan. I am applying for a Master’s degree through the CSC Scholarship and am very interested in your research.

My final-year project, "Smart Helmet," focuses on enhancing safety and communication for workers in hazardous environments. I believe my background aligns well with your work, and I would be honored to contribute to your research.

I have attached my CV for your review. Please let me know if you need any further information. I look forward to your response.

Best regards,
Muneeb Ahmed
"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        
        if os.path.exists(pdf_filename):
            with open(pdf_filename, 'rb') as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(pdf_filename)}"')
                msg.attach(part)

        # Send Email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"✅ Email sent to {recipient_email}")

except Exception as e:
    print(f"❌ SMTP Connection Error: {e}")

finally:
    server.quit()



