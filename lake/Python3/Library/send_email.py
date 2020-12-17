# This file is used to automatically send emails

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sender_email = ''  # 发件人邮箱账号
passwd = ''  # 发件人邮箱SMTP授权码
receiver_email = ''  # 收件人邮箱账号，我这边发送给自己


def mail():
    ret = True
    try:
        data = "email content"
        msg = MIMEText(data, 'plain', 'utf-8')
        msg['From'] = formataddr(["pi", sender_email])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["pi_rec", receiver_email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "daily ip"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.126.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender_email, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender_email, [receiver_email, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")
