from celery import shared_task
from .models import Listing
from django.core.mail import send_mail
from .scraper import Scraper
from django.contrib.auth.models import User

@shared_task
def check_price_updates(user_id):
    user = User.objects.get(id= user_id)  # Adjust as necessary
    listings = user.liked_listings.all()
    price_drops = []

    scraper = Scraper()
    if listings:
        for listing in listings:
            new_price = scraper.compare_prices(listing.link)
            if new_price < listing.price:
                price_drops.append((listing, listing.price, new_price))
                listing.price = new_price
                listing.save()
        scraper.__del__()

    if price_drops:
        send_email(user.email, price_drops)

def send_email(email, listings):
    subject = "Price Drop Alert!"
    message = "Here are your listings that have dropped in price!"
    for listing, old_price, new_price in listings:
        message += f"{listing.title}: was {old_price}, now {new_price}\n"

    # Specify the from_email address
    from_email = 'airfindermail@gmail.com'  # Replace with your actual sender email address

    # Send the email
    send_mail(subject, message, from_email, [email], fail_silently=False)