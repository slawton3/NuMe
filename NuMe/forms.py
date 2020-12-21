from django import forms
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _
from .models import NMUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterUsername(UserCreationForm):
    email = forms.EmailField(required=True, label="Email: ", error_messages={'exists': 'Email already used.'})
    class Meta:
      model = User
      fields = ('username', 'email', 'password1', 'password2')


    def save(self, commit=True):
        user = super(RegisterUsername, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def cleanEmail(self):
        if NMUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class SignInUserForm(forms.Form):
  username = forms.CharField(max_length=30, required=True)
  password = forms.CharField(widget=forms.TextInput(attrs={'type' : 'password'}))

