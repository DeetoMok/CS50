from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auction, Bid, Comment

# LEFT WITH PICTURES AND THE PRICING AT THE INDEX
def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(open_status=True)
    })

def inactive(request):
    return render(request, "auctions/inactive.html", {
        "auctions": Auction.objects.filter(open_status=False)
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
    if request.method == "POST":
        title = request.POST["title"]
        url = request.POST["url"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        category = request.POST["category"]
        creator = request.user.username
        user = User.objects.get(username=creator)
        auction_entry = Auction(title=title, url=url, description=description, start_bid=bid, category=category, creator=creator, open_status=True)
        auction_entry.save()
        list_id = Auction.objects.get(title=title).id
        start_bid = Bid(auction=auction_entry, bidder=user, bid=bid)
        start_bid.save()        
        return HttpResponseRedirect(reverse("listing", args=(list_id,)))     
    else:
        return render(request, "auctions/create.html")

@login_required(login_url='login')
def listing(request, list_id):
    listing = Auction.objects.filter(pk=list_id)
    username = request.user.username
    user = User.objects.get(username=username)
    user_watchlist = user.watchlists.filter(title=listing.first().title)
    creator = listing.first().creator
    if user_watchlist.count()==0:
        is_watch = False
    else:
        is_watch = True
    if listing.first().creator == username:
        is_creator = True
    else:
        is_creator = False
    start_price = listing.first().start_bid   
    bid_price = Bid.objects.get(auction=listing.first()).bid
    highest_bidder = Bid.objects.get(auction=listing.first()).bidder
    is_open = listing.first().open_status
    comments = Comment.objects.filter(auction=listing.first())
    return render(request, "auctions/listing.html", {
        "title": listing.first().title,
        "url": listing.first().url,
        "description": listing.first().description,
        "start_bid": start_price,
        "bid": bid_price,
        "category": listing.first().category,
        "is_watch": is_watch,
        "is_creator": is_creator,
        "creator": str(creator),
        "highest_bidder": str(highest_bidder),
        "is_open": is_open,
        "comments": comments
    })

def watching(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return render(request, "auctions/watching.html", {
        "auctions": Auction.objects.filter(watchers=user).all()
    })

def watch(request, title):
    username = request.user.username
    auction = Auction.objects.get(title=title)
    user = User.objects.get(username=username)
    # add auction to watchlist
    user.watchlists.add(auction)
    list_id = Auction.objects.get(title=title).id
    return HttpResponseRedirect(reverse("listing", args=(list_id,)))

def unwatch(request, title):
    username = request.user.username
    auction = Auction.objects.get(title=title)
    user = User.objects.get(username=username)
    # remove auction to watchlist
    user.watchlists.remove(auction)
    user_watchlist = user.watchlists.all()
    list_id = Auction.objects.get(title=title).id
    return HttpResponseRedirect(reverse("listing", args=(list_id,)))
    
def bid(request, title):
    bid = request.POST["bid"] 
    auction = Auction.objects.get(title=title)
    current_bid = Bid.objects.get(auction=auction).bid
    username = request.user.username
    user = User.objects.get(username=username)
    if int(bid) > int(current_bid):
        higher_bid = True
        new_bid = Bid.objects.get(auction=auction)
        new_bid.bid = bid
        new_bid.bidder = user
        new_bid.save()
    else:
        higher_bid = False

    listing = Auction.objects.filter(title=title)

    user_watchlist = user.watchlists.filter(title=listing.first().title)
    creator = listing.first().creator
    if user_watchlist.count()==0:
        is_watch = False
    else:
        is_watch = True
    if listing.first().creator == username:
        is_creator = True
    else:
        is_creator = False
    start_price = listing.first().start_bid   
    bid_price = Bid.objects.get(auction=listing.first()).bid
    highest_bidder = Bid.objects.get(auction=listing.first()).bidder
    is_open = listing.first().open_status
    comments = Comment.objects.filter(auction=listing.first())    
    return render(request, "auctions/listing.html", {
        "title": listing.first().title,
        "url": listing.first().url,
        "description": listing.first().description,
        "start_bid": start_price,
        "bid": bid_price,
        "category": listing.first().category,
        "is_watch": is_watch,
        "is_creator": is_creator,
        "creator": str(creator),
        "failed_bid": "Enter a bid higher than the current bid",
        "higher_bid": higher_bid,
        "highest_bidder": str(highest_bidder),
        "is_open": is_open,
        "comments": comments
    })

def close_listing(request, title):
    username = request.user.username
    user = User.objects.get(username=username)
    auction = Auction.objects.get(title=title)
    auction.open_status = False
    auction.save()
    list_id = auction.id
    return HttpResponseRedirect(reverse("listing", args=(list_id,)))

def comment(request, title):
    username = request.user.username
    user = User.objects.get(username=username)
    auction = Auction.objects.get(title=title)
    comment_text = request.POST["comment"]
    new_comment = Comment(auction=auction, comment_user=user, text=comment_text)
    new_comment.save()
    list_id = auction.id
    return HttpResponseRedirect(reverse("listing", args=(list_id,)))    
    # add into comment and save. Later still need to retreive comments to throw into listings