#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 23:16
# @Author  : Nice
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)
