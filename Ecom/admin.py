from django.contrib import admin
from .models import Product,Contact,Orders
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

admin.site.register(Contact)

admin.site.register(Orders)