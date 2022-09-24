from django.contrib import admin
from index.models import *

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'brand', 'category', 'price')

admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Payment)
admin.site.register(PaymentType)