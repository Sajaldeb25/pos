from django.contrib.sessions.models import Session
from django.db import models, Error, IntegrityError, transaction, DatabaseError
from django.db.models import Prefetch, Count, Sum, FloatField, F, Value
from django.db.models.functions import Coalesce
from django.http import Http404
from django.utils.timezone import now, localtime

from scripts import employee_code_generator as code_generator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin, Group


class UserManager(BaseUserManager):
    use_in_migrations = True

    @transaction.atomic
    def create_user(self, **extra_fields):
        """Create new user with auto-generated code and password"""
        if 'name' not in extra_fields.keys():
            raise ValueError('Name must be needed')
        code = code_generator.generate_employee_code(extra_fields['name'][:2])
        if code == "":
            raise ValueError('Code must be needed')
        password = extra_fields.get('password', 'bd464258')
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True

        user = self.model(code=code, **extra_fields)
        user.set_password(password)
        if 'email' in extra_fields.keys():
            email = self.normalize_email(extra_fields['email'])
            user.email = email
        try:
            user.save(using=self._db)
            if user.is_superuser:
                superuser = Group.objects.get(name='superuser')
                user.groups.add(superuser)
            elif user.is_admin:
                admin = Group.objects.get(name='admin')
                user.groups.add(admin)
            else:
                staff = Group.objects.get(name='staff')
                user.groups.add(staff)
        except IntegrityError as e:
            raise ValueError(e)
            # raise ValueError("Email has already been used")
        return user

    def create_superuser(self, code, password):
        """Create and save super user"""
        user = self.create_user(password=password, name=code)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_all_users(self):
        """Fetch all users"""
        from product.models import Order
        users = self.filter(is_active=True).prefetch_related('order_sold_by')
        return users

    def user_details(self, code):
        from product.models import Order
        from product.models import OrderedItem

        user = self.model.objects.filter(code=code).prefetch_related(
            Prefetch(
                'order_sold_by',
                queryset=Order.objects.get_all_order(),
                to_attr='orders'
            )
        ).first()

        order_data = user.order_sold_by.get_all_order().aggregate(
            total_order_billed=Coalesce(Sum(F('total_billed')), Value(0)),
            total_order_item=Coalesce(Sum(F('total_item')), Value(0)),
            total_due_from_order=Coalesce(Sum(F('total_due')), Value(0))
        )
        user.total_order_billed = order_data['total_order_billed']
        user.total_order_item = order_data['total_order_item']
        user.total_due_from_order = order_data['total_due_from_order']

        return user

    def deactivate_user(self, code):
        try:
            user = self.get(code=code)
            user.is_active = False
            user.save(using=self.db)

            user_sessions = []
            all_sessions = Session.objects.all()
            for session in all_sessions:
                session_data = session.get_decoded()
                if user.pk == session_data.get('_auth_user_id'):
                    user_sessions.append(session.pk)
            curruser_sessions = Session.objects.filter(pk__in=user_sessions)
            curruser_sessions.delete()
        except DatabaseError as e:
            raise DatabaseError('Technical problem to deactivate user')
        return True

    def activate_user(self, code):
        try:
            user = self.get(code=code)
            user.is_active = True
            user.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Technical problem to activate user")
        return True

    @transaction.atomic
    def update_user(self, instance):
        try:
            updated_user = instance.save()
            updated_user.groups.clear()
            if updated_user.is_superuser:
                user_group = Group.objects.get(name='superuser')
            elif updated_user.is_admin:
                user_group = Group.objects.get(name='admin')
            elif updated_user.is_staff:
                user_group = Group.objects.get(name='staff')
            updated_user.groups.add(user_group)
        except DatabaseError as e:
            raise DatabaseError("Error occurred while updating")
        return updated_user

    def deactivate_user_list(self):
        try:
            data = self.filter(is_active=False).prefetch_related('order_sold_by')
        except DatabaseError as e:
            raise DatabaseError('Technical problem')
        return data

    def calculate_seller_performance_curmonth(self, code):
        from product.models import Order
        from product.models import OrderedItem
        data = Order.objects.get_all_order().filter(sold_by__code=code)
        performance = data.filter(ordered_date__month=now().month, ordered_date__year=now().year).values(
            'ordered_date__day', 'total_item').annotate(
            total_order=Count('id')
        ).order_by('ordered_date__day')
        order_data = data.aggregate(
            total_order_billed=Coalesce(Sum(F('total_billed')), Value(0)),
            total_order_item=Coalesce(Sum(F('total_item')), Value(0)),
            total_due_from_order=Coalesce(Sum(F('total_due')), Value(0))
        )
        performance = list(performance)
        from product.models import ProductVariant
        performance_temp = []
        flag = 0
        for i in range(1, int(localtime(now()).day) + 1):
            if flag < len(performance) and performance[flag][
                'ordered_date__day'] is i:
                performance_temp.append(performance[flag])
                flag += 1
            else:
                performance_temp.append(
                    {'ordered_date_day': i, 'total_item': 0, 'total_order': 0})
        data = {
            'performance': performance_temp,
            'total_order_billed': order_data['total_order_billed'],
            'total_order_item': order_data['total_order_item'],
            'total_collected_cash': order_data['total_order_billed'] - order_data['total_due_from_order'],
            'total_due_from_order': order_data['total_due_from_order'],
            'total_taken_order': data.aggregate(Count('id'))['id__count'],
            'net_stock': ProductVariant.objects.net_stock()['net_stock']
        }
        return data


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    code = models.CharField(max_length=20, unique=True, blank=False, null=False, auto_created=True)
    phone_no1 = models.CharField(max_length=11, unique=True)
    phone_no2 = models.CharField(max_length=11, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    nid = models.CharField(max_length=30, blank=True, unique=True)
    profile_pic = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    city = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)
    dob = models.DateField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'code'

    # REQUIRED_FIELDS = ['name']
    class Meta:
        permissions = [
            ("delete_admin", "Can delete an admin"),
            ("promote_admin", "Can promote a staff to admin"),
            ("demote_admin", "Can demote admin to staff"),
            ("promote_superuser", "Can promote a staff or admin to superuser"),
        ]
