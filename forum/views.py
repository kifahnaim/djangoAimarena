from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.db import connection
from django.views import View

from .forms import PostForm
from .models import Post, Userreg, topic
from useraddpost.models import UserPost
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)


# Create your views here.

class forumhome(ListView):
    model = Post
    template_name = "forumhome.html"
    login_url = 'signin/'
    queryset = Post.objects.all()


# @login_required(login_url='/auth/signin/')
def trys(request):
    print(request.session.get('Username'))
    posts = Post.objects.all()
    p = Paginator(posts, 7)
    print(p.num_pages)
    numberofpage = p.num_pages
    pagenum = request.GET.get('page', 1)
    try:
        page = p.page(pagenum)
    except EmptyPage:
        page = p.page(1)

    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {"item": page,
               'latest': latest,
               'page': page,
               'numberofpage': numberofpage}

    return render(request, "detail.html", context)


def create_forum(request):
    return render(request, "forum-create.html", {})


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        userid = self.request.session.get('userid')
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super(PostDetail, self).get_context_data(**kwargs)
        liked = False
        if stuff.likes.filter(id=userid).exists():
            liked = True

        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context["liked"] = liked

        return context


def Addpost(request):
    context = {"item": Post.objects.values('topic_title').distinct()}
    if request.method == "POST":
        userid = request.session.get('userid')
        print(userid)
        print(request.POST.get("title"))
        print(request.POST.get("body"))
        print(request.POST.get("topicdropdown"))
        try:
            if request.POST.get("title") and request.POST.get("body") and userid is not None and request.POST.get(
                    "topicdropdown"):
                saverecord = Post()

                saverecord.title = request.POST.get("title")
                saverecord.body = request.POST.get("body")
                saverecord.topic_title = topic(request.POST.get("topicdropdown"))
                saverecord.author = Userreg.objects.get(id=userid)
                saverecord.clean()
                saverecord.save()
                return redirect('../forum/forum_create')
        except:
            return redirect('../forum/forum_create')



    else:
        return render(request, "forum-create.html", context)


def my_post(request):
    userid = request.session.get('userid')
    try:
        cursor = connection.cursor()
        cursor.execute(
            "select p.id as id, p.title as title, p.body as body, p.timestamp as time, u.Username as Username FROM posts p, useregister u where p.author_id = u.id and deleted=False and p.author_id=" + str(
                userid))
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
    except Exception as e:
        cursor.close()
    context = {"items": resultsList}
    return render(request, 'my_post.html', context)


def editpost(request, pk):
    obj = get_object_or_404(Post, pk=pk)
    userid = request.session.get('userid')
    posts = Post.objects.values('topic_title').distinct()
    if request.method == "POST":
        try:
            if request.POST.get("title") and request.POST.get("body") and userid is not None and request.POST.get(
                    "topicdropdown"):
                Post.objects.filter(pk=pk).update(title=request.POST.get("title"), body=request.POST.get("body"),
                                                  topic_title=request.POST.get("topicdropdown"),
                                                  author=Userreg.objects.get(id=userid))
                return redirect('../../my_posts')
        except:
            return redirect('../forum/forum_create')

    return render(request, 'forum_editpost.html', {"obj": obj, "posts": posts})


def deletepost(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.is_ajax():
        Post.objects.filter(pk=pk).update(deleted=True)
        print("deleted")
        return JsonResponse({"message": "success"})
    return JsonResponse({"message": "Wrong route"})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('Post_like'))
    liked = False
    if post.likes.filter(id=request.session.get('userid')).exists():
        post.likes.remove(request.session.get('userid'))
        liked = False
    else:
        post.likes.add(request.session.get('userid'))
        liked = True
    return HttpResponseRedirect(reverse('forums:Post_detail', args=[str(pk)]))
