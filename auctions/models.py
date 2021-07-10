from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email

class User(AbstractUser):
    pass

class DateTimeCreated(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
    
class Category(models.Model):
    category = models.CharField(max_length=20)
    image_url = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.category

class AuctionListing(DateTimeCreated):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image_url = models.CharField(max_length=1000, blank=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listing_creator")
    watcher = models.ManyToManyField(User, blank=True, related_name="listing_watcher")
    deactivate = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, related_name="listing_buyer")
    
    def __str__(self):
        return f"{self.title}"
        
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, default=None, on_delete=models.PROTECT, related_name="listing_bid")
    current_bid = models.DecimalField(max_digits=10, default=None, decimal_places=2)
    highest_bidder = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name="highest_bidder")
    bidder = models.ManyToManyField(User, default=None, related_name="bidder")

    def __str__(self):
        return f"{self.listing}"

class Comment(DateTimeCreated):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    comment_title = models.CharField(max_length=50, null=True)
    comments = models.TextField(max_length=300, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.listing}"