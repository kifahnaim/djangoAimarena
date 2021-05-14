from django.urls import path
from .views import signin, signup, signout, Userregistration, Userlogin, resetpassword, resetpasswordsendemail, \
    CompletePasswordReset, homelogin, VerificationView

urlpatterns = [
    path('signin/', Userlogin, name='signin'),
    path('home/', homelogin, name='home'),
    path('signup/', Userregistration, name='signup'),
    path('logout/', signout, name='signout'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('resetpassword/sendemail', resetpasswordsendemail, name='resetpasswordsendemail'),
    path('set-new-password/<uidb64>/<token>',CompletePasswordReset.as_view(), name="reset-user-password"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name="activate")
]