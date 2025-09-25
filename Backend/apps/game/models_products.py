"""
Modelos adicionais para produtos e estoque do jogo.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager
from .models import GameSession, ProductCategory


class Supplier(BaseModel):
    """
    Fornecedores de produtos para o supermercado.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    
    contact_person = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Pessoa de Contato'
    )
    
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone'
    )
    
    address = models.TextField(
        blank=True,
        verbose_name='Endereço'
    )
    
    # Configurações de negócio
    delivery_time_days = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        verbose_name='Prazo de Entrega (dias)'
    )
    
    minimum_order_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('100.00'),
        verbose_name='Valor Mínimo do Pedido'
    )
    
    reliability_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('5.00'),
        validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name='Pontuação de Confiabilidade'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_suppliers(cls):
        """Retorna fornecedores padrão."""
        return [
            {
                'name': 'Distribuidora Central',
                'contact_person': 'João Silva',
                'email': 'joao@central.com',
                'phone': '(11) 99999-9999',
                'address': 'Rua das Flores, 123 - São Paulo/SP',
                'delivery_time_days': 1,
                'minimum_order_value': Decimal('200.00'),
                'reliability_score': Decimal('4.50'),
            },
            {
                'name': 'Fornecedor Express',
                'contact_person': 'Maria Santos',
                'email': 'maria@express.com',
                'phone': '(11) 88888-8888',
                'address': 'Av. Principal, 456 - São Paulo/SP',
                'delivery_time_days': 2,
                'minimum_order_value': Decimal('150.00'),
                'reliability_score': Decimal('4.20'),
            },
            {
                'name': 'Mega Distribuidora',
                'contact_person': 'Pedro Costa',
                'email': 'pedro@mega.com',
                'phone': '(11) 77777-7777',
                'address': 'Rua Comercial, 789 - São Paulo/SP',
                'delivery_time_days': 3,
                'minimum_order_value': Decimal('300.00'),
                'reliability_score': Decimal('4.80'),
            },
        ]


class Product(BaseModel):
    """
    Produtos do supermercado.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Nome'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Categoria'
    )
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Fornecedor'
    )
    
    # Preços
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço de Compra'
    )
    
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço de Venda'
    )
    
    # Estoque
    current_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Estoque Atual'
    )
    
    min_stock = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        verbose_name='Estoque Mínimo'
    )
    
    max_stock = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        verbose_name='Estoque Máximo'
    )
    
    # Validade
    shelf_life_days = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        verbose_name='Validade (dias)'
    )
    
    # Configurações de venda
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    
    is_promotional = models.BooleanField(
        default=False,
        verbose_name='Em Promoção'
    )
    
    promotional_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço Promocional'
    )
    
    promotional_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Início da Promoção'
    )
    
    promotional_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fim da Promoção'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['supplier', 'is_active']),
            models.Index(fields=['current_stock']),
        ]

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    @property
    def profit_margin(self):
        """Calcula a margem de lucro."""
        if self.sale_price <= 0:
            return Decimal('0.00')
        return ((self.sale_price - self.purchase_price) / self.sale_price) * 100

    @property
    def profit_margin_formatted(self):
        """Retorna a margem de lucro formatada."""
        return f"{self.profit_margin:.2f}%"

    @property
    def current_price(self):
        """Retorna o preço atual (promocional ou normal)."""
        if self.is_promotional and self.promotional_price:
            today = date.today()
            if (self.promotional_start_date and self.promotional_end_date and
                self.promotional_start_date <= today <= self.promotional_end_date):
                return self.promotional_price
        return self.sale_price

    @property
    def is_low_stock(self):
        """Verifica se o estoque está baixo."""
        return self.current_stock <= self.min_stock

    @property
    def is_out_of_stock(self):
        """Verifica se o produto está fora de estoque."""
        return self.current_stock <= 0

    @property
    def stock_status(self):
        """Retorna o status do estoque."""
        if self.is_out_of_stock:
            return 'OUT_OF_STOCK'
        elif self.is_low_stock:
            return 'LOW_STOCK'
        else:
            return 'NORMAL'

    def add_stock(self, quantity):
        """Adiciona quantidade ao estoque."""
        if quantity < 0:
            raise ValueError("Quantidade deve ser positiva")
        self.current_stock += quantity
        self.save()

    def remove_stock(self, quantity):
        """Remove quantidade do estoque."""
        if quantity < 0:
            raise ValueError("Quantidade deve ser positiva")
        if self.current_stock < quantity:
            raise ValueError("Estoque insuficiente")
        self.current_stock -= quantity
        self.save()

    def set_stock(self, quantity):
        """Define a quantidade do estoque."""
        if quantity < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self.current_stock = quantity
        self.save()


class ProductStockHistory(BaseModel):
    """
    Histórico de alterações no estoque de produtos.
    """
    OPERATION_CHOICES = [
        ('PURCHASE', 'Compra'),
        ('SALE', 'Venda'),
        ('ADJUSTMENT', 'Ajuste'),
        ('LOSS', 'Perda'),
        ('RETURN', 'Devolução'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_history',
        verbose_name='Produto'
    )
    
    operation = models.CharField(
        max_length=10,
        choices=OPERATION_CHOICES,
        verbose_name='Operação'
    )
    
    quantity = models.IntegerField(
        verbose_name='Quantidade'
    )
    
    previous_stock = models.IntegerField(
        verbose_name='Estoque Anterior'
    )
    
    new_stock = models.IntegerField(
        verbose_name='Novo Estoque'
    )
    
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Preço Unitário'
    )
    
    total_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor Total'
    )
    
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Descrição'
    )
    
    game_date = models.DateField(
        default=date.today,
        verbose_name='Data do Jogo'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Histórico de Estoque'
        verbose_name_plural = 'Históricos de Estoque'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operation} - {self.product.name} - {self.quantity} unidades"
