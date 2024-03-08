from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile, Post



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email', 
        ]

        widgets={

            'username':forms.TextInput(attrs={'class' : 'form-control'}),
            'first_name':forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name':forms.TextInput(attrs={'class' : 'form-control'}),
            'email':forms.EmailInput(attrs={'class' : 'form-control'}),

        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        
        widgets={

            'name':forms.TextInput(attrs={'class' : 'form-control'}),
            'body':forms.Textarea(attrs={'class' : 'form-control'})

        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')
        
        widgets={

            'title':forms.TextInput(attrs={'class' : 'form-control'}),
            'body':forms.Textarea(attrs={'class' : 'form-control'})

        }