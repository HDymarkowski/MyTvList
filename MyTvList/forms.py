from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from MyTvList.models import UserProfile
from django.db import models
import tmdbSimpleApi

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())    

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    favouriteShow = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = UserProfile
        fields = ('picture', 'favourite_Show_Name', 'favouriteShow',)

    
    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        favourite_Show_Name = cleaned_data.get("favourite_Show_Name")
        favouriteShow = tmdbSimpleApi.getId(favourite_Show_Name)
        if favouriteShow == None:
            self.add_error('favourite_Show_Name', 'Can not find show')        

        return cleaned_data