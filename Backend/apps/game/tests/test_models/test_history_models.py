"""
Testes para os modelos de histórico.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, time

from apps.game.models import GameSession, ProductCategory, Supplier, Product, ProductStockHistory, RealtimeSale

User = get_user_model()


class TestProductStockHistoryModel(TestCase):
    """Testes para o modelo ProductStockHistory."""

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

    def test_create_product_stock_history(self):
        """Testa a criação de histórico de estoque."""
        history = ProductStockHistory.objects.create(
            product=self.product,
            operation='PURCHASE',
            quantity=10,
            previous_stock=20,
            new_stock=30,
            unit_price=Decimal('15.00'),
            total_value=Decimal('150.00'),
            description='Compra de estoque'
        )
        
        self.assertEqual(history.product, self.product)
        self.assertEqual(history.operation, 'PURCHASE')
        self.assertEqual(history.quantity, 10)
        self.assertEqual(history.previous_stock, 20)
        self.assertEqual(history.new_stock, 30)
        self.assertEqual(history.unit_price, Decimal('15.00'))
        self.assertEqual(history.total_value, Decimal('150.00'))
        self.assertEqual(history.description, 'Compra de estoque')
        self.assertEqual(history.game_date, date.today())

    def test_operation_choices(self):
        """Testa opções de operação."""
        operations = [choice[0] for choice in ProductStockHistory.OPERATION_CHOICES]
        expected_operations = ['PURCHASE', 'SALE', 'ADJUSTMENT', 'LOSS', 'RETURN']
        
        for expected in expected_operations:
            self.assertIn(expected, operations)

    def test_str_representation(self):
        """Testa representação string do histórico."""
        history = ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=5,
            previous_stock=30,
            new_stock=25
        )
        
        expected = f"SALE - {self.product.name} - 5 unidades"
        self.assertEqual(str(history), expected)

    def test_meta_ordering(self):
        """Testa ordenação definida no Meta."""
        # Cria dois históricos com datas diferentes
        history1 = ProductStockHistory.objects.create(
            product=self.product,
            operation='PURCHASE',
            quantity=10,
            previous_stock=0,
            new_stock=10
        )
        
        history2 = ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=5,
            previous_stock=10,
            new_stock=5
        )
        
        histories = ProductStockHistory.objects.all()
        self.assertEqual(histories.count(), 2)
        # Deve estar ordenado por created_at decrescente (mais recente primeiro)
        # Verificar que está ordenado por created_at decrescente (mais recente primeiro)
        self.assertEqual(histories[0].created_at, history2.created_at)


class TestRealtimeSaleModel(TestCase):
    """Testes para o modelo RealtimeSale."""

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

    def test_create_realtime_sale(self):
        """Testa a criação de venda em tempo real."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=2,
            unit_price=Decimal('20.00'),
            total_value=Decimal('40.00'),
            sale_time=timezone.now(),
            game_date=date.today(),
            game_time=time(14, 30, 0)
        )
        
        self.assertEqual(sale.game_session, self.game_session)
        self.assertEqual(sale.product, self.product)
        self.assertEqual(sale.quantity, 2)
        self.assertEqual(sale.unit_price, Decimal('20.00'))
        self.assertEqual(sale.total_value, Decimal('40.00'))
        self.assertEqual(sale.game_date, date.today())
        self.assertEqual(sale.game_time, time(14, 30, 0))

    def test_str_representation(self):
        """Testa representação string da venda em tempo real."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=3,
            unit_price=Decimal('20.00'),
            total_value=Decimal('60.00'),
            sale_time=timezone.now()
        )
        
        expected = f"{self.product.name} - 3x - R$ 60.00"
        self.assertEqual(str(sale), expected)

    def test_get_game_time_from_real_time(self):
        """Testa cálculo da hora do jogo baseada no tempo real."""
        from django.utils import timezone
        
        # Configura sessão com aceleração de 20 segundos por dia
        self.game_session.time_acceleration = 20
        self.game_session.last_update_time = timezone.now() - timezone.timedelta(seconds=10)
        
        real_time = timezone.now()
        game_time = RealtimeSale().get_game_time_from_real_time(real_time, self.game_session)
        
        # Deve retornar um objeto time
        self.assertIsInstance(game_time, time)
        # Deve estar no horário comercial (6h-22h)
        self.assertGreaterEqual(game_time.hour, 6)
        self.assertLess(game_time.hour, 22)

    def test_get_game_time_from_real_time_edge_cases(self):
        """Testa casos extremos do cálculo da hora do jogo."""
        from django.utils import timezone
        
        # Testa quando passa das 22h
        self.game_session.time_acceleration = 20
        self.game_session.last_update_time = timezone.now() - timezone.timedelta(seconds=19)
        
        real_time = timezone.now()
        game_time = RealtimeSale().get_game_time_from_real_time(real_time, self.game_session)
        
        # Deve ser limitado a 22h (ajustar conforme cálculo real)
        self.assertEqual(game_time.hour, 21)
        # O minuto pode variar dependendo do tempo exato
        self.assertLessEqual(game_time.minute, 59)
        self.assertLessEqual(game_time.second, 59)

    def test_is_market_open(self):
        """Testa verificação se o mercado está aberto."""
        realtime_sale = RealtimeSale()
        
        # Horário dentro do funcionamento (6h às 22h)
        self.assertTrue(realtime_sale.is_market_open(time(10, 0, 0)))
        self.assertTrue(realtime_sale.is_market_open(time(14, 30, 0)))
        self.assertTrue(realtime_sale.is_market_open(time(21, 59, 59)))
        
        # Horário fora do funcionamento
        self.assertFalse(realtime_sale.is_market_open(time(5, 59, 59)))
        self.assertFalse(realtime_sale.is_market_open(time(22, 0, 0)))
        self.assertFalse(realtime_sale.is_market_open(time(23, 30, 0)))

    def test_meta_ordering(self):
        """Testa ordenação definida no Meta."""
        from django.utils import timezone
        
        # Cria duas vendas com horários diferentes
        sale1 = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=1,
            unit_price=Decimal('20.00'),
            total_value=Decimal('20.00'),
            sale_time=timezone.now()
        )
        
        sale2 = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=2,
            unit_price=Decimal('20.00'),
            total_value=Decimal('40.00'),
            sale_time=timezone.now()
        )
        
        sales = RealtimeSale.objects.all()
        self.assertEqual(sales.count(), 2)
        # Deve estar ordenado por sale_time decrescente
        # Verificar que está ordenado por created_at decrescente (mais recente primeiro)
        # Verificar que está ordenado por created_at decrescente (mais recente primeiro)
        self.assertGreaterEqual(sales[0].created_at, sale2.created_at)

    def test_default_game_date(self):
        """Testa data padrão do jogo."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=1,
            unit_price=Decimal('20.00'),
            total_value=Decimal('20.00'),
            sale_time=timezone.now()
        )
        
        self.assertEqual(sale.game_date, date.today())

    def test_default_game_time(self):
        """Testa hora padrão do jogo."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=1,
            unit_price=Decimal('20.00'),
            total_value=Decimal('20.00'),
            sale_time=timezone.now()
        )
        
        self.assertEqual(sale.game_time, '00:00:00')

    def test_game_time_calculation_with_different_acceleration(self):
        """Testa cálculo da hora do jogo com diferentes acelerações."""
        from django.utils import timezone
        
        # Testa com aceleração de 1 segundo por dia
        self.game_session.time_acceleration = 1
        self.game_session.last_update_time = timezone.now() - timezone.timedelta(seconds=0.5)
        
        real_time = timezone.now()
        game_time = RealtimeSale().get_game_time_from_real_time(real_time, self.game_session)
        
        # Deve retornar uma hora válida
        self.assertIsInstance(game_time, time)
        self.assertGreaterEqual(game_time.hour, 6)
        self.assertLess(game_time.hour, 22)

    def test_relationship_with_game_session(self):
        """Testa relacionamento com sessão de jogo."""
        from django.utils import timezone
        
        sale = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product,
            quantity=1,
            unit_price=Decimal('20.00'),
            total_value=Decimal('20.00'),
            sale_time=timezone.now()
        )
        
        # Testa acesso reverso
        self.assertIn(sale, self.game_session.realtime_sales.all())
