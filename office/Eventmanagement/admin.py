from django.contrib import admin

# Register your models here.

from .models import EventDetails ,EventProduct,temporaryaddeventdb

admin.site.register(EventDetails)
admin.site.register(EventProduct)
admin.site.register(temporaryaddeventdb)