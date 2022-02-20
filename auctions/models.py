from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    startingbid = models.IntegerField()
    desc = models.TextField(default='')
    img = models.URLField(blank = True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.TextField(blank = True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
    amount = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    content = models.TextField()

class Watchlist(models.Model):
    userid = models.ForeignKey(User,on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)