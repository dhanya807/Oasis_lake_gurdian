import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(user_email, lake_name, lake_area, threshold=50000):
    sender_email = "datathon3@gmail.com"  
    sender_password = "npef sqll lcze bzzs"
    subject = f"Lake Area Alert: {lake_name}"
    
    if lake_area < threshold:
        message = (f"Alert! The lake '{lake_name}' has an area of {lake_area:.2f} square meters, "
                   f"which is less then the threshold. Immediate action may be needed.")
    else:
        message = (f"The lake '{lake_name}' has an area of {lake_area:.2f} square meters, "
                   "which is within the safe limit. No alert is needed.")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {user_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
