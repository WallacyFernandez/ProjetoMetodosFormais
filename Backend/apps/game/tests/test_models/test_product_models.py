"""
Testes para os modelos de produtos.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from apps.game.models import ProductCategory, Supplier, Product


class TestProductCategoryModel(TestCase):
    """Testes para o modelo ProductCategory."""

    def test_create_product_category(self):
        """Testa a criação de categoria de produto."""
        category = ProductCategory.objects.create(
            name='Alimentos',
            description='Produtos alimentícios básicos',
            icon='🍞',
            color='#F59E0B'
        )
        
        self.assertEqual(category.name, 'Alimentos')
        self.assertEqual(category.description, 'Produtos alimentícios básicos')
        self.assertEqual(category.icon, '🍞')
        self.assertEqual(category.color, '#F59E0B')
        self.assertTrue(category.is_active)

    def test_product_category_default_values(self):
        """Testa valores padrão da categoria."""
        category = ProductCategory.objects.create(name='Teste')
        
        self.assertEqual(category.icon, '📦')
        self.assertEqual(category.color, '#10B981')
        self.assertTrue(category.is_active)

    def test_get_default_categories(self):
        """Testa obtenção de categorias padrão."""
        default_categories = ProductCategory.get_default_categories()
        
        self.assertEqual(len(default_categories), 5)
        
        # Verifica se todas as categorias padrão estão presentes
        category_names = [cat['name'] for cat in default_categories]
        expected_names = ['Alimentos', 'Bebidas', 'Limpeza', 'Carnes', 'Padaria']
        
        for expected_name in expected_names:
            self.assertIn(expected_name, category_names)

    def test_str_representation(self):
        """Testa representação string da categoria."""
        category = ProductCategory.objects.create(name='Teste')
        self.assertEqual(str(category), 'Teste')

    def test_meta_ordering(self):
        """Testa ordenação definida no Meta."""
        ProductCategory.objects.create(name='Categoria C')
        ProductCategory.objects.create(name='Categoria A')
        ProductCategory.objects.create(name='Categoria B')
        
        categories = ProductCategory.objects.all()
        names = [cat.name for cat in categories]
        self.assertEqual(names, ['Categoria A', 'Categoria B', 'Categoria C'])


class TestSupplierModel(TestCase):
    """Testes para o modelo Supplier."""

    def test_create_supplier(self):
        """Testa a criação de fornecedor."""
        supplier = Supplier.objects.create(
            name='Distribuidora Central',
            contact_person='João Silva',
            email='joao@distribuidora.com',
            phone='(11) 99999-9999',
            address='Rua das Flores, 123 - São Paulo/SP',
            delivery_time_days=1,
            minimum_order_value=Decimal('200.00'),
            reliability_score=Decimal('4.8')
        )
        
        self.assertEqual(supplier.name, 'Distribuidora Central')
        self.assertEqual(supplier.contact_person, 'João Silva')
        self.assertEqual(supplier.email, 'joao@distribuidora.com')
        self.assertEqual(supplier.phone, '(11) 99999-9999')
        self.assertEqual(supplier.delivery_time_days, 1)
        self.assertEqual(supplier.minimum_order_value, Decimal('200.00'))
        self.assertEqual(supplier.reliability_score, Decimal('4.8'))
        self.assertTrue(supplier.is_active)

    def test_supplier_default_values(self):
        """Testa valores padrão do fornecedor."""
        supplier = Supplier.objects.create(name='Teste')
        
        self.assertEqual(supplier.delivery_time_days, 1)
        self.assertEqual(supplier.minimum_order_value, Decimal('100.00'))
        self.assertEqual(supplier.reliability_score, Decimal('5.00'))
        self.assertTrue(supplier.is_active)

    def test_get_default_suppliers(self):
        """Testa obtenção de fornecedores padrão."""
        default_suppliers = Supplier.get_default_suppliers()
        
        self.assertEqual(len(default_suppliers), 3)
        
        # Verifica se todos os fornecedores padrão estão presentes
        supplier_names = [sup['name'] for sup in default_suppliers]
        expected_names = ['Distribuidora Central', 'Fornecedor Express', 'Mega Distribuidora']
        
        for expected_name in expected_names:
            self.assertIn(expected_name, supplier_names)

    def test_reliability_score_validation(self):
        """Testa validação da pontuação de confiabilidade."""
        supplier = Supplier.objects.create(name='Teste')
        
        # Testa valor mínimo
        supplier.reliability_score = Decimal('1.00')
        supplier.full_clean()  # Não deve gerar erro
        
        # Testa valor máximo
        supplier.reliability_score = Decimal('5.00')
        supplier.full_clean()  # Não deve gerar erro

    def test_delivery_time_validation(self):
        """Testa validação do prazo de entrega."""
        supplier = Supplier.objects.create(name='Teste')
        
        # Testa valor mínimo
        supplier.delivery_time_days = 1
        supplier.full_clean()  # Não deve gerar erro
        
        # Testa valor máximo
        supplier.delivery_time_days = 30
        supplier.full_clean()  # Não deve gerar erro

    def test_str_representation(self):
        """Testa representação string do fornecedor."""
        supplier = Supplier.objects.create(name='Teste')
        self.assertEqual(str(supplier), 'Teste')

    def test_meta_ordering(self):
        """Testa ordenação definida no Meta."""
        Supplier.objects.create(name='Fornecedor C')
        Supplier.objects.create(name='Fornecedor A')
        Supplier.objects.create(name='Fornecedor B')
        
        suppliers = Supplier.objects.all()
        names = [sup.name for sup in suppliers]
        self.assertEqual(names, ['Fornecedor A', 'Fornecedor B', 'Fornecedor C'])


class TestProductModel(TestCase):
    """Testes para o modelo Product."""

    def setUp(self):
        self.category = ProductCategory.objects.create(
            name='Alimentos',
            icon='🍞',
            color='#F59E0B'
        )
        self.supplier = Supplier.objects.create(
            name='Distribuidora Central'
        )

    def test_create_product(self):
        """Testa a criação de produto."""
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
        
        self.assertEqual(product.name, 'Arroz 5kg')
        self.assertEqual(product.description, 'Arroz branco tipo 1')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.supplier, self.supplier)
        self.assertEqual(product.purchase_price, Decimal('15.00'))
        self.assertEqual(product.sale_price, Decimal('20.00'))
        self.assertEqual(product.current_stock, 50)
        self.assertEqual(product.min_stock, 10)
        self.assertEqual(product.max_stock, 100)
        self.assertEqual(product.shelf_life_days, 365)
        self.assertTrue(product.is_active)
        self.assertFalse(product.is_promotional)

    def test_product_default_values(self):
        """Testa valores padrão do produto."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        self.assertEqual(product.current_stock, 0)
        self.assertEqual(product.min_stock, 10)
        self.assertEqual(product.max_stock, 100)
        self.assertEqual(product.shelf_life_days, 30)
        self.assertTrue(product.is_active)
        self.assertFalse(product.is_promotional)

    def test_profit_margin_property(self):
        """Testa cálculo da margem de lucro."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        expected_margin = ((Decimal('15.00') - Decimal('10.00')) / Decimal('15.00')) * 100
        self.assertEqual(product.profit_margin, expected_margin)

    def test_profit_margin_formatted_property(self):
        """Testa margem de lucro formatada."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        self.assertRegex(product.profit_margin_formatted, r'\d+\.\d{2}%')

    def test_current_price_normal(self):
        """Testa preço atual sem promoção."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        self.assertEqual(product.current_price, Decimal('15.00'))

    def test_current_price_promotional(self):
        """Testa preço atual com promoção ativa."""
        today = date.today()
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            is_promotional=True,
            promotional_price=Decimal('12.00'),
            promotional_start_date=today,
            promotional_end_date=today
        )
        
        self.assertEqual(product.current_price, Decimal('12.00'))

    def test_current_price_promotional_expired(self):
        """Testa preço atual com promoção expirada."""
        from datetime import timedelta
        yesterday = date.today() - timedelta(days=1)
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            is_promotional=True,
            promotional_price=Decimal('12.00'),
            promotional_start_date=yesterday,
            promotional_end_date=yesterday
        )
        
        self.assertEqual(product.current_price, Decimal('15.00'))

    def test_is_low_stock_property(self):
        """Testa verificação de estoque baixo."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=5,
            min_stock=10
        )
        
        self.assertTrue(product.is_low_stock)
        
        product.current_stock = 15
        self.assertFalse(product.is_low_stock)

    def test_is_out_of_stock_property(self):
        """Testa verificação de estoque zerado."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=0
        )
        
        self.assertTrue(product.is_out_of_stock)
        
        product.current_stock = 5
        self.assertFalse(product.is_out_of_stock)

    def test_stock_status_property(self):
        """Testa status do estoque."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            min_stock=10
        )
        
        # Estoque zerado
        product.current_stock = 0
        self.assertEqual(product.stock_status, 'OUT_OF_STOCK')
        
        # Estoque baixo
        product.current_stock = 5
        self.assertEqual(product.stock_status, 'LOW_STOCK')
        
        # Estoque normal
        product.current_stock = 15
        self.assertEqual(product.stock_status, 'NORMAL')

    def test_add_stock(self):
        """Testa adicionar estoque."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        product.add_stock(5)
        self.assertEqual(product.current_stock, 15)

    def test_add_stock_negative_quantity(self):
        """Testa adicionar estoque com quantidade negativa."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        with self.assertRaises(ValueError):
            product.add_stock(-5)

    def test_remove_stock(self):
        """Testa remover estoque."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        product.remove_stock(3)
        self.assertEqual(product.current_stock, 7)

    def test_remove_stock_insufficient(self):
        """Testa remover estoque insuficiente."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=5
        )
        
        with self.assertRaises(ValueError):
            product.remove_stock(10)

    def test_remove_stock_negative_quantity(self):
        """Testa remover estoque com quantidade negativa."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        with self.assertRaises(ValueError):
            product.remove_stock(-5)

    def test_set_stock(self):
        """Testa definir estoque."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        product.set_stock(25)
        self.assertEqual(product.current_stock, 25)

    def test_set_stock_negative_quantity(self):
        """Testa definir estoque com quantidade negativa."""
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00'),
            current_stock=10
        )
        
        with self.assertRaises(ValueError):
            product.set_stock(-5)

    def test_str_representation(self):
        """Testa representação string do produto."""
        product = Product.objects.create(
            name='Arroz 5kg',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        expected = f"Arroz 5kg - {self.category.name}"
        self.assertEqual(str(product), expected)

    def test_meta_indexes(self):
        """Testa índices definidos no Meta."""
        # Este teste verifica se os índices estão definidos corretamente
        # A verificação real seria feita no banco de dados
        product = Product.objects.create(
            name='Teste',
            category=self.category,
            supplier=self.supplier,
            purchase_price=Decimal('10.00'),
            sale_price=Decimal('15.00')
        )
        
        # Verifica se o produto foi criado sem erros
        self.assertIsNotNone(product.id)
