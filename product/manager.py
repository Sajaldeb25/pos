from decimal import *

from django.core.exceptions import ValidationError
from django.db import models, DatabaseError, transaction
from django.db.models import Prefetch, F, When, Q, Value, Case, FloatField, QuerySet, ExpressionWrapper, Sum, Avg, \
    Count, IntegerField, Func
from django.db.models.functions import Coalesce, Round
from django.utils.timezone import now, localtime


class ColorManager(models.Manager):
    def create(self, **kwargs):
        """Create new color"""
        if 'color' not in kwargs:
            raise ValueError('Please input a color')
        kwargs['color'] = kwargs['color'].capitalize()
        color = self.model(**kwargs)
        color.save(using=self.db)
        return color

    @transaction.atomic
    def update_color(self, id, new_color):
        try:
            old_color = self.model.objects.get(id=id)
            old_color.color = new_color.capitalize()
            old_color.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError('Error updating color')
        return True

    def delete_color(self, id):
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError("Error occurred while deleting color")
        return True


class SizeManager(models.Manager):
    @transaction.atomic
    def delete_size(self, id):
        from product.models import ProductVariant
        from product.models import OrderedItem
        will_delete_size = self.filter(id=id).prefetch_related(
            Prefetch(
                'product_size',
                queryset=ProductVariant.objects.prefetch_related(
                    Prefetch(
                        'orderedItem_variants',
                        queryset=OrderedItem.objects.select_related('order'),
                        to_attr='orders_item'
                    )
                ),
                to_attr='variants'
            )
        ).first()
        orders = [item.order for variant in will_delete_size.variants for item in variant.orders_item]
        variants_id = [variant.id for variant in will_delete_size.variants]
        try:
            will_delete_size.delete()
        except DatabaseError as e:
            raise DatabaseError("Error occurred while deleting size")
        for order in orders:
            try:
                order.delete()
            except DatabaseError as e:
                raise DatabaseError("Technical problem to delete size")
        return variants_id

    @transaction.atomic
    def update_size(self, id, new_size):
        try:
            old_size = self.model.objects.get(id=id)
            old_size.size = new_size
            old_size.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError('Error updating size')
        return True


class CategoryManager(models.Manager):
    @transaction.atomic
    def delete_category(self, id):
        from product.models import ProductVariant
        from product.models import OrderedItem
        will_delete_category = self.filter(id=id).prefetch_related(
            Prefetch(
                'product_category',
                queryset=ProductVariant.objects.prefetch_related(
                    Prefetch(
                        'orderedItem_variants',
                        queryset=OrderedItem.objects.select_related('order'),
                        to_attr='orders_item'
                    )
                ),
                to_attr='variants'
            )
        ).first()
        orders = [item.order for variant in will_delete_category.variants for item in variant.orders_item]
        variants_id = [variant.id for variant in will_delete_category.variants]
        try:
            will_delete_category.delete()
        except DatabaseError as e:
            raise DatabaseError("Error occurred while deleting size")
        for order in orders:
            try:
                order.delete()
            except DatabaseError as e:
                raise DatabaseError("Technical problem to delete size")
        return variants_id

    @transaction.atomic
    def update_category(self, id, new_category):
        try:
            old_category = self.model.objects.get(id=id)
            old_category.category = new_category
            old_category.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError('Error updating category')
        return True


class ProductManager(models.Manager):
    def get_all_product(self):
        from product.models import ProductVariant
        from product.models import OrderedItem
        from product.models import OtherCost
        other_price = OtherCost.objects.current_month_bill()
        data = self.prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category').prefetch_related(
                         'orderedItem_variants',
                     )
                     .annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                                     + F('transport_cost') + F('profit') + Value(other_price['others_bill'],
                                                                                 output_field=FloatField())).annotate(
                         total_order=Count('orderedItem_variants')).order_by('-stock_total'),
                     to_attr="product_variant")) \
            .annotate(total_stock=Coalesce(Sum('variant__stock_total'), Value(0))).order_by('-total_stock')
        return data

    def get_all_product_stock_filter(self):

        from product.models import ProductVariant
        from product.models import OtherCost
        other_price = OtherCost.objects.current_month_bill()
        return self.prefetch_related(
            Prefetch("variant",
                     queryset=ProductVariant.objects.select_related('color', 'size', 'category')
                     .annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                                     + F('transport_cost') + F('profit') + Value(other_price['others_bill'],
                                                                                 output_field=FloatField())).filter(
                         stock_total__gt=0).order_by('id'),
                     to_attr="product_variant")) \
            .annotate(total_stock=Sum('variant__stock_total'))

    def get_product_details(self, id):
        from product.models import ProductVariant
        from product.models import OtherCost
        other_price = OtherCost.objects.current_month_bill()
        data = self.filter(id=id).prefetch_related(
            Prefetch(
                'variant',
                queryset=ProductVariant.objects.select_related('color', 'size', 'category').annotate(
                    price=F('bag_purchase_price') + F('marketing_cost') + F('transport_cost') + F('printing_cost') + F(
                        'vat') + F('profit') + Value(other_price['others_bill'],
                                                     output_field=FloatField())),
                to_attr='variants'
            )
        ).first()
        return data

    @transaction.atomic
    def create_product(self, **fields):
        if 'new_product' in fields:
            product = self.model(**fields['new_product'])
            try:
                product.save(using=self._db)
            except DatabaseError as e:
                raise DatabaseError(e)

            fields['product'] = product
            del fields['new_product']

        if 'new_color' in fields:
            from product.models import Color
            color = Color.objects.create(color=fields['new_color'])
            fields['color'] = color
            del fields['new_color']

        if 'new_size' in fields:
            from product.models import Size
            size = Size.objects.create(size=fields['new_size'])
            fields['size'] = size
            del fields['new_size']

        if 'new_category' in fields:
            from product.models import Category
            category = Category.objects.create(category=fields['new_category'])
            fields['category'] = category
            del fields['new_category']

        if 'product' in fields:
            keys = [
                'product',
                'size',
                'category',
                'marketing_cost',
                'vat',
                'profit',
                'stock_total',
                'transport_cost',
                'bag_purchase_price'
            ]
        if 'supplier' not in fields or not fields['supplier']:
            raise ValueError("Supplier field can't be empty.")

        if all(key in fields and fields[key] for key in keys):
            from product.models import ProductVariant
            supplier = fields['supplier']
            del fields['supplier']
            product = ProductVariant(**fields)
            product.save(using=self.db)
            from product.models import SupplierTransaction
            supplier = SupplierTransaction(supplier=supplier, product=product, total_supplied=fields['stock_total'],
                                           per_product_purchase_price=fields['bag_purchase_price'])
            supplier.save(using=self.db)
            return product
        else:
            raise ValueError(
                'Product name, size, category, marketing cost, vat, bag purchase price, transport cost, '
                'stock total, profit can\t be empty')

    def update_product(self, id, data):
        old_product = self.get(id=id)
        old_product.product_name = data['product_name']
        old_product.product_description = data['product_description']
        try:
            old_product.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical problem updating product")
        return old_product

    @transaction.atomic
    def delete_product(self, id):
        try:
            product = self.model.objects.get(id=id)
            from product.models import Order
            orders = Order.objects.prefetch_related('ordered_items').filter(ordered_items__product__product=product)
            for order in orders:
                try:
                    order.delete()
                except DatabaseError as e:
                    raise DatabaseError("Technical problem to delete product")
            product.delete()

        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete product")

        return True


class ProductVariantManager(models.Manager):
    def get_product_variant_details(self, id):
        from product.models import SupplierTransaction
        from product.models import OtherCost
        other_price = OtherCost.objects.current_month_bill()
        data = self.filter(id=id).select_related('size', 'color', 'category', 'product') \
            .prefetch_related(
            Prefetch('product_variant',
                     queryset=SupplierTransaction.objects.select_related('supplier').annotate(
                         total_purchase_price=ExpressionWrapper(F('total_supplied') * F('per_product_purchase_price'),
                                                                output_field=FloatField())
                     ).order_by('-date'),
                     to_attr='supplier_list'
                     )

        ).annotate(price=F('bag_purchase_price') + F('marketing_cost') + F('vat') + F('printing_cost')
                         + F('transport_cost') + F('profit') + Value(other_price['others_bill'],
                                                                     output_field=FloatField())).first()
        return data

    def net_stock(self):
        data = self.aggregate(net_stock=Sum(F('stock_total')))
        return data

    @transaction.atomic
    def update_variant(self, id, form_data):
        old_variant = self.get(id=id)
        for key, value in form_data.items():
            setattr(old_variant, key, value)

        try:
            old_variant.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("In updating variant there is database technical problem.")
        return old_variant

    @transaction.atomic
    def add_new_stock(self, id, form_data):
        old_variant = self.model.objects.get(id=id)
        old_variant.stock_total = old_variant.stock_total + form_data['new_stock']
        from product.models import SupplierTransaction
        try:
            old_variant.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Adding new stock problem in database")
        try:
            supplier = SupplierTransaction(supplier=form_data['supplier'], product=old_variant,
                                           total_supplied=form_data['new_stock'],
                                           per_product_purchase_price=form_data['per_product_purchase_price'])
            supplier.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Adding supplier info problem in database")
        return supplier

    @transaction.atomic
    def delete_variant(self, id):
        if id is None:
            raise ValueError("Id is required")
        try:
            from product.models import OrderedItem
            variant = self.model.objects.get(id=id)
            from product.models import Order
            orders = Order.objects.prefetch_related('ordered_items').filter(ordered_items__product=variant)
            for order in orders:
                try:
                    order.delete()
                except DatabaseError as e:
                    raise DatabaseError("Technical problem to delete variant")
            variant.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete variant")
        return True


class SupplierManager(models.Manager):
    def get_all_supplier(self):
        data = self.prefetch_related('product_supplier') \
            .annotate(
            total_supplied=Coalesce(Sum('product_supplier__total_supplied'), Value(0)),
            total_price=Sum(F('product_supplier__total_supplied') * F('product_supplier__per_product_purchase_price'),
                            output_field=FloatField())
        ).order_by(
            '-total_supplied')
        return data

    def get_supplier_details(self, id):
        from product.models import SupplierTransaction
        data = self.filter(id=id).prefetch_related(
            Prefetch('product_supplier',
                     queryset=SupplierTransaction.objects.select_related(
                         'product', 'product__size', 'product__color', 'product__category',
                         'product__product').annotate(
                         total_price=ExpressionWrapper(F('per_product_purchase_price') * F('total_supplied'),
                                                       output_field=FloatField())).order_by('-date'),
                     to_attr='product_list')).first()
        return data

    @transaction.atomic
    def update_supplier(self, id, data):
        if not id or not data:
            raise ValueError('This field is required')

        if all(key in data and data[key] for key in ['name', 'mobile_no', 'address']):
            try:
                old_supplier = self.model.objects.get(id=id)
                old_supplier.name = data['name']
                old_supplier.mobile_no = data['mobile_no']
                old_supplier.address = data['address']
                old_supplier.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError("Database technical problem")
        else:
            raise ValueError("name, mobile_no, address are required.")

        return old_supplier

    @transaction.atomic
    def delete_supplier(self, id):
        if id is None:
            raise ValueError('Supplier id is required')
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError('Technical problem occurred while deleting supplier')
        return True


class SupplierTransactionManager(models.Manager):
    def get_all_supplier(self):
        data = self.all()
        return data


class CustomerManger(models.Manager):
    def get_all_customer(self):
        data = self.prefetch_related('order_customer', 'order_customer__ordered_items') \
            .annotate(
            total_paid=Coalesce(Sum(F('order_customer__paid_total'), output_field=FloatField()), Value(0)),
            total_billed=Coalesce(Sum(
                F('order_customer__ordered_items__quantity') * F('order_customer__ordered_items__price_per_product') *
                (Value(1) - F('order_customer__ordered_items__discount_percent') / 100.00), output_field=FloatField()),
                Value(0)),
            total_item=Coalesce(Sum(F('order_customer__ordered_items__quantity')), Value(0))
        ).annotate(total_due=Coalesce(F('total_billed') - F('total_paid'), Value(0))).order_by('-total_due',
                                                                                               '-total_item')

        return data

    def get_customer_details(self, id):
        from product.models import Order
        from product.models import PaymentHistory
        data = self.filter(id=id).prefetch_related(
            Prefetch(
                'order_customer',
                queryset=Order.objects.prefetch_related('ordered_items', Prefetch(
                    'payment_history',
                    queryset=PaymentHistory.objects.select_related('received_by').order_by('-date'),
                    to_attr='payments')).select_related('sold_by').annotate(
                    billed=Sum(
                        (F('ordered_items__quantity') * F(
                            'ordered_items__price_per_product')) *
                        (Value(1) - F('ordered_items__discount_percent') / 100.00),
                        output_field=FloatField()
                    ),
                    items=Count('ordered_items')

                ).annotate(
                    due=ExpressionWrapper(F('billed') - F('paid_total'), output_field=FloatField())
                ).order_by('-due', '-items'),
                to_attr='orders'
            )
        ) \
            .annotate(
            total_paid=Coalesce(Sum(F('order_customer__paid_total'), output_field=FloatField()), Value(0)),
            total_billed=Coalesce(Sum(
                F('order_customer__ordered_items__quantity') * F('order_customer__ordered_items__price_per_product') *
                (Value(1) - F('order_customer__ordered_items__discount_percent') / 100.00), output_field=FloatField()),
                Value(0)),
            total_item=Coalesce(Sum(F('order_customer__ordered_items__quantity')), Value(0))
        ).annotate(total_due=Coalesce(F('total_billed') - F('total_paid'), Value(0))).first()

        return data

    @transaction.atomic
    def update_customer_details(self, id, data):
        customer_info = self.get(id=id)
        customer_info.customer_name = data['customer_name']
        customer_info.customer_phone = data['customer_phone']
        customer_info.customer_address = data['customer_address']
        try:
            customer_info.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Technical problem occurred during updating customer")
        return True

    @transaction.atomic
    def delete_customer(self, id):
        if id is None:
            raise ValueError('Customer id is required')
        try:
            self.model.objects.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError('Technical problem occurred while deleting customer')
        return True


class OrderManager(models.Manager):
    def net_order(self):
        data = self.prefetch_related('ordered_items').annotate(
            due=Case(
                When(is_paid=False,
                     then=Sum((F('ordered_items__quantity')
                               * F('ordered_items__price_per_product'))
                              * (Value(1) - (F('ordered_items__discount_percent') / 100.00))
                              ) - F('paid_total')),
                default=Value(0),
                output_field=FloatField()
            )
        ).aggregate(
            net_order=Count(F('id')),
            full_paid_order=Count(Case(When(is_paid=True, then=1), output_field=IntegerField())),
            semi_paid_order=Count(
                Case(When(is_paid=False, then=1), output_field=IntegerField())),
            total_due=Sum(F('due'))
        )

        return data

    def order_statistics_month(self, month=localtime(now()).month, year=localtime(now()).year):
        data = self.model.objects.filter(ordered_date__month=month, ordered_date__year=year).values(
            'ordered_date__day').annotate(
            total_order=Count('id')
        ).order_by('ordered_date__day')
        return data

    def get_all_order(self):
        data = self.prefetch_related('ordered_items').select_related('customer', 'sold_by') \
            .annotate(total_item=Coalesce(Sum('ordered_items__quantity'), Value(0)),
                      total_billed=Coalesce(Sum(
                          (F('ordered_items__quantity') * F('ordered_items__price_per_product'))
                          * (Value(1) - (F('ordered_items__discount_percent') / 100.00)),
                          output_field=FloatField()), Value(0)),
                      ).annotate(
            total_due=Case(
                When(is_paid=False,
                     then=Sum((F('ordered_items__quantity')
                               * F('ordered_items__price_per_product'))
                              * (Value(1) - (F('ordered_items__discount_percent') / 100.00))
                              ) - F('paid_total')),
                default=Value(0),
                output_field=FloatField()
            )).annotate(total_paid=Coalesce(F('total_billed') - F('total_due'), Value(0))).order_by('-total_due')
        return data

    def get_order_detail(self, order_id):
        from product.models import OrderedItem
        from product.models import PaymentHistory
        data = self.filter(pk=order_id).prefetch_related(
            Prefetch('ordered_items',
                     queryset=OrderedItem.objects.annotate(
                         sub_total=ExpressionWrapper(F('quantity') * F('price_per_product') * (
                                 Value(1) - (F('discount_percent') / 100.00)), output_field=FloatField()))
                     .select_related('product', 'product__product', 'product__category', 'product__color',
                                     'product__size'),
                     to_attr='items'
                     ),
            Prefetch('payment_history',
                     queryset=PaymentHistory.objects.select_related('received_by').order_by('-date'),
                     to_attr='order_payment_history'
                     )
        ).select_related(
            'customer', 'sold_by') \
            .annotate(
            total_item=Coalesce(Sum('ordered_items__quantity'), Value(0)),
            total_billed=Coalesce(Sum(
                (F('ordered_items__quantity') * F('ordered_items__price_per_product'))
                * (Value(1) - (F('ordered_items__discount_percent') / 100.00)),
                output_field=FloatField()), Value(0)),
        ).annotate(
            total_due=Case(
                When(is_paid=False,
                     then=Sum((F('ordered_items__quantity')
                               * F('ordered_items__price_per_product'))
                              * (Value(1) - (F('ordered_items__discount_percent') / 100.00))
                              ) - F('paid_total')),
                default=Value(0),
                output_field=FloatField()
            )).first()
        return data

    @transaction.atomic
    def crate_new_order(self, order=None, items=None):
        if not order or not items:
            raise ValueError("Order && items are missing")
        """Save the new customer"""
        if 'customer' not in order:
            new_customer_data = {
                'customer_name': order['customer_name'],
                'customer_phone': order['customer_phone'],
                'customer_address': order['customer_address']
            }
            del order['customer_name'],
            del order['customer_phone'],
            del order['customer_address']
            from product.models import Customer
            try:
                new_customer = Customer(**new_customer_data)
                new_customer.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError(e)
            order['customer'] = new_customer

        """Save the new order"""
        try:
            total_billed = 0
            for item in items:
                total_billed += item['price_per_product'] * item['quantity'] * (1 - (item['discount_percent'] / 100.0))
            if round(total_billed, 2) == round(order['paid_total'], 2):
                order['is_paid'] = True
            new_order = self.model(**order)
            new_order.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        from product.models import OrderedItem
        from product.models import ProductVariant
        """Save the paid total as history"""
        if order['paid_total'] is not 0 or order['paid_total']:
            try:
                from product.models import PaymentHistory
                new_payment = PaymentHistory(order=new_order, amount=order['paid_total'], received_by=order['sold_by'])
                new_payment.save(using=self.db)
            except DatabaseError as e:
                raise DatabaseError("Database technical issue")
        """Save the items of the order"""
        try:
            new_item_queryset = list(ProductVariant.objects.filter(id__in=[i['product'] for i in items]))
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")
        new_item_list = [OrderedItem(
            product=new_item_queryset[i],
            price_per_product=items[i]['price_per_product'],
            discount_percent=items[i]['discount_percent'],
            profit_per_product=new_item_queryset[i].profit,
            quantity=items[i]['quantity'],
            order=new_order
        ) for i in range(len(items))]

        try:
            OrderedItem.objects.bulk_create(new_item_list)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        """Update the stock of the items"""
        for i in range(len(items)):
            new_stock = new_item_queryset[i].stock_total - items[i]['quantity']
            new_item_queryset[i].stock_total = new_stock if new_stock >= 0 else 0

        try:
            ProductVariant.objects.bulk_update(new_item_queryset, ['stock_total'])
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        return new_order

    @transaction.atomic
    def make_payment(self, order_id, amount, received_by):
        """This method is responsible for add new payment to payment history"""
        if not order_id or not amount or not received_by:
            raise ValueError("All field is required")
        order = self.filter(id=order_id).prefetch_related('ordered_items').annotate(
            total_billed=Sum(
                (F('ordered_items__quantity') * F('ordered_items__price_per_product'))
                * (Value(1) - (F('ordered_items__discount_percent') / 100.00)),
                output_field=FloatField()),
        ).first()
        order.paid_total = order.paid_total + float(amount)
        if round(order.paid_total, 2) == round(order.total_billed, 2):
            order.is_paid = True
        try:
            order.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")

        try:
            from product.models import PaymentHistory
            new_payment = PaymentHistory(order=order, amount=amount, received_by=received_by)
            new_payment.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Database technical issue")
        return new_payment

    @transaction.atomic
    def delete_order(self, id):
        if id is None:
            raise ValueError("Id is required")
        try:
            from product.models import OrderedItem
            order = self.filter(id=id).prefetch_related(
                Prefetch(
                    'ordered_items',
                    queryset=OrderedItem.objects.select_related('product'),
                    to_attr='items'
                )
            ).first()
            product_variant = []
            for item in order.items:
                item.product.stock_total = item.product.stock_total + item.quantity
                product_variant.append(item.product)
            from product.models import ProductVariant
            ProductVariant.objects.bulk_update(product_variant, ['stock_total'])
            order.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete order")
        return True

    @transaction.atomic
    def delete_payment(self, id):
        if id is None:
            raise ValueError("Id is required")
        try:
            from product.models import PaymentHistory
            payment = PaymentHistory.objects.get(id=id)
            order = payment.order
            order.paid_total = order.paid_total - payment.amount
            order.save(using=self.db)
            payment.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to delete order")
        return True

    @transaction.atomic
    def delete_ordered_item(self, id):
        if id is None:
            raise ValueError("Item Id is required")
        try:
            from product.models import OrderedItem
            item = OrderedItem.objects.get(id=id)
            if OrderedItem.objects.filter(order=item.order).count() <= 1:
                raise ValidationError('This order can not be deleted as a order need at least 1 item.')
            product_variant = item.product
            product_variant.stock_total = product_variant.stock_total + item.quantity
            product_variant.save(using=self.db)
            item.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem raised while deleting item")
        return True


class OrderedItemManager(models.Manager):
    def net_sold_item(self):
        data = self.aggregate(net_sold_item=Sum(F('quantity'), output_field=IntegerField()))
        return data

    def calculate_net_profit_and_revenue(self):
        data = self.aggregate(
            net_profit=Sum(F('profit_per_product') * F('quantity') - (
                    F('price_per_product') * F('quantity') * F('discount_percent') / 100.0),
                           output_field=FloatField()),
            net_revenue=Sum(F('price_per_product') * F('quantity') * (Value(1) - (F('discount_percent') / 100.0)),
                            output_field=FloatField())
        )
        return data

    def calculate_net_profit_and_revenue_current_month(self, present_month=localtime(now()).month,
                                                       present_year=localtime(now()).year):
        data = self.select_related('order').filter(order__ordered_date__month=present_month,
                                                                 order__ordered_date__year=present_year).values(
            'order__ordered_date__day').annotate(
            total_item=Coalesce(Sum('quantity'), Value(0)),
            net_profit=Sum(F('profit_per_product') * F('quantity') - (
                    F('price_per_product') * F('quantity') * F('discount_percent') / 100.0),
                           output_field=FloatField()),
            net_revenue=Sum(F('price_per_product') * F('quantity') * (Value(1) - (F('discount_percent') / 100.0)),
                            output_field=FloatField())
        ).order_by('order__ordered_date__day')
        return data

    def calculate_profit_revenue_all_month(self):
        data = self.select_related('order').values('order__ordered_date__year',
                                                                 'order__ordered_date__month').annotate(
            total_item=Coalesce(Sum('quantity'), Value(0)),
            net_profit=Sum(F('profit_per_product') * F('quantity') - (
                    F('price_per_product') * F('quantity') * F('discount_percent') / 100.0),
                           output_field=FloatField()),
            net_revenue=Sum(F('price_per_product') * F('quantity') * (Value(1) - (F('discount_percent') / 100.0)),
                            output_field=FloatField())
        ).order_by('-order__ordered_date__year', '-order__ordered_date__month')
        return data


class OtherCostManager(models.Manager):
    def current_month_bill(self):
        current_month = now().month
        current_year = now().year
        data = self.filter(date__month=current_month, date__year=current_year).aggregate(
            others_bill=Coalesce(Sum(
                F('shop_rent_per_product') + F('electricity_bill_per_product') + F('others_bill_per_product') + F(
                    'employee_cost_per_product'),
                output_field=FloatField()), Value(0, output_field=FloatField())))
        return data

    def delete_utility_bill(self, id):
        try:
            self.get(id=id).delete()
        except DatabaseError as e:
            raise DatabaseError('Error occurred while deleting utility bill')

        return True

    def update_utility_bill(self, id, data):
        try:
            old_data = self.get(id=id)
            old_data.shop_rent = data['shop_rent']
            old_data.shop_rent_per_product = data['shop_rent_per_product']
            old_data.electricity_bill = data['electricity_bill']
            old_data.electricity_bill_per_product = data['electricity_bill_per_product']
            old_data.others_bill = data['others_bill']
            old_data.others_bill_per_product = data['others_bill_per_product']
            old_data.employee_cost = data['employee_cost']
            old_data.employee_cost_per_product = data['employee_cost_per_product']
            old_data.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError('Error occurred while updating utility bill')
        return True
