from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^send_code$', views.send_validation_code_email, name='send_code'),
    url(r'^logout$', views.logout, name='logout')
]

#django downgrade from 1.7 to 1.6 added
admin.autodiscover()