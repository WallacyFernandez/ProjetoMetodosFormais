"""
Modelos para o jogo Supermercado Simulator.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import date, datetime, timedelta
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager

User = get_user_model()


class GameSession(BaseModel):
    """
    Sessão de jogo do usuário.
    Controla o estado atual do jogo, incluindo tempo e progresso.
    """
    GAME_STATUS_CHOICES = [
        ('ACTIVE', 'Ativo'),
        ('PAUSED', 'Pausado'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Falhou'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='game_session',
        verbose_name='Usuário'
    )
    
    # Controle de tempo do jogo
    game_start_date = models.DateField(
        default=date(2025, 1, 1),
        verbose_name='Data de Início do Jogo'
    )
    current_game_date = models.DateField(
        default=date(2025, 1, 1),
        verbose_name='Data Atual do Jogo'
    )
    game_end_date = models.DateField(
        default=date(2026, 1, 1),
        verbose_name='Data de Fim do Jogo'
    )
    
    # Controle de tempo real
    session_start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Hora de Início da Sessão'
    )
    last_update_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Última Atualização'
    )
    
    # Estado do jogo
    status = models.CharField(
        max_length=10,
        choices=GAME_STATUS_CHOICES,
        default='ACTIVE',
        verbose_name='Status do Jogo'
    )
    
    # Configurações do jogo
    time_acceleration = models.IntegerField(
        default=1440,  # 1 dia = 1 minuto (1440 minutos por dia)
        validators=[MinValueValidator(1), MaxValueValidator(10080)],  # Entre 1 min e 1 semana
        verbose_name='Aceleração do Tempo (minutos por dia)'
    )
    
    # Progresso do jogo
    total_score = models.IntegerField(
        default=0,
        verbose_name='Pontuação Total'
    )
    days_survived = models.IntegerField(
        default=0,
        verbose_name='Dias Sobrevividos'
    )
    
    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Sessão de Jogo'
        verbose_name_plural = 'Sessões de Jogo'
        ordering = ['-last_update_time']

    def __str__(self):
        return f"Sessão de {self.user.full_name} - {self.current_game_date}"

    def update_game_time(self):
        """Atualiza o tempo do jogo baseado no tempo real decorrido."""
        now = timezone.now()
        time_diff = now - self.last_update_time
        
        # Calcula quantos dias do jogo passaram
        minutes_passed = time_diff.total_seconds() / 60
        game_days_passed = minutes_passed / self.time_acceleration
        
        if game_days_passed >= 1:
            days_to_add = int(game_days_passed)
            self.current_game_date += timedelta(days=days_to_add)
            self.days_survived += days_to_add
            self.last_update_time = now
            self.save()
            
            # Verifica se o jogo terminou
            if self.current_game_date >= self.game_end_date:
                self.status = 'COMPLETED'
                self.save()
            
            return days_to_add
        
        return 0

    def pause_game(self):
        """Pausa o jogo."""
        self.update_game_time()
        self.status = 'PAUSED'
        self.save()

    def resume_game(self):
        """Retoma o jogo."""
        self.status = 'ACTIVE'
        self.last_update_time = timezone.now()
        self.save()

    def reset_game(self):
        """Reinicia o jogo."""
        self.current_game_date = self.game_start_date
        self.days_survived = 0
        self.total_score = 0
        self.status = 'ACTIVE'
        self.session_start_time = timezone.now()
        self.last_update_time = timezone.now()
        self.save()

    @property
    def game_progress_percentage(self):
        """Retorna o progresso do jogo em porcentagem."""
        total_days = (self.game_end_date - self.game_start_date).days
        current_days = (self.current_game_date - self.game_start_date).days
        return min(100, (current_days / total_days) * 100)

    @property
    def days_remaining(self):
        """Retorna quantos dias restam no jogo."""
        return max(0, (self.game_end_date - self.current_game_date).days)


class SupermarketBalance(BaseModel):
    """
    Saldo do supermercado (caixa da loja).
    Substitui o UserBalance para o contexto do jogo.
    """
    game_session = models.OneToOneField(
        GameSession,
        on_delete=models.CASCADE,
        related_name='supermarket_balance',
        verbose_name='Sessão de Jogo'
    )
    
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('10000.00'),  # Capital inicial de R$ 10.000
        verbose_name='Saldo Atual'
    )
    
    # Limites e alertas
    minimum_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('1000.00'),  # Saldo mínimo para evitar falência
        verbose_name='Saldo Mínimo'
    )
    
    bankruptcy_threshold = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Limite de Falência'
    )
    
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Atualização'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Saldo do Supermercado'
        verbose_name_plural = 'Saldos dos Supermercados'
        ordering = ['-last_updated']

    def __str__(self):
        return f"Caixa do Supermercado: R$ {self.current_balance}"

    def add_amount(self, amount, description=""):
        """Adiciona um valor ao saldo atual."""
        if amount < 0:
            raise ValueError("Use subtract_amount() para valores negativos")
        
        previous_balance = self.current_balance
        self.current_balance += Decimal(str(amount))
        self.save()
        
        # Registra no histórico
        BalanceHistory.objects.create(
            supermarket_balance=self,
            operation='ADD',
            amount=amount,
            previous_balance=previous_balance,
            new_balance=self.current_balance,
            description=description
        )
        
        return self.current_balance

    def subtract_amount(self, amount, description=""):
        """Subtrai um valor do saldo atual."""
        if amount < 0:
            raise ValueError("Use add_amount() para valores positivos")
        
        previous_balance = self.current_balance
        self.current_balance -= Decimal(str(amount))
        self.save()
        
        # Verifica falência
        if self.current_balance <= self.bankruptcy_threshold:
            self.game_session.status = 'FAILED'
            self.game_session.save()
        
        # Registra no histórico
        BalanceHistory.objects.create(
            supermarket_balance=self,
            operation='SUBTRACT',
            amount=amount,
            previous_balance=previous_balance,
            new_balance=self.current_balance,
            description=description
        )
        
        return self.current_balance

    def set_balance(self, amount, description=""):
        """Define um novo valor para o saldo."""
        previous_balance = self.current_balance
        self.current_balance = Decimal(str(amount))
        self.save()
        
        # Registra no histórico
        BalanceHistory.objects.create(
            supermarket_balance=self,
            operation='SET',
            amount=amount,
            previous_balance=previous_balance,
            new_balance=self.current_balance,
            description=description
        )
        
        return self.current_balance

    @property
    def balance_formatted(self):
        """Retorna o saldo formatado em reais."""
        return f"R$ {self.current_balance:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def is_low_balance(self):
        """Verifica se o saldo está baixo."""
        return self.current_balance <= self.minimum_balance

    @property
    def is_bankrupt(self):
        """Verifica se o supermercado está falido."""
        return self.current_balance <= self.bankruptcy_threshold


class BalanceHistory(BaseModel):
    """
    Histórico de alterações no saldo do supermercado.
    """
    OPERATION_CHOICES = [
        ('ADD', 'Adição'),
        ('SUBTRACT', 'Subtração'),
        ('SET', 'Definição'),
        ('RESET', 'Reset'),
        ('SALE', 'Venda'),
        ('PURCHASE', 'Compra'),
        ('SALARY', 'Pagamento de Salário'),
        ('RENT', 'Aluguel'),
        ('UTILITY', 'Contas'),
    ]

    supermarket_balance = models.ForeignKey(
        SupermarketBalance,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Saldo do Supermercado'
    )
    
    operation = models.CharField(
        max_length=10,
        choices=OPERATION_CHOICES,
        verbose_name='Operação'
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor'
    )
    
    previous_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Saldo Anterior'
    )
    
    new_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Novo Saldo'
    )
    
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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
        verbose_name = 'Histórico de Saldo'
        verbose_name_plural = 'Históricos de Saldo'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operation} - R$ {self.amount} - {self.game_date}"


class ProductCategory(BaseModel):
    """
    Categorias de produtos do supermercado.
    Substitui Category para o contexto do jogo.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    
    icon = models.CharField(
        max_length=50,
        default='shopping-cart',
        verbose_name='Ícone'
    )
    
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        verbose_name='Cor'
    )
    
    # Configurações específicas do jogo
    profit_margin_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('10.00'),  # Margem mínima de 10%
        verbose_name='Margem de Lucro Mínima (%)'
    )
    
    profit_margin_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('50.00'),  # Margem máxima de 50%
        verbose_name='Margem de Lucro Máxima (%)'
    )
    
    # Durabilidade dos produtos (em dias)
    shelf_life_min = models.IntegerField(
        default=1,
        verbose_name='Validade Mínima (dias)'
    )
    
    shelf_life_max = models.IntegerField(
        default=30,
        verbose_name='Validade Máxima (dias)'
    )
    
    # Demanda sazonal
    seasonal_demand_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('1.00'),
        verbose_name='Multiplicador de Demanda Sazonal'
    )

    # Managers
    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Categoria de Produto'
        verbose_name_plural = 'Categorias de Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_categories(cls):
        """Retorna as categorias padrão do supermercado."""
        return [
            {
                'name': 'Alimentos',
                'description': 'Produtos alimentícios básicos',
                'icon': 'apple',
                'color': '#10B981',
                'profit_margin_min': 15.00,
                'profit_margin_max': 40.00,
                'shelf_life_min': 1,
                'shelf_life_max': 7,
            },
            {
                'name': 'Bebidas',
                'description': 'Refrigerantes, sucos e água',
                'icon': 'coffee',
                'color': '#3B82F6',
                'profit_margin_min': 20.00,
                'profit_margin_max': 60.00,
                'shelf_life_min': 30,
                'shelf_life_max': 365,
            },
            {
                'name': 'Limpeza',
                'description': 'Produtos de limpeza e higiene',
                'icon': 'droplet',
                'color': '#8B5CF6',
                'profit_margin_min': 25.00,
                'profit_margin_max': 70.00,
                'shelf_life_min': 365,
                'shelf_life_max': 1095,
            },
            {
                'name': 'Carnes',
                'description': 'Carnes e frios',
                'icon': 'meat',
                'color': '#EF4444',
                'profit_margin_min': 10.00,
                'profit_margin_max': 35.00,
                'shelf_life_min': 1,
                'shelf_life_max': 3,
            },
            {
                'name': 'Padaria',
                'description': 'Pães e produtos de padaria',
                'icon': 'bread',
                'color': '#F59E0B',
                'profit_margin_min': 20.00,
                'profit_margin_max': 50.00,
                'shelf_life_min': 1,
                'shelf_life_max': 5,
            },
        ]


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
