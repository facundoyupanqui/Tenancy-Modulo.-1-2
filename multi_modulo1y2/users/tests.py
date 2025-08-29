from django.test import TestCase
from django.contrib.auth import get_user_model
from clinics.models import Tenant

User = get_user_model()

class UserModelTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Clinic")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            tenant=self.tenant
        )

    def test_user_creation_with_tenant(self):
        self.assertEqual(self.user.tenant, self.tenant)

    def test_user_cannot_change_tenant(self):
        original_tenant = self.user.tenant
        new_tenant = Tenant.objects.create(name="Another Clinic")
        
        with self.assertRaises(ValueError):
            self.user.tenant = new_tenant
            self.user.save()

        # Ensure the tenant remains unchanged
        self.user.refresh_from_db()
        self.assertEqual(self.user.tenant, original_tenant)