from django import forms
from django.forms.widgets import TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Ticket, Review, UserFollows


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username*'})
        self.fields["password1"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password*'})
        self.fields["password2"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password Confirmation*'})

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomAuthenticationForm(AuthenticationForm):
    """Custom Authentication form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username*'})
        self.fields["password"].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password*'})


class UserFollowForm(forms.ModelForm):
    """Form for user follows"""
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        widgets = {'followed_user': TextInput(attrs={'class': 'form-control', 'placeholder': 'Type the username'})}


class TicketForm(forms.ModelForm):
    """Form for creating tickets"""

    class Meta:
        model = Ticket
        fields = ['title', 'description', "image"]
        labels = {"title": "Title", "description": "Description"}


class ReviewForm(forms.ModelForm):
    """Form for creating reviews"""
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "Title", "rating": "Rating", "body": "Body"}
        CHOICES = [(1, '1'), (2, '2'), (4, '3'), (4, '4'), (5, '5')]
        widgets = {"rating": forms.RadioSelect(choices=CHOICES), "body": forms.Textarea()}
