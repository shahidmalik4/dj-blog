from django.urls import path
from .views import (
                    home, post_detail,
                    user_login,user_logout, signup, profile, update_profile,
                    my_posts, user_posts,
                    create_post, update_post, delete_post
                )

urlpatterns = [
    path("", home, name="home"),
    path("post/<slug>/", post_detail, name="post_detail"),

    path('user/<id>/my-posts/', my_posts, name='my_posts'),
    path('user/<id>/posts/', user_posts, name='user_posts'),
    
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('user/<id>/profile/', profile, name='profile'),
    path('user/<id>/profile-update/', update_profile, name='update_profile'),

    path('create-post/', create_post, name='create_post'),
    path("post/<slug>/update", update_post, name="update_post"),
    path("post/<slug>/delete", delete_post, name="delete_post"),]
