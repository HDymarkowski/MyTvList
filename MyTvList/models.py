from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import tmdbSimpleApi
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    favourite_Show_Name = models.CharField(max_length=1000, blank=True)
    # favouriteShow = models.IntegerField()

    def __str__(self):
        return self.user.username