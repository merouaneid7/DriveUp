
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from . EmailBackEnd import EmailBackEnd

def home(request):
    return render(request,"main/home.html")


def user_login(request):
    if request.method == 'POST' and 'btns' in request.POST :
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'auth/login.html')




def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        # check email
        if User.objects.filter(email=email).exists():
           
           messages.warning(request,'Email are Already Exists !')
           return redirect('signup')
        

        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'Username are Already exists !')
           return redirect('signup')
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('login')
    return render(request,'auth/signup.html')