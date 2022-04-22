from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_new_user_with_email_successful(self):
        """Create new user with employee code and password"""

        email = "almabud37@gmail.com"
        password = "bd464258"
        name = "Almaubud Juwal"
        gender = "Male"
        user = get_user_model().objects.create_user(
            name="Almaubud Juwal",
            email=email,
            gender="Male",
            nid=123456789303,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))

    def test_name_null_error(self):
        with self.assertRaises(ValueError):
            password = "bd464258"
            get_user_model().objects.create_user(
                # password=password
            )

    def test_create_new_user_email_normalize(self):
        """Check email is normalize or not"""
        email = "almabud37@gmail.com"
        user = get_user_model().objects.create_user(
            name="Almaubud Juwal",
            email=email,
            gender="Male",
            nid=123456789303,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )
        self.assertEqual(user.email, email.lower())

    def test_employee_code_generator_generate_unique_code(self):
        """Check the employee code generator can generate unique code all the time """
        user1 = get_user_model().objects.create_user(
            name="Almaubud Juwal",
            gender="Male",
            nid=123456789303,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )
        user2 = get_user_model().objects.create_user(
            name="Almaubud Juwal",
            gender="Male",
            nid=12345678903,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )

        self.assertNotEqual(user1.code, user2.code)

    def test_same_email_error(self):
        """Same email raise appropriate error"""
        email = "almabud37@gmail.com"
        get_user_model().objects.create_user(
            # password=password,
            name="Almaubud Juwal",
            email=email,
            gender="Male",
            nid=1234567890,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )
        with self.assertRaises(ValueError):
            email = "almabud37@gmail.com"
            get_user_model().objects.create_user(
                # password=password,
                name="Almaubud Juwal",
                email=email,
                gender="Male",
                nid=12345678901,
                city='Dhaka',
                country='Bangladesh',
                dob='2020-03-02'
            )

    def test_create_super_user(self):
        """Test creation of super user"""
        name = "Almabud Juwal"
        password = "bd464258"
        user = get_user_model().objects.create_superuser(name, password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
