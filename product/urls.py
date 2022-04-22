from django.urls import path

from product import views

app_name = 'product'
urlpatterns = [
    path('variant_list/', views.VariantList.as_view(), name='variant_list'),
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('new_product/', views.AddNewProduct.as_view(), name='new_product'),
    path('supplier_list/', views.SupplierList.as_view(), name='supplier_list'),
    path('new_supplier/', views.AddNewSupplier.as_view(), name='new_supplier'),
    path('customer_list/', views.CustomerList.as_view(), name='customer_list'),
    path('customer_details/<int:customer_id>/', views.CustomerDetails.as_view(), name='customer_details'),
    path('order_list/', views.OrderList.as_view(), name='order_list'),
    path('create_invoice/', views.CreateInvoice.as_view(), name='create_invoice'),
    path('order_details/<int:order_id>/', views.OrderDetail.as_view(), name='order_details'),
    path('supplier_details/<int:supplier_id>/', views.SupplierDetail.as_view(), name='supplier_details'),
    path('variant_details/<int:variant_id>/', views.VariantDetails.as_view(), name='variant_details'),
    path('product_details/<int:product_id>/', views.ProductDetails.as_view(), name='product_details'),
    path('other_cost/', views.UtilityBill.as_view(), name='other_cost'),
]
