from django.contrib import admin
from .models import Listing
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
# Define an inline admin descriptor for the liked listings which acts a bit like a singleton
class LikedListingsInline(admin.TabularInline):
    model = Listing.liked_by.through  # This accesses the through model of the ManyToMany relationship
    extra = 1  # How many rows to show

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (LikedListingsInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Listing)
