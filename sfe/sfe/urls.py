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
    path('dashboard/welcome_admin',views.welcome_adm,name="dashboard"),
    path('logout',views.logout_view,name="logout"),
    path('active_users',views.active_users,name="active_users"),
    path('inactive_users',views.inactive_users,name="inactive_users"),
    path('last_added',views.last_added,name="last_added"),
    path('only_admin',views.only_admin,name="only_admin"),
    path('only_superviseur',views.only_superviseur,name="only_superviseur"),
    path('only_client',views.only_client,name="only_client"),
    path('search_user',views.search_user,name="search_user"),
    path('edit_user/<int:user_id>',views.Edit_user,name="Edit_user"),
    path('edit_userbyadmin/<int:user_id>',views.Edit_userbyadmin,name="Edit_userbyadmin"),
    path('dashboard/profile/<int:user_id>',views.Profile,name="profile"),
    path('dashboard/profile/edit_img/<int:user_id>',views.Edit_profileimg,name="edit_profileimg"),

    path('my_dashboard/inbox',views.inbox,name="inbox"),
    path('my_dashboard/welcome',views.welcome,name="my_dash/welcome"),
    path('make_appoint',views.make_appoint,name="make_appoint"),
    path('dashboard/appointement',views.appointement,name="appointement"),
    path('dashboard/appointement/approuve/<int:app_id>',views.approve_appoint,name="approve_appoint"),
    path('dashboard/appointement/active',views.active_appoint,name="active_appoint"),
    path('dashboard/appointement/inactive',views.inactive_appoint,name="inactive_appoint"),
    path('dashboard/appointement/inactive/add_appoint',views.add_appoint,name="add_appoint"),
    path('take_driver',views.take_driver,name="take_driver"),
    path('driving_offers',views.Driving_offers,name="driving_offers"),
    path('drivers_list',views.drivers_list,name="drivers_list"),
    path('add_driver',views.add_driver,name="add_driver"),
    path('my_dashboard/my_offers',views.driver_offers,name="my_dash/my_offers")
   
    
   
]


