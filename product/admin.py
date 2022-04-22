from django.contrib import admin
from product import models
# from product.models import Quantity


class ProductVariantAdmin(admin.StackedInline):
    model = models.ProductVariant
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_description']
    inlines = (ProductVariantAdmin,)


class SupplierTransactionAdmin(admin.TabularInline):
    model = models.SupplierTransaction
    extra = 1


class SupplierAdmin(admin.ModelAdmin):
    inlines = (SupplierTransactionAdmin,)


class OrderedItemAdmin(admin.TabularInline):
    model = models.OrderedItem
    extra = 1


class PaymentHistoryAdmin(admin.TabularInline):
    model = models.PaymentHistory
    extra = 1


class OrderedAdmin(admin.ModelAdmin):
    inlines = (OrderedItemAdmin, PaymentHistoryAdmin)


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Order, OrderedAdmin)
