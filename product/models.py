from django.db import models

# Create your models here.
from django.utils.timezone import now

from core.models import User
from product.manager import ColorManager, ProductManager, SupplierTransactionManager, SupplierManager, CustomerManger, \
    OrderManager, ProductVariantManager, SizeManager, CategoryManager, OtherCostManager, OrderedItemManager


class Size(models.Model):
    """The model of bags size"""
    size = models.CharField(max_length=100, unique=True)

    objects = SizeManager()

    def __str__(self):
        return self.size


class Category(models.Model):
    """The model of bags category"""
    category = models.CharField(max_length=100, unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.category


class Color(models.Model):
    """The model define the color of the products"""
    color = models.CharField(max_length=100, unique=True)
    objects = ColorManager()

    def __str__(self):
        return self.color


class Product(models.Model):
    """The model of bags"""
    product_name = models.CharField(max_length=100, unique=True)
    product_description = models.TextField(null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return self.product_name


class ProductVariant(models.Model):
    GSM_CHOICES = [
        (None, '----'),
        ('25 GSM', 25),
        ('30 GSM', 30),
        ('40 GSM', 40),
        ('50 GSM', 50),
        ('60 GSM', 60),
        ('70 GSM', 70),
        ('80 GSM', 80),
        ('90 GSM', 90),
        ('100 GSM', 100),
        ('110 GSM', 110)
    ]
    gsm = models.CharField(max_length=8, choices=GSM_CHOICES, null=True, blank=True)
    bag_purchase_price = models.FloatField(default=0.0)
    marketing_cost = models.FloatField(default=0.0)
    transport_cost = models.FloatField(default=0.0)
    printing_cost = models.FloatField(default=0.0)
    vat = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    discount_percent = models.IntegerField(default=0)
    discount_min_purchase = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name='product_color', on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, related_name='product_size', on_delete=models.CASCADE)
    stock_total = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name='variant', on_delete=models.CASCADE)

    objects = ProductVariantManager()

    class Meta:
        unique_together = ('size', 'product', 'category')

    # def __str__(self):
    #     return self.product.product_name


class Supplier(models.Model):
    """This model define the supplier details"""
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(unique=True, max_length=11)
    address = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.name, self.mobile_no)

    objects = SupplierManager()


class SupplierTransaction(models.Model):
    """This model define the supplier specific  details"""
    supplier = models.ForeignKey(Supplier, related_name='product_supplier', on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    total_supplied = models.IntegerField()
    per_product_purchase_price = models.FloatField(default=0.0)
    product = models.ForeignKey(ProductVariant, related_name='product_variant', on_delete=models.CASCADE)

    objects = SupplierTransactionManager()

    def __str__(self):
        return self.supplier.name


class Customer(models.Model):
    """This model store data about customer"""
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(unique=True, max_length=11)
    customer_address = models.TextField(max_length=200, null=True)

    objects = CustomerManger()

    def __str__(self):
        return str("{} ({})".format(self.customer_name, self.customer_phone))


class Order(models.Model):
    """This model store data about order"""
    customer = models.ForeignKey(Customer, related_name='order_customer', on_delete=models.CASCADE)
    sold_by = models.ForeignKey(User, related_name='order_sold_by', null=True, blank=True, on_delete=models.SET_NULL)
    ordered_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    paid_total = models.FloatField(default=0)

    objects = OrderManager()

    def __str__(self):
        return "Order No- {}".format(str(self.id))


class PaymentHistory(models.Model):
    """This model track the payment history"""
    order = models.ForeignKey(Order, related_name="payment_history", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=now)
    received_by = models.ForeignKey(User, related_name='received_by', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str('Payment No- {}'.format(self.id))


class OrderedItem(models.Model):
    """This model store products of a particular order """
    product = models.ForeignKey(ProductVariant, related_name='orderedItem_variants', on_delete=models.CASCADE)
    price_per_product = models.FloatField(default=0.0)
    profit_per_product = models.FloatField(default=0.0)
    discount_percent = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)
    objects = OrderedItemManager()

    def __str__(self):
        return "Item No- {}".format(self.id)


class OtherCost(models.Model):
    """This model store the other cost of the host"""
    date = models.DateField(default=now)
    shop_rent = models.FloatField(default=0.0)
    shop_rent_per_product = models.FloatField(default=0.0)
    electricity_bill = models.FloatField(default=0.0)
    electricity_bill_per_product = models.FloatField(default=0.0)
    employee_cost = models.FloatField(default=0.0)
    employee_cost_per_product = models.FloatField(default=0.0)
    others_bill = models.FloatField(default=0.0)
    others_bill_per_product = models.FloatField(default=0.0)

    objects = OtherCostManager()