from django.urls import path

from authentication import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = "game"
urlpatterns = [
    path('game/', views.nonmotiongame, name="nonmotiongame"),
    path('game/savescore', views.savescore, name="savescore"),
    path('shop/', views.shop, name="shop"),
    path('shop/purchase/<int:pk>/', views.purchase, name="purchase"),
    path('Ranked/', views.survival, name="Ranked"),
    path('casual/', views.casual, name="casual"),
    path('lives/', views.lives, name="lives"),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)