from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posts
from .forms import PostForm,RegisterForm,LoginForm
from django.conf import settings

from django.core.mail import send_mail

from django.contrib.auth import(
    authenticate,
    login,
    logout
)

def home(request):
    return render(request,'InstaApp/base.html')

def post_list(request):
    posts=Posts.objects.all()
    return render(request,'InstaApp/postlist.html',{'posts':posts})

@login_required
def view_post(request,post_id):
    post=get_object_or_404(Posts,id=post_id)
    return render(request,'InstaApp/viewpost.html',{'post':post})

@login_required()
def create_post(request):
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            email_to=[request.user.username]
            subject="Created new post!"
            message=f"Posted successfully.\nPost image or video:{post.postmedia}\nCaption:{post.caption}\nLocation:{post.postlocation}"

            send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,email_to)
            return redirect('postlist')

        else:
            form=PostForm()
    return render(request,'InstaApp/postcreate.html',{'form':form})

@login_required
def update_post(request,post_id):
    post=get_object_or_404(Posts,id=post_id)
    if request.method=='POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('postlist')
    else:
        form=PostForm(instance=post)
    return render(request,'InstaApp/postupdate.html',{'form':form})

@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Posts,id=post_id)
    post.delete()
    return redirect('home')



def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                messages.success(request, f'Login Successfully')
                login(request,user)
                return redirect('home')
            else:
                form.add_error(None,'Invalid Username or password.Try Again')
    else:
        form=LoginForm()
    return render(request,"InstaApp/login.html",{'form':form})

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, f'User Registered Successfully')

            return redirect('login')
    else:
        form=RegisterForm()
    return render(request,'InstaApp/login.html',{'form':form})

@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')




# Create your views here.
