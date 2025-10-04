"""
Comando para criar cargos padrão de funcionários.
"""

from django.core.management.base import BaseCommand
from apps.employees.models import EmployeePosition


class Command(BaseCommand):
    help = 'Cria cargos padrão para funcionários do supermercado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a criação mesmo se os cargos já existirem',
        )

    def handle(self, *args, **options):
        force = options['force']
        created_count = 0
        updated_count = 0

        for position_data in EmployeePosition.get_default_positions():
            position, created = EmployeePosition.objects.get_or_create(
                name=position_data['name'],
                defaults=position_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Cargo criado: {position.name}')
                )
            elif force:
                # Atualizar cargo existente
                for key, value in position_data.items():
                    setattr(position, key, value)
                position.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Cargo atualizado: {position.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Cargo já existe: {position.name}')
                )

        # Resumo
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Cargos criados: {created_count}')
        self.stdout.write(f'Cargos atualizados: {updated_count}')
        self.stdout.write(f'Total de cargos: {EmployeePosition.objects.count()}')
