from django.core.management.base import BaseCommand
from apps.game.models import GameSession

class Command(BaseCommand):
    help = 'Corrige a aceleração do tempo das sessões de jogo para 3 minutos por dia.'

    def handle(self, *args, **options):
        # Atualiza todas as sessões para ter aceleração de 3 minutos por dia
        updated_count = GameSession.objects.filter(time_acceleration=1440).update(time_acceleration=3)
        
        self.stdout.write(
            self.style.SUCCESS(f'{updated_count} sessões de jogo atualizadas com aceleração de 3 minutos por dia.')
        )
