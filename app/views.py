from django.shortcuts import render, redirect
from .models import Post, Profile
# Create your views here.

from .forms import UserRegisterForm, PostForm

def newsfeed(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False) # aqui si se necesita agregar que usuario hace el post
            post.user = request.user
            post.save()
            return redirect('home')


    else:
        form = PostForm

    ctx ={'posts': posts, 'form':form}
    return render(request, 'twitter/newsfeed.html', ctx)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UserRegisterForm()
    ctx = {
        'form': form
    }
    return render(request, 'twitter/register.html', ctx)

def delPost(request, pk):
    postTarget = Post.objects.get(id=pk)
    postTarget.delete()

    return redirect('home')

from django.contrib.auth.models import User

def profile(request, username):
    user = User.objects.get(username= username)
    posts = user.posts.all()

    ctx = { 'user':user, 'posts':posts}
    return render(request, 'twitter/profile.html', ctx)

    