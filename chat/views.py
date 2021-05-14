from django.shortcuts import render, redirect
from .models import Chat, Userreg, Room as r
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse, HttpResponse
import json
from django.db.models import Q


def chat(request):
    obj_chat = Chat.objects.all()

    context = {
        'data1': obj_chat
    }
    return render(request, 'chat.html', context)


def chat_sender(request):
    obj_chat = Chat()
    print('this is the message--->', request.GET.get('chat'))
    print(request.session['userid'])
    chat = str(request.GET.get('chat'))
    userid = request.session['userid']
    roomid = request.session['roomId']
    obj_chat.uid = Userreg.objects.get(id=userid)
    obj_chat.chat = chat
    obj_chat.roomid = r.objects.get(id=roomid)
    obj_chat.save()
    return JsonResponse({'response': True}, safe=False)


def fetch(request):
    obj_chat = Chat.objects.filter(roomid=request.session['roomId'])

    context = {
        'data1': obj_chat
    }
    return render(request, "fetch_chat.html", context)


############################################################################################


def room(request):
    userid = request.session.get("userid")
    if userid:
        rooms = r.objects.all()
        if "room" in request.POST:
            room = r()
            room.name = request.POST["room"]
            room.save()
            return render(request, "room.html", {"room": rooms})
        return render(request, "room.html", {"room": rooms})
    else:
        return render(request, "room.html", {"room": ""})

def selectRoom(request):
    if "room" in request.POST:
        roomData = request.POST["room"].split(',')
        request.session["roomId"] = roomData[0]
        request.session["roomName"] = roomData[1]
        return redirect('/chat')
