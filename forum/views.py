import json
from datetime import datetime, timedelta

from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from authapp.models import login_details, admin_actions, Role_permissions, UserRoles, Banfromforum, Banfromgame
from forum.models import Notification, subtopic, subtopiclatestposts

from django.http import request, JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.db import connection
from nonmotiongame.models import Game_Statistics, User_Info, GameMode_User
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from .models import Post, Userreg, topic, Comment
from django.views.generic import (
    DetailView,
    ListView,

)


# Create your views here.


class forumhome(ListView):
    model = Post
    template_name = "forumhome.html"
    login_url = 'signin/'
    queryset = Post.objects.all()


def trys(request):
    userid = request.session.get('userid')

    userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)
    if userbanforum:
        print("this user is banned")
        return redirect('forums:forumcategroieseach', slug="appeal")

    print(request.session.get('Username'))
    posts = Post.objects.filter(deleted=0).order_by('-timestamp')
    usersonline = login_details.objects.all()
    p = Paginator(posts, 7)
    print(p.num_pages)
    numberofpage = p.num_pages
    date = datetime.now() - timedelta(seconds=300)
    pagenum = request.GET.get('page', 1)
    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)
    Userdetails = None
    if request.session.get("userid"):
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {"item": page,
               'latest': latest,
               'page': page,
               'numberofpage': numberofpage,
               'usersonline': usersonline,
               'date': date,
               'Userdetails': Userdetails}

    return render(request, "detail.html", context)
    

def create_forum(request):
    return render(request, "forum-create.html", {})


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"

    def dispatch(self, request, *args, **kwargs):
        userid = request.session.get('userid')
        userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)

        if not userbanforum:
            return super().dispatch(request, *args, **kwargs)
        return redirect('signin')

    def get_context_data(self, **kwargs):
        resultsList = None
        userid = self.request.session.get('userid')
        Userdetails = None
        if self.request.session.get("userid"):
            Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super(PostDetail, self).get_context_data(**kwargs)
        role = self.request.session.get('Role')
        post = Post.objects.get(id=self.kwargs['pk'])
        post.post_views = int(post.post_views) + 1
        post.save()
        try:
            cursor = connection.cursor()

            cursor.execute(
                "select ur.RoleName as RoleName, rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur where rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
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
        comments = Comment.objects.filter(post=self.kwargs['pk'], reply_id=None, deleted=False)
        liked = False
        if stuff.likes.filter(id=userid).exists():
            liked = True

        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["com"] = comments
        context["permission"] = resultsList
        context["Userdetails"] = Userdetails

        return context


@csrf_exempt
def Addpost(request):
    userid = request.session.get('userid')
    userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)

    context = {"item": topic.objects.values('topic_title').distinct()}
    if request.method == "POST" and request.is_ajax():

        userid = request.session.get('userid')
        print(userid)
        print(request.POST.get("title"))
        print(request.POST.get("body"))
        topicid = subtopic.objects.get(slug=request.POST.get("slug")).pk
        allusersintopic = Post.objects.exclude(author=userid).filter(topic_title_id=topicid).values(
            'author__Useremail').distinct()

        print(allusersintopic)
        for item in allusersintopic.values('author__Useremail'):
            print(item["author__Useremail"])
            msg = EmailMessage(subtopic.objects.get(slug=request.POST.get("slug")).sub_topic_title,
                               "New posts available here, Please come and check latest posts on AimArena and interact with others !",
                               to=[item["author__Useremail"]])
            msg.content_subtype = 'html'

            msg.send()
        print("allusersintopic")
        print(allusersintopic)
        print(topicid)

        if request.POST.get("title") and request.POST.get("body") and userid is not None:
            image_path = None
            file_input = None

            saverecord = Post()

            try:
                file_input = request.FILES['image']
                fs = FileSystemStorage()
                x = datetime.now()

                image_path = fs.save("AimArena" + x.strftime("%a%m%y%H%S") + file_input.name, file_input)
                saverecord.thumbnail = image_path
            except MultiValueDictKeyError:
                image_path = None

            print(image_path)
            saverecord.title = request.POST.get("title")
            saverecord.body = request.POST.get("body")
            saverecord.topic_title = subtopic(topicid)
            saverecord.author = Userreg.objects.get(id=userid)
            saverecord.clean()
            saverecord.save()
            admin_actions.objects.filter(user_id=userid).update(create_appeal=True)
            stuff = Post.objects.filter(topic_title__slug=request.POST.get("slug"))
            allusers = Userreg.objects.filter(is_active=True)
            print("allusers")
            print(allusers)
            userinfoexists = User_Info.objects.filter(User_ID_id=userid).count()
            if userinfoexists > 0:
                x = User_Info.objects.get(User_ID_id=userid)
                if x.forumpoints is None:
                    x.forumpoints = 0
                x.forumpoints = int(x.forumpoints) + int(5)
                x.save()
            else:
                infoforuser = User_Info()
                infoforuser.forumpoints = 5
                infoforuser.Shots_Avg = 0
                infoforuser.Accuracy_Avg = 0
                infoforuser.Hits_Avg = 0
                infoforuser.Score_Avg = 0
                infoforuser.forumpoints = 0
                infoforuser.User_ID = Userreg(userid)
                infoforuser.save()
            included = subtopiclatestposts.objects.filter(subtopicnew=topicid)
            if included and subtopiclatestposts.objects.filter(subtopicnew=topicid).count() == allusers.count():
                subtopiclatestposts.objects.filter(subtopicnew=topicid).update(is_read=False)
            else:
                for i in allusers:
                    notifynewposts = subtopiclatestposts()
                    print(i.id)
                    notifynewposts.subtopicnew = subtopic(topicid)
                    notifynewposts.is_read = False
                    notifynewposts.user = Userreg(i.id)
                    notifynewposts.save()

            return JsonResponse({"filtereddata": "success"})

        else:
            return JsonResponse({"filtereddata": "fail"})


    else:
        return JsonResponse({"filtereddata": "fail"})


def my_post(request):
    userid = request.session.get('userid')
    Userdetails = None
    if request.session.get("userid"):
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    if not userid:
        print("Signin please")

        return redirect('forums:forum')
    userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)

    if userbanforum:
        return redirect('signin')

    resultsList = Post.objects.filter(deleted=False, author_id=userid)

    count = resultsList.count()
    print(count)
    p = Paginator(resultsList, 17)
    print(p.num_pages)
    numberofpage = p.num_pages
    pagenum = request.GET.get('page', 1)
    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)

    context = {"items": page, "page": page, "numberofpage": numberofpage, "count": count, "Userdetails": Userdetails}
    return render(request, 'my_post.html', context)


@csrf_exempt
def editpost(request, pk):
    obj = get_object_or_404(Post, pk=pk)
    userid = request.session.get('userid')
    if request.method == "POST" and request.is_ajax():
        try:
            if request.POST.get("title") and request.POST.get("body") and userid is not None:
                try:

                    file_input = request.FILES['image']
                    fs = FileSystemStorage()
                    image_path = fs.save(file_input.name, file_input)
                    print(image_path)
                except MultiValueDictKeyError:
                    image_path = imagedefault()

                Post.objects.filter(pk=pk).update(title=request.POST.get("title"), body=request.POST.get("body"),
                                                  thumbnail=image_path)
                resultsList = None

                resultsList = Post.objects.filter(deleted=False, author_id=userid)

                count = resultsList.count()

                p = Paginator(resultsList, 17)
                print(p.num_pages)
                numberofpage = p.num_pages
                pagenum = request.GET.get('page', 1)
                try:
                    page = p.page(pagenum)
                except EmptyPage:
                    page = p.page(1)

                context = {"items": page, "count": count, "page": page, "numberofpage": numberofpage}
                print("success")
                return render(request, "post_edittest_filter.html", context)
        except:
            print("error")
            return JsonResponse({"message": "fail"})
    print("error2")
    return JsonResponse({"message": "fail"})


def imagedefault():
    x = "logo.png"
    return x


def deletepost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.is_ajax():
        Post.objects.filter(pk=pk).update(deleted=True)
        print("deleted suucessfully")
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "Wrong route"})


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
    return HttpResponseRedirect(reverse('forums:Post_detail', args=[str(pk)]))


def CommentView(request, pk):
    if request.method == "POST":

        saverecord = Comment()
        comment_qs = None
        userid = request.session.get('userid')

        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        if request.is_ajax():
            userid = request.session.get('userid')
            post = get_object_or_404(Post, id=request.POST.get('post_id'))
            thispost = Post.objects.filter(id=request.POST.get('post_id'))
            print(post.id)
            print("kifah")
            commentsall = Comment.objects.filter(post_id=request.POST.get('post_id'))
            saverecord.user = Userreg.objects.get(id=userid)
            saverecord.body = request.POST.get('comment')
            saverecord.post = post
            saverecord.save()
            sender = Userreg.objects.get(id=userid)
            if userid != post.author_id:
                print("not same" + str(userid) + str(post.author_id))
                notify = Notification(post=post, sender=sender, user=post.author,
                                      text_preview=str(sender) + " " + "commented on your post", Notification_type=2)
                notify.save()
            return JsonResponse({"message": "success"})

        reply_id = request.POST.get("comment_id")
        if reply_id:
            print("hello")
            comment_qs = Comment.objects.get(id=reply_id)
            sender = Userreg.objects.get(id=userid)
            print(reply_id)
            saverecord.reply = comment_qs
            saverecord.user = Userreg.objects.get(id=userid)
            saverecord.body = request.POST.get('reply')
            saverecord.post = post
            saverecord.save()

            if userid != comment_qs.user.id:
                notify = Notification(post=post, sender=sender, user=post.author,
                                      text_preview=str(sender) + " " + "replied to your comment", Notification_type=3)
                notify.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_reply_to_comment(request, pk):
    userid = request.session.get('userid')

    if request.method == 'POST' and request.is_ajax():
        comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
        print(comment)
        return JsonResponse({"message": "success"})

    return JsonResponse({"message": "Wrong route"})


def shownotifications(request):
    user = request.session.get("userid")
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    context = {

        'notifications': notifications

    }
    return render(request, "my_post.html", context)


def deletenotification(request, noti_id):
    user = request.session.get("userid")
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect("my_post")


def CountNotifications(request):
    count_notifications = None
    notifi_text = None

    if request.session.get("userid"):
        count_notifications = Notification.objects.filter(user=request.session.get("userid"), is_read=False).count()

        notifi_text = Notification.objects.filter(user=request.session.get("userid"), is_read=False)
    return {'count_notifications': count_notifications, 'notifi_text': notifi_text

            }


def countcomments(request, pk):
    count_comments = None

    count_comments = Comment.objects.filter(post_id=pk).count()

    return {'count_comments': count_comments}


def reply(request):
    reply_id = request.POST.get("comment_id")
    print("reply" + "  " + str(reply_id))
    if reply_id:
        comment_qs = Comment.objects.get(id=reply_id)

    comment = Comment.objects.create()


def search_titles(request):
    global selectedoption
    global query
    if request.method == 'POST':
        search_text = request.POST.get("search_text")
        selectedoption = request.POST.get("selectedoption")

    else:
        search_text = ''

    # specific = Post.objects.select_related('author')
    # posts = Post.objects.filter(title__contains=search_text)
    # data = specific.values()

    cursor = connection.cursor()
    if selectedoption == "Titles":
        query = "select ur.RoleName as Role, p.id as id, p.title as title, p.timestamp as timestamp, u.id as uid , p.body as body, u.Username as Username, u.user_thumbnail as user_thumbnail FROM posts p, useregister u, Userrole ur where p.author_id = u.id and u.Role_id = ur.id and deleted=False and p.title LIKE  '%%%%%s%%%%' " % (
            search_text)

    elif selectedoption == "Descriptions":
        query = "select ur.RoleName as Role, p.id as id, p.title as title, p.body as body, u.id as uid , u.Username as Username, u.user_thumbnail as user_thumbnail FROM posts p, useregister u, Userrole ur where p.author_id = u.id and u.Role_id = ur.id and deleted=False and p.body LIKE '%%%%%s%%%%' " % (
            search_text)

    cursor.execute(query)

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
    print("hello world")

    if resultsList:

        return render(request, "post_filter.html", {"item": resultsList})
    else:
        return JsonResponse({"filtereddata":
                                 "No Posts found!"})


def forumcategories(request):
    userid = request.session.get('userid')
    userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)
    if userbanforum:
        print("this user is banned")
        return redirect('forums:forumcategroieseach', slug="appeal")
    roleslist = UserRoles.objects.all()
    obj = topic.objects.filter(is_visible=True, is_deleted=False)
    startdate = datetime.now()
    lastdate = startdate - timedelta(hours=8)

    print(lastdate)
    newposts = Post.objects.filter(timestamp__range=(lastdate, startdate)).count()
    print(newposts)
    latest = Post.objects.order_by('-timestamp')[0:3]
    print(obj)
    Userdetails = None
    if request.session.get("userid"):
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    return render(request, "forums.html", {"obj": obj, "latest": latest, "roleslist": roleslist, "Userdetails": Userdetails})


# def forumcategroieseach(request, topic_id):
#     obj = Post.objects.filter(topic_title_id__topic_title=topic_id)
#     print(obj)
#     return render(request, "forumcategorieseach.html", {"obj": obj})


class forumcategroieseach(DetailView):
    template_name = "forumcategorieseach.html"
    model = subtopic

    def dispatch(self, request, *args, **kwargs):
        userid = request.session.get('userid')

        userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)
        if not userbanforum:
            return super().dispatch(request, *args, **kwargs)
        else:
            if self.kwargs['slug'] == "appeal":
                print("appeal")
                return super().dispatch(request, *args, **kwargs)
            return redirect("signin")

    def get_context_data(self, **kwargs):
        userid = self.request.session.get('userid')
        Userdetails = None
        userbanforum = admin_actions.objects.filter(user_id_id=userid, user_ban_forum=True)
        subtopicid = subtopic.objects.get(slug=self.kwargs['slug']).pk
        subtopiclatestposts.objects.filter(subtopicnew=subtopicid, user=userid, is_read=False).update(is_read=True)
        stuff = Post.objects.filter(topic_title__slug=self.kwargs['slug'], Featured=False, appeal_accepted=False,
                                    appeal_rejected=False, is_available=False, is_rejected=False).order_by('-timestamp')
        if self.request.session.get("userid"):
            Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        stuffcount = Post.objects.filter(topic_title__slug=self.kwargs['slug']).count()
        # stuff = get_object_or_404(Post, topic_title=x)
        context = super(forumcategroieseach, self).get_context_data(**kwargs)
        # print(stuff)
        role = self.request.session.get('Role')
        rolename = self.request.session.get('RoleName')
        accepted = Post.objects.filter(is_available=True).order_by('-timestamp')[0:3]
        rejected = Post.objects.filter(is_rejected=True).order_by('-timestamp')[0:3]
        acceptedappeal = Post.objects.filter(appeal_accepted=True).order_by('-timestamp')[0:3]
        rejectedappeal = Post.objects.filter(appeal_rejected=True).order_by('-timestamp')[0:3]
        pinned = Post.objects.filter(topic_title__slug=self.kwargs['slug'], Featured=True)
        print(pinned)
        topicvisible = subtopic.objects.values_list('is_visible', flat=True).get(slug=self.kwargs['slug'])
        topicpinnedvisible = subtopic.objects.values_list('pinned_visible', flat=True).get(
            slug=self.kwargs['slug'])
        topicacceptedvisible = subtopic.objects.values_list('accepted_visible', flat=True).get(
            slug=self.kwargs['slug'])
        topicrejectedvisible = subtopic.objects.values_list('rejected_visible', flat=True).get(
            slug=self.kwargs['slug'])
        topicrejectedappeal = subtopic.objects.values_list('rejectedappeal_visible', flat=True).get(
            slug=self.kwargs['slug'])
        topicacceptedappeal = subtopic.objects.values_list('acceptedappeal_visible', flat=True).get(
            slug=self.kwargs['slug'])
        if userbanforum:
            createappeal = admin_actions.objects.values_list('create_appeal', flat=True).get(
                user_id=userid)

        print(topicpinnedvisible)
        print(topicvisible)
        p = Paginator(stuff, 7)
        print(p.num_pages)
        numberofpage = p.num_pages
        pagenum = self.request.GET.get('page', 1)
        try:
            page = p.page(pagenum)
        except EmptyPage:
            page = p.page(1)
        if userbanforum:
            context["createappeal"] = createappeal
        context["acceptedappeal"] = acceptedappeal
        context["rejectedappeal"] = rejectedappeal
        context["topicacceptedappeal"] = topicacceptedappeal
        context["topicrejectedappeal"] = topicrejectedappeal
        context['page'] = page
        context['numberofpage'] = numberofpage
        RoleName = self.request.session.get("RoleName")
        resultsList = None
        context["item"] = page
        context["stuffcount"] = stuffcount
        context["pinned"] = pinned
        context["accepted"] = accepted
        context["rejected"] = rejected
        context["userbanforum"] = userbanforum
        context["Userdetails"] = Userdetails
        try:
            cursor = connection.cursor()

            cursor.execute(
                "select p.permission_name as permission_name, ur.RoleName as RoleName, rp.can_promote as can_promote ,rp.ban as ban, rp.email as email, rp.kick as kick, rp.manage_posts as manage_posts,rp.can_view as can_view, rp.textwelcome as textwelcome FROM role_permissions rp, userrole ur, pages p where rp.permission_id_id=p.id and rp.Role_id_id=ur.id and rp.Role_id_id =" + str(
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
            context["permission"] = resultsList
            print(resultsList)

        except Exception as e:
            cursor.close()
            print("fail")

        if rolename != "User":
            topicvisible = True
        context["topicrejectedvisible"] = topicrejectedvisible
        context["topicacceptedvisible"] = topicacceptedvisible
        context["permission"] = resultsList
        context["topicvisible"] = topicvisible
        context["topicpinnedvisible"] = topicpinnedvisible

        # if subtopics in topics and topics == 'Announcements' and role == "User":
        #     context["view"] = False
        #     print("only staff")
        # else:
        #     context["view"] = True
        #     if self.kwargs['slug'] == 'Games':
        #         context["view"] = True
        #     if self.kwargs['slug'] == 'Introduction':
        #         context["view"] = True

        return context


def my_profile(request):
    userid = request.session.get('userid')
    if userid:
        role = request.session.get('Role')
        resultsList = None
        allstatistics = Game_Statistics.objects.filter(
            Game_ID__User_ID=Userreg(request.session.get('userid'))).order_by(
            '-Date')[0:6]

        stuff = Userreg.objects.filter(id=userid)
        context = {}
        print("stuff")
        print(stuff)
        context["item"] = stuff
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
            context["permission"] = resultsList
            print(resultsList)
            context["gamestats"] = allstatistics
            print(request.session.get("RoleName"))
            if request.session.get("RoleName") == "Admin" or request.session.get("RoleName") == "Forum moderator":
                print("admin")
                bans = Banfromforum.objects.filter(banned_by_id=userid).count()
                context["bans"] = bans

            if role == "Admin":
                gamebans = Banfromgame.objectsfilter(banned_by_id=userid).count()
                context["gamebans"] = gamebans
            info = User_Info.objects.filter(User_ID_id=userid)
            rankinfo = GameMode_User.objects.filter(User_ID_id=userid, Game_Mode_ID=1).values("Rank_id__Rank_Name",
                                                                                              "Rank_id__Rank_image")
            print(info)
            print(rankinfo)
            context["info"] = info
            context["rankinfo"] = rankinfo
        except Exception as e:
            cursor.close()
            print("fail")
        return render(request, "userprofile.html", context)
    else:
        return redirect("forums:forumcategroies")


@csrf_exempt
def user_image_view(request):
    print(request.POST)
    try:
        file_input = request.FILES['image']
        fs = FileSystemStorage()
        image_path = fs.save(file_input.name, file_input)
        userid = request.session.get('userid')
        stuff = Userreg.objects.filter(id=userid).update(user_thumbnail=image_path)
    except:
        pass
    return HttpResponse("uploaded")


def editprofile(request):
    userid = request.session.get('userid')
    if userid:
        if request.method == 'POST' and request.is_ajax():
            print("here")
            Firstname = request.POST.get("firstname").strip()
            Lastname = request.POST.get("lastname").strip()
            Email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()
            encryptedpass= pbkdf2_sha256.hash(request.POST.get("password"))
            stuff = Userreg.objects.filter(id=userid).update(Firstname=Firstname, Lastname=Lastname, Useremail=Email,
                                                             password=encryptedpass)

            print("here2")
            return JsonResponse({"update": "success"})
        print("nothere")
        return JsonResponse({"update": "fail"})


def returns(x):
    print("before")
    context = {}
    if x:
        context["check"] = True
        print("after")
        return context


def CommentDelete(request, pk):
    if request.method == "POST" and request.is_ajax():
        comment_id = request.POST.get('comment_id')
        print(comment_id)
        commentspecific = Comment.objects.filter(id=comment_id).update(deleted=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def replyDelete(request, pk):
    if request.method == "POST" and request.is_ajax():
        reply_id = request.POST.get('replyid')
        print(reply_id)
        commentspecific = Comment.objects.filter(id=reply_id).update(deleted=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def pinpost(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(Featured=True, is_closed=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def unpinpost(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(Featured=False, is_closed=False)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def acceptpost(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(is_available=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def rejectpost(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(is_rejected=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def typeofposts(request, posttype):
    x = None
    count = None
    if posttype == "reject":
        ans = 'reject'
        x = Post.objects.filter(is_rejected=True)
        count = Post.objects.filter(is_rejected=True).count()
    elif posttype == "accept":
        ans = 'accept'
        x = Post.objects.filter(is_available=True)
        count = Post.objects.filter(is_available=True).count()
    elif posttype == "acceptedappeal":
        ans = 'accept'
        x = Post.objects.filter(appeal_accepted=True)
        count = Post.objects.filter(appeal_accepted=True).count()
    elif posttype == "rejectedappeal":
        ans = 'reject'
        x = Post.objects.filter(appeal_rejected=True)
        count = Post.objects.filter(appeal_rejected=True).count()

    return render(request, "Post_types.html", {"items": x, "count": count, "ans": ans})


def acceptappeal(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(appeal_accepted=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def rejectappeal(request, pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        Post.objects.filter(id=post_id).update(appeal_rejected=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def editreply(request, pk):
    if request.method == "POST":
        replyid = request.POST.get("replyid")
        bodyreply = request.POST.get("bodyreply")
        Comment.objects.filter(id=replyid).update(body=bodyreply)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


def editcomment(request, pk):
    if request.method == "POST":
        replyid = request.POST.get("replyid")
        bodyreply = request.POST.get("bodyreply")
        Comment.objects.filter(id=replyid).update(body=bodyreply)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


@csrf_exempt
def readnotification(request, pk):
    if request.method == "POST":
        postid = request.POST.get("postid")
        notid = request.POST.get("notid")
        print(notid)
        sender = request.POST.get("sender")
        user = request.POST.get("user")

        Notification.objects.filter(post=postid, id=notid, sender=sender, user=user).update(is_read=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})


@csrf_exempt
def clearall(request):
    if request.method == "POST":
        userid = request.session.get('userid')
        Postsusers = Notification.objects.filter(user=userid).update(is_read=True)
        return JsonResponse({"message": "success"})
    else:
        return JsonResponse({"message": "fail"})