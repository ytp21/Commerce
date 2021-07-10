from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionListing, Bid, Comment, Category

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Category)

@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    filter_horizontal = ('watcher',) 

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    filter_horizontal = ('bidder',) 