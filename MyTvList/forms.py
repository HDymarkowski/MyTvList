from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from MyTvList.models import User, UserProfile
from MyTvList.models import Review
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
    #favouriteShow = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = UserProfile
        fields = ('picture', 'favourite_Show_Name',)

    
    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()

        favourite_Show_Name = cleaned_data.get("favourite_Show_Name")
        favouriteShow = tmdbSimpleApi.getId(favourite_Show_Name)
        if favouriteShow == None:
            self.add_error('favourite_Show_Name', 'Can not find show')        

        return cleaned_data
    
class ReviewForm(forms.ModelForm):
    #RatingInput = forms.IntegerField(initial=1)
    #ReviewInput = forms.CharField(initial="")
    showTitle = forms.CharField(max_length = 10000)    
    #username = request.user
    #rating = forms.IntegerField(widget=forms.RatingInput())
    #writtenReview = forms.CharField(widget=forms.ReviewInput())    

    class Meta:
        model = Review
        fields = ('username', 'rating', 'review', 'showTitle',)    #idk if username should be in here cause it's a part of User and not review, 
                                                      #it might work different cause it's a foriegn key tho idk how they work really

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        Rating = cleaned_data.get("rating")
        Review = cleaned_data.get("review")

        if Rating < 1:
            self.add_error('ratingInput', "Must be between 1 and 5.")
        elif Rating > 5:
            self.add_error('ratingInput', "Must be between 1 and 5.")

        return cleaned_data
