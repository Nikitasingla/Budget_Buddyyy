from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Stock, CartItem


admin.site.register(Stock)
admin.site.register(CartItem)
# @admin.site.register(Stock)
# class StockAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'image_url')
#     search_fields = ('name',)

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('stock', 'quantity', 'get_total_price')
#     readonly_fields = ('get_total_price',)

#     def get_total_price(self, obj):
#         return obj.get_total_price()
#     get_total_price.short_description = 'Total Price'
