#Django imports
import json
import time
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Listing
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .utils.network_utils import fetch_data
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import csv

#Scraping imports
from .scraper import Scraper
from .tasks import check_price_updates


# Create your views here.
class Index(TemplateView):
    template_name = 'base/index.html'

class Regsiter(LoginView):
    template_name = 'base/login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'signup':
            return self.signup(request)
        elif action == 'signin':
            return self.signin(request)
        
    def signup(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if a user with the provided username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'User already exsists.')
            return redirect('register') 
        
        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(request, 'Account created successfully,' +'\n' 'please login')
        return redirect('register')
    
    def signin(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'Wrong username or password')
            return redirect('register')   
        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')
    
class About(TemplateView):
    template_name = 'base/about.html'
    
class Contact(TemplateView):
    template_name = 'base/contact.html'

class Search(LoginRequiredMixin, TemplateView):
    template_name = 'base/search.html'

    
    def get(self, request, *args, **kwargs):
        request.session.pop('listings', None)
        return render(request, self.template_name)

    def post(self, request,  *args, **kwargs):
        user = request.user
        # Collect all inputs
        city = request.POST.get('city')
        check_in_date = request.POST.get('check-in')
        check_out_date = request.POST.get('check-out')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        infants = request.POST.get('infants')
        pets = request.POST.get('pets')

        
       
    

        # Assuming client-side validation is handling empty fields and basic checks
        # Proceed with operations that require validated inputs
        scraper = Scraper()
        listing_ids, links, titles, prices, ratings, images = scraper.scrape(
            city, check_in_date, check_out_date,
            int(adults), int(children), int(infants), int(pets)
        )

        #If innitail scraping failed
        scrape_again = False
        if len(listing_ids) == 0 and len(links) == 0 and len(titles) == 0 and len(prices) == 0 and len(ratings) == 0 and len(images) == 0:
           scrape_again = True

        #Try until scraping succeeds
        while scrape_again:
            listing_ids, links, titles, prices, ratings, images = scraper.scrape(
            city, check_in_date, check_out_date,
            int(adults), int(children), int(infants), int(pets)
        )
            if len(listing_ids) == 0 and len(links) == 0 and len(titles) == 0 and len(prices) == 0 and len(ratings) == 0 and len(images) == 0:
                scrape_again = True
            else:
                scrape_again = False
            

        # Filter listings
        filtered_ids, filtered_links, filtered_titles, filtered_prices, filtered_ratings, filtered_images = scraper.filter_listings(
            listing_ids, links, titles, prices, ratings, images)

        # Zip these lists together and create a dictionary for each listing
        listings = [
            {
                'id': id,
                'link': link,
                'title': title,
                'price': price,
                'rating': rating,
                'image': image
            }
            for id, link, title, price, rating, image in zip(filtered_ids, filtered_links, filtered_titles, filtered_prices, filtered_ratings, filtered_images)
        ]

        

        for listing in listings:
            # Check if the listing already exists in the database
            if not Listing.objects.filter(listing_id=listing['id']).exists():
                # Create a new Listing object
                Listing.objects.create(link = listing['link'],
                                    image = listing['image'],
                                    listing_id = listing['id'],
                                    title = listing['title'],
                                    price = listing['price'],
                                    rating = listing['rating'],
                                    check_in = check_in_date,
                                    check_out = check_out_date,
                                    adults = adults,
                                    children = children,
                                    infants = infants,
                                    pets = pets
                                    )
                

        liked_listings = Listing.objects.filter(liked_by=user)
        # Build a dictionary with listing IDs as keys
        liked_listings_dict = {listing.listing_id: True for listing in liked_listings}


        # Save listings to session as a list of dictionaries
        request.session['liked_listings'] = liked_listings_dict
        request.session['listings'] = listings
        scraper.__del__()
        # Redirect
        return redirect('listings_results')            

class ListingsResults(TemplateView):
    template_name = 'base/listings_results.html'

    def get(self, request, *args, **kwargs):
        # Check if listings are already stored in the session
        if 'listings' in request.session:
            listings_dict = request.session['listings']
            liked_listings_dict = request.session['liked_listings']  # Use get to avoid KeyError if not present
        context = {
            'listings': listings_dict,
            'liked_listings': liked_listings_dict
        }
        return render(request, self.template_name, context)

class MyListings(TemplateView):
    template_name = 'base/my_listings.html'

    def get(self, request, *args, **kwargs):
        allowed_notifications = False
        user = request.user
        liked_listings = list(Listing.objects.filter(liked_by=user))
        if allowed_notifications:
            check_price_updates.delay(user.id)
        return render(request, self.template_name, {'liked_listings': liked_listings})
   
@csrf_exempt
def toggle_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        listing_id = data.get('listingId')
        liked = data.get('liked')
        
        # Assuming you have a user and a listing model with a ManyToMany relationship
        listing = Listing.objects.get(listing_id=listing_id)
        if liked:
            request.user.liked_listings.add(listing)
        else:
            request.user.liked_listings.remove(listing)
        
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
@require_POST
def toggle_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        listing_id = data.get('listingId')
        user = request.user

        try:
            # Ensure that only listings belonging to the logged-in user can be deleted
            listing = Listing.objects.get(listing_id=listing_id)
            user.liked_listings.remove(listing)
            return JsonResponse({'status': 'success', 'message': 'Listing deleted successfully.'}, status=200)
        except Listing.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Listing not found or not owned by user.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


def load_cities(request):
    path_to_csv = '/Users/shaharishay/Programming/Python/Django/airfinder/worldcities.csv'  # Update this to the path of your CSV file
    cities = []
    with open(path_to_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            result = row[0] + ", " + row[4]
            cities.append(result)  # Assuming city names are in the first column

    return JsonResponse({'cities': cities})
