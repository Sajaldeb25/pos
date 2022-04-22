from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSitesTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects\
            .create_superuser("Almaub Juwal", "bd464258")
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            name="Almaubud Juwal",
            email="almabud37@gmail.com",
            gender="Male",
            nid=12345678901,
            city='Dhaka',
            country='Bangladesh',
            dob='2020-03-02'
        )

    def test_user_listed(self):
        """Test that user is listed on user page"""
        url = reverse('admin:core_user_changelist')
        rs = self.client.get(url)
        self.assertContains(rs, self.user.name)
        self.assertContains(rs, "code")

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, 200)
