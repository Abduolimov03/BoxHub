from django.contrib import admin

from apps.models import Category, Product, CoffeeAndTea, Settings, CoffeeSize, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_in", "price_out")
    list_filter = ("category",)
    search_fields = ("name", "category__name")


admin.site.register(CoffeeAndTea)
admin.site.register(CoffeeSize)
admin.site.register(Settings)

admin.site.site_header = "Jzr Coffee"
admin.site.site_title = "Jzr Coffee Admin"
admin.site.index_title = "Jzr Coffee Dashboard"
admin.site.register(Order)
admin.site.register(OrderItem)
