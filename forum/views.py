from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import Register , Login , newThread , commentForm , forgotPassword
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , logout
from django.contrib.auth import login as auth_login 
from django.template import RequestContext
from .models import Thread
# Create your views here.
def index(request):
    return HttpResponse(render(request , "forum/index.html")) 

def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request , username = username , password = password)

            if user is not None :
                if user.is_active :
                    auth_login(request , user)
                    return HttpResponseRedirect(reverse('space'))
            else :
                messages.error(request , "Invalid credentials , please try again.")
                context  = {
                    'form' : Login() 
                }
                return render(request , 'forum/login.html' , context)
            
    if request.method == "GET":

        if request.user.is_authenticated:

            return HttpResponseRedirect(reverse('space'))
        
        form = Login()
    
    return HttpResponse(render(request , 'forum/login.html' , {"form" : form}))

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            del data['cpassword']
            user = User.objects.create_user(**data)
            user.set_password(data['password'])
            user.save()
            return HttpResponseRedirect(reverse('login'))

        else :

            return HttpResponse(render(request , 'forum/register.html' , {'form' : form}))

    
    if request.method == "GET":
        
        form = Register()

    return HttpResponse(render(request , 'forum/register.html' , {'form' : form})) 

def space(request):
    if request.user.is_authenticated:
        threadForm = newThread() 
        comment = commentForm()
        threads = Thread.objects.all()
        context = {
            "threadForm": threadForm,
            "commentForm":comment,
            "threads" : threads[::-1]
        }
        return render(request , 'forum/space.html' , context = context) 
    else:
        return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index')) 

def postThread(request):
    if request.method == "POST":
        if request.user.is_authenticated :
            form = newThread(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                thread = Thread.objects.create(user=user , title=cd['title'] , content=cd['content'])
                thread.save()
                messages.success(request ,"Thread created successfully !")
            return HttpResponseRedirect(reverse('space')) 

def forgotView(request):
    if request.method == "GET":
        context = {
            "form" : forgotPassword()
        }
        return render(request , "forum/forgot.html" , context=context) 

    if request.method == "POST":
        form = forgotPassword(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            try:
                user = User.objects.get(email__exact = cd['email'])
            except User.DoesNotExist:
                user = None
            if user is not None:
                messages.success(request , "An email has been sent to the given email address. Please check your inbox to continue")
            else :
                messages.error(request , "Please enter a valid email address.")
            return HttpResponseRedirect(reverse('forgot')) 


def profile(request , username):
    if request.method == "GET" :
        try:
            profile = User.objects.get(username=username)
        except User.DoesNotExist :
            profile = None 
        if profile is not None:
            context = {
                "profile" : profile
            }
            return render(request , "forum/profile.html" , context = context)
        else:
            return HttpResponseRedirect(reverse(space))
        