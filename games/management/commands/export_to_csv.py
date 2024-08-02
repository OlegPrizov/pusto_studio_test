import csv
from django.core.management.base import BaseCommand

from ...models import User, Level

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Выгрузка началась')
        filename = 'player_data.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Player ID', 'Level Title', 'Completed', 'Prize Title'])
            users = User.objects.prefetch_related('levels', 'playerprize_set')
            levels = Level.objects.prefetch_related('levelprize_set')
            for user in users:
                user_levels = {pl.level.id: pl for pl in user.levels.all()}
                for level in levels:
                    if level.id in user_levels:
                        player_level = user_levels[level.id]
                        player_id = user.id
                        level_title = level.title
                        completed = player_level.completed if player_level.is_completed else 'Not Completed'
                        level_prizes = set(lp.prize_id for lp in level.levelprize_set.all())
                        prize_titles = [prize.prize.title for prize in user.playerprize_set.all() if prize.prize_id in level_prizes]
                        if prize_titles:
                            for prize_title in prize_titles:
                                writer.writerow([player_id, level_title, completed, prize_title])
                        else:
                            writer.writerow([player_id, level_title, completed, 'No Prize'])
                    else:
                        writer.writerow([user.id, level.title, 'Not Completed', 'No Prize'])      
        print('Выгрузка закончилась')
