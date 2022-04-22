import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Prefetch
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

# from product.models import ProductTransaction
from django.views.generic import FormView, TemplateView

from product.forms import AddNewProductForm, AddNewSupplierForm, OrderForm, ItemForm, BaseItemFormSet, ProductForm, \
    VariantForm, NewStockForm, CustomerForm, OtherCostForm
from product.models import Product, Supplier, Customer, Order, ProductVariant, Size, Color, Category, OtherCost
from scripts.pos_invoice_genarator import generate_pos_invoice


class ProductList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_product', 'product.view_productvariant')
    template_name = 'product/product_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Product.objects.get_all_product()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            if not self.request.user.has_perm('product.delete_product'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            id = request.POST['product_id']
            if id:
                if Product.objects.delete_product(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class ProductDetails(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_product', 'product.view_productvariant')
    template_name = 'product/product_details.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        product_id = kwargs['product_id']
        product_details = Product.objects.get_product_details(product_id)
        product_edit_form = ProductForm(initial={
            'product_name': product_details.product_name,
            'product_description': product_details.product_description
        })
        if self.request.user.has_perm('product.change_product'):
            kwargs['product_form'] = product_edit_form
        kwargs['product_details'] = product_details
        return super().get_context_data(**kwargs)

    def post(self, request, product_id):
        if 'variant_id' in request.POST and request.POST['variant_id']:
            if not self.request.user.has_perm('product.delete_product'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            variant_id = request.POST['variant_id']
            if ProductVariant.objects.delete_variant(variant_id):
                return JsonResponse("success", status=201, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)
        else:
            if not self.request.user.has_perm('product.change_product'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            form = ProductForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                Product.objects.update_product(product_id, cleaned_data)
                return JsonResponse("success", status=201, safe=False)
            else:
                return JsonResponse(form.errors, status=400)


class VariantList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_product', 'product.view_productvariant')
    template_name = 'product/variant_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['product_list'] = Product.objects.get_all_product()
        kwargs['sizes'] = Size.objects.all()
        kwargs['colors'] = Color.objects.all()
        kwargs['categories'] = Category.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            data = request.POST

            def check_is_edited():
                if 'is_edited' not in data or not data['is_edited']:
                    return JsonResponse({'error': 'is_edited field is required'}, status=400, safe=False)
                if 'id' not in data or not data['id']:
                    return JsonResponse({'error': 'id field is required'}, status=400, safe=False)
                return True

            if 'variant_id' in data and data['variant_id']:
                if not self.request.user.has_perm('product.delete_productvariant'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                id = data['variant_id']
                if ProductVariant.objects.delete_variant(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif 'size' in data and data['size']:
                if not self.request.user.has_perm('product.change_size'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if check_is_edited():
                    if data['is_edited'] == '0':
                        if Size.objects.filter(size__iexact=data['size']).count() > 0:
                            return JsonResponse({'error': 'This size is already exist'}, status=400, safe=False)
                    if Size.objects.update_size(data['id'], data['size']):
                        return JsonResponse('success', status=200, safe=False)

            elif 'color' in data and data['color']:
                if not self.request.user.has_perm('product.change_color'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if check_is_edited():
                    if data['is_edited'] == '0':
                        if Color.objects.filter(color__iexact=data['color']).count() > 0:
                            return JsonResponse({'error': 'This color is already exist'}, status=400, safe=False)
                    if Color.objects.update_color(data['id'], data['color']):
                        return JsonResponse('success', status=200, safe=False)
            elif 'category' in data and data['category']:
                if not self.request.user.has_perm('product.change_category'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if check_is_edited():
                    if data['is_edited'] == '0':
                        if Category.objects.filter(category__iexact=data['category']).count() > 0:
                            return JsonResponse({'error': 'This category is already exist'}, status=400, safe=False)
                    if Category.objects.update_category(data['id'], data['category']):
                        return JsonResponse('success', status=200, safe=False)
            elif 'size_id' in data and data['size_id']:
                if not self.request.user.has_perm('product.delete_size'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                id = data['size_id']
                variants = Size.objects.delete_size(id)
                return JsonResponse(variants, status=200, safe=False)
            elif 'color_id' in data and data['color_id']:
                if not self.request.user.has_perm('product.delete_color'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                id = data['color_id']
                if Color.objects.delete_color(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif 'category_id' in data and data['category_id']:
                if not self.request.user.has_perm('product.delete_category'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                id = data['category_id']
                variants = Category.objects.delete_category(id)
                return JsonResponse(variants, status=200, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class VariantDetails(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_product', 'product.view_productvariant')
    template_name = 'product/variant_details.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        variant_id = kwargs['variant_id']
        variant_details = ProductVariant.objects.get_product_variant_details(variant_id)
        if self.request.user.has_perm('product.change_product') and self.request.user.has_perm(
                'product.change_productvariant'):
            product_edit_form = ProductForm(initial={
                'product_name': variant_details.product.product_name,
                'product_description': variant_details.product.product_description
            })
            variant_edit_form = VariantForm(initial={
                'product': variant_details.product,
                'new_product_name': variant_details.product.product_name,
                'product_description': variant_details.product.product_description,
                'gsm': variant_details.gsm,
                'color': variant_details.color,
                'size': variant_details.size,
                'category': variant_details.category,
                'bag_purchase_price': variant_details.bag_purchase_price,
                'marketing_cost': variant_details.marketing_cost,
                'transport_cost': variant_details.transport_cost,
                'printing_cost': variant_details.printing_cost,
                'vat': variant_details.vat,
                'profit': variant_details.profit,
                'discount_percent': variant_details.discount_percent,
                'discount_min_purchase': variant_details.discount_min_purchase,
                'stock_total': variant_details.stock_total
            })
            kwargs['product_form'] = product_edit_form
            kwargs['variant_form'] = variant_edit_form
            kwargs['new_stock_form'] = NewStockForm()
        kwargs['variant_details'] = variant_details
        return super().get_context_data(**kwargs)

    def post(self, request, variant_id):
        if request.is_ajax():
            data = request.POST
            if 'is_product_edited' in data and data['is_product_edited']:
                if not self.request.user.has_perm('product.change_product'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                form = ProductForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    Product.objects.update_product(data['id'], cleaned_data)
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse(form.errors, status=400)
            elif 'is_variant_edited' in data and data['is_variant_edited']:
                if not self.request.user.has_perm('product.change_productvariant'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                form = VariantForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    ProductVariant.objects.update_variant(variant_id, cleaned_data)
                    return JsonResponse("success", status=201, safe=False)
                else:
                    return JsonResponse(form.errors, status=400)
            else:
                if not self.request.user.has_perm('product.change_product') and self.request.user.has_perm(
                        'product.change_productvariant'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                form = NewStockForm(data)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    supplier = ProductVariant.objects.add_new_stock(id=variant_id, form_data=cleaned_data)
                    date = datetime.strftime(supplier.date, '%d/%m/%Y %I:%M %p')
                    return JsonResponse({'date': date, 'name': cleaned_data['supplier'].name,
                                         'mobile_no': cleaned_data['supplier'].mobile_no,
                                         'total_supplied': supplier.total_supplied,
                                         'per_product_purchase_price': supplier.per_product_purchase_price,
                                         'address': cleaned_data['supplier'].address}, status=201)
                else:
                    return JsonResponse(form.errors, status=400)


class AddNewProduct(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ('product.add_product', 'product.add_productvariant')
    template_name = 'product/create_product.html'
    form_class = AddNewProductForm

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def form_valid(self, form):
        clean_form = form.cleaned_data
        Product.objects.create_product(**clean_form)
        return redirect('product:variant_list')


class SupplierList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_supplier',)
    template_name = 'product/supplier_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['supplier_list'] = Supplier.objects.get_all_supplier()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            id = request.POST['supplier_id']
            if id:
                if not self.request.user.has_perm('product.delete_supplier'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if Supplier.objects.delete_supplier(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class AddNewSupplier(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = ('product.add_supplier',)
    template_name = 'product/create_supplier.html'
    form_class = AddNewSupplierForm

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def form_valid(self, form):
        # clean_form = form.cleaned_data
        supplier = form.save()
        return redirect('product:supplier_list')


class SupplierDetail(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_supplier', 'product.change_supplier')
    template_name = 'product/supplier_details.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        supplier_id = kwargs['supplier_id']
        supplier_details = Supplier.objects.get_supplier_details(supplier_id)
        if self.request.user.has_perm('product.change_supplier'):
            kwargs['form'] = AddNewSupplierForm(
                initial={'name': supplier_details.name, 'mobile_no': supplier_details.mobile_no,
                         'address': supplier_details.address})
        kwargs['supplier_details'] = supplier_details
        return super().get_context_data(**kwargs)

    def post(self, request, supplier_id):
        if request.is_ajax():
            if not self.request.user.has_perm('product.change_supplier'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            data = request.POST
            form = AddNewSupplierForm(data)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                Supplier.objects.update_supplier(id=supplier_id, data=cleaned_data)
                return JsonResponse("success", status=201, safe=False)
            else:
                return JsonResponse(form.errors, status=400)


class CustomerList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_customer',)
    template_name = 'product/customer_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['customer_list'] = Customer.objects.get_all_customer()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            id = request.POST['customer_id']
            if id:
                if not self.request.user.has_perm('product.delete_customer'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if Customer.objects.delete_customer(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class CustomerDetails(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_customer',)
    template_name = 'product/customer_details.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        customer_id = kwargs['customer_id']
        customer_details = Customer.objects.get_customer_details(customer_id)
        if self.request.user.has_perm('product.change_customer'):
            customer_edit_form = CustomerForm(initial={
                'customer_name': customer_details.customer_name,
                'customer_phone': customer_details.customer_phone,
                'customer_address': customer_details.customer_address
            })
            kwargs['customer_form'] = customer_edit_form
        kwargs['customer_details'] = customer_details
        return super().get_context_data(**kwargs)

    def post(self, request, customer_id):
        if request.is_ajax():
            if not self.request.user.has_perm('product.change_customer'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            customer = Customer.objects.filter(id=customer_id).first()
            if customer is None:
                raise Http404("Customer not found")
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                edited_customer_info = form.cleaned_data
                if Customer.objects.update_customer_details(id=customer_id, data=edited_customer_info):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse(form.errors, status=400)


class OrderList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_order',)
    template_name = 'product/order_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        kwargs['order_list'] = Order.objects.get_all_order()
        return super().get_context_data(**kwargs)

    def post(self, request):
        if request.is_ajax():
            if not self.request.user.has_perm('product.delete_order'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            id = request.POST['order_id']
            if id:
                if Order.objects.delete_order(id):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                return JsonResponse('error', status=400, safe=False)


class CreateInvoice(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.add_order',)
    template_name = 'product/create_invoice.html'
    ItemFormSet = formset_factory(ItemForm, formset=BaseItemFormSet, extra=0)

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        product_list = Product.objects.get_all_product_stock_filter()
        if 'items' not in kwargs:
            kwargs['items'] = self.ItemFormSet()

        if 'order' not in kwargs:
            kwargs['order'] = OrderForm()

        kwargs['product_list'] = product_list

        return super().get_context_data(**kwargs)

    def post(self, request):
        item_formset = self.ItemFormSet(request.POST)
        order_form = OrderForm(request.POST)
        if order_form.is_valid() and item_formset.is_valid():
            order = order_form.cleaned_data
            items = item_formset.cleaned_data
            order['sold_by'] = request.user
            created_order = Order.objects.crate_new_order(order=order, items=items)
            order_details = Order.objects.get_order_detail(created_order.id)
            return self.render_to_response(
                self.get_context_data(pos_invoice=generate_pos_invoice(order_details), order_id=created_order.id))
        else:
            return self.render_to_response(
                self.get_context_data(order=order_form, selected_items=item_formset.cleaned_data))


class OrderDetail(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_order',)
    template_name = 'product/order_details.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        order_details = Order.objects.get_order_detail(order_id=self.kwargs['order_id'])
        if order_details:
            kwargs['order_details'] = order_details
            kwargs['pos_invoice'] = generate_pos_invoice(order_details)

        return super().get_context_data(**kwargs)

    def post(self, request, order_id):
        if request.is_ajax():
            if 'payment_id' in request.POST:
                if not self.request.user.has_perm('product.delete_paymenthistory'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                id = request.POST['payment_id']
                if id:
                    if Order.objects.delete_payment(id):
                        order_details = Order.objects.get_order_detail(order_id=order_id)
                        pos_invoice = generate_pos_invoice(order_details)
                        return JsonResponse(pos_invoice, status=200, safe=False)
                    else:
                        return JsonResponse('error', status=400, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            elif 'item_id' in request.POST:
                id = request.POST['item_id']
                if not self.request.user.has_perm('product.change_order'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if id:
                    if Order.objects.delete_ordered_item(id):
                        order_details = Order.objects.get_order_detail(order_id=order_id)
                        pos_invoice = generate_pos_invoice(order_details)
                        return JsonResponse(pos_invoice, status=200, safe=False)
                    else:
                        return JsonResponse('error', status=400, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
        if not self.request.user.has_perm('product.add_paymenthistory'):
            return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
        current_user = request.user
        new_payment = Order.objects.make_payment(order_id, request.POST['amount'], current_user)
        return HttpResponseRedirect(self.request.path_info)


class UtilityBill(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('product.view_othercost',)
    template_name = 'product/other_cost_list.html'

    def handle_no_permission(self):
        messages.error(self.request, 'You have no permission')
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def get_context_data(self, **kwargs):
        data = OtherCost.objects.all().order_by('-date')
        if 'form' not in kwargs and self.request.user.has_perm('product.add_othercost'):
            form = OtherCostForm()
        elif self.request.user.has_perm('product.change_othercost'):
            form = kwargs['form']
        kwargs['other_cost_list'] = data
        kwargs['form'] = form
        return super().get_context_data(**kwargs)

    def post(self, request):
        data = request.POST
        if request.is_ajax():
            if 'utility_bill_dlt_id' in data and data['utility_bill_dlt_id']:
                if not self.request.user.has_perm('product.delete_othercost'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                if OtherCost.objects.delete_utility_bill(data['utility_bill_dlt_id']):
                    return JsonResponse('success', status=200, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
            else:
                if not self.request.user.has_perm('product.change_othercost'):
                    return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
                form = OtherCostForm(data)
                if form.is_valid():
                    id = data['id']
                    if OtherCost.objects.update_utility_bill(id=id, data=form.cleaned_data):
                        return JsonResponse('success', status=201, safe=False)
                    else:
                        return JsonResponse('error', status=400, safe=False)
                else:
                    return JsonResponse('error', status=400, safe=False)
        else:
            if not self.request.user.has_perm('product.add_othercost'):
                return JsonResponse({'permission_denied': 'Permission denied'}, status=400, safe=False)
            form = OtherCostForm(data)
            if form.is_valid():
                form.save()
                return redirect('product:other_cost')
            else:
                return self.render_to_response(self.get_context_data(form=form))
