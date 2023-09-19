from django.contrib import admin
from .models.country import Country
from .models.state import State
from .models.city import City
from .models.area import Area
from .models.degree import Degree
from .models.gender import Gender
from .models.zip_address import ZipAddress
# Register your models here.

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Degree)
admin.site.register(Gender)
admin.site.register(ZipAddress)
