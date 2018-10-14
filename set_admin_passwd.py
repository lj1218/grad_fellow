# -*- coding:utf-8 -*-
from grad_fellow.admin import set_password

password = input("Input password for admin: ")
# password = raw_input("Input password for admin: ")  # python2
set_password(password)
