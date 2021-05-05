from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    rozmiar_buta = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'rozmiar_buta'] # fields of form
        

class YourNameForm(forms.Form):
    your_name = forms.CharField(label='Enter ur name:', max_length=100)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    rozmiar_buta = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'rozmiar_buta']

        
from .models import Profile # import model to build ur form on
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        # sometimes u can use: fields = "__all__"