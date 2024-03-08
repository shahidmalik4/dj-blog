from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from .models import Post, Comment
from .forms import CommentForm, UserForm, ProfileForm, SignupForm, PostForm




def home(request):
	context = {
		"posts":Post.objects.all()
	}
	return render(request, 'home.html', context=context)


def my_posts(request, id):
    context = {
        "posts":Post.objects.filter(author=id)
    }
    return render(request, 'user_posts.html', context=context)


def user_posts(request, id):
    posts = Post.objects.filter(author=id)
    user = get_object_or_404(User, id=id)
    context = {
        "posts":posts,
        "user":user

    }
    return render(request, 'user_posts.html', context=context)


def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)
    comments=Comment.objects.filter(post=post).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get('body')
            name = request.POST.get('name')
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {

    }
    context = {
    	'post': post, 
        'comments' : comments,
        'comment_form' : comment_form
    }

    return render(request, 'detail.html', context=context)


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
        return render(request, "auth/login.html")
    return redirect("home")


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_c = request.POST.get("password-c")
        print(f'username={username}')
        if (password == password_c):
            try:
                user = User.objects.create_user(username, email, password);
                user.save()
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect("home")
            except IntegrityError:
                messages.info(request, "Try different Username")
                return render(request, "signup.html")
        messages.error(request, "Password doesn't match Confirm Password")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "auth/signup.html")


def profile(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        context = {
            "user":user
        }
        return render(request, 'auth/profile.html', context=context)
    else:
        return redirect('login')


def update_profile(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        user_form = UserForm()
        profile_form = ProfileForm()

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={"id":request.user.id}))

        context = {
            "user":user,
            "user_form":user_form,
            "profile_form":profile_form
        }

        return render(request, 'auth/profile-update.html', context=context)


def create_post(request):
    if request.user.is_authenticated:
        post_form = PostForm()
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                messages.success(request, "The post has been created successfully.")
            return HttpResponseRedirect(new_post.get_absolute_url())
    else:
        return redirect('home')

    context = {
        "post_form":post_form
    }

    return render(request, 'create_post.html', context=context)


def update_post(request, slug):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        post_form = PostForm(request.POST or None, instance=post)
        if post_form.is_valid():
            up_post = post_form.save(commit=False)
            up_post.save()
            messages.success(request, 'Post is updated successfully!')
            return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "post_form":post_form
    }

    return render(request, 'update_post.html', context=context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    #if request.user.is_authenticated and request.user.username == post.author:
    post.delete()
    messages.success(request,'Post was deleted Successfully!')
    return redirect('home')