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

from .models import Profile

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			Profile.objects.create(user = user) # crea el perfil 		
			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)

def delPost(request, pk):
    postTarget = Post.objects.get(id=pk)
    if request.user == postTarget.user:
        postTarget.delete()
    return redirect('home')

from django.contrib.auth.models import User

def profile(request, username):
    user = User.objects.get(username= username)
    posts = user.posts.all()

    ctx = { 'user':user, 'posts':posts}
    return render(request, 'twitter/profile.html', ctx)



from .forms import UserUpdateForm, ProfileUpdateForm

def editar(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('home')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form' : u_form, 'p_form' : p_form}
	return render(request, 'twitter/editar.html', context)

# Seguir usuario

from .models import Relationship

def follow(request, username):                      # parametro para obtener el usuario que estamos visitando
	current_user = request.user                     # nuestro perfil de usuario
	to_user = User.objects.get(username=username)   # obtenemos el usuario que visitamos
	to_user_id = to_user                            # le saca la id al usuario que visitamos
	rel = Relationship(from_user=current_user, to_user=to_user_id) # se crea una instancia del modelo relacional
	rel.save()                                      # guarda el model
	return redirect('home')

# dejar de seguirusuario

from .models import Relationship

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('home')