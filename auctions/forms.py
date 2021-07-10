import re

from django import forms
from django.forms import ModelForm
from django.core import validators

from .models import AuctionListing, Bid, Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        
        fields = ('title', 'description', 'starting_price', 'category', 'image_url')

        labels = {
            'image_url': '',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control mt-1"}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-1', 'rows': '2'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control mt-1'}),
            'category': forms.Select(attrs={'class': 'form-control mt-1'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control mt-1'}),
        }

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        title_pattern = '^[\w\-\_\/\(\)\.\%\$\~\s\&]+$'         
        if not re.search(title_pattern, title):
            raise forms.ValidationError('Valid title is required (alphabet "a-z/A-Z" and -_/().%$~&)')
        return title

    def clean_starting_price(self, *args, **kwargs):
        starting_price = self.cleaned_data.get('starting_price')       
        if starting_price < 0:
            raise forms.ValidationError('Negative value is invalid')
        return starting_price
    
class BidForm(ModelForm):
    class Meta:
        model = Bid

        fields = ('current_bid',)

        labels = {
            'current_bid': '',
        }

        widgets = {
            'current_bid': forms.NumberInput(attrs={'class': "form-control; mt-2"}),
        }

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

    def clean_current_bid(self, *args, **kwargs):
        current_bid = self.cleaned_data.get('current_bid')
        listing = AuctionListing.objects.get(id=self.pk)
        if current_bid <= listing.starting_price:
            raise forms.ValidationError('Your bid is lower than the starting price')
        elif Bid.objects.filter(listing=listing.pk).count() != 0:
            listing_bid = Bid.objects.get(listing=listing.pk)
            if current_bid <= listing_bid.current_bid:
                raise forms.ValidationError('Your bid is lower than the current highest bid price')
        return current_bid
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment

        fields = ('comment_title', 'comments')

        labels = {
            'comment_title': 'Title',
            'comments': 'Comment',
        }

        widgets = {
            'comment_title': forms.TextInput(attrs={'class': "form-control; mt-2"}),
            'comments': forms.Textarea(attrs={'class': "form-control; mt-2", 'rows': '4'})
        }