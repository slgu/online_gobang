from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import events
from django.core.mail import send_mail
from settings import gobang_logger, validation_cache
import utils
import httputils
import settings
import logging
import json

# Create your views here.
from models import Person
from django_socketio import broadcast_channel,broadcast

@utils.login_check
def index(request):
    person = Person.objects.get(pk=request.session['pk'])
    online_people = list(settings.online_people)
    return httputils.render_html(request,'gobang/index.html',{'person':person, 'people':online_people})

def login(request):
    if request.method == 'POST':
        #check post data login
        username = request.POST.get("username", default = None)
        passwd = request.POST.get("passwd", default = None)
        #check parameters in
        if username is None or passwd is None:
            return Http404('parameters wrong')
        person = list(Person.objects.filter(username = username, passwd = utils.encrypt_passwd(passwd)))
        if len(person) == 0:
            #validation wrong so relogin
            return HttpResponseRedirect('/gobang/login')
        else:
            person = person[0]

        #set session
        request.session['pk'] = person.pk
        request.session['username'] = person.username
        request.session['login'] = True
        return HttpResponseRedirect('/gobang/index')
    else:
        return httputils.render_html(request,'gobang/login.html', {})

def register(request):
    if request.method == 'GET':
        return httputils.render_html(request,'gobang/register.html', {})
    else:
        email = request.POST.get('email', default = None)
        passwd = request.POST.get('passwd', default = None)
        username = request.POST.get('username', default = None)
        validation_code = request.POST.get('validation_code', default = None)
        #check input not none
        for item in (email, passwd,username,validation_code):
            if item is None:
                return render(request, 'gobang/register.html',{'error_msg':'input has none'})
        #check validation code right
        server_validation_code = validation_cache.get(email)
        if server_validation_code is None or server_validation_code != validation_code:
            return render(request, 'gobang/register.html',{'error_msg':'validation code not right'})

        #insert db and use model to check input format right
        added_person = Person(username=username,passwd=passwd,email=email)
        try:
            added_person.save()
        except Exception as e:
            #record exception
            gobang_logger.error("insert db error, {0}".format(e))
            return render(request, 'gobang/register.html',{'error_msg':str(e)})

        #set sessions and redirect
        request.session['login'] = True
        request.session['pk'] = added_person.pk
        request.session['username'] = added_person.username
        return HttpResponseRedirect('/gobang/index')

@csrf_exempt
def send_validation_code_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', default = None)
        #check cache
        print email
        validation_code = validation_cache.get(email)
        if validation_code:
            print "already",validation_code
            return httputils.make_json_response({"message":"validation code already","error_code":"1"})
        else:
            random_number = utils.random_code(6)
            #send email
            #from django.core.mail import send_mail
            #send_mail('Subject here', 'Here is the message.', '892413269@qq.com',['attacker98@163.com'], fail_silently=False)
            print "new_random", random_number
            #set number to cache
            validation_cache.set(email, random_number, settings.VALIDATION_TIME)
        return httputils.make_json_response({"error_code":"0"})
    else:
        return HttpResponseNotFound()

@utils.login_check
def logout(request):
    if request.method == 'POST':
        del request.session['login']
        del request.session['pk']
        del request.session['username']
        return HttpResponseRedirect('/gobang/login')
    else:
        return httputils.make_404('method not right')