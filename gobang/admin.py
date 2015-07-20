from django.contrib import admin
from models import Person
from models import Game
# Register your models here.

#add person managed by admin
admin.site.register(Person)
admin.site.register(Game)
