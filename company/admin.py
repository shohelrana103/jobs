from django.contrib import admin
from .models.company import Company
from .models.industry import Industry


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_contact_number', 'company_address_line_1',
                     'contact_person_name']
    # list_display_links = None
    # list_editable = ['quantity', 'description', 'tax_rate', ]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Industry)
