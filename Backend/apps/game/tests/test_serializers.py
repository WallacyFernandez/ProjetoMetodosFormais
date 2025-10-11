"""
Testes para serializers do app de jogo.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date

from apps.game.models import GameSession, ProductCategory, Supplier, Product, ProductStockHistory, RealtimeSale
from apps.game.serializers import (
    GameSessionSerializer, ProductCategorySerializer, SupplierSerializer,
    ProductSerializer, ProductStockHistorySerializer, RealtimeSaleSerializer,
    GameDashboardSerializer, ProductStockOperationSerializer, ProductPurchaseSerializer
)

User = get_user_model()


class GameSessionSerializerTest(TestCase):
    """Testes para GameSessionSerializer."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )

    def test_serialize_game_session(self):
        """Testa serialização de sessão de jogo."""
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        serializer = GameSessionSerializer(game_session)
        data = serializer.data
        
        self.assertEqual(data['user_name'], f'{self.user.first_name} {self.user.last_name}')
        self.assertEqual(data['game_start_date'], '2025-01-01')
        self.assertEqual(data['current_game_date'], '2025-01-01')
        self.assertEqual(data['game_end_date'], '2026-01-01')
        self.assertEqual(data['status'], 'NOT_STARTED')
        self.assertEqual(data['time_acceleration'], 20)
        # daily_sales_target não está no serializer
        # auto_sales_enabled não está no serializer

    def test_deserialize_game_session(self):
        """Testa deserialização/atualização de uma sessão de jogo existente."""
        # Criar uma sessão existente
        game_session, _ = GameSession.objects.get_or_create(user=self.user)
        
        # Atualizar sessão existente com campos disponíveis no serializer
        data = {
            'status': 'ACTIVE',
            'time_acceleration': 30
        }
        
        serializer = GameSessionSerializer(game_session, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_session = serializer.save()
        
        self.assertEqual(updated_session.user, self.user)
        self.assertEqual(updated_session.status, 'ACTIVE')
        self.assertEqual(updated_session.time_acceleration, 30)

    def test_game_session_validation(self):
        """Testa validação de dados da sessão de jogo."""
        data = {
            'user': self.user.id,
            'time_acceleration': 0  # Valor inválido
        }
        
        serializer = GameSessionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('time_acceleration', serializer.errors)


class ProductCategorySerializerTest(TestCase):
    """Testes para ProductCategorySerializer."""

    def test_serialize_product_category(self):
        """Testa serialização de categoria de produto."""
        category = ProductCategory.objects.create(
            name='Alimentos',
            description='Produtos alimentícios',
            icon='🍞',
            color='#F59E0B'
        )
        
        serializer = ProductCategorySerializer(category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Alimentos')
        self.assertEqual(data['description'], 'Produtos alimentícios')
        self.assertEqual(data['icon'], '🍞')
        self.assertEqual(data['color'], '#F59E0B')
        self.assertTrue(data['is_active'])

    def test_deserialize_product_category(self):
        """Testa deserialização de categoria de produto."""
        data = {
            'name': 'Bebidas',
            'description': 'Bebidas e líquidos',
            'icon': '🥤',
            'color': '#3B82F6'
        }
        
        serializer = ProductCategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        category = serializer.save()
        self.assertEqual(category.name, 'Bebidas')
        self.assertEqual(category.description, 'Bebidas e líquidos')
        self.assertEqual(category.icon, '🥤')
        self.assertEqual(category.color, '#3B82F6')


class SupplierSerializerTest(TestCase):
    """Testes para SupplierSerializer."""

    def test_serialize_supplier(self):
        """Testa serialização de fornecedor."""
        supplier = Supplier.objects.create(
            name='Distribuidora Central',
            contact_person='João Silva',
            email='joao@distribuidora.com',
            phone='(11) 99999-9999',
            address='Rua das Flores, 123',
            delivery_time_days=1,
            minimum_order_value=Decimal('200.00'),
            reliability_score=Decimal('4.8')
        )
        
        serializer = SupplierSerializer(supplier)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Distribuidora Central')
        self.assertEqual(data['contact_person'], 'João Silva')
        self.assertEqual(data['email'], 'joao@distribuidora.com')
        self.assertEqual(data['phone'], '(11) 99999-9999')
        self.assertEqual(data['delivery_time_days'], 1)
        self.assertEqual(data['minimum_order_value'], '200.00')
        self.assertEqual(data['reliability_score'], '4.80')

    def test_deserialize_supplier(self):
        """Testa deserialização de fornecedor."""
        data = {
            'name': 'Fornecedor Teste',
            'contact_person': 'Maria Santos',
            'email': 'maria@fornecedor.com',
            'phone': '(11) 88888-8888',
            'delivery_time_days': 2,
            'minimum_order_value': '150.00',
            'reliability_score': '4.5'
        }
        
        serializer = SupplierSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        supplier = serializer.save()
        self.assertEqual(supplier.name, 'Fornecedor Teste')
        self.assertEqual(supplier.contact_person, 'Maria Santos')
        self.assertEqual(supplier.email, 'maria@fornecedor.com')
        self.assertEqual(supplier.delivery_time_days, 2)


class ProductSerializerTest(TestCase):
    """Testes para ProductSerializer."""

    def setUp(self):
        self.category = ProductCategory.objects.create(
            name='Alimentos',
            icon='🍞',
            color='#F59E0B'
        )
        self.supplier = Supplier.objects.create(
            name='Fornecedor Teste'
        )

    def test_serialize_product(self):
        """Testa serialização de produto."""
        product = Product.objects.create(
            name='Arroz 5kg',
            description='Arroz branco tipo 1',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('15.00'),
            sale_price=Decimal('20.00'),
            current_stock=50,
            min_stock=10,
            max_stock=100,
            shelf_life_days=365
        )
        
        serializer = ProductSerializer(product)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Arroz 5kg')
        self.assertEqual(data['description'], 'Arroz branco tipo 1')
        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['supplier'], self.supplier.id)
        self.assertEqual(data['purchase_price'], '15.00')
        self.assertEqual(data['sale_price'], '20.00')
        self.assertEqual(data['current_stock'], 50)
        self.assertEqual(data['min_stock'], 10)
        self.assertEqual(data['max_stock'], 100)
        self.assertEqual(data['shelf_life_days'], 365)

    def test_serialize_product_with_nested_data(self):
        """Testa serialização de produto com dados aninhados."""
        product = Product.objects.create(
            name='Arroz 5kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('15.00'),
            sale_price=Decimal('20.00')
        )
        
        # Usar context para incluir dados aninhados
        serializer = ProductSerializer(product, context={'include_nested': True})
        data = serializer.data
        
        # Verifica se os dados relacionados estão presentes
        self.assertIn('category_name', data)
        self.assertIn('supplier_name', data)

    def test_deserialize_product(self):
        """Testa deserialização de produto."""
        data = {
            'name': 'Feijão 1kg',
            'description': 'Feijão carioca',
            'category': self.category.id,
            'supplier': self.supplier.id,
            'purchase_price': '8.00',
            'sale_price': '12.00',
            'current_stock': 30,
            'min_stock': 5,
            'max_stock': 50,
            'shelf_life_days': 180
        }
        
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        product = serializer.save()
        self.assertEqual(product.name, 'Feijão 1kg')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.supplier, self.supplier)
        self.assertEqual(product.purchase_price, Decimal('8.00'))
        self.assertEqual(product.sale_price, Decimal('12.00'))


class ProductStockHistorySerializerTest(TestCase):
    """Testes para ProductStockHistorySerializer."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        self.category = ProductCategory.objects.create(name='Alimentos')
        self.supplier = Supplier.objects.create(name='Fornecedor Teste')
        self.product = Product.objects.create(
            name='Arroz 5kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('15.00'),
            sale_price=Decimal('20.00')
        )

    def test_serialize_product_stock_history(self):
        """Testa serialização de histórico de estoque."""
        history = ProductStockHistory.objects.create(
            product=self.product,
            operation='PURCHASE',
            quantity=10,
            previous_stock=0,
            new_stock=10,
            unit_price=Decimal('15.00'),
            total_value=Decimal('150.00'),
            description='Compra inicial',
            game_date=date.today()
        )
        
        serializer = ProductStockHistorySerializer(history)
        data = serializer.data
        
        self.assertEqual(data['product'], self.product.id)
        self.assertEqual(data['operation'], 'PURCHASE')
        self.assertEqual(data['quantity'], 10)
        self.assertEqual(data['previous_stock'], 0)
        self.assertEqual(data['new_stock'], 10)
        self.assertEqual(data['unit_price'], '15.00')
        self.assertEqual(data['total_value'], '150.00')
        self.assertEqual(data['description'], 'Compra inicial')
        self.assertEqual(data['game_date'], date.today().strftime('%Y-%m-%d'))

    def test_serialize_product_stock_history_with_product_data(self):
        """Testa serialização com dados do produto."""
        history = ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=5,
            previous_stock=10,
            new_stock=5,
            description='Venda'
        )
        
        # Usar context para incluir dados do produto
        serializer = ProductStockHistorySerializer(history, context={'include_product': True})
        data = serializer.data
        
        self.assertIn('product_name', data)
        self.assertEqual(data['product_name'], 'Arroz 5kg')


class RealtimeSaleSerializerTest(TestCase):
    """Testes para RealtimeSaleSerializer."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        self.game_session, _ = GameSession.objects.get_or_create(user=self.user)
        self.category = ProductCategory.objects.create(name='Alimentos')
        self.supplier = Supplier.objects.create(name='Fornecedor Teste')
        self.product = Product.objects.create(
            name='Arroz 5kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('15.00'),
            sale_price=Decimal('20.00')
        )

    def test_serialize_realtime_sale(self):
        """Testa serialização de venda em tempo real."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=2,
            unit_price=Decimal('20.00'),
            total_value=Decimal('40.00'),
            sale_time=timezone.now(),
            game_date=date.today(),
            game_time='14:30:00'
        )
        
        serializer = RealtimeSaleSerializer(sale)
        data = serializer.data
        
        # Campo game_session não está no serializer
        self.assertIn('id', data)
        # product não está no serializer básico
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['unit_price'], '20.00')
        self.assertEqual(data['total_value'], '40.00')
        self.assertEqual(data['game_date'], date.today().strftime('%Y-%m-%d'))
        self.assertEqual(data['game_time'], '14:30:00')

    def test_serialize_realtime_sale_with_nested_data(self):
        """Testa serialização com dados aninhados."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=1,
            unit_price=Decimal('20.00'),
            total_value=Decimal('20.00'),
            sale_time=timezone.now()
        )
        
        # Usar context para incluir dados aninhados
        serializer = RealtimeSaleSerializer(sale, context={'include_nested': True})
        data = serializer.data
        
        self.assertIn('product_name', data)
        # category_name não está no serializer básico


class GameDashboardSerializerTest(TestCase):
    """Testes para GameDashboardSerializer."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        self.game_session, _ = GameSession.objects.get_or_create(user=self.user)

    def test_serialize_game_dashboard_data(self):
        """Testa serialização de dados do dashboard."""
        dashboard_data = {
            'game_session': self.game_session,
            'balance': {
                'current_balance': Decimal('15000.00'),
                'balance_formatted': 'R$ 15.000,00'
            },
            'products': {
                'total': 10,
                'low_stock': 2,
                'out_of_stock': 1
            },
            'sales': {
                'total_sales': 25,
                'total_revenue': Decimal('500.00')
            },
            'stock_alerts': {
                'low_stock_count': 2,
                'out_of_stock_count': 1,
                'has_alerts': True
            },
            'realtime_sales': []
        }
        
        serializer = GameDashboardSerializer(dashboard_data)
        data = serializer.data
        
        self.assertEqual(data['balance']['current_balance'], 15000.00)
        self.assertEqual(data['balance']['balance_formatted'], 'R$ 15.000,00')
        self.assertEqual(data['products']['total'], 10)
        self.assertEqual(data['sales']['total_sales'], 25)
        self.assertTrue(data['stock_alerts']['has_alerts'])


class ProductStockOperationSerializerTest(TestCase):
    """Testes para ProductStockOperationSerializer."""

    def test_valid_data(self):
        """Testa dados válidos."""
        data = {
            'quantity': 10,
            'description': 'Operação de teste'
        }
        
        serializer = ProductStockOperationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['quantity'], 10)
        self.assertEqual(serializer.validated_data['description'], 'Operação de teste')

    def test_invalid_quantity(self):
        """Testa quantidade inválida."""
        data = {
            'quantity': -5
        }
        
        serializer = ProductStockOperationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_missing_quantity(self):
        """Testa quantidade ausente."""
        data = {
            'description': 'Operação sem quantidade'
        }
        
        serializer = ProductStockOperationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_optional_description(self):
        """Testa descrição opcional."""
        data = {
            'quantity': 5
        }
        
        serializer = ProductStockOperationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['quantity'], 5)
        self.assertIsNone(serializer.validated_data.get('description'))


class ProductPurchaseSerializerTest(TestCase):
    """Testes para ProductPurchaseSerializer."""

    def test_valid_data(self):
        """Testa dados válidos."""
        data = {
            'quantity': 10,
            'unit_price': Decimal('15.00'),
            'description': 'Compra de teste'
        }
        
        serializer = ProductPurchaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['quantity'], 10)
        self.assertEqual(serializer.validated_data['unit_price'], Decimal('15.00'))

    def test_invalid_unit_price(self):
        """Testa preço unitário inválido."""
        data = {
            'quantity': 10,
            'unit_price': Decimal('-5.00')
        }
        
        serializer = ProductPurchaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('unit_price', serializer.errors)

    def test_missing_required_fields(self):
        """Testa campos obrigatórios ausentes."""
        data = {
            'description': 'Compra sem quantidade'
        }
        
        serializer = ProductPurchaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_optional_fields(self):
        """Testa campos opcionais."""
        data = {
            'quantity': 5
        }
        
        serializer = ProductPurchaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['quantity'], 5)
        self.assertIsNone(serializer.validated_data.get('unit_price'))
        self.assertIsNone(serializer.validated_data.get('description'))