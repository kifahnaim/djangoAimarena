from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import forumhome, PostDetail, Addpost, trys, my_post, editpost, deletepost, LikeView, CommentView, \
    search_titles, forumcategories, forumcategroieseach, my_profile, user_image_view, editprofile, CommentDelete, \
    pinpost, unpinpost, acceptpost, rejectpost, typeofposts, acceptappeal, rejectappeal, replyDelete, editcomment, \
    editreply, readnotification, clearall

app_name = 'forums'
urlpatterns = [
    path('forum/categories', forumcategories, name="forumcategroies"),
    path('forum/categories/<slug:slug>', forumcategroieseach.as_view(), name="forumcategroieseach"),
    path('forum/pin/<int:pk>', pinpost, name="forumpinpost"),
    path('forum/accept/<int:pk>', acceptpost, name="forumacceptpost"),
    path('forum/reject/<int:pk>', rejectpost, name="forumrejectpost"),
    path('forum/acceptappeal/<int:pk>', acceptappeal, name="acceptappeal"),
    path('forum/rejectappeal/<int:pk>', rejectappeal, name="rejectappeal"),
    path('polls/<str:posttype>', typeofposts, name="typeofposts"),
    path('forum/unpin/<int:pk>', unpinpost, name="forumunpinpost"),
    path('forum/', trys, name='forum'),
    path('forum/my_posts', my_post, name='my_post'),
    path('forum/my_profile/', my_profile, name='my_profile'),
    path('forum/<int:pk>', PostDetail.as_view(), name='Post_detail'),
    path('forum/forum_create/', Addpost, name='create_forum'),
    path('forum/my_posts/edit/<int:pk>/', editpost, name='editpost'),
    path('forum/my_posts/read/<int:pk>/', readnotification, name='readnotification'),
    path('forum/my_posts/delete/<int:pk>/', deletepost, name='deletepost'),
    path('forum/like/<int:pk>', LikeView, name='like_post'),
    path('forum/comment/<int:pk>', CommentView, name='Comment_post'),
    path('forum/comment/edit/<int:pk>', editcomment, name='editcomment'),
    path('forum/comment/delete/<int:pk>', CommentDelete, name='CommentDelete'),
    path('forum/reply/delete/<int:pk>', replyDelete, name='replyDelete'),
    path('forum/reply/edit/<int:pk>', editreply, name='editreply'),
    path('forum/search', search_titles, name='search_post'),
    path('forum/clearall', clearall, name='clearall'),
    path('forum/my_profile/uploadimage', user_image_view, name='user_image_view'),
    path('forum/my_profile/editprofile', editprofile, name='editprofile'),
    # path('forum/comment/reply', add_reply_to_comment, name='reply_comment'),

]
