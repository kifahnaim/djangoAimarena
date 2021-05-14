import datetime
import json
from distutils.command import register

from django import template
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail, EmailMessage
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from home.models import newsbanner, emailnews
from nonmotiongame.models import products as p
from authapp.models import Role_permissions, UserRoles, Userreg, admin_actions, Banfromforum, Banfromgame, UserSession, \
    kickedfromwebsite
from authapp.models import Userreg

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
# Create your views here.
from authentication import settings
from forum.models import Post, Comment, Notification, topic, subtopic


def baseview(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    roleName = request.session.get('RoleName')
    latestusers = Userreg.objects.filter(Role_id__RoleName='User').order_by('-datecreated')[0:8]
    latestuserscount = Userreg.objects.filter(Role_id__RoleName='User').order_by('-datecreated')[0:8].count()
    userdetails = Userreg.objects.filter(id=userid)
    print(userdetails)
    print(latestuserscount)
    listusers = None
    print("Roleid" + str(role))
    if roleName == "Forum Moderator":
        listusers = Userreg.objects.filter(Role_id__RoleName='User')
    elif roleName == "Admin":
        listusers = Userreg.objects.exclude(Role_id__RoleName='Admin')
    allusers = Userreg.objects.filter(is_active=True).count()
    manageposts = Post.objects.exclude(deleted=True).order_by('-timestamp')[0:20]
    print(listusers)
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "stafftemplate.html",
                  {"permission": resultsList, "listusers": listusers, "manageposts": manageposts,
                   "latestusers": latestusers, "latestuserscount": latestuserscount, "allusers": allusers,
                   "userdetails": userdetails,
                   })


def staffusers(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    roleName = request.session.get('RoleName')

    userdetails = Userreg.objects.filter(id=userid)
    print(userdetails)
    listroles = None
    listusers = None
    print("Roleid" + str(role))
    if roleName == "Forum Moderator":
        listusers = Userreg.objects.filter(Role_id__RoleName='User')
    elif roleName == "Admin":
        listusers = Userreg.objects.exclude(Role_id__RoleName='Admin')
    listroles = UserRoles.objects.all()
    allusers = Userreg.objects.filter(is_active=True).count()
    bannedusersforum = Banfromforum.objects.all()
    bannedusersgame = Banfromgame.objects.all()
    admin_actionsbans = admin_actions.objects.all()
    kicks = kickedfromwebsite.objects.all()
    nowtime = datetime.datetime.now()
    print(listusers)
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "staffusers.html",
                  {"permission": resultsList, "listusers": listusers,
                   "nowtime": nowtime,
                   "allusers": allusers,
                   "userdetails": userdetails,
                   "listroles": listroles,
                   "bannedusersforum": bannedusersforum,
                   "bannedusersgame": bannedusersgame,
                   "admin_actionsbans": admin_actionsbans,
                   "kicks": kicks
                   })


def staffposts(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    manageposts = Post.objects.all()
    userdetails = Userreg.objects.filter(id=userid)
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "staffposts.html",
                  {"permission": resultsList, "manageposts": manageposts, "userdetails": userdetails
                   })


def banuser(request, pk):
    if request.method == "POST" and request.is_ajax():
        bannedby = request.session.get('userid')
        user_id = request.POST.get('user_id')
        hours = request.POST.get('hours')
        choice = request.POST.get('choice')
        print("hello")
        print(user_id)
        if choice == "Ban from forum":
            if Banfromforum.objects.filter(user_id_id=user_id).count() < 1:
                print("Ban from forum")
                ban = Banfromforum()
                ban.user_id = Userreg(user_id)
                ban.Banned_until = datetime.datetime.now() + datetime.timedelta(hours=int(hours))
                ban.banned_by = Userreg(bannedby)
                ban.save()
            else:
                Banfromforum.objects.filter(user_id_id=user_id).update(
                    Banned_until=datetime.datetime.now() + datetime.timedelta(hours=int(hours)))
                print("under 1")
            if admin_actions.objects.filter(user_id_id=user_id).count() < 1:
                print("banned forum")
                adminactions = admin_actions()
                adminactions.user_ban_forum = True
                adminactions.user_id = Userreg(user_id)
                adminactions.save()
            else:
                print("banned update")
                admin_actions.objects.filter(user_id_id=user_id).update(user_ban_forum=True)

        elif choice == "Ban from game":
            print("Ban from nonmotiongame")
            if Banfromgame.objects.filter(user_id_id=user_id).count() < 1:
                ban = Banfromgame()
                ban.user_id = Userreg(user_id)
                ban.Banned_until = datetime.datetime.now() + datetime.timedelta(hours=int(hours))
                ban.banned_by = Userreg(bannedby)
                ban.save()
            else:
                Banfromgame.objects.filter(user_id_id=user_id).update(
                    Banned_until=datetime.datetime.now() + datetime.timedelta(hours=int(hours)))

            if admin_actions.objects.filter(user_id_id=user_id).count() < 1:
                adminactions = admin_actions()
                adminactions.user_ban_game = True
                adminactions.user_id = Userreg(user_id)
                adminactions.save()
            else:
                admin_actions.objects.filter(user_id_id=user_id).update(user_ban_game=True)

        return JsonResponse({"response": "success"})
    else:
        print("fail")
        return JsonResponse({"response": "fail"})


def unbanuser(request, pk):
    if request.method == "POST" and request.is_ajax():

        user_id = request.POST.get('user_id')
        choice = request.POST.get('choice')
        if choice == "unbanbtn":
            admin_actions.objects.filter(user_id_id=user_id).update(user_ban_game=False)
            Banfromgame.objects.filter(user_id_id=user_id).delete()

        elif choice == "unban":
            admin_actions.objects.filter(user_id_id=user_id).update(user_ban_forum=False)
            Banfromforum.objects.filter(user_id_id=user_id).delete()
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def kickuser(request, pk):
    if request.method == "POST" and request.is_ajax():

        user_id = request.POST.get('user_id')
        if admin_actions.objects.filter(user_id_id=user_id).count() < 1:
            adminactions = admin_actions()
            adminactions.user_kick_forum = True
            adminactions.user_id = Userreg(user_id)

            adminactions.save()
        else:
            admin_actions.objects.filter(user_id_id=user_id).update(user_kick_forum=True)

        kicks = kickedfromwebsite()
        kicks.kicked_time = datetime.datetime.now()
        kicks.user_id = Userreg(user_id)
        kicks.kicked_by = Userreg(request.session.get('userid'))
        kicks.save()

        delete_user_sessions(user_id)

        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


class Detailmanageposts(DetailView):
    model = Post

    template_name = "Detailmanageposts.html"

    def get_context_data(self, **kwargs):
        userid = self.request.session.get('userid')
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super(Detailmanageposts, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.kwargs['pk'], reply_id=None)
        closedposts = Post.objects.filter(is_closed=True, id=self.kwargs['pk'])
        print(closedposts)
        liked = False
        if stuff.likes.filter(id=userid).exists():
            liked = True

        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["com"] = comments
        context["closedposts"] = closedposts

        return context


def closepost(request, pk):
    if request.method == "POST" and request.is_ajax():
        print("closed0")
        post_id = request.POST.get('post_id')
        print("closed1")
        Post.objects.filter(id=post_id).update(is_closed=True)
        print("closed2")
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def deletepost(request, pk):
    if request.method == "POST" and request.is_ajax():
        post = Post.objects.filter(id=pk).update(deleted=True)
        print("deleted")
        return JsonResponse({"pk": pk})
    else:
        return JsonResponse({"message": "fail"})


def openpost(request, pk):
    if request.method == "POST" and request.is_ajax():
        post = Post.objects.filter(id=pk).update(is_closed=False)
        print("opened")
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('Post_like'))
    userid = request.session.get('userid')
    liked = False
    if post.likes.filter(id=request.session.get('userid')).exists():
        post.likes.remove(request.session.get('userid'))
        sender = Userreg.objects.get(id=userid)
        notify = Notification.objects.filter(post=post, sender=sender, user=post.author, Notification_type=1)
        notify.delete()
        liked = False
    else:
        post.likes.add(request.session.get('userid'))

        sender = Userreg.objects.get(id=userid)
        if userid != post.author_id:
            notify = Notification(post=post, sender=sender, user=post.author,
                                  text_preview=str(sender) + " " + "liked your post", Notification_type=1)
            notify.save()
        liked = True
    return HttpResponseRedirect(reverse('staff:Detailmanageposts', args=[str(pk)]))


def updaterank(request, pk):
    if request.method == "POST" and request.is_ajax():
        userid = request.POST.get('user_id')
        role = request.POST.get('role')
        print(role)

        roleid = None
        if role:
            print("role kifah")
            print(role)
            roleid = UserRoles.objects.get(id=role).pk
            print(roleid)
        print(roleid)
        print(userid)
        print("roleid")

        Userreg.objects.filter(id=userid).update(Role_id=roleid)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def contact(request):
    if request.method == "POST":
        message_name = request.POST.get("message_name").strip()
        message_email = request.POST.get('message_email').strip()
        message = request.POST.get("message").strip()
        attachment = request.FILES.get('file')
        print('attachment')
        print(attachment)

        try:
            msg = EmailMessage(message_name,
                               message, to=[message_email])
            msg.content_subtype = 'html'
            if attachment:
                msg.attach(attachment.name, attachment.read(), attachment.content_type)
            msg.send()
        except:
            print("exception thrown")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def inbox(request):
    return render(request, "mailbox.html")


def compose(request):
    userid = request.session.get('userid')
    userdetails = Userreg.objects.filter(id=userid)
    role = request.session.get('Role')
    roleName = request.session.get('RoleName')
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "compose.html",
                  {"permission": resultsList, "userdetails": userdetails
                   })


class useractions(DetailView):
    model = Userreg
    template_name = 'useractions.html'

    def get_context_data(self, **kwargs):
        user = Userreg.objects.get(id=self.kwargs['pk'])
        print(user)
        usermanage = admin_actions.objects.filter(user_ban=True).values('user_ban', 'user_id_id')
        context = super(useractions, self).get_context_data(**kwargs)
        context["usermanage"] = usermanage

        return context


def staffactions(request):
    context = {}

    listusers = Userreg.objects.exclude(Role_id__RoleName='Admin')

    context["users"] = listusers
    print(listusers)

    return context


def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()


def searchusers(request):
    global query
    if request.method == 'POST':
        role = request.session.get('Role')
        search_text = request.POST.get("search_text")

        cursor = None

        permission = None

        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, pages p, userrole ur where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        permission = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            permission.append(d)
        print(permission)

        resultsList = None
        try:

            cursor = connection.cursor()

            cursor.execute(
                "select rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome, u.id as id, u.Username as Username, r.RoleName as RoleName from useregister u, userrole r, role_permissions rp where u.Role_id = r.id and rp.Role_id_id=r.id and u.Username LIKE '%%%%%s%%%%' " % search_text)
            items = cursor.fetchall()

            x = cursor.description

            resultsList = []

            for r in items:
                i = 0
                d = {}
                while i < len(x):
                    d[x[i][0]] = r[i]
                    i = i + 1
                resultsList.append(d)
            print("resultsList")
            print(resultsList)
        except:
            print("fail")

        if resultsList:
            listusers = Userreg.objects.exclude(Role_id__RoleName='Admin').filter(Username__contains=search_text)
            print("list of users")
            print(listusers)
            return render(request, 'staff-filter.html', {"permission": permission, "listusers": listusers})
        else:
            return JsonResponse({"filtereddata":
                                     "No Users found!"})
    else:
        search_text = ''


def searchposts(request):
    global query
    if request.method == 'POST':
        search_text = request.POST.get("search_text")
        role = request.session.get('Role')

        # specific = Post.objects.select_related('author')
        # posts = Post.objects.filter(title__contains=search_text)
        # data = specific.values()
        postslist = None
        # cursor = connection.cursor()
        #
        # query = "select ur.RoleName as Role, p.id as id, p.title as title, p.thumbnail as thumbnail, p.deleted as deleted ,p.body as body, u.Username as Username FROM posts p, useregister u, Userrole ur where p.author_id = u.id and u.Role_id = ur.id and p.title LIKE  '%%%%%s%%%%' " % search_text
        #
        # cursor.execute(query)
        #
        # items = cursor.fetchall()
        #
        # x = cursor.description
        # postslist = []
        #
        # for r in items:
        #     i = 0
        #     d = {}
        #     while i < len(x):
        #         d[x[i][0]] = r[i]
        #         i = i + 1
        #     postslist.append(d)
        # print("postslist")
        # print(postslist)

        postslist = Post.objects.filter(title__contains=search_text)
        cursor = connection.cursor()

        cursor.execute(
            "select ur.RoleName as RoleName, rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur where  rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        permission = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            permission.append(d)
        print(permission)

        if postslist:
            return render(request, 'post-filter.html', {"permission": permission, "manageposts": postslist})
        else:
            return JsonResponse({"filtereddata":
                                     "No Posts found!"})
    else:
        search_text = ''


def userprofile(request, pk):
    if request.is_ajax and request.method == 'POST':
        context = {}
        user_profile = Userreg.objects.filter(id=pk).values('Role_id__RoleName', 'Username', 'Firstname', 'Lastname',
                                                            'user_thumbnail', 'authorpost')

        print("userprofile")

        print(user_profile)
        print(user_profile.count())
        count = user_profile.count()
        context['user_profile'] = user_profile
        context["count"] = count
        return JsonResponse({"data": list(user_profile), "count": count})
    else:
        print("userprofile2")

        return JsonResponse({"data": 'fail'})


def stafftopics(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    userdetails = Userreg.objects.filter(id=userid)
    topics = topic.objects.all()
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "stafftopics.html",
                  {"topics": topics, "userdetails": userdetails, "permission": resultsList})


def stafftopicscreate(request):
    if request.method == "POST":
        topiccreate = topic()
        if request.POST.get("title"):
            topiccreate.topic_title = request.POST.get("title").strip()
        if request.POST.get("description"):
            topiccreate.topic_description = request.POST.get("description").strip()
        if request.POST.get("visible"):
            topiccreate.is_visible = request.POST.get("visible").strip()
        else:
            topiccreate.is_visible = False
        topiccreate.save()
        return redirect("staff:stafftopics")
    return redirect("staff:stafftopics")


def stafftopicsedit(request, pk):
    if request.method == "POST" and request.is_ajax():
        topic_id = request.POST.get('topic_id')
        title = request.POST.get('title')
        desc = request.POST.get('desc')

        if request.POST.get("visible") == "True":
            visible = request.POST.get('visible')
        else:
            visible = False
        print(visible)
        topic.objects.filter(id=topic_id).update(topic_title=title, topic_description=desc, is_visible=visible)
        return redirect("staff:stafftopics")
    return redirect("staff:stafftopics")


def stafftopicsdelete(request, pk):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        topic.objects.filter(id=topic_id).update(is_deleted=True)
        print(topic_id)
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def stafftopicsundo(request, pk):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        topic.objects.filter(id=topic_id).update(is_deleted=False)
        print(topic_id)

        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def staffsubtopics(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    userdetails = Userreg.objects.filter(id=userid)
    subtopics = subtopic.objects.all()

    subtopicsdistinct = topic.objects.values('topic_title', 'id').distinct()
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "staffsubtopics.html",
                  {"subtopics": subtopics, "userdetails": userdetails, "permission": resultsList,
                   "subtopicsdistinct": subtopicsdistinct})


def staffsubtopicscreate(request):
    if request.method == "POST":
        print(request.POST.get("dropdowntopics"))
        subtopiccreate = subtopic()
        if request.POST.get("subtitle"):
            subtopiccreate.sub_topic_title = request.POST.get("subtitle").strip()
        if request.POST.get("subdescription"):
            subtopiccreate.sub_topic_description = request.POST.get("subdescription").strip()
        subtopiccreate.topic = topic(request.POST.get("dropdowntopics"))
        if request.POST.get("visible"):
            subtopiccreate.subtopic_visible = request.POST.get("visible").strip()
        else:
            subtopiccreate.subtopic_visible = False

        if request.POST.get("rejectedappeal"):
            subtopiccreate.rejectedappeal_visible = request.POST.get("rejectedappeal").strip()
        else:
            subtopiccreate.rejectedappeal_visible = False

        if request.POST.get("acceptedappeal"):
            subtopiccreate.acceptedappeal_visible = request.POST.get("acceptedappeal").strip()
        else:
            subtopiccreate.acceptedappeal_visible = False

        if request.POST.get("acceptedstaff"):
            subtopiccreate.accepted_visible = request.POST.get("acceptedstaff").strip()
        else:
            subtopiccreate.accepted_visible = False

        if request.POST.get("rejectedstaff"):
            subtopiccreate.rejected_visible = request.POST.get("rejectedstaff").strip()
        else:
            subtopiccreate.rejected_visible = False

        if request.POST.get("onlystaff"):
            subtopiccreate.is_visible = False
        else:
            subtopiccreate.is_visible = True

        if request.POST.get("pinned"):
            subtopiccreate.pinned_visible = request.POST.get("pinned").strip()

        else:
            subtopiccreate.pinned_visible = False

        subtopiccreate.save()
        return redirect("staff:stafftopics")
    return redirect("staff:stafftopics")


def staffsubtopicsdelete(request, pk):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        subtopic.objects.filter(id=topic_id).update(subtopic_deleted=True)
        print(topic_id)
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def staffsubtopicsundo(request, pk):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        subtopic.objects.filter(id=topic_id).update(subtopic_deleted=False)
        print(topic_id)

        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def staffsubtopicsedit(request, pk):
    if request.method == "POST":
        sub_topic_id = request.POST.get('topic_id')
        topic_id = request.POST.get('dropdowntopics')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        print(title)
        print(desc)
        print(request.POST.get('editonlystaff'))
        print(request.POST.get('acceptedappeal'))

        if request.POST.get('visible') == "True":
            visible = request.POST.get('visible')
        else:
            visible = False

        if request.POST.get('editonlystaff') == "True":
            editonlystaff = False
        else:
            editonlystaff = True
        if request.POST.get('pinned') == "True":
            pinned = request.POST.get('pinned')
        else:
            pinned = False
        if request.POST.get('acceptedstaff') == "True":
            acceptedstaff = request.POST.get('acceptedstaff')
        else:
            acceptedstaff = False

        if request.POST.get('rejectedstaff') == "True":
            rejectedstaff = request.POST.get('rejectedstaff')
        else:
            rejectedstaff = False

        if request.POST.get('acceptedappeal') == "True":
            acceptedappeal = request.POST.get('acceptedappeal')
        else:
            acceptedappeal = False

        if request.POST.get('rejectedappeal') == "True":
            rejectedappeal = request.POST.get('rejectedappeal')
        else:
            rejectedappeal = False
        topicid = topic.objects.get(id=topic_id)
        subtopic.objects.filter(id=sub_topic_id).update(accepted_visible=acceptedstaff, rejected_visible=rejectedstaff,
                                                        pinned_visible=pinned, acceptedappeal_visible=acceptedappeal,
                                                        rejectedappeal_visible=rejectedappeal, is_visible=editonlystaff,
                                                        topic=topicid, sub_topic_title=title,
                                                        sub_topic_description=desc, subtopic_visible=visible)

        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def staffpostsundo(request, pk):
    if request.method == "POST":
        postid = request.POST.get('post_id')
        Post.objects.filter(id=postid).update(deleted=False)
        print(postid)

        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})


def manageproducts(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    products = p.objects.all()
    userdetails = Userreg.objects.filter(id=userid)
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
            "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    return render(request, "manageshop.html",
                  {"userdetails": userdetails, "permission": resultsList,
                   "products": products})


@csrf_exempt
def editproduct(request, pk):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        p.objects.filter(id=product_id).update(product_name=title, product_desc=desc)
        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "fail"})


def deleteproduct(request, pk):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        p.objects.filter(id=product_id).update(is_deleted=True)
        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "fail"})


def undoproduct(request, pk):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        p.objects.filter(id=product_id).update(is_deleted=False)
        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "fail"})


@csrf_exempt
def createproduct(request):
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        type = request.POST.get("type")
        image_path1 = None
        image_path2 = None
        try:
            file_input1 = request.FILES['productsprite']
            file_input2 = request.FILES['productimage']
            fs = FileSystemStorage()
            x = datetime.datetime.now()
            image_path1 = fs.save("AimArena" + x.strftime("%a%m%y%H%S") + file_input1.name, file_input1)
            image_path2 = fs.save("AimArena" + x.strftime("%a%m%y%H%S") + file_input2.name, file_input2)
        except MultiValueDictKeyError:
            pass

        create = p()
        create.product_price = price
        create.product_desc = desc.strip()
        create.product_name = name.strip()
        create.product_type = type
        create.product_image = image_path2
        create.product_spriteimage = image_path1
        create.save()

        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "fail"})

def managenews(request):
    userid = request.session.get('userid')
    role = request.session.get('Role')
    cursor = None
    resultsList = None
    try:
        cursor = connection.cursor()

        cursor.execute(
                "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
                    role))
        items = cursor.fetchall()

        x = cursor.description

        resultsList = []

        for r in items:
            i = 0
            d = {}
            while i < len(x):
                d[x[i][0]] = r[i]
                i = i + 1
            resultsList.append(d)

        print(resultsList)

    except Exception as e:
        cursor.close()
        print("fail")
    news = newsbanner.objects.all()
    userdetails = Userreg.objects.filter(id=userid)
    context = {"permission": resultsList, "userdetails": userdetails, "news": news}
    return render(request, "staffnews.html", context)


def managenewscreate(request):
    if request.method == "POST":
        x = newsbanner()
        x.news = request.POST.get("news").strip()
        x.datetime = datetime.datetime.now()
        x.is_deleted = False
        x.updated_by = Userreg(request.session.get("userid"))
        x.save()
        message_name = "Aim Arena"
        message = "New news are there ! Come and check latest news on our website!"
        emails = emailnews.objects.values_list('email', flat=True).filter(subscription=True)
        for i in emails:
            msg = EmailMessage(message_name,
                               message, to=[i])
            msg.content_subtype = 'html'

            msg.send()
        return redirect('staff:managenews')
    else:
        return redirect('staff:managenews')


def newsdelete(request, pk):
    if request.method == "POST":
        news_id = request.POST.get("news_id")
        newsbanner.objects.filter(id=news_id).update(is_deleted=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def newsundo(request, pk):
    if request.method == "POST":
        news_id = request.POST.get("news_id")
        newsbanner.objects.filter(id=news_id).update(is_deleted=False)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def newsedit(request, pk):
    if request.method == "POST":
        news_id = request.POST.get("news_id")
        newsbanner.objects.filter(id=news_id).update(news=request.POST.get("newsedit").strip())
        message_name = "Aim Arena"
        message = "New news are there ! Come and check latest news on our website!"
        emails = emailnews.objects.values_list('email', flat=True).filter(subscription=True)
        for i in emails:
            msg = EmailMessage(message_name,
                               message, to=[i])
            msg.content_subtype = 'html'

            msg.send()
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})