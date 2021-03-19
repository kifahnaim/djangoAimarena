from django.urls import path
from .views import signin, signup, signout, Userregistration,Userlogin

urlpatterns = [
    path('signin/', Userlogin, name='signin'),
    path('signup/', Userregistration, name='signup'),
    path('logout/', signout, name='signout')
]