from . import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('',views.home,name="home"),
    path('authentication/signup',views.signup,name="signup"),
    path('authentication/login',views.user_login,name="login"),
    path('userlist',views.userslist,name="userslist"),
    path('approve_user/<int:user_id>',views.approve_user,name="approve_user"),
    path('inapprove_user/<int:user_id>',views.inapprove_user,name="inapprove_user"),
    path('delete_user/<int:user_id>',views.delete_user,name="delete_user"),
    path('dashboard',views.adm_dash,name="dashborad"),
    path('logout',views.logout_view,name="logout")
]
