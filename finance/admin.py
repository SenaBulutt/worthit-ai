from django.contrib import admin
from .models import Profile, Category, PurchaseCheck, Feedback

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(PurchaseCheck)
admin.site.register(Feedback)