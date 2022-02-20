from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Listing, Watchlist, Bid

class ListingForm(forms.Form):
    title = forms.CharField(label="Title")
    desc = forms.CharField(label="Description")
    startbid = forms.IntegerField(label="Starting Price")
    img = forms.CharField(label="Image link (optional)", required=False)
    category = forms.CharField(label="Category (optional)",required=False)

class BidForm(forms.Form):
    amount = forms.IntegerField(label="Bid")


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            img = ''
            category = ''
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["desc"]
            startingbid = form.cleaned_data["startbid"]
            if form.cleaned_data["img"]:
                img = form.cleaned_data["img"]
            if form.cleaned_data["category"]:
                category = form.cleaned_data["category"]
            listing = Listing.objects.create(title = title,desc=desc,startingbid=startingbid,author=request.user,img=img,category=category)
            Bid.objects.create(amount=startingbid,listing=listing,user=request.user)
            return HttpResponseRedirect(reverse("index"))

    return render(request,'auctions/create.html', {
        'form': ListingForm
    })


def listing(request,listing):
    listing = Listing.objects.get(id=listing)
    bids = Bid.objects.all().filter(listing=listing)
    topbid = 0
    bidcount = 0
    topuser = ''
    for each in bids:
        bidcount += 1
        if each.amount > topbid:
            topbid = each.amount
            topuser = each.user
    
    if request.method == "POST" and request.POST["watchlist"] == 'true':
        Watchlist.objects.create(userid=request.user,listing=Listing.objects.get(id=listing))
        return HttpResponseRedirect(reverse("watchlist"))
    if request.method == "POST" and request.POST["close"] == 'true':
        Listing.objects.filter(id=listing.id).delete()
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST" and request.POST["bid"] == 'true': 
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['amount']
            if bid > topbid and bid > listing.startingbid:
                Bid.objects.create(amount=bid,listing=listing,user = request.user)
                Listing.objects.filter(id=listing.id).update(startingbid=bid)
            return HttpResponseRedirect(reverse("listing",args=[listing.id]))


    if request.method == "GET":
        watchlisted = False
        if request.user.is_authenticated:
            if Watchlist.objects.all().filter(userid=request.user,listing=listing):
                watchlisted = True
        return render(request, 'auctions/listing.html',{
            "listing": listing,
            "watchlisted": watchlisted,
            "bidform": BidForm,
            "bidcount": bidcount,
            "topuser": topuser,
            "author": listing.author
        })

def watchlist(request):

    if request.method == "POST":
        Watchlist.objects.all().filter(userid = request.user,listing=request.POST["item"]).delete()

    listings = Watchlist.objects.all().filter(userid=request.user)
    return render(request,'auctions/watchlist.html',{
        'listings': listings
    })