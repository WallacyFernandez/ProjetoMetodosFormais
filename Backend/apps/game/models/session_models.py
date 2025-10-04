"""
Modelos relacionados às sessões de jogo.
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
        ('NOT_STARTED', 'Não Iniciado'),
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
        max_length=12,
        choices=GAME_STATUS_CHOICES,
        default='NOT_STARTED',
        verbose_name='Status do Jogo'
    )
    
    # Configurações do jogo
    time_acceleration = models.IntegerField(
        default=20,  # 1 dia = 20 segundos (para testes)
        validators=[MinValueValidator(1), MaxValueValidator(10080)],  # Entre 1 min e 1 semana
        verbose_name='Aceleração do Tempo (segundos por dia)'
    )
    
    # Configurações de vendas automáticas
    daily_sales_target = models.IntegerField(
        default=40,
        verbose_name='Meta de Vendas Diárias'
    )
    auto_sales_enabled = models.BooleanField(
        default=True,
        verbose_name='Vendas Automáticas Habilitadas'
    )
    
    # Rastreamento de vendas do dia atual
    current_day_sales_count = models.IntegerField(
        default=0,
        verbose_name='Vendas do Dia Atual'
    )
    last_sales_reset_date = models.DateField(
        default=date.today,
        verbose_name='Última Data de Reset de Vendas'
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
        seconds_passed = time_diff.total_seconds()
        game_days_passed = int(seconds_passed / self.time_acceleration)
        
        if game_days_passed > 0:
            self.current_game_date += timedelta(days=game_days_passed)
            self.days_survived += game_days_passed
            # Atualiza last_update_time apenas quando há dias suficientes
            self.last_update_time = now
            self.save()
            
            # Processa vendas automáticas para cada dia que passou
            if self.auto_sales_enabled and self.status == 'ACTIVE':
                self.process_auto_sales(game_days_passed)
            
            # Verifica se o jogo terminou
            if self.current_game_date >= self.game_end_date:
                self.status = 'COMPLETED'
                self.save()
        
        # Processa vendas durante o dia atual (mesmo sem dias completos)
        # Só processa se passou pelo menos 1 segundo para evitar spam
        # IMPORTANTE: Depois da atualização da data para usar a data correta
        if self.auto_sales_enabled and self.status == 'ACTIVE' and seconds_passed >= 1:
            self.process_daily_sales(seconds_passed)
        
        return game_days_passed
    
    def process_daily_sales(self, seconds_passed):
        """Processa vendas durante o dia atual baseado no tempo decorrido."""
        from .product_models import Product
        from .history_models import ProductStockHistory, RealtimeSale
        from apps.finance.models import UserBalance, Transaction, Category
        from django.db import transaction
        import random
        from datetime import datetime
        
        # Calcula o progresso do dia (0-1)
        day_progress = (seconds_passed % self.time_acceleration) / self.time_acceleration
        
        # Calcula quantas vendas já deveriam ter acontecido hoje
        expected_sales_today = int(self.daily_sales_target * day_progress)
        
        # Reseta contador se mudou de dia
        if self.current_game_date != self.last_sales_reset_date:
            self.current_day_sales_count = 0
            self.last_sales_reset_date = self.current_game_date
            self.save()
        
        today_sales = self.current_day_sales_count
        
        # Se ainda não atingiu o número esperado de vendas, cria mais vendas
        if today_sales < expected_sales_today:
            sales_to_create = expected_sales_today - today_sales
            
            # Busca produtos disponíveis para venda
            available_products = Product.objects.filter(
                is_active=True,
                current_stock__gt=0
            ).select_related('category')
            
            if available_products.exists():
                with transaction.atomic():
                    # Obtém o saldo do usuário
                    user_balance = UserBalance.objects.get(user=self.user)
                    
                    # Obtém ou cria categoria de vendas
                    vendas_category, _ = Category.objects.get_or_create(
                        name='Vendas',
                        defaults={
                            'description': 'Receitas de vendas automáticas',
                            'color': '#10B981',
                            'icon': '💰'
                        }
                    )
                    
                    for _ in range(min(sales_to_create, 3)):  # Máximo 3 vendas por vez
                        # Seleciona produto aleatório
                        product = random.choice(list(available_products))
                        
                        # Quantidade aleatória para venda (1-3 unidades)
                        quantity = random.randint(1, min(3, product.current_stock))
                        
                        # Calcula receita
                        revenue = product.current_price * quantity
                        
                        # Remove do estoque
                        product.remove_stock(quantity)
                        
                        # Registra no histórico de estoque
                        ProductStockHistory.objects.create(
                            product=product,
                            operation='SALE',
                            quantity=quantity,
                            previous_stock=product.current_stock + quantity,
                            new_stock=product.current_stock,
                            total_value=revenue,
                            description=f'Venda automática - Dia {self.current_game_date}'
                        )
                        
                        # Calcula a hora do jogo atual
                        now = timezone.now()
                        game_time = RealtimeSale().get_game_time_from_real_time(now, self)
                        
                        # Só cria venda se o mercado estiver aberto (6h às 22h)
                        if RealtimeSale().is_market_open(game_time):
                            # Cria registro de venda em tempo real
                            RealtimeSale.objects.create(
                                game_session=self,
                                product=product,
                                quantity=quantity,
                                unit_price=product.current_price,
                                total_value=revenue,
                                sale_time=now,
                                game_date=self.current_game_date,
                                game_time=game_time
                            )
                        
                        # Adiciona receita ao saldo
                        user_balance.add_amount(revenue)
                        
                        # Cria transação financeira
                        Transaction.objects.create(
                            user=self.user,
                            category=vendas_category,
                            amount=revenue,
                            description=f'Venda: {product.name} ({quantity}x)',
                            transaction_type='INCOME'
                        )
                        
                        # Incrementa contador de vendas do dia
                        self.current_day_sales_count += 1
                        self.save()
    
    def process_auto_sales(self, days_passed):
        """Processa vendas automáticas para os dias que passaram."""
        from .product_models import Product
        from .history_models import ProductStockHistory, RealtimeSale
        from apps.finance.models import UserBalance, Transaction, Category
        from django.db import transaction
        import random
        from datetime import datetime, timedelta
        
        for day in range(days_passed):
            # Busca produtos disponíveis para venda
            available_products = Product.objects.filter(
                is_active=True,
                current_stock__gt=0
            ).select_related('category')
            
            if not available_products.exists():
                continue
            
            # Calcula quantos produtos vender neste dia
            products_to_sell = min(self.daily_sales_target, available_products.count())
            
            # Seleciona produtos aleatórios para venda
            products_for_sale = random.sample(
                list(available_products), 
                min(products_to_sell, len(available_products))
            )
            
            total_revenue = 0
            
            with transaction.atomic():
                # Obtém o saldo do usuário
                user_balance = UserBalance.objects.get(user=self.user)
                
                # Obtém ou cria categoria de vendas
                vendas_category, _ = Category.objects.get_or_create(
                    name='Vendas',
                    defaults={
                        'description': 'Receitas de vendas automáticas',
                        'color': '#10B981',
                        'icon': '💰'
                    }
                )
                
                for product in products_for_sale:
                    # Quantidade aleatória para venda (1-5 unidades)
                    quantity = random.randint(1, min(5, product.current_stock))
                    
                    # Calcula receita
                    revenue = product.current_price * quantity
                    total_revenue += revenue
                    
                    # Remove do estoque
                    product.remove_stock(quantity)
                    
                    # Registra no histórico de estoque
                    ProductStockHistory.objects.create(
                        product=product,
                        operation='SALE',
                        quantity=quantity,
                        previous_stock=product.current_stock + quantity,
                        new_stock=product.current_stock,
                        unit_price=product.current_price,
                        total_value=revenue,
                        description=f'Venda automática - Dia {self.current_game_date}'
                    )
                    
                    # Calcula a hora do jogo atual
                    now = timezone.now()
                    game_time = RealtimeSale().get_game_time_from_real_time(now, self)
                    
                    # Só cria venda se o mercado estiver aberto (6h às 22h)
                    if RealtimeSale().is_market_open(game_time):
                        # Cria registro de venda em tempo real
                        RealtimeSale.objects.create(
                            game_session=self,
                            product=product,
                            quantity=quantity,
                            unit_price=product.current_price,
                            total_value=revenue,
                            sale_time=now,
                            game_date=self.current_game_date,
                            game_time=game_time
                        )
                
                # Adiciona receita ao saldo
                if total_revenue > 0:
                    user_balance.add_amount(total_revenue)
                    
                    # Cria transação financeira
                    Transaction.objects.create(
                        user=self.user,
                        amount=total_revenue,
                        transaction_type='INCOME',
                        category=vendas_category,
                        description=f'Vendas automáticas - {products_to_sell} produtos vendidos',
                        transaction_date=self.current_game_date
                    )
    
    def get_game_progress(self):
        """Calcula o progresso do jogo em porcentagem."""
        total_days = (self.game_end_date - self.game_start_date).days
        current_days = (self.current_game_date - self.game_start_date).days
        return min(100, (current_days / total_days) * 100) if total_days > 0 else 0
    
    @property
    def days_remaining(self):
        """Calcula os dias restantes para o fim do jogo."""
        remaining = (self.game_end_date - self.current_game_date).days
        return max(0, remaining)
    
    def is_game_over(self):
        """Verifica se o jogo terminou."""
        return self.status in ['COMPLETED', 'FAILED']
    
    def start_game(self):
        """Inicia o jogo."""
        self.status = 'ACTIVE'
        self.session_start_time = timezone.now()
        self.last_update_time = timezone.now()
        self.save()
    
    def pause_game(self):
        """Pausa o jogo."""
        self.status = 'PAUSED'
        self.save()
    
    def resume_game(self):
        """Retoma o jogo."""
        self.status = 'ACTIVE'
        self.last_update_time = timezone.now()
        self.save()
    
    def reset_game(self):
        """Reinicia o jogo completamente."""
        from apps.finance.models import UserBalance, Transaction
        from django.db import transaction
        from .product_models import Product
        from .history_models import ProductStockHistory, RealtimeSale
        
        with transaction.atomic():
            # Resetar dados da sessão de jogo
            self.current_game_date = self.game_start_date
            self.days_survived = 0
            self.total_score = 0
            self.status = 'ACTIVE'
            self.session_start_time = timezone.now()
            self.last_update_time = timezone.now()
            self.current_day_sales_count = 0
            self.last_sales_reset_date = date.today()
            
            # Resetar saldo do usuário para R$ 10.000
            try:
                user_balance = UserBalance.objects.get(user=self.user)
                user_balance.current_balance = Decimal('10000.00')
                user_balance.save()
            except UserBalance.DoesNotExist:
                UserBalance.objects.create(
                    user=self.user,
                    current_balance=Decimal('10000.00')
                )
            
            # Limpar todas as transações financeiras do usuário
            Transaction.objects.filter(user=self.user).delete()
            
            # Limpar histórico de vendas em tempo real
            RealtimeSale.objects.filter(game_session=self).delete()
            
            # Resetar estoque de todos os produtos para valores iniciais
            # Valores padrão baseados nos produtos criados pelo comando create_default_data
            default_stock_values = {
                'Arroz 5kg': 50,
                'Feijão 1kg': 30,
                'Macarrão 500g': 40,
                'Coca-Cola 2L': 25,
                'Água Mineral 500ml': 60,
                'Detergente 500ml': 35,
                'Papel Higiênico 4 rolos': 20,
                'Carne Bovina 1kg': 15,
                'Frango Inteiro 1kg': 20,
                'Pão Francês': 100,
                'Bolo de Chocolate': 8,
            }
            
            for product in Product.objects.filter(is_active=True):
                # Usar valor padrão se disponível, senão usar 50% do estoque máximo
                default_stock = default_stock_values.get(product.name, max(10, product.max_stock // 2))
                product.current_stock = default_stock
                product.save()
            
            # Limpar histórico de estoque
            ProductStockHistory.objects.filter(product__is_active=True).delete()
            
            self.save()

