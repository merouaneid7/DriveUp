
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout
from . EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage
from app.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime




def home(request):
    course=Course.objects.all()
    context={
        'course':course,
    }
    return render(request,"main/home.html",context)


def take_driver(request):
    return render(request,"main/take_driver.html")


def appointement(request):
    new_appointement=Appointement.objects.all().order_by('accepted')

    context={
        'new_appointement':new_appointement,
    }
    return render(request,"adm/appointement.html",context)

def make_appoint(request):
    if request.method == 'POST':
        nom=request.POST.get('last_name')
        prenom=request.POST.get('first_name')
        email=request.POST.get('email')
        cni=request.POST.get('cni')
        phone_number=request.POST.get('phone_number')
        msg=request.POST.get('msg')
        
    if nom is not "" and prenom is not "" and email is not "":         
        appointement=Appointement.objects.create(nom=nom,prenom=prenom,cni=cni,numero_telephone=phone_number,email=email,message=msg)
        appointement.save()
        messages.success(request,"la demande est envoyer avec succes")
    else:
        messages.error(request,"Entre au moins Votre nom,prenom et email")

   
    return redirect('/#appointement')

def add_appoint(request):
    if request.method == 'POST':
        nom=request.POST.get('last_name')
        prenom=request.POST.get('first_name')
        email=request.POST.get('email')
        cni=request.POST.get('cni')
        phone_number=request.POST.get('phone_number')
        msg=request.POST.get('msg')
        date=request.POST.get('date')
    
    appointement=Appointement.objects.create(nom=nom,prenom=prenom,cni=cni,numero_telephone=phone_number,email=email,message=msg,date=date)
    appointement.save()
    messages.success(request,"la demande est envoyer avec succes")
    return redirect('appointement')



from datetime import date
def approve_appoint(request,app_id):
    our_appoint=Appointement.objects.get(pk=app_id)
    user_email=our_appoint.email
    user_name=our_appoint.nom

    if request.method == 'POST':
        date1=request.POST.get('date')
    actual_date=date.today()  
    actual_date_str = actual_date.strftime("%d/%m/%Y")
    print(actual_date_str)
    print(date1)
    print(date1>actual_date_str)
    
    

    if date1 is not "" :
        appointement=Appointement.objects.filter(id=app_id)
        appointement.update(date=date1,accepted=True)
        messages.success(request,"Rendez vous accepte pour le " f"{date1}")
        send_mail(
            "Votre compte IKKIS AE est active",
            "Bonjour " f"{user_name}" " , Votre rendez vous est accepter pour la date " f"{date1} .",
            "ikkisauto@gmail.com",
            [user_email],
            fail_silently=False,
        )
    else:
        messages.error(request,"date non valide")
    
    return redirect("appointement")

def active_appoint(request):
    new_appointement=Appointement.objects.filter(accepted=True)
    context={
        'new_appointement':new_appointement,
    }

    return render(request,"adm/appointement.html",context)

def inactive_appoint(request):
    new_appointement=Appointement.objects.filter(accepted=False)
    context={
        'new_appointement':new_appointement,
    }

    return render(request,"adm/appointement.html",context)
    


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

def only_superviseur(request):
    users=User.objects.filter(driver__is_driver=True)
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
        messages.success(request,"Vous avez ajoutee l'utilisateur " f"{user.username} ")
        return redirect('userlist')
    
    
    return render(request,'adm/userslist.html')


def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def welcome_adm(request):
    user_active=User.objects.filter(is_active=True).count()
    user_inactive=User.objects.filter(is_active=False).count()
    pourcent=(user_active)/(user_active + user_inactive)
    new_appointement=Appointement.objects.filter(accepted=False)

    


    context={
        'user_active':user_active,
        'user_inactive':user_inactive,
        'pourcent':pourcent,
        'new_appointement':new_appointement,
        

    }
    return render(request,"adm/welcome_admin.html",context)




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
    


def Edit_user(request,user_id):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        cni=request.POST.get('cni')
        password=request.POST.get('password')
        c_password=request.POST.get('c_password')
        
    if not all(request.POST.get(field) for field in request.POST.keys()):
        messages.warning(request,"non complet")

    elif password != c_password:
        messages.error(request,"mot de passe non valide")
    else:
        hashed_password = make_password(password)
        user=User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name,password=hashed_password)
        User_otherfields.objects.filter(user=user_id).update(cni=cni)
        messages.success(request,"profile modifie avec succes")
    return redirect(reverse('profile', args=[user_id]))

from django.urls import reverse
    
def Profile(request,user_id):
    user=User.objects.get(pk=user_id)
    context={
        'user':user,
        'user_id':user_id,
    }
    return render(request,"main/profile.html",context) 


def Edit_userbyadmin(request,user_id):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        cni=request.POST.get('cni')
        password=request.POST.get('password')
        c_password=request.POST.get('c_password')
        
    if not all(request.POST.get(field) for field in request.POST.keys()):
        messages.warning(request,"non complet")

    elif password != c_password:
        messages.error(request,"mot de passe non valide")
    else:
        hashed_password = make_password(password)
        user=User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name,password=hashed_password)
        User_otherfields.objects.filter(user=user_id).update(cni=cni)
        messages.success(request,"profile modifie avec succes")
    return redirect('userlist')

from django.urls import reverse
    
def Profile(request,user_id):
    user=User.objects.get(pk=user_id)
    context={
        'user':user,
        'user_id':user_id,
    }
    return render(request,"main/profile.html",context)

def Edit_profileimg(request,user_id):
    if request.method == 'POST':
        profile_img=request.POST.get('profile_img')

    user=User.objects.get(pk=user_id)
    print(user)

    return render(request,"main/profile.html")


def user_dash(request):
    return render(request,"user/my_dash.html")

def welcome(request):
    return render(request,"user/welcome.html")

def inbox(request):
    return render(request,"user/inbox.html")
