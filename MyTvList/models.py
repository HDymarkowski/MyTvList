from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
#from django.contrib.auth.models import Review
import tmdbSimpleApi
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    favourite_Show_Name = models.CharField(max_length=1000, blank=True)

    #watchlist = [favouriteShow,] removed favouriteShow
    watchlist = [tmdbSimpleApi.getId(favourite_Show_Name),]
    



    def __str__(self):
        return self.user

    def add_watchlist(show):
        watchlist.append(tmdbSimpleApi.getId(show))
        
class Review(models.Model):
        
        username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
         
        rating = models.IntegerField(default = 1)
        review = models.CharField(max_length = 10000, blank = True) 

        def getRating(self):
            return self.Rating
        
        def getreview(self):
            return self.review
        
        def Getuser(self):
            return self.user.username