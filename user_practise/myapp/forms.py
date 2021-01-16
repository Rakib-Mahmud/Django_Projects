from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from myapp.models import UserProfile

class UserInfo(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','email','password']

class MoreInfo(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['portfolio','dp']
