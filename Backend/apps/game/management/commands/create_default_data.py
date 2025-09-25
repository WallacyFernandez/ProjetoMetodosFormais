"""
Comando de management para criar fornecedores e produtos padrão.
"""

from django.core.management.base import BaseCommand
from apps.game.models import Supplier, Product, ProductCategory


class Command(BaseCommand):
    help = 'Cria fornecedores e produtos padrão para o jogo'

    def handle(self, *args, **options):
        """Executa o comando."""
        
        # Cria fornecedores padrão se não existirem
        if not Supplier.objects.exists():
            self.stdout.write('Criando fornecedores padrão...')
            for supplier_data in Supplier.get_default_suppliers():
                Supplier.objects.create(**supplier_data)
            self.stdout.write(
                self.style.SUCCESS('Fornecedores padrão criados com sucesso.')
            )
        else:
            self.stdout.write('Fornecedores já existem.')
        
        # Cria produtos padrão se não existirem
        if not Product.objects.exists():
            self.stdout.write('Criando produtos padrão...')
            self.create_default_products()
            self.stdout.write(
                self.style.SUCCESS('Produtos padrão criados com sucesso.')
            )
        else:
            self.stdout.write('Produtos já existem.')

    def create_default_products(self):
        """Cria produtos padrão para o supermercado."""
        try:
            # Busca categorias e fornecedores
            alimentos = ProductCategory.objects.get(name='Alimentos')
            bebidas = ProductCategory.objects.get(name='Bebidas')
            limpeza = ProductCategory.objects.get(name='Limpeza')
            carnes = ProductCategory.objects.get(name='Carnes')
            padaria = ProductCategory.objects.get(name='Padaria')
            
            central = Supplier.objects.get(name='Distribuidora Central')
            express = Supplier.objects.get(name='Fornecedor Express')
            mega = Supplier.objects.get(name='Mega Distribuidora')
            
            # Produtos padrão
            default_products = [
                # Alimentos
                {
                    'name': 'Arroz 5kg',
                    'description': 'Arroz branco tipo 1',
                    'category': alimentos,
                    'supplier': central,
                    'purchase_price': 15.00,
                    'sale_price': 22.50,
                    'current_stock': 50,
                    'min_stock': 10,
                    'max_stock': 100,
                    'shelf_life_days': 365,
                },
                {
                    'name': 'Feijão 1kg',
                    'description': 'Feijão carioca',
                    'category': alimentos,
                    'supplier': central,
                    'purchase_price': 8.00,
                    'sale_price': 12.00,
                    'current_stock': 30,
                    'min_stock': 5,
                    'max_stock': 50,
                    'shelf_life_days': 365,
                },
                {
                    'name': 'Macarrão 500g',
                    'description': 'Macarrão espaguete',
                    'category': alimentos,
                    'supplier': express,
                    'purchase_price': 3.50,
                    'sale_price': 5.25,
                    'current_stock': 40,
                    'min_stock': 10,
                    'max_stock': 80,
                    'shelf_life_days': 730,
                },
                
                # Bebidas
                {
                    'name': 'Coca-Cola 2L',
                    'description': 'Refrigerante Coca-Cola',
                    'category': bebidas,
                    'supplier': mega,
                    'purchase_price': 4.50,
                    'sale_price': 7.50,
                    'current_stock': 25,
                    'min_stock': 5,
                    'max_stock': 50,
                    'shelf_life_days': 365,
                },
                {
                    'name': 'Água Mineral 500ml',
                    'description': 'Água mineral sem gás',
                    'category': bebidas,
                    'supplier': express,
                    'purchase_price': 1.20,
                    'sale_price': 2.00,
                    'current_stock': 60,
                    'min_stock': 20,
                    'max_stock': 100,
                    'shelf_life_days': 730,
                },
                
                # Limpeza
                {
                    'name': 'Detergente 500ml',
                    'description': 'Detergente líquido',
                    'category': limpeza,
                    'supplier': central,
                    'purchase_price': 2.50,
                    'sale_price': 4.50,
                    'current_stock': 35,
                    'min_stock': 10,
                    'max_stock': 60,
                    'shelf_life_days': 1095,
                },
                {
                    'name': 'Papel Higiênico 4 rolos',
                    'description': 'Papel higiênico macio',
                    'category': limpeza,
                    'supplier': mega,
                    'purchase_price': 8.00,
                    'sale_price': 14.00,
                    'current_stock': 20,
                    'min_stock': 5,
                    'max_stock': 40,
                    'shelf_life_days': 1095,
                },
                
                # Carnes
                {
                    'name': 'Carne Bovina 1kg',
                    'description': 'Carne bovina patinho',
                    'category': carnes,
                    'supplier': central,
                    'purchase_price': 25.00,
                    'sale_price': 35.00,
                    'current_stock': 15,
                    'min_stock': 5,
                    'max_stock': 30,
                    'shelf_life_days': 3,
                },
                {
                    'name': 'Frango Inteiro 1kg',
                    'description': 'Frango inteiro congelado',
                    'category': carnes,
                    'supplier': express,
                    'purchase_price': 12.00,
                    'sale_price': 18.00,
                    'current_stock': 20,
                    'min_stock': 5,
                    'max_stock': 40,
                    'shelf_life_days': 7,
                },
                
                # Padaria
                {
                    'name': 'Pão Francês',
                    'description': 'Pão francês fresco',
                    'category': padaria,
                    'supplier': express,
                    'purchase_price': 0.80,
                    'sale_price': 1.20,
                    'current_stock': 100,
                    'min_stock': 20,
                    'max_stock': 200,
                    'shelf_life_days': 1,
                },
                {
                    'name': 'Bolo de Chocolate',
                    'description': 'Bolo de chocolate caseiro',
                    'category': padaria,
                    'supplier': central,
                    'purchase_price': 15.00,
                    'sale_price': 25.00,
                    'current_stock': 8,
                    'min_stock': 2,
                    'max_stock': 15,
                    'shelf_life_days': 3,
                },
            ]
            
            for product_data in default_products:
                Product.objects.create(**product_data)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar produtos padrão: {e}')
            )
