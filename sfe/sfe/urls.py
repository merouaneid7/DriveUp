from . import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('',views.home,name="home"),
    path('authentication/signup',views.signup,name="signup"),
    path('add_user',views.add_user,name="add_user"),
    path('authentication/login',views.user_login,name="login"),
    path('userlist',views.userslist,name="userlist"),
    path('approve_user/<int:user_id>',views.approve_user,name="approve_user"),
    path('inapprove_user/<int:user_id>',views.inapprove_user,name="inapprove_user"),
    path('delete_user/<int:user_id>',views.delete_user,name="delete_user"),
    path('dashboard',views.adm_dash,name="dashboard"),
    path('logout',views.logout_view,name="logout"),
    path('active_users',views.active_users,name="active_users"),
    path('inactive_users',views.inactive_users,name="inactive_users"),
    path('last_added',views.last_added,name="last_added"),
    path('only_admin',views.only_admin,name="only_admin"),
    path('only_client',views.only_client,name="only_client"),
    path('search_user',views.search_user,name="search_user"),
    path('edit_user/<int:user_id>',views.Edit_user,name="Edit_user"),
    path('edit_userbyadmin/<int:user_id>',views.Edit_userbyadmin,name="Edit_userbyadmin"),
    path('dashboard/profile/<int:user_id>',views.Profile,name="profile"),
    path('dashboard/profile/edit_img/<int:user_id>',views.Edit_profileimg,name="edit_profileimg"),
]
