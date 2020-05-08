import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import  formatdate
from email import encoders

def send_mail(send_from, send_to, subject, text, files=[]):
  smtp = smtplib.SMTP('smtpout.secureserver.net', 587)
  smtp.ehlo()
  smtp.starttls()
  smtp.ehlo()
  smtp.login("kaustav@banerjee.life", "kaustav@123")
  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = ','.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject
  msg.attach( MIMEText(text,'html') )
  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()


send_mail('kaustav@banerjee.life', ['kaustavsmailbox21@gmail.com'], 'TEST', "<h1>TEST</h1>", [])
