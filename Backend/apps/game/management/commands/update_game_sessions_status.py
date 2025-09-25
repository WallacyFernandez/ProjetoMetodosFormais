from django.core.management.base import BaseCommand
from apps.game.models import GameSession

class Command(BaseCommand):
    help = 'Atualiza o status das sessões de jogo existentes para NOT_STARTED.'

    def handle(self, *args, **options):
        # Atualiza todas as sessões com status ACTIVE para NOT_STARTED
        updated_count = GameSession.objects.filter(status='ACTIVE').update(status='NOT_STARTED')
        
        self.stdout.write(
            self.style.SUCCESS(f'{updated_count} sessões de jogo atualizadas para NOT_STARTED.')
        )
