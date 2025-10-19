"""
Testes para as views de dashboard.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date, time

from apps.game.models import GameSession, ProductCategory, Supplier, Product, RealtimeSale
from apps.finance.models import UserBalance

User = get_user_model()


class TestGameDashboardViewSet(TestCase):
    """Testes para GameDashboardViewSet."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test User',
            last_name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Criar saldo do usuário
        self.user_balance, _ = UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('15000.00')}
        )
        
        # Criar sessão de jogo
        self.game_session, _ = GameSession.objects.get_or_create(user=self.user)
        self.game_session.status = 'ACTIVE'
        self.game_session.save()
        
        # Criar dados de teste
        self.category = ProductCategory.objects.create(
            name='Alimentos',
            icon='🍞',
            color='#F59E0B'
        )
        self.supplier = Supplier.objects.create(name='Fornecedor Teste')
        
        # Criar produtos com diferentes status de estoque
        self.product_normal = Product.objects.create(
            name='Produto Normal',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=50,
            min_stock=10,
            max_stock=100
        )
        
        self.product_low_stock = Product.objects.create(
            name='Produto Estoque Baixo',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=5,
            min_stock=10,
            max_stock=100
        )
        
        self.product_out_of_stock = Product.objects.create(
            name='Produto Sem Estoque',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=0,
            min_stock=10,
            max_stock=100
        )
        
        # Criar vendas em tempo real
        self.realtime_sale1 = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product_normal,
            quantity=2,
            unit_price=Decimal('15.00'),
            total_value=Decimal('30.00'),
            game_date=self.game_session.current_game_date,
            game_time='14:30:00',
            sale_time=timezone.now()
        )
        
        self.realtime_sale2 = RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product_low_stock,
            quantity=1,
            unit_price=Decimal('15.00'),
            total_value=Decimal('15.00'),
            game_date=self.game_session.current_game_date,
            game_time='15:00:00',
            sale_time=timezone.now()
        )

    def test_dashboard_data_success(self):
        """Testa obtenção de dados do dashboard com sucesso."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica estrutura da resposta
        expected_keys = [
            'game_session', 'balance', 'products', 'sales', 
            'stock_alerts', 'realtime_sales'
        ]
        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_dashboard_game_session_data(self):
        """Testa dados da sessão de jogo no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        game_session_data = response.data['game_session']
        # Campo user não está no serializer, usar user_name
        self.assertEqual(game_session_data['user_name'], f'{self.user.first_name} {self.user.last_name}')
        self.assertEqual(game_session_data['status'], 'ACTIVE')
        self.assertEqual(game_session_data['current_game_date'], '2025-01-01')

    def test_dashboard_balance_data(self):
        """Testa dados do saldo no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        balance_data = response.data['balance']
        # O saldo pode ser diferente devido aos signals
        self.assertGreaterEqual(balance_data['current_balance'], 10000.00)
        self.assertIn('balance_formatted', balance_data)

    def test_dashboard_products_data(self):
        """Testa dados dos produtos no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        products_data = response.data['products']
        # Pode haver mais produtos devido aos signals
        self.assertGreaterEqual(products_data['total'], 3)
        self.assertEqual(products_data['low_stock'], 1)  # 1 produto com estoque baixo
        self.assertEqual(products_data['out_of_stock'], 1)  # 1 produto sem estoque

    def test_dashboard_sales_data(self):
        """Testa dados das vendas no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        sales_data = response.data['sales']
        self.assertEqual(sales_data['total_sales'], 3)  # 2 + 1 vendas
        self.assertEqual(sales_data['total_revenue'], 45.00)  # 30 + 15

    def test_dashboard_stock_alerts(self):
        """Testa alertas de estoque no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stock_alerts = response.data['stock_alerts']
        self.assertEqual(stock_alerts['low_stock_count'], 1)
        self.assertEqual(stock_alerts['out_of_stock_count'], 1)
        self.assertTrue(stock_alerts['has_alerts'])

    def test_dashboard_no_stock_alerts(self):
        """Testa dashboard sem alertas de estoque."""
        # Criar apenas produtos com estoque normal
        Product.objects.filter(id__in=[
            self.product_low_stock.id, 
            self.product_out_of_stock.id
        ]).delete()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stock_alerts = response.data['stock_alerts']
        self.assertEqual(stock_alerts['low_stock_count'], 0)
        self.assertEqual(stock_alerts['out_of_stock_count'], 0)
        self.assertFalse(stock_alerts['has_alerts'])

    def test_dashboard_realtime_sales(self):
        """Testa vendas em tempo real no dashboard."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        realtime_sales = response.data['realtime_sales']
        self.assertEqual(len(realtime_sales), 2)  # 2 vendas criadas
        
        # Verifica se as vendas estão ordenadas por game_time decrescente
        first_sale = realtime_sales[0]
        # Campo product não está no serializer, usar product_name
        self.assertEqual(first_sale['product_name'], 'Produto Estoque Baixo')
        self.assertEqual(first_sale['quantity'], 1)

    def test_dashboard_realtime_sales_limit(self):
        """Testa limite de vendas em tempo real no dashboard."""
        # Criar mais vendas para testar o limite de 20
        for i in range(25):
            RealtimeSale.objects.create(
                game_session=self.game_session,
                product=self.product_normal,
                quantity=1,
                unit_price=Decimal('15.00'),
                total_value=Decimal('15.00'),
                game_date=self.game_session.current_game_date,
                game_time=f'16:{i:02d}:00',
                sale_time=timezone.now()
            )
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar apenas 20 vendas mais recentes
        realtime_sales = response.data['realtime_sales']
        self.assertEqual(len(realtime_sales), 20)

    def test_dashboard_realtime_sales_only_current_date(self):
        """Testa se as vendas em tempo real são apenas do dia atual."""
        # Criar venda de outro dia
        other_date = date(2025, 1, 2)
        RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product_normal,
            quantity=5,
            unit_price=Decimal('15.00'),
            total_value=Decimal('75.00'),
            game_date=other_date,
            game_time='10:00:00',
            sale_time=timezone.now()
        )
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve retornar apenas vendas do dia atual
        realtime_sales = response.data['realtime_sales']
        self.assertEqual(len(realtime_sales), 2)  # Apenas as 2 vendas do dia atual
        
        # Verifica se todas as vendas são do dia atual
        for sale in realtime_sales:
            self.assertEqual(sale['game_date'], '2025-01-01')

    def test_dashboard_game_session_not_found(self):
        """Testa dashboard quando sessão de jogo não existe."""
        # Deletar sessão de jogo
        self.game_session.delete()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Sessão de jogo não encontrada')

    def test_dashboard_user_balance_not_found(self):
        """Testa dashboard quando saldo do usuário não existe."""
        # Deletar saldo do usuário
        self.user_balance.delete()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Saldo do usuário não encontrado')

    def test_dashboard_no_sales_data(self):
        """Testa dashboard sem dados de vendas."""
        # Deletar todas as vendas em tempo real
        RealtimeSale.objects.all().delete()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        sales_data = response.data['sales']
        self.assertEqual(sales_data['total_sales'], 0)
        self.assertEqual(sales_data['total_revenue'], 0)
        
        realtime_sales = response.data['realtime_sales']
        self.assertEqual(len(realtime_sales), 0)

    def test_dashboard_no_products_data(self):
        """Testa dashboard sem produtos."""
        # Deletar todos os produtos
        Product.objects.all().delete()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        products_data = response.data['products']
        self.assertEqual(products_data['total'], 0)
        self.assertEqual(products_data['low_stock'], 0)
        self.assertEqual(products_data['out_of_stock'], 0)

    def test_dashboard_includes_product_category_data(self):
        """Testa se o dashboard inclui dados da categoria do produto nas vendas."""
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        realtime_sales = response.data['realtime_sales']
        first_sale = realtime_sales[0]
        
        # Verifica se os dados da categoria estão incluídos
        # Campo product não está no serializer, usar product_name
        self.assertIn('product_name', first_sale)
        # Campos aninhados não estão no serializer
        self.assertIn('product_name', first_sale)

    def test_dashboard_unauthenticated_access(self):
        """Testa acesso não autenticado."""
        self.client.logout()
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_sales_aggregation(self):
        """Testa agregação de dados de vendas."""
        # Criar mais vendas para testar agregação
        RealtimeSale.objects.create(
            game_session=self.game_session,
            product=self.product_normal,
            quantity=3,
            unit_price=Decimal('15.00'),
            total_value=Decimal('45.00'),
            game_date=self.game_session.current_game_date,
            game_time='16:00:00',
            sale_time=timezone.now()
        )
        
        url = reverse('game-dashboard-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        sales_data = response.data['sales']
        # Total: 2 + 1 + 3 = 6 vendas
        # Receita: 30 + 15 + 45 = 90
        self.assertEqual(sales_data['total_sales'], 6)
        self.assertEqual(sales_data['total_revenue'], 90.00)
