"""
Comando de management para limpar produtos de teste e criar produtos reais.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.game.models import Supplier, Product, ProductCategory
from decimal import Decimal


class Command(BaseCommand):
    help = 'Remove produtos de teste e cria uma gama completa de produtos reais'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a remoção de todos os produtos existentes',
        )

    def handle(self, *args, **options):
        """Executa o comando."""
        
        # Remove produtos de teste
        self.stdout.write('Removendo produtos de teste...')
        test_products = Product.objects.filter(
            name__icontains='teste'
        ) | Product.objects.filter(
            name__icontains='api test'
        ) | Product.objects.filter(
            category__name__icontains='teste'
        )
        
        test_count = test_products.count()
        if test_count > 0:
            test_products.delete()
            self.stdout.write(
                self.style.SUCCESS(f'{test_count} produtos de teste removidos.')
            )
        else:
            self.stdout.write('Nenhum produto de teste encontrado.')

        # Se --force, remove todos os produtos
        if options['force']:
            self.stdout.write('Removendo todos os produtos existentes...')
            Product.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Todos os produtos foram removidos.')
            )

        # Cria produtos reais
        self.stdout.write('Criando produtos reais...')
        self.create_real_products()
        self.stdout.write(
            self.style.SUCCESS('Produtos reais criados com sucesso.')
        )

    def create_real_products(self):
        """Cria uma gama completa de produtos reais."""
        try:
            with transaction.atomic():
                # Busca ou cria categorias
                categories = self.get_or_create_categories()
                
                # Busca fornecedores
                suppliers = self.get_suppliers()
                
                # Produtos reais por categoria
                products_data = self.get_products_data(categories, suppliers)
                
                # Cria os produtos
                for product_data in products_data:
                    Product.objects.create(**product_data)
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar produtos: {e}')
            )

    def get_or_create_categories(self):
        """Busca ou cria categorias de produtos."""
        categories_data = [
            {'name': 'Alimentos', 'icon': '🍞', 'color': '#F59E0B'},
            {'name': 'Bebidas', 'icon': '🥤', 'color': '#3B82F6'},
            {'name': 'Limpeza', 'icon': '🧽', 'color': '#8B5CF6'},
            {'name': 'Carnes', 'icon': '🥩', 'color': '#EF4444'},
            {'name': 'Padaria', 'icon': '🥖', 'color': '#F97316'},
            {'name': 'Frios e Laticínios', 'icon': '🧀', 'color': '#10B981'},
            {'name': 'Hortifruti', 'icon': '🥬', 'color': '#84CC16'},
            {'name': 'Congelados', 'icon': '🧊', 'color': '#06B6D4'},
            {'name': 'Doces e Snacks', 'icon': '🍫', 'color': '#F59E0B'},
            {'name': 'Higiene Pessoal', 'icon': '🧴', 'color': '#EC4899'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'description': f'Produtos da categoria {cat_data["name"]}'
                }
            )
            categories[cat_data['name']] = category
            
        return categories

    def get_suppliers(self):
        """Busca fornecedores existentes."""
        suppliers = {}
        for supplier in Supplier.objects.all():
            suppliers[supplier.name] = supplier
        return suppliers

    def get_products_data(self, categories, suppliers):
        """Retorna dados dos produtos reais."""
        products = []
        
        # Alimentos
        products.extend([
            {
                'name': 'Arroz Branco 5kg',
                'description': 'Arroz branco tipo 1, grão longo',
                'category': categories['Alimentos'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('15.50'),
                'sale_price': Decimal('22.90'),
                'current_stock': 45,
                'min_stock': 10,
                'max_stock': 100,
                'shelf_life_days': 365,
            },
            {
                'name': 'Feijão Carioca 1kg',
                'description': 'Feijão carioca selecionado',
                'category': categories['Alimentos'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('8.50'),
                'sale_price': Decimal('12.90'),
                'current_stock': 35,
                'min_stock': 8,
                'max_stock': 60,
                'shelf_life_days': 365,
            },
            {
                'name': 'Macarrão Espaguete 500g',
                'description': 'Macarrão espaguete tipo 8',
                'category': categories['Alimentos'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('3.80'),
                'sale_price': Decimal('5.90'),
                'current_stock': 50,
                'min_stock': 15,
                'max_stock': 80,
                'shelf_life_days': 730,
            },
            {
                'name': 'Açúcar Cristal 1kg',
                'description': 'Açúcar cristal refinado',
                'category': categories['Alimentos'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('4.20'),
                'sale_price': Decimal('6.50'),
                'current_stock': 40,
                'min_stock': 10,
                'max_stock': 70,
                'shelf_life_days': 730,
            },
            {
                'name': 'Óleo de Soja 900ml',
                'description': 'Óleo de soja refinado',
                'category': categories['Alimentos'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('5.50'),
                'sale_price': Decimal('8.90'),
                'current_stock': 30,
                'min_stock': 8,
                'max_stock': 50,
                'shelf_life_days': 365,
            },
        ])

        # Bebidas
        products.extend([
            {
                'name': 'Coca-Cola 2L',
                'description': 'Refrigerante Coca-Cola original',
                'category': categories['Bebidas'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('4.80'),
                'sale_price': Decimal('7.90'),
                'current_stock': 25,
                'min_stock': 5,
                'max_stock': 50,
                'shelf_life_days': 365,
            },
            {
                'name': 'Pepsi 2L',
                'description': 'Refrigerante Pepsi cola',
                'category': categories['Bebidas'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('4.50'),
                'sale_price': Decimal('7.50'),
                'current_stock': 20,
                'min_stock': 5,
                'max_stock': 40,
                'shelf_life_days': 365,
            },
            {
                'name': 'Água Mineral 500ml',
                'description': 'Água mineral sem gás',
                'category': categories['Bebidas'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('1.30'),
                'sale_price': Decimal('2.20'),
                'current_stock': 80,
                'min_stock': 20,
                'max_stock': 120,
                'shelf_life_days': 730,
            },
            {
                'name': 'Suco de Laranja 1L',
                'description': 'Suco de laranja natural',
                'category': categories['Bebidas'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('6.50'),
                'sale_price': Decimal('9.90'),
                'current_stock': 15,
                'min_stock': 5,
                'max_stock': 30,
                'shelf_life_days': 7,
            },
            {
                'name': 'Cerveja Skol 350ml',
                'description': 'Cerveja Skol lata',
                'category': categories['Bebidas'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('2.80'),
                'sale_price': Decimal('4.50'),
                'current_stock': 60,
                'min_stock': 15,
                'max_stock': 100,
                'shelf_life_days': 180,
            },
        ])

        # Limpeza
        products.extend([
            {
                'name': 'Detergente Líquido 500ml',
                'description': 'Detergente líquido concentrado',
                'category': categories['Limpeza'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('2.80'),
                'sale_price': Decimal('4.90'),
                'current_stock': 40,
                'min_stock': 10,
                'max_stock': 70,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Papel Higiênico 4 rolos',
                'description': 'Papel higiênico macio 3 folhas',
                'category': categories['Limpeza'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('8.50'),
                'sale_price': Decimal('14.90'),
                'current_stock': 25,
                'min_stock': 8,
                'max_stock': 50,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Sabão em Pó 1kg',
                'description': 'Sabão em pó para roupas',
                'category': categories['Limpeza'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('12.50'),
                'sale_price': Decimal('19.90'),
                'current_stock': 20,
                'min_stock': 5,
                'max_stock': 40,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Amaciante 1L',
                'description': 'Amaciante de roupas',
                'category': categories['Limpeza'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('8.90'),
                'sale_price': Decimal('14.50'),
                'current_stock': 18,
                'min_stock': 5,
                'max_stock': 35,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Desinfetante 1L',
                'description': 'Desinfetante multiuso',
                'category': categories['Limpeza'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('6.50'),
                'sale_price': Decimal('10.90'),
                'current_stock': 22,
                'min_stock': 8,
                'max_stock': 45,
                'shelf_life_days': 1095,
            },
        ])

        # Carnes
        products.extend([
            {
                'name': 'Carne Bovina Patinho 1kg',
                'description': 'Carne bovina patinho fresca',
                'category': categories['Carnes'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('28.50'),
                'sale_price': Decimal('39.90'),
                'current_stock': 12,
                'min_stock': 3,
                'max_stock': 25,
                'shelf_life_days': 3,
            },
            {
                'name': 'Frango Inteiro 1kg',
                'description': 'Frango inteiro congelado',
                'category': categories['Carnes'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('13.50'),
                'sale_price': Decimal('19.90'),
                'current_stock': 18,
                'min_stock': 5,
                'max_stock': 35,
                'shelf_life_days': 7,
            },
            {
                'name': 'Linguiça Toscana 500g',
                'description': 'Linguiça toscana temperada',
                'category': categories['Carnes'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('12.90'),
                'sale_price': Decimal('18.90'),
                'current_stock': 15,
                'min_stock': 5,
                'max_stock': 30,
                'shelf_life_days': 5,
            },
            {
                'name': 'Peito de Frango 1kg',
                'description': 'Peito de frango sem osso',
                'category': categories['Carnes'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('18.90'),
                'sale_price': Decimal('26.90'),
                'current_stock': 10,
                'min_stock': 3,
                'max_stock': 20,
                'shelf_life_days': 3,
            },
        ])

        # Padaria
        products.extend([
            {
                'name': 'Pão Francês',
                'description': 'Pão francês fresco',
                'category': categories['Padaria'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('0.85'),
                'sale_price': Decimal('1.30'),
                'current_stock': 120,
                'min_stock': 30,
                'max_stock': 200,
                'shelf_life_days': 1,
            },
            {
                'name': 'Bolo de Chocolate',
                'description': 'Bolo de chocolate caseiro',
                'category': categories['Padaria'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('16.50'),
                'sale_price': Decimal('27.90'),
                'current_stock': 6,
                'min_stock': 2,
                'max_stock': 12,
                'shelf_life_days': 3,
            },
            {
                'name': 'Croissant',
                'description': 'Croissant de manteiga',
                'category': categories['Padaria'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('3.50'),
                'sale_price': Decimal('5.90'),
                'current_stock': 25,
                'min_stock': 8,
                'max_stock': 40,
                'shelf_life_days': 2,
            },
            {
                'name': 'Pão de Açúcar',
                'description': 'Pão doce com açúcar',
                'category': categories['Padaria'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('2.80'),
                'sale_price': Decimal('4.50'),
                'current_stock': 20,
                'min_stock': 5,
                'max_stock': 35,
                'shelf_life_days': 2,
            },
        ])

        # Frios e Laticínios
        products.extend([
            {
                'name': 'Leite Integral 1L',
                'description': 'Leite integral pasteurizado',
                'category': categories['Frios e Laticínios'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('4.20'),
                'sale_price': Decimal('6.90'),
                'current_stock': 35,
                'min_stock': 10,
                'max_stock': 60,
                'shelf_life_days': 7,
            },
            {
                'name': 'Queijo Mussarela 200g',
                'description': 'Queijo mussarela fatiado',
                'category': categories['Frios e Laticínios'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('8.90'),
                'sale_price': Decimal('14.90'),
                'current_stock': 18,
                'min_stock': 5,
                'max_stock': 30,
                'shelf_life_days': 10,
            },
            {
                'name': 'Presunto Cozido 200g',
                'description': 'Presunto cozido fatiado',
                'category': categories['Frios e Laticínios'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('9.50'),
                'sale_price': Decimal('15.90'),
                'current_stock': 15,
                'min_stock': 5,
                'max_stock': 25,
                'shelf_life_days': 7,
            },
            {
                'name': 'Iogurte Natural 500g',
                'description': 'Iogurte natural cremoso',
                'category': categories['Frios e Laticínios'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('5.80'),
                'sale_price': Decimal('9.50'),
                'current_stock': 25,
                'min_stock': 8,
                'max_stock': 40,
                'shelf_life_days': 7,
            },
        ])

        # Hortifruti
        products.extend([
            {
                'name': 'Banana Prata kg',
                'description': 'Banana prata por quilo',
                'category': categories['Hortifruti'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('3.50'),
                'sale_price': Decimal('5.90'),
                'current_stock': 30,
                'min_stock': 10,
                'max_stock': 50,
                'shelf_life_days': 7,
            },
            {
                'name': 'Tomate kg',
                'description': 'Tomate vermelho por quilo',
                'category': categories['Hortifruti'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('4.80'),
                'sale_price': Decimal('7.90'),
                'current_stock': 25,
                'min_stock': 8,
                'max_stock': 40,
                'shelf_life_days': 5,
            },
            {
                'name': 'Cebola kg',
                'description': 'Cebola branca por quilo',
                'category': categories['Hortifruti'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('2.90'),
                'sale_price': Decimal('4.90'),
                'current_stock': 35,
                'min_stock': 10,
                'max_stock': 60,
                'shelf_life_days': 15,
            },
            {
                'name': 'Alface Unidade',
                'description': 'Alface crespa unidade',
                'category': categories['Hortifruti'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('1.80'),
                'sale_price': Decimal('2.90'),
                'current_stock': 20,
                'min_stock': 8,
                'max_stock': 35,
                'shelf_life_days': 3,
            },
        ])

        # Congelados
        products.extend([
            {
                'name': 'Pizza Margherita 400g',
                'description': 'Pizza margherita congelada',
                'category': categories['Congelados'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('12.90'),
                'sale_price': Decimal('19.90'),
                'current_stock': 15,
                'min_stock': 5,
                'max_stock': 25,
                'shelf_life_days': 90,
            },
            {
                'name': 'Hambúrguer 4 unidades',
                'description': 'Hambúrguer bovino congelado',
                'category': categories['Congelados'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('8.50'),
                'sale_price': Decimal('13.90'),
                'current_stock': 20,
                'min_stock': 8,
                'max_stock': 35,
                'shelf_life_days': 60,
            },
            {
                'name': 'Sorvete Napolitano 1L',
                'description': 'Sorvete napolitano cremoso',
                'category': categories['Congelados'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('8.90'),
                'sale_price': Decimal('14.90'),
                'current_stock': 12,
                'min_stock': 3,
                'max_stock': 20,
                'shelf_life_days': 90,
            },
        ])

        # Doces e Snacks
        products.extend([
            {
                'name': 'Chocolate ao Leite 100g',
                'description': 'Chocolate ao leite cremoso',
                'category': categories['Doces e Snacks'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('4.50'),
                'sale_price': Decimal('7.50'),
                'current_stock': 30,
                'min_stock': 10,
                'max_stock': 50,
                'shelf_life_days': 180,
            },
            {
                'name': 'Biscoito Recheado 130g',
                'description': 'Biscoito recheado sabor chocolate',
                'category': categories['Doces e Snacks'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('3.20'),
                'sale_price': Decimal('5.50'),
                'current_stock': 40,
                'min_stock': 15,
                'max_stock': 70,
                'shelf_life_days': 120,
            },
            {
                'name': 'Salgadinho 80g',
                'description': 'Salgadinho de milho temperado',
                'category': categories['Doces e Snacks'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('2.80'),
                'sale_price': Decimal('4.90'),
                'current_stock': 35,
                'min_stock': 12,
                'max_stock': 60,
                'shelf_life_days': 90,
            },
        ])

        # Higiene Pessoal
        products.extend([
            {
                'name': 'Shampoo 400ml',
                'description': 'Shampoo para todos os tipos de cabelo',
                'category': categories['Higiene Pessoal'],
                'supplier': list(suppliers.values())[0],
                'purchase_price': Decimal('8.90'),
                'sale_price': Decimal('14.90'),
                'current_stock': 20,
                'min_stock': 5,
                'max_stock': 35,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Sabonete 90g',
                'description': 'Sabonete líquido hidratante',
                'category': categories['Higiene Pessoal'],
                'supplier': list(suppliers.values())[1],
                'purchase_price': Decimal('3.50'),
                'sale_price': Decimal('5.90'),
                'current_stock': 45,
                'min_stock': 15,
                'max_stock': 70,
                'shelf_life_days': 1095,
            },
            {
                'name': 'Creme Dental 90g',
                'description': 'Creme dental com flúor',
                'category': categories['Higiene Pessoal'],
                'supplier': list(suppliers.values())[2],
                'purchase_price': Decimal('4.20'),
                'sale_price': Decimal('7.50'),
                'current_stock': 30,
                'min_stock': 10,
                'max_stock': 50,
                'shelf_life_days': 1095,
            },
        ])

        return products
