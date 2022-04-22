from django import forms
from django.forms import ModelForm, TextInput, NumberInput, Textarea, BaseFormSet, Select

from product.models import Category, Size, Color, Product, Supplier, Order, Customer, ProductVariant, OtherCost


class ProductForm(forms.ModelForm):
    is_product_edited = forms.IntegerField(
        widget=forms.NumberInput(attrs={'value': '0', 'id': 'isProductEdited', 'hidden': True}))

    class Meta:
        model = Product
        fields = ['product_name', 'product_description']
        widgets = {
            'product_name': TextInput(
                attrs={'class': 'form-control', 'id': 'productName'}),
            'product_description': Textarea(
                attrs={'class': 'form-control', 'id': 'productDescription'}),
        }

    def clean(self):
        if self.cleaned_data['is_product_edited'] is 0 and 'product_name' in self.cleaned_data and self.cleaned_data[
            'product_name']:
            if Product.objects.filter(product_name__iexact=self.cleaned_data['product_name']).exists():
                self.add_error('product_name', 'This product is already exist.')
                raise forms.ValidationError('Product name already exist')


class VariantForm(forms.ModelForm):
    is_variant_edited = forms.IntegerField(
        widget=forms.NumberInput(attrs={'value': '0', 'id': 'isVariantEdited', 'hidden': True}))

    class Meta:
        model = ProductVariant
        fields = ['gsm', 'bag_purchase_price', 'marketing_cost', 'transport_cost', 'printing_cost', 'vat', 'profit',
                  'discount_percent', 'discount_min_purchase', 'category', 'color', 'size', 'stock_total']
        widgets = {
            'gsm': Select(attrs={'class': 'form-control', 'id': 'gsm'}),
            'category': Select(attrs={'class': 'form-control', 'id': 'category'}),
            'color': Select(attrs={'class': 'form-control', 'id': 'color'}),
            'size': Select(attrs={'class': 'form-control', 'id': 'size'}),
            'bag_purchase_price': NumberInput(attrs={'class': 'form-control'}),
            'marketing_cost': NumberInput(attrs={'class': 'form-control'}),
            'transport_cost': NumberInput(attrs={'class': 'form-control'}),
            'printing_cost': NumberInput(attrs={'class': 'form-control'}),
            'vat': NumberInput(attrs={'class': 'form-control'}),
            'profit': NumberInput(attrs={'class': 'form-control'}),
            'discount_percent': NumberInput(attrs={'class': 'form-control'}),
            'discount_min_purchase': NumberInput(attrs={'class': 'form-control'}),
            'stock_total': NumberInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        if 'is_variant_edited' in self.cleaned_data and self.cleaned_data['is_variant_edited'] is 0:
            if ProductVariant.objects.filter(size=self.cleaned_data['size'],
                                             category=self.cleaned_data['category']).exists():
                raise forms.ValidationError('Variant is already exist')


class NewStockForm(forms.Form):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    per_product_purchase_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    new_stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class AddNewProductForm(forms.Form):
    GSM_CHOICES = [
        (None, '----'),
        ('25', 25),
        ('30', 30),
        ('40', 40),
        ('50', 50),
        ('60', 60),
        ('70', 70),
        ('80', 80),
        ('90', 90),
        ('100', 100),
        ('110', 110)
    ]
    product = forms.ModelChoiceField(required=False, queryset=Product.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'product_select'}))
    new_product_name = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'product_input',
                                                                     'placeholder': 'Enter Product Name eg. Handle Bag'}))
    gsm = forms.ChoiceField(required=False, choices=GSM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    product_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'descriptionInput'}))
    bag_purchase_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    marketing_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    transport_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    printing_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vat = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    profit = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    discount_percent = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    discount_min_purchase = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'category_select'}))
    new_category = forms.CharField(required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'category_input',
                                                                 'placeholder': 'Enter Category eg. D-Cut'}))
    size = forms.ModelChoiceField(required=False, queryset=Size.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control', 'id': 'size_select'}))
    new_size = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'size_input',
                                                             'placeholder': 'Enter Size eg. 12/14'}))
    color = forms.ModelChoiceField(required=False, queryset=Color.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control', 'id': 'color_select'}))
    new_color = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'color_input',
                                                              'placeholder': 'Enter Color eg. Red'}))
    stock_total = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    supplier = forms.ModelChoiceField(required=True, queryset=Supplier.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'supplier_select'}))

    def clean(self):
        """If need more validation than default form validation. Then extend this method."""
        if 'new_product_name' in self.cleaned_data and self.cleaned_data['new_product_name']:
            if Product.objects.filter(product_name__iexact=self.cleaned_data['new_product_name']).exists():
                self.add_error('new_product_name', 'This product is already exist.')
                raise forms.ValidationError('This product is already exist.')
            self.cleaned_data['new_product'] = {
                'product_name': self.cleaned_data['new_product_name'],
                'product_description': self.cleaned_data['product_description']
            }
            del self.cleaned_data['product']
            del self.cleaned_data['new_product_name']
            del self.cleaned_data['product_description']
        else:
            if 'product' not in self.cleaned_data or not self.cleaned_data['product']:
                # self.add_error('product', 'This field can\'t be empty')
                raise forms.ValidationError('Product Name can\'t be empty')
            del self.cleaned_data['product_description']
            del self.cleaned_data['new_product_name']

        if 'new_category' in self.cleaned_data and self.cleaned_data['new_category']:
            if Category.objects.filter(category__iexact=self.cleaned_data['new_category']).exists():
                self.add_error('new_category', 'This category is already exist.')
                raise forms.ValidationError('This category is already exist.')
            del self.cleaned_data['category']

        else:
            if 'category' not in self.cleaned_data or not self.cleaned_data['category']:
                # self.add_error('category', 'This field can\'t be empty')
                raise forms.ValidationError('Category field can\'t be empty')
            del self.cleaned_data['new_category']

        if 'new_color' in self.cleaned_data and self.cleaned_data['new_color']:
            if Color.objects.filter(color__iexact=self.cleaned_data['new_color']).exists():
                self.add_error('new_color', 'This color is already exist.')
                raise forms.ValidationError('This color is already exist.')
            del self.cleaned_data['color']
        else:
            del self.cleaned_data['new_color']

        if 'new_size' in self.cleaned_data and self.cleaned_data['new_size']:
            print(self.cleaned_data['new_size'])
            if Size.objects.filter(size__iexact=self.cleaned_data['new_size']).exists():
                self.add_error('new_size', 'This size is already exist.')
                raise forms.ValidationError('This size is already exist.')
            del self.cleaned_data['size']
        else:
            if 'size' not in self.cleaned_data and not self.cleaned_data['size']:
                # self.add_error('size', 'This field can\'t be empty')
                raise forms.ValidationError('Size field can\'t be empty')
            del self.cleaned_data['new_size']

        return self.cleaned_data


class AddNewSupplierForm(ModelForm):
    supplier_id = forms.IntegerField(required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                     'hidden': True, 'value': 0,
                                                                     'id': 'supplierId'}))

    class Meta:
        model = Supplier
        fields = ['name', 'mobile_no', 'address']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'fullname', 'placeholder': 'Supplier Name',
                                     'oninput': 'showName()', 'autofocus': True, 'required': True}),
            'mobile_no': NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Mobile No',
                                            'required': True, 'maxlength': 11}),
            'address': Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True, }),
        }

    def clean(self):
        """If need more validation than default form validation. Then extend this method."""

        if 'mobile_no' in self.cleaned_data and self.cleaned_data['mobile_no'] \
                and 'supplier_id' in self.cleaned_data and self.cleaned_data['supplier_id'] is 0:
            if Supplier.objects.filter(mobile_no=self.cleaned_data['mobile_no']).exists():
                self.add_error('mobile_no', 'This mobile no is already exist.')
                raise forms.ValidationError('This mobile no is already exist.')
        else:
            if 'mobile_no' not in self.cleaned_data or not self.cleaned_data['mobile_no']:
                # self.add_error('mobile_no', 'This field can\'t be empty')
                raise forms.ValidationError('Mobile no field can\'t be empty')
        return self.cleaned_data


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_phone', 'customer_address']
        widgets = {
            'customer_name': TextInput(
                attrs={'class': 'form-control', 'id': 'customerName', 'placeholder': 'Customer Name', }),
            'customer_phone': NumberInput(
                attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Mobile No', 'maxlength': 11}),
            'customer_address': Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True, }),
        }


class OrderForm(forms.Form):
    customer_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'hidden': True, 'id': 'new_customer_name'}))

    customer_address = forms.CharField(required=False,
                                       widget=forms.Textarea(attrs={'class': 'form-control',
                                                                    'id': 'new_customer_address'}))
    customer_phone = forms.IntegerField(required=False,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'form-control', 'id': 'new_customer_phone'}))
    customer = forms.ModelChoiceField(required=False, queryset=Customer.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control', 'id': 'customer_select'}))
    paid_total = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0,
                                                                  'id': 'paid_total_field', 'step': '.01',
                                                                  'disabled': True}))

    def clean(self):
        if 'customer' in self.cleaned_data and self.cleaned_data['customer']:
            del self.cleaned_data['customer_name']
            del self.cleaned_data['customer_phone']
            del self.cleaned_data['customer_address']

        if 'customer_name' in self.cleaned_data and not self.cleaned_data['customer_name']:
            raise forms.ValidationError("Customer name field is required")
        if 'customer_phone' in self.cleaned_data and not self.cleaned_data['customer_phone']:
            raise forms.ValidationError("Customer phone field is required")

        if all(k in self.cleaned_data for k in ['customer_name', 'customer_phone']):
            if 'customer' in self.cleaned_data and self.cleaned_data['customer_name'] and self.cleaned_data[
                'customer_phone']:
                del self.cleaned_data['customer']
            if Customer.objects.filter(customer_phone=self.cleaned_data['customer_phone']).exists():
                self.add_error('customer_phone', 'This phone no is already exist.')
                raise forms.ValidationError('This phone is already exist.')

        return self.cleaned_data


class ItemForm(forms.Form):
    product = forms.IntegerField(required=True,
                                 widget=forms.NumberInput(attrs={'class': 'form-control invoice_readonly_field',
                                                                 'min': 0, 'readonly': True, 'hidden': True}))
    price_per_product = forms.FloatField(required=True,
                                         widget=forms.NumberInput(attrs={'class': 'form-control invoice_readonly_field',
                                                                         'min': 0, 'readonly': True, 'hidden': True}))
    discount_percent = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control invoice_readonly_field',
               'min': 0, 'readonly': True, 'hidden': True}))
    quantity = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control invoice_field quantity_field', 'min': 1}))


class BaseItemFormSet(BaseFormSet):
    def clean(self):
        super(BaseItemFormSet, self).clean()
        if not self.forms:
            raise forms.ValidationError("Please select at least 1 item")


class OtherCostForm(forms.ModelForm):
    class Meta:
        model = OtherCost
        fields = ['shop_rent', 'shop_rent_per_product', 'electricity_bill', 'electricity_bill_per_product',
                  'employee_cost', 'employee_cost_per_product', 'others_bill', 'others_bill_per_product']
        widgets = {
            'shop_rent': NumberInput(
                attrs={'class': 'form-control', 'id': 'shopRentInput'}),
            'shop_rent_per_product': NumberInput(
                attrs={'class': 'form-control', 'id': 'shopRentPerProductInput'}),
            'electricity_bill': NumberInput(
                attrs={'class': 'form-control', 'id': 'electricityBillInput'}),
            'electricity_bill_per_product': NumberInput(
                attrs={'class': 'form-control', 'id': 'electricityBillPerProductInput'}),
            'employee_cost': NumberInput(
                attrs={'class': 'form-control', 'id': 'employeeCostInput'}),
            'employee_cost_per_product': NumberInput(
                attrs={'class': 'form-control', 'id': 'employeeCostPerProductInput'}),
            'others_bill': NumberInput(
                attrs={'class': 'form-control', 'id': 'otherBillInput'}),
            'others_bill_per_product': NumberInput(
                attrs={'class': 'form-control', 'id': 'otherBillPerProductInput'}),

        }
