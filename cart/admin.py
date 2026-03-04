from django.contrib import admin
from .models import CartItem, BookPricing

@admin.register(BookPricing)
class BookPricingAdmin(admin.ModelAdmin):
    list_display = ('livre', 'base_price', 'discount_percent', 'final_price',
    'is_on_sale', 'discount_start', 'discount_end')
    list_filter = ('discount_percent',)
    search_fields = ('livre__titre',)

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ('livre', 'user', 'quantity', 'unit_price', 'subtotal',
    'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('livre__titre', 'user__username')
