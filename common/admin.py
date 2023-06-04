from django.contrib import admin
from .models.country import Country
from .models.state import State
from .models.city import City
from .models.area import Area
# Register your models here.

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Area)
