#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Author__ = "Sewell"

'''
指定多个人发邮件报警
'''

import smtplib
from email.mime.text import MIMEText

send_hosts = ['@qq.com',]


def send_mail(SUBJECT, CONTENT):
    email_host = 'smtp.139.com'
    email_user = ''
    email_pwd = ''
    for send_host in send_hosts:
        msg = MIMEText(CONTENT, 'html', 'utf-8')
        msg['Subject'] = SUBJECT
        msg['From'] = email_user
        msg['To'] = send_host
        try:
            smtp = smtplib.SMTP(email_host)
            smtp.set_debuglevel(1)
            smtp.login(email_user,email_pwd)
            smtp.sendmail(email_user, send_host, msg.as_string())
            print('Send Success.')
        except smtplib.SMTPException as e:
            print(e)
        finally:
            smtp.quit()


send_mail('朋友','早上好')
