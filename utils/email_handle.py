import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import Email

def send_email(file_path=None):
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtp.login(Email.user, Email.pwd)
    smg = MIMEMultipart()
    text_smg = MIMEText("这是邮件文本内容", "plain", "utf8")
    smg.attach(text_smg)

    file_msg = MIMEApplication(open(file_path, "rb").read())
    file_msg.add_header('content-disposition', 'attachment', filename='report.html')
    smg.attach(file_msg)

    smg["Subject"] = "测试报告"
    smg["From"] = "11@qq.com"
    smg["To"] = "11@163.com"
    smtp.send_message(smg, from_addr="11@qq.com", to_addrs="11@qq.com")


if __name__ == '__main__':
    send_email()
