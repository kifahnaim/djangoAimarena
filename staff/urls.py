from django.urls import path
from . import views

app_name = 'staff'
urlpatterns = [
    path('staff/', views.baseview, name="baseview"),
    path('staff/users/', views.staffusers, name="staffusers.css"),
    path('staff/topics/', views.stafftopics, name="stafftopics"),
    path('staff/topics/create', views.stafftopicscreate, name="stafftopicscreate"),
    path('staff/topics/delete/<int:pk>/', views.stafftopicsdelete, name="stafftopicsdelete"),
    path('staff/topics/undo/<int:pk>/', views.stafftopicsundo, name="stafftopicsundo"),
    path('staff/topics/edit/<int:pk>/', views.stafftopicsedit, name="stafftopicsedit"),
    path('staff/subtopics/', views.staffsubtopics, name="staffsubtopics"),
    path('staff/subtopics/create', views.staffsubtopicscreate, name="staffsubtopicscreate"),
    path('staff/subtopics/delete/<int:pk>/', views.staffsubtopicsdelete, name="staffsubtopicsdelete"),
    path('staff/subtopics/undo/<int:pk>/', views.staffsubtopicsundo, name="staffsubtopicsundo"),
    path('staff/subtopics/edit/<int:pk>/', views.staffsubtopicsedit, name="staffsubtopicsedit"),
    path('staff/posts/', views.staffposts, name="staffposts"),
    path('staff/users/updaterank/<int:pk>/', views.updaterank, name="updaterank"),
    path('staff/mailbox', views.inbox, name="mailbox"),
    path('staff/compose', views.compose, name="compose"),
    # path('staff/users/<int:pk>/', views.useractions.as_view(), name="useractions"),
    path('staff/ban/<int:pk>/', views.banuser, name="banuser"),
    path('staff/posts/<int:pk>/', views.Detailmanageposts.as_view(), name="Detailmanageposts"),
    path('staff/kick/<int:pk>/', views.kickuser, name="kickuser"),
    path('staff/users/<int:pk>/', views.userprofile, name="userprofile"),
    path('staff/unban/<int:pk>/', views.unbanuser, name="unbanuser"),
    path('staff/posts/close/<int:pk>/', views.closepost, name="closeposts"),
    path('staff/posts/open/<int:pk>/', views.openpost, name="openposts"),
    path('staff/posts/delete/<int:pk>/', views.deletepost, name="deleteposts"),
    path('staff/posts/undo/<int:pk>/', views.staffpostsundo, name="undoposts"),
    path('staff/posts/like/<int:pk>', views.LikeView, name='like_post'),
    path('staff/contact', views.contact, name="customer_service"),
    path('staff/searchusers', views.searchusers, name="searchusers"),
    path('staff/searchposts', views.searchposts, name="searchposts"),
    path('staff/manageshop/', views.manageproducts, name="manageproducts"),
    path('staff/manageshop/editproduct/<int:pk>/', views.editproduct, name="editproduct"),
    path('staff/manageshop/deleteproduct/<int:pk>/', views.deleteproduct, name="deleteproduct"),
    path('staff/manageshop/undoproduct/<int:pk>/', views.undoproduct, name="undoproduct"),
    path('staff/manageshop/createproduct/', views.createproduct, name="createproduct"),
    path('staff/managenews/', views.managenews, name="managenews"),
    path('staff/managenews/managenewscreate', views.managenewscreate, name="managenewscreate"),
    path('staff/managenews/delete/<int:pk>/', views.newsdelete, name="newsdelete"),
    path('staff/managenews/undo/<int:pk>/', views.newsundo, name="newsundo"),
    path('staff/managenews/edit/<int:pk>/', views.newsedit, name="newsedit"),
]
