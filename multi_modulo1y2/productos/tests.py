from django.test import TestCase
from django.contrib.auth import get_user_model
from multi_modulo1y2.clinics.models import Tenant
from .models import Producto

User = get_user_model()

class ProductoModelTests(TestCase):
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
        
        self.producto1 = Producto.objects.create(
            nombre="Producto 1",
            descripcion="Descripción del producto 1",
            precio=100.00,
            stock=10,
            tenant=self.tenant1
        )
        
        self.producto2 = Producto.objects.create(
            nombre="Producto 2",
            descripcion="Descripción del producto 2",
            precio=200.00,
            stock=20,
            tenant=self.tenant2
        )
    
    def test_producto_creation(self):
        self.assertEqual(self.producto1.nombre, "Producto 1")
        self.assertEqual(self.producto1.tenant, self.tenant1)
        self.assertEqual(self.producto2.nombre, "Producto 2")
        self.assertEqual(self.producto2.tenant, self.tenant2)
    
    def test_producto_tenant_isolation(self):
        # Verificar que cada tenant solo ve sus propios productos
        tenant1_productos = Producto.objects.filter(tenant=self.tenant1)
        tenant2_productos = Producto.objects.filter(tenant=self.tenant2)
        
        self.assertEqual(tenant1_productos.count(), 1)
        self.assertEqual(tenant2_productos.count(), 1)
        
        self.assertIn(self.producto1, tenant1_productos)
        self.assertIn(self.producto2, tenant2_productos)
        
        self.assertNotIn(self.producto1, tenant2_productos)
        self.assertNotIn(self.producto2, tenant1_productos)