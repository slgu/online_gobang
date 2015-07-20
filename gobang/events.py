from django_socketio import events
from models import Game
from models import Person
from django.core.cache import cache
from django.utils import timezone
import settings
@events.on_message(channel="^gobang-")
def deal_on_msg(request, socket, context, message):
    action = message['action']
    if action == 'play':
        req_pk = request.session['pk']
        acc_pk = message['msg']
        if req_pk == acc_pk:
            #same play
            return
        socket.broadcast_channel({'action':'come','msg':'challenge from ' + request.session['username'],'uid':str(req_pk)}, channel = 'gobang-' + acc_pk)
    elif action == 'accept':
        #set play cache
        fid = str(message['msg'])
        sid = str(request.session['pk'])
        settings.play_info_cache.set(fid,sid, settings.REALTIME_MAXDELTA)
        settings.play_info_cache.set(sid,fid, settings.REALTIME_MAXDELTA)
        #set client ready info
        socket.broadcast_channel({'action':'ready','fid':fid,'sid':sid}, channel = 'gobang-' + fid);
        socket.send({'action':'ready','fid':fid,'sid':sid});
    elif action == 'go':
        #just re-send message
        other_pk = settings.play_info_cache.get(str(request.session['pk']))
        if other_pk is None:
            return
        if message['win_status'] == 1:
            #has won
            socket.send({'action':'done','win_status':1})
            socket.broadcast_channel({'action':'done',
                    'x':message['x'],
                    'y':message['y'],
                    'color':message['color'],
                    'win_status':0}, channel = 'gobang-' + other_pk);
            #clear cache
            fid = str(request.session['pk'])
            sid = other_pk
            settings.play_info_cache.delete(sid)
            settings.play_info_cache.delete(fid)
            #record in database
            Game(win_person = Person.objects.get(pk=fid), lose_person = Person.objects.get(pk=sid), game_time=timezone.now()).save()
        else:
            socket.broadcast_channel(dict(message), channel = 'gobang-' + other_pk);
    elif action == 'refuse':
        return

@events.on_subscribe(channel="^gobang-")
def deal_on_subscribe(request, socket, context, channel):
    print channel

@events.on_connect
def deal_on_connect(request, socket, context):
    #add online people
    settings.online_people.add((request.session['pk'], request.session['username']))
    print 'connect', settings.online_people

@events.on_finish
def deal_on_disconnect(request, socket, context):
    #delete online people
    try:
        settings.online_people.remove((request.session['pk'],request.session['username']))
    except Exception as e:
        pass
    print 'disconnect', settings.online_people
