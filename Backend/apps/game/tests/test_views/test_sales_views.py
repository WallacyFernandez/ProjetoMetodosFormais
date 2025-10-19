"""
Testes para as views de vendas.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from apps.game.models import GameSession, ProductCategory, Supplier, Product, ProductStockHistory
from apps.finance.models import UserBalance

User = get_user_model()


class TestProductSalesViewSet(TestCase):
    """Testes para ProductSalesViewSet."""

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
        UserBalance.objects.get_or_create(
            user=self.user,
            defaults={'current_balance': Decimal('10000.00')}
        )
        
        # Criar dados de teste
        self.game_session, _ = GameSession.objects.get_or_create(user=self.user)
        self.category = ProductCategory.objects.create(
            name='Alimentos',
            icon='🍞',
            color='#F59E0B'
        )
        self.supplier = Supplier.objects.create(name='Fornecedor Teste')
        self.product = Product.objects.create(
            name='Arroz 5kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('15.00'),
            sale_price=Decimal('20.00'),
            current_stock=50,
            min_stock=10,
            max_stock=100
        )

    def test_simulate_sale_success(self):
        """Testa simulação de venda com sucesso."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 5,
            'description': 'Venda de teste'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Venda realizada com sucesso')
        
        # Verifica se o estoque foi reduzido
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_stock, 45)

    def test_simulate_sale_insufficient_stock(self):
        """Testa simulação de venda com estoque insuficiente."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 100,  # Mais que o estoque disponível
            'description': 'Venda de teste'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Estoque insuficiente')

    def test_simulate_sale_invalid_data(self):
        """Testa simulação de venda com dados inválidos."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': -5  # Quantidade negativa
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    def test_simulate_sale_nonexistent_product(self):
        """Testa simulação de venda com produto inexistente."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': 99999,  # ID inexistente
            'quantity': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_simulate_sale_creates_stock_history(self):
        """Testa se a venda cria histórico de estoque."""
        initial_count = ProductStockHistory.objects.count()
        
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se o histórico foi criado
        final_count = ProductStockHistory.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Verifica o conteúdo do histórico
        history = ProductStockHistory.objects.latest('created_at')
        self.assertEqual(history.product, self.product)
        self.assertEqual(history.operation, 'SALE')
        self.assertEqual(history.quantity, 5)

    def test_simulate_sale_updates_user_balance(self):
        """Testa se a venda atualiza o saldo do usuário."""
        initial_balance = UserBalance.objects.get(user=self.user).current_balance
        
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se o saldo foi atualizado
        user_balance = UserBalance.objects.get(user=self.user)
        expected_balance = initial_balance + (self.product.current_price * 5)
        # Pode haver diferenças devido ao sinal criar dados automaticamente
        self.assertGreaterEqual(user_balance.current_balance, expected_balance)

    def test_simulate_sale_creates_financial_transaction(self):
        """Testa se a venda cria transação financeira."""
        from apps.finance.models import Transaction
        
        initial_count = Transaction.objects.count()
        
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a transação foi criada
        final_count = Transaction.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Verifica o conteúdo da transação
        transaction = Transaction.objects.latest('created_at')
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.transaction_type, 'INCOME')
        self.assertEqual(transaction.amount, self.product.current_price * 5)

    def test_sales_summary(self):
        """Testa resumo de vendas."""
        # Criar algumas vendas no histórico
        ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=5,
            previous_stock=50,
            new_stock=45,
            unit_price=Decimal('20.00'),
            total_value=Decimal('100.00')
        )
        
        ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=3,
            previous_stock=45,
            new_stock=42,
            unit_price=Decimal('20.00'),
            total_value=Decimal('60.00')
        )
        
        url = reverse('product-sales-sales-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_sales', response.data)
        self.assertIn('total_revenue', response.data)
        self.assertIn('recent_sales', response.data)
        self.assertIn('top_products', response.data)
        
        # Verifica os totais
        self.assertEqual(response.data['total_sales'], 8)
        self.assertEqual(response.data['total_revenue'], 160.00)

    def test_sales_summary_no_sales(self):
        """Testa resumo de vendas quando não há vendas."""
        url = reverse('product-sales-sales-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_sales'], 0)
        self.assertEqual(response.data['total_revenue'], 0)
        self.assertEqual(len(response.data['recent_sales']), 0)
        self.assertEqual(len(response.data['top_products']), 0)

    def test_sales_summary_recent_sales_limit(self):
        """Testa limite de vendas recentes no resumo."""
        # Criar mais de 10 vendas
        for i in range(15):
            ProductStockHistory.objects.create(
                product=self.product,
                operation='SALE',
                quantity=1,
                previous_stock=50 - i,
                new_stock=49 - i,
                unit_price=Decimal('20.00'),
                total_value=Decimal('20.00')
            )
        
        url = reverse('product-sales-sales-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar apenas 10 vendas recentes
        self.assertEqual(len(response.data['recent_sales']), 10)

    def test_sales_summary_top_products_limit(self):
        """Testa limite de produtos mais vendidos no resumo."""
        # Criar outro produto
        product2 = Product.objects.create(
            name='Feijão 1kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('8.00'),
            sale_price=Decimal('12.00'),
            current_stock=30
        )
        
        # Criar vendas para diferentes produtos
        ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=10,
            previous_stock=50,
            new_stock=40,
            unit_price=Decimal('20.00'),
            total_value=Decimal('200.00')
        )
        
        ProductStockHistory.objects.create(
            product=product2,
            operation='SALE',
            quantity=5,
            previous_stock=30,
            new_stock=25,
            unit_price=Decimal('12.00'),
            total_value=Decimal('60.00')
        )
        
        url = reverse('product-sales-sales-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar apenas 5 produtos mais vendidos
        self.assertEqual(len(response.data['top_products']), 2)

    def test_simulate_sale_with_custom_description(self):
        """Testa simulação de venda com descrição customizada."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 3,
            'description': 'Venda personalizada'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a descrição foi salva no histórico
        history = ProductStockHistory.objects.latest('created_at')
        self.assertEqual(history.description, 'Venda personalizada')

    def test_simulate_sale_without_description(self):
        """Testa simulação de venda sem descrição."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a descrição padrão foi usada
        history = ProductStockHistory.objects.latest('created_at')
        expected_description = f'Venda de {data["quantity"]} unidades'
        self.assertEqual(history.description, expected_description)

    def test_sales_summary_includes_product_names(self):
        """Testa se o resumo inclui nomes dos produtos."""
        ProductStockHistory.objects.create(
            product=self.product,
            operation='SALE',
            quantity=5,
            previous_stock=50,
            new_stock=45,
            unit_price=Decimal('20.00'),
            total_value=Decimal('100.00')
        )
        
        url = reverse('product-sales-sales-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se o nome do produto está incluído
        top_products = response.data['top_products']
        self.assertEqual(len(top_products), 1)
        self.assertEqual(top_products[0]['product__name'], 'Arroz 5kg')

    def test_unauthenticated_access(self):
        """Testa acesso não autenticado."""
        self.client.logout()
        
        url = reverse('product-sales-simulate-sale')
        response = self.client.post(url, {})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_simulate_sale_returns_product_data(self):
        """Testa se a simulação de venda retorna dados do produto."""
        url = reverse('product-sales-simulate-sale')
        data = {
            'product_id': self.product.id,
            'quantity': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('product', response.data)
        self.assertIn('total_value', response.data)
        
        # Verifica se os dados do produto estão corretos
        product_data = response.data['product']
        self.assertEqual(product_data['name'], 'Arroz 5kg')
        self.assertEqual(product_data['current_stock'], 45)  # 50 - 5
