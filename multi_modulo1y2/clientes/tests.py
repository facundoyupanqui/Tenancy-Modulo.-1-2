from django.test import TestCase
from django.contrib.auth import get_user_model
from multi_modulo1y2.clinics.models import Tenant
from .models import Cliente

User = get_user_model()

class ClienteModelTests(TestCase):
    def setUp(self):
        self.tenant1 = Tenant.objects.create(name="Clínica A", address="Dirección A", phone_number="123456789")
        self.tenant2 = Tenant.objects.create(name="Clínica B", address="Dirección B", phone_number="987654321")
        
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            tenant=self.tenant1
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            tenant=self.tenant2
        )
        
        self.cliente1 = Cliente.objects.create(
            nombre="Juan",
            apellido="Pérez",
            email="juan@example.com",
            telefono="123456789",
            direccion="Calle 123",
            tenant=self.tenant1
        )
        
        self.cliente2 = Cliente.objects.create(
            nombre="María",
            apellido="González",
            email="maria@example.com",
            telefono="987654321",
            direccion="Avenida 456",
            tenant=self.tenant2
        )
    
    def test_cliente_creation(self):
        self.assertEqual(self.cliente1.nombre, "Juan")
        self.assertEqual(self.cliente1.tenant, self.tenant1)
        self.assertEqual(self.cliente2.nombre, "María")
        self.assertEqual(self.cliente2.tenant, self.tenant2)
    
    def test_cliente_tenant_isolation(self):
        # Verificar que cada tenant solo ve sus propios clientes
        tenant1_clientes = Cliente.objects.filter(tenant=self.tenant1)
        tenant2_clientes = Cliente.objects.filter(tenant=self.tenant2)
        
        self.assertEqual(tenant1_clientes.count(), 1)
        self.assertEqual(tenant2_clientes.count(), 1)
        
        self.assertIn(self.cliente1, tenant1_clientes)
        self.assertIn(self.cliente2, tenant2_clientes)
        
        self.assertNotIn(self.cliente1, tenant2_clientes)
        self.assertNotIn(self.cliente2, tenant1_clientes)