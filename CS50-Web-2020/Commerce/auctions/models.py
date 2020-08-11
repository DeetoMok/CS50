from django.contrib.auth.models import AbstractUser
from django.db import models

class Auction(models.Model):
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=64, default="")
    description = models.CharField(max_length=160)
    start_bid = models.IntegerField(default=0)
    category = models.CharField(max_length=64, default="others")
    creator = models.CharField(max_length=64, default="")
    open_status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} (${self.start_bid}): {self.description}"

class User(AbstractUser):
    watchlists = models.ManyToManyField(Auction, blank=True, null=True, default="", related_name="watchers")

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default="", related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="bidder")
    bid = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.id}. {self.auction}: {self.bidder} bid ${self.bid}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default="", related_name="auction")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="user")
    text = models.CharField(max_length=160, default="")
    def __str__(self):
        return f"{self.comment_user}: {self.text}"
