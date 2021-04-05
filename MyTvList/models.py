from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import Review
import tmdbSimpleApi
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    favourite_Show_Name = models.CharField(max_length=1000, blank=True)
    favouriteShow = models.IntegerField(default = None)
    

    watchlist = [favouriteShow,]
    

    def getFavouriteShow(self):
        return self.favouriteShow

    def __str__(self):
        return self.user.username

    def add_watchlist(show):
        watchlist.append(tmdbSimpleApi.getId(favourite_Show_Name))
        
class Review(forms.ModelForm):
        
        username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
         
        rating = forms.IntegerField(widget=forms.Rating())
        review = forms.CharField(widget=forms.Review()) 
        
        class Meta:
            model = Reviews
            fields = (showID, review, rating, userID)
            
        def getRating(self):
            return self.Rating
        
        def getreview(self):
            return self.review
        
        def Getuser(self):
            return self.user.username
