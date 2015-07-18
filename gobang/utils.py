#!/bin/env python
#  coding=utf-8
import hashlib
import random
import sys
import re
from django.http import HttpResponseRedirect,HttpResponseNotFound
def encrypt_passwd(string):
    m = hashlib.new('ripemd160')
    m.update(string)
    return m.hexdigest()

def to_unicode(string):
    if isinstance(string, str):
        return unicode(string)
    else:
        return string

def to_str(string):
    if isinstance(string, unicode):
        return str(string)
    else:
        return string

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

def random_code(length):
    string = ""
    for i in range(0, length):
        string = string + str(random.randint(0,9))
    return string

def login_check(method):
    def wrapper(request):
        login_flg = request.session.get('login', default = False)
        if not login_flg:
            return HttpResponseRedirect('/gobang/login')
        else:
            return method(request)
    return wrapper

