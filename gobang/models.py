#!/bin/env python
#  coding=utf-8
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models
import utils
# Create your models here.



#represent player
class Person(models.Model):

    #unique username
    username = models.CharField(max_length = 30, unique = True)
    passwd = models.CharField(max_length = 50, blank = False)
    email = models.CharField(max_length = 30, unique = True)
    #TODO add status

    #rewrite save function to encrpyt passwd
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        origin_obj = None
        origin_objs = list(Person.objects.filter(pk=self.pk))

        if len(origin_objs) == 0 or origin_objs[0].passwd != self.passwd:
            #encrpt passwd
            encrypt_passwd = utils.encrypt_passwd(self.passwd)
            self.passwd = encrypt_passwd

        #super save
        super(Person,self).save()

    def clean(self):
        #validate field mainly for email
        if not utils.validateEmail(self.email):
            raise Exception,'email format wrong'

    #for debug
    def __unicode__(self):
        return "username:%s email:%s encrypt_passwd:%s" % (self.username, self.email, self.passwd)
