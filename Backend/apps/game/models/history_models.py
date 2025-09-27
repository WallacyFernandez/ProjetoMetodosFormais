"""
Modelos relacionados ao histórico de operações.
"""

from django.db import models
from datetime import date
from apps.core.models import BaseModel, ActiveManager, AllObjectsManager


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

    product = models.ForeignKey('game.Product', on_delete=models.CASCADE, related_name='stock_history', verbose_name='Produto')
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES, verbose_name='Operação')
    quantity = models.IntegerField(verbose_name='Quantidade')
    previous_stock = models.IntegerField(verbose_name='Estoque Anterior')
    new_stock = models.IntegerField(verbose_name='Novo Estoque')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Preço Unitário')
    total_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Valor Total')
    description = models.CharField(max_length=255, blank=True, verbose_name='Descrição')
    game_date = models.DateField(default=date.today, verbose_name='Data do Jogo')

    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Histórico de Estoque'
        verbose_name_plural = 'Históricos de Estoque'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.operation} - {self.product.name} - {self.quantity} unidades"


class RealtimeSale(BaseModel):
    """
    Vendas em tempo real para exibição no frontend.
    """
    game_session = models.ForeignKey('game.GameSession', on_delete=models.CASCADE, related_name='realtime_sales', verbose_name='Sessão de Jogo')
    product = models.ForeignKey('game.Product', on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.IntegerField(verbose_name='Quantidade Vendida')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Preço Unitário')
    total_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor Total')
    sale_time = models.DateTimeField(verbose_name='Horário da Venda')
    game_date = models.DateField(default=date.today, verbose_name='Data do Jogo')
    game_time = models.TimeField(default='00:00:00', verbose_name='Hora do Jogo')

    objects = models.Manager()
    all_objects = AllObjectsManager()
    active = ActiveManager()

    class Meta:
        verbose_name = 'Venda em Tempo Real'
        verbose_name_plural = 'Vendas em Tempo Real'
        ordering = ['-sale_time']

    def __str__(self):
        return f"{self.product.name} - {self.quantity}x - R$ {self.total_value}"
    
    def get_game_time_from_real_time(self, real_time, game_session):
        """
        Calcula a hora do jogo baseada no tempo real decorrido.
        Um dia do jogo = time_acceleration segundos reais.
        Horário comercial: 6h às 22h (16 horas úteis por dia).
        """
        from datetime import time
        
        # Calcula quantos segundos se passaram desde o início do dia atual
        time_diff = real_time - game_session.last_update_time
        seconds_in_day = time_diff.total_seconds() % game_session.time_acceleration
        
        # Converte para hora do jogo considerando horário comercial (6h-22h = 16 horas úteis)
        # Mapeia os segundos para o horário comercial
        business_hours_ratio = seconds_in_day / game_session.time_acceleration
        
        # Converte para hora comercial (6h às 22h)
        business_hour = int(business_hours_ratio * 16) + 6  # 6h + (0-16 horas)
        business_minute = int((business_hours_ratio * 16 * 60) % 60)
        business_second = int((business_hours_ratio * 16 * 3600) % 60)
        
        # Garante que não passe das 22h
        if business_hour >= 22:
            business_hour = 22
            business_minute = 0
            business_second = 0
        
        return time(business_hour, business_minute, business_second)
    
    def is_market_open(self, game_time):
        """
        Verifica se o mercado está aberto no horário do jogo.
        Horário comercial: 6h às 22h.
        """
        return 6 <= game_time.hour < 22
