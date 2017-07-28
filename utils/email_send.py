#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 15:24
from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from yhg_items.settings import EMAIL_FROM


def random_str(randomlength=8):
	str = ''
	chars = 'abcdefgABCDEFGHIJKLMLNOPQRSTUVWSYZ1234567890'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def send_register_email(email, send_type='regsiter'):
	email_record = EmailVerifyRecord()
	code = random_str(8)
	email_record.code = code
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()
	
	email_title = ""
	email_body = ""
	
	if send_type == 'register':
		email_title = "慕课网激活链接"
		email_body = "请点击下面的连接地址激活账号：http://127.0.0.1:8000/active/{0}".format(code)
	elif send_type == "forget":
		email_title = "找回密码"
		email_body = "请点击下面的连接地址激活账号：http://127.0.0.1:8000/reset/{0}".format(code)
	else:
		pass
	
	send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
	if send_status:
		pass
