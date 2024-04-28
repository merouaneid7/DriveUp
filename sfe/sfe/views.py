
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout
from . EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app.models import *


def home(request):
    return render(request,"main/home.html")

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def userslist(request):
    users = User.objects.all()
    user_otherfields=User_otherfields.objects.all()
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')
    
    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
        'user_otherfields':user_otherfields,
    }
    return render(request, "adm/userslist.html", context)


def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def approve_user(request,user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active is True:
        messages.warning(request,"Ce compte est deja activé")
    else:
        email=user.email
        send_mail(
            "Votre compte IKKIS AE est active",
            "Bonjour " f"{user.username}" " , vous pouvez accéder à la plateforme IKKIS AE maintenat .",
            "ikkisauto@gmail.com",
            [email],
            fail_silently=False,
    )
        user.is_active=True
        user.save()
        messages.success(request,"Le Compte d'utilisateur " f"{user.username} est activé")

    return redirect(userslist)

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def inapprove_user(request,user_id):
    user = User.objects.get(pk=user_id)
    email=user.email
    if user.is_active is False:
        messages.warning(request,"Ce compte est deja inactivé")
    else:
        send_mail(
            "Votre compte IKKIS AE est inactive",
            "Bonjour " f"{user.username}" " , vous ne pouvez pas accéder à la plateforme IKKIS AE .",
            "ikkisauto@gmail.com",
            [email],
            fail_silently=False,
        )
        user.is_active=False
        user.save()
        messages.error(request,"Le Compte d'utilisateur " f"{user.username} est inactivé" )
    return redirect(userslist)


def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def delete_user(request,user_id):
    user= User.objects.get(pk=user_id)
    email=user.email
    send_mail(
        "Vous pouvez plus acceder IKKIS AE",
        "Bonjour " f"{user.username}" " malheureusement, vous pouvez plus accéder à la plateforme IKKIS AE, si vous pensez que c'est un problème pour contacter votre agence.",
        "ikkisauto@gmail.com",
        [email],
        fail_silently=False,
    )
    user.delete()
    messages.error(request,"Le Compte d'utilisateur " f"{user.username} est supprimé" )
    return redirect(userslist)



def user_login(request):
    if request.method == 'POST' and 'btns' in request.POST :
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        print(user)
        if user is not None and user.is_active is True:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard') 
            else:
                return redirect('home')
        elif user is None:
            messages.error(request, 'Email ou mot de passe invalide')
        else:
            messages.warning(request,"Votre compte n'est pas activé ")
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        profile_img=request.POST.get('profile_img')
        cni=request.POST.get('cni')

        if User.objects.filter(email=email).exists():
           
           messages.error(request,"Ce e-mail existe déjà ")
           return redirect('signup')

        if User.objects.filter(username=username).exists():
           messages.error(request,"Le nom d'utilisateur existe déjà ")
           return redirect('signup')
        
        if confirm_password != password:
            messages.error(request,"Les mots de passe ne correspondent pas!")
            return redirect('signup')
        
        user = User.objects.create_user(username=username,email=email,password=password,last_name=last_name,first_name=first_name)
        user.is_active=False
        user.save()

        otherfields=User_otherfields.objects.create(user=user,profile_image=profile_img,cni=cni)
        otherfields.save()

        send_mail(
                "Bienvenue sur IKKIS AE !", 
                f"Bienvenue {last_name} ! Amusez-vous bien et n'hésitez pas à nous contacter si vous avez besoin d'aide. 🚀",
                "ikkisauto@gmail.com",
                [email],
                fail_silently=False,
                )
        return redirect('login')
    return render(request,'auth/signup.html')


def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        profile_img=request.POST.get('profile_img')
        cni=request.POST.get('cni')

        if User.objects.filter(email=email).exists():
           
           messages.error(request,"Ce e-mail existe déjà ")
           return redirect('userlist')

        if User.objects.filter(username=username).exists():
           messages.error(request,"Le nom d'utilisateur existe déjà ")
           return redirect('userlist')
        
        if confirm_password != password:
            messages.error(request,"Les mots de passe ne correspondent pas")
            return redirect('userlist')
        
        user = User.objects.create_user(username=username,email=email,password=password,last_name=last_name,first_name=first_name)
        user.is_active=False
        user.save()

        otherfields=User_otherfields.objects.create(user=user,profile_image=profile_img,cni=cni)
        otherfields.save()

        send_mail(
                "Bienvenue sur IKKIS AE !", 
                f"Bienvenue {last_name} ! Amusez-vous bien et n'hésitez pas à nous contacter si vous avez besoin d'aide. 🚀",
                "ikkisauto@gmail.com",
                [email],
                fail_silently=False,
                )
        return redirect('userlist')
    messages.success(request,"Vous avez ajoutee l'utilisateur " f"{user.username}")
    return render(request,'adm/userlist.html')


def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def adm_dash(request):
    user_active=User.objects.filter(is_active=True).count()
    user_inactive=User.objects.filter(is_active=False).count()
    pourcent=(user_active)/(user_active + user_inactive)

    


    context={
        'user_active':user_active,
        'user_inactive':user_inactive,
        'pourcent':pourcent,
        

    }
    return render(request,"adm/dash.html",context)


def active_users(request):
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')

    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
    }
    return render(request, "adm/userslist.html", context)


def inactive_users(request):
    users = User.objects.filter(is_active=False)
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')

    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
    }
    return render(request, "adm/userslist.html", context)
    
   
def last_added(request):
    users = User.objects.all().order_by('-id')
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')

    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
    }
    return render(request, "adm/userslist.html", context)
    
def only_admin(request):
    users = User.objects.filter(is_superuser=True)
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')

    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
    }
    return render(request, "adm/userslist.html", context)

def only_client(request):
    users = User.objects.filter(is_superuser=False)
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')

    
    page_obj = paginator.get_page(page_number)
    
    if page_obj is EmptyPage:
        
        render("userslist")

    user_approved = User.objects.filter(is_active=True)
    user_inapproved = User.objects.filter(is_active=False)
    context = {
        'users':users,
        'page_obj': page_obj,  
        'user_approved': user_approved,
        'user_inapproved': user_inapproved,
    }
    return render(request, "adm/userslist.html", context)
    
   
def search_user(request):
    search_input=request.GET.get("search_input")

    users=User.objects.filter(first_name=search_input) | User.objects.filter(last_name=search_input)  | User.objects.filter(email=search_input)

    if not users.exists():
        messages.error(request,"Aucun utilisateur avec   ' " f"{search_input} ' comme nom d'utilisateur ou bien email")

    context={
        'page_obj':users,
    }
    return render(request,"adm/userslist.html",context)
    
   