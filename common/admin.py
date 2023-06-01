from django.contrib import admin
from .models.country import Country
from .models.state import State
from .models.city import City

# Register your models here.

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
