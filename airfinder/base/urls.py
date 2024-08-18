from django.urls import path
from .views import *

urlpatterns = [path("", Index.as_view(), name="index"),
               path("register", Regsiter.as_view(), name="register"),
               path("about", About.as_view(), name="about"),
               path("contact", Contact.as_view(), name="contact"),
               path("search", Search.as_view(), name="search"),              
               path('logout', Logout.as_view(), name='logout'),
               path('results', ListingsResults.as_view(), name='listings_results'),
               path('my_listings', MyListings.as_view(), name="my_listings"),
               path('toggle-like', toggle_like, name="toggle-like"),
               path('toggle-delete', toggle_delete, name="toggle-delete"),
               path('load-cities/', load_cities, name='load-cities')]
