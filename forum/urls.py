from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import forumhome, PostDetail, Addpost, trys, my_post, editpost, deletepost, LikeView

app_name = 'forums'
urlpatterns = [
    path('forum/', trys, name='forum'),
    path('forum/my_posts', my_post, name='my_post'),
    path('forum/<int:pk>', PostDetail.as_view(), name='Post_detail'),
    path('forum/forum_create', Addpost, name='create_forum'),
    path('forum/my_posts/edit/<int:pk>/', editpost, name='editpost'),
    path('forum/my_posts/delete/<int:pk>/', deletepost, name='deletepost'),
    path('forum/like/<int:pk>', LikeView, name='like_post')

]
