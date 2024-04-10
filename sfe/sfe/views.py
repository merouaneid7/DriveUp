
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from . EmailBackEnd import EmailBackEnd
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request,"main/home.html")

def uerslist(request):
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request,"adm/userslist.html",context)


def approve_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.is_active=True
    user.save()
    return HttpResponse("DONE")
    
def delete_user(request,user_id):
    user= User.objects.get(pk=user_id)
    user.delete()
    return redirect(uerslist)



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
            return redirect('home')  
        elif user is None:
            messages.error(request, 'Email ou mot de passe invalide')
        else:
            messages.warning(request,"Votre compte n'est pas activé ")
    return render(request, 'auth/login.html')




def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
           
           messages.error(request,"Ce e-mail existe déjà ")
           return redirect('signup')

        if User.objects.filter(username=username).exists():
           messages.error(request,"Le nom d'utilisateur existe déjà ")
           return redirect('signup')
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.is_active=False
        user.save()
        return redirect('login')
    return render(request,'auth/signup.html')

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def adm_dash(request):
    user_active=User.objects.filter(is_active=True).count()
    user_inactive=User.objects.filter(is_active=False).count()
    pourcent=(user_active-user_inactive)/100
    

    context={
        'user_active':user_active,
        'user_inactive':user_inactive,
        'pourcent':pourcent,
    }
    return render(request,"adm/dash.html",context)