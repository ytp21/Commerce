from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Category, Bid, Comment
import re

from .forms import ListingForm, BidForm, CommentForm

# Render active listing page
def index(request):
    active_listing = AuctionListing.objects.filter(deactivate=False)
    listing_with_bid = Bid.objects.all()
    ID_with_bid = []
    for listing in active_listing:
        if Bid.objects.filter(listing=listing.pk).count() != 0:
            ID_with_bid.append(listing.pk)
    return render(request, "auctions/index.html",{
        "active_listing": True,
        "all_listing": active_listing,
        "listing_with_bid": listing_with_bid,
        "ID_with_bid": ID_with_bid,
    })

def closed_listing(request):
    closed_listing = AuctionListing.objects.filter(deactivate=True)
    return render(request, "auctions/index.html",{
        "closed_listing": True,
        "all_listing": closed_listing,
    })

# Render page that shows the details and information of selected listing by the user
def listing(request, pk):
    listing_content = AuctionListing.objects.get(id=pk)
    comment_content = Comment.objects.filter(listing=pk)
    no_of_comment = len(comment_content)
    if Bid.objects.filter(listing=pk).count() != 0:
        bid_details = Bid.objects.get(listing=pk)
        total_bidder = len(bid_details.bidder.all())
    else:
        bid_details = ""
        total_bidder = 0
    return render(request, "auctions/listing.html",{
        "listing_content": listing_content,
        "comment_content": comment_content,
        "bid_details": bid_details,
        "total_bidder": total_bidder,
        "no_of_comment": no_of_comment,
        "bidform": BidForm,
        "commentform": CommentForm,
    })

def bid(request, pk):
    forms = BidForm(request.POST, pk=pk)
    if forms.is_valid():
        if Bid.objects.filter(listing=pk).count() != 0:
            Bid.objects.filter(listing=pk).update(current_bid=forms.cleaned_data.get('current_bid'), highest_bidder=request.user)
            updated_listing_bid = Bid.objects.get(listing=pk)
            if request.user not in updated_listing_bid.bidder.all():
                updated_listing_bid.bidder.add(request.user)
            return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk}))
        else:
            new_listing_bid = forms.save(commit=False)
            new_listing_bid.listing = AuctionListing.objects.get(id=pk)
            new_listing_bid.highest_bidder = request.user
            new_listing_bid.save()
            new_listing_bid.bidder.add(request.user)
            return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk}))
    else:
        listing_content = AuctionListing.objects.get(id=pk)
        comment_content = Comment.objects.filter(listing=pk)
        no_of_comment = len(comment_content)
        if Bid.objects.filter(listing=pk).count() != 0:
            bid_details = Bid.objects.get(listing=pk)
            total_bidder = len(bid_details.bidder.all())
        else:
            bid_details = ""
            total_bidder = 0
        return render(request, "auctions/listing.html",{
            "listing_content": listing_content,
            "comment_content": comment_content,
            "bid_details": bid_details,
            "total_bidder": total_bidder,
            "no_of_comment": no_of_comment,
            "bidform": forms,
            "commentform": CommentForm,
        })

def status(request, pk):
    listing = AuctionListing.objects.get(id=pk)
    if request.user.is_authenticated and request.user == listing.creator:
        if listing.deactivate is False:
            listing.deactivate = True
            if Bid.objects.filter(listing=listing.pk).count() != 0:
                bid = Bid.objects.get(listing=pk)
                listing.buyer = bid.highest_bidder
        else:
            listing.deactivate = False
            if listing.buyer is not None:
                listing.buyer = None

        listing.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk}))

    else:
        # Render login page if the guest has not signed in
        return render(request, "auctions/login.html",{
            "message": "ERROR Deactivate Listing: Account signed in is not the owner of the listing"
        })

def comment(request, pk):
    forms = CommentForm(request.POST)
    if forms.is_valid():
        comment = forms.save(commit=False)
        comment.listing = AuctionListing.objects.get(id=pk)
        comment.commenter = request.user
        comment.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk}))
    else:
        listing_content = AuctionListing.objects.get(id=pk)
        comment_content = Comment.objects.filter(listing=pk)
        no_of_comment = len(comment_content)
        if Bid.objects.filter(listing=pk).count() != 0:
            bid_details = Bid.objects.get(listing=pk)
            total_bidder = len(bid_details.bidder.all())
        else:
            bid_details = ""
            total_bidder = 0
        return render(request, "auctions/listing.html",{
            "listing_content": listing_content,
            "comment_content": comment_content,
            "bid_details": bid_details,
            "total_bidder": total_bidder,
            "no_of_comment": no_of_comment,
            "bidform": BidForm,
            "commentform": forms,
        })

# Render user login page
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # Setting minimum length for password
    min_password_length = 8

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Setting to case-insensitive username and email
        case_insensitive_username = username.lower()
        case_insensitive_email = email.lower()
        
        # Create an empty list of error message for validity check
        error_messages = []

        # Check length and validity of first name and last name 
        name_pattern = '^[a-zA-Z\s]+$'
        max_name_length = 20
        if not re.search(name_pattern, first_name) or len(first_name) > max_name_length:
            error_messages.append("invalid_firstName")
        if not re.search(name_pattern, last_name) or len(last_name) > max_name_length:
            error_messages.append("invalid_lastName")
        
        # Check username validity and length. If username is valid, then check if username has already existed
        username_pattern = '^[\w\.\-\_]+$'
        max_username_length = 20
        if not re.search(username_pattern, username) or len(username) > max_username_length:
            error_messages.append("invalid_username")
        elif User.objects.filter(username = case_insensitive_username):
            error_messages.append("username_exists")

        # Check email validity and length. If email is valid, then check if email has already existed
        email_pattern = '^[\w\.\-]+@[\w\.\-]+\.\w{2,4}$'
        max_email_length = 35
        if not re.search(email_pattern, email) or len(email) > max_email_length:
            error_messages.append("invalid_email")
        elif User.objects.filter(email = case_insensitive_email):
            error_messages.append("email_exists")

        # Check password and confirm password validity with min-length = 8 
        password_pattern = '^[\w\.\-\_\$\@\!\~\&]+$'
        if len(password) < min_password_length:
            error_messages.append("passwordTooShort")
        elif not re.search(password_pattern, password):
            error_messages.append("invalid_password")

        # Send error messages if exist
        if len(error_messages) != 0:
            return render(request, "auctions/register.html", {
                "error": error_messages,
                "typed_firstName": first_name,
                "typed_lastName": last_name,
                "typed_username": username,
                "typed_email": email,
                "max_name": max_name_length,
                "max_username": max_username_length,
                "max_email": max_email_length,
                "min_password": min_password_length
            })

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Password and confirmation password do not match",
                "typed_firstName": first_name,
                "typed_lastName": last_name,
                "typed_username": username,
                "typed_email": email
            })

        # Create new user
        user = User.objects.create_user(case_insensitive_username, case_insensitive_email, password, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "auctions/register.html", {
            "min_password": min_password_length
        })

@login_required
def create_listing(request):
    if request.method == "POST":
        forms = ListingForm(request.POST)
        if forms.is_valid():
            new_listing = forms.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
            "form": forms
        })
    else:
        form = ListingForm
        return render(request, "auctions/create_listing.html", {
            "form": form
        })


def watchlist_button(request, view, pk):
    if request.user.is_authenticated:
        listing = AuctionListing.objects.get(id=pk)

        # Add user if not exist in watcher & Remove user if exist in watcher
        if request.user in listing.watcher.all():
            listing.watcher.remove(request.user)
        else:
            listing.watcher.add(request.user) 
        
        # Return back to the request page
        if view == "activePage":
            return HttpResponseRedirect(reverse("index"))
        elif view == "listingContent":
            return HttpResponseRedirect(reverse("listing", kwargs={'pk': pk}))
    else:
        # Render login page if the guest has not signed in
        return render(request, "auctions/login.html",{
            "message": "Login is required to access watchlist feature."
        })

# Render page that shows all of the watched listing by the user
@login_required
def watchlist(request):
    watched_listing = AuctionListing.objects.filter(watcher=request.user)
    return render(request, "auctions/index.html",{
        "watchlist": True,
        "all_listing": watched_listing,
        })

def category(request, cat):
    # Render page that shows all of the categories when user clicked on the "Cateory" nav link from the top navbar
    if cat == "allCatogories":
        every_category = Category.objects.all()
        return render(request, "auctions/category.html",{
            "all_categories": every_category
        })
    elif cat == "No Category":
        category_listing = AuctionListing.objects.filter(category__category=None)
    else:
        try:
            # Render page that shows all of the listing of any selected category by the user
            Category.objects.get(category=cat)
            category_listing = AuctionListing.objects.filter(category__category=cat)
        except IntegrityError:
            None
    return render(request, "auctions/index.html",{
        "cat_dropdown": True,
        "all_listing": category_listing,
        "category": cat,
        "categoryType": Category.objects.all(),
        })

# Render page that shows all listing created by the user
def my_listing(request):
    user_listing = AuctionListing.objects.filter(creator=request.user)
    return render(request, "auctions/index.html",{
        "mylisting": True,
        "all_listing": user_listing,
        })


