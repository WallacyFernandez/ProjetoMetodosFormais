from django.core.management.base import BaseCommand
from apps.game.models import GameSession

class Command(BaseCommand):
    help = 'Atualiza a aceleração do tempo das sessões de jogo para 20 segundos por dia.'

    def handle(self, *args, **options):
        # Atualiza todas as sessões para ter aceleração de 20 segundos por dia
        updated_count = GameSession.objects.all().update(time_acceleration=20)
        
        self.stdout.write(
            self.style.SUCCESS(f'{updated_count} sessões de jogo atualizadas com aceleração de 20 segundos por dia.')
        )
