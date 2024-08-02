import csv
from django.db import models
from django.utils import timezone


class Player(models.Model):
    """Пользователь"""
    player_id = models.CharField(max_length=100) 
    # 1. ID создается автоматически, лучше назвать поле по-другому
    
    
class Level(models.Model):
    """Уровень"""
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0) 
    # 1. Лучше добавить уникальность поля order,
    # чтобы не было, например, несколько седьмых уровней.
    # 2. Также лучше добавить максимально возможное количество очков,
    # которое можно получить за прохождение уровня
    
    
class Prize(models.Model):
    """Приз"""
    title = models.CharField(max_length=100) 
    # Нужно обязательно добавить параметр max_length, добавил
    
    
class PlayerLevel(models.Model):
    """Прогресс пользователя на определенном уровне"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    # Поле is_completed можно убрать, так как уже есть completed
    # Completed либо пустое (null=True), либо уже с датой прохождения
    
    def assign_prize(self):
        if self.is_completed:
            level_prizes = LevelPrize.objects.filter(level=self.level) # нашли все призы, которые положены за данный уровень
            for level_prize in level_prizes:
                PlayerPrize.objects.create(player=self.player, prize=level_prize.prize, received=timezone.now()) # добавили призы пользователю

class LevelPrize(models.Model):
    """Выдаваемый приз за прохождение уровня"""
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()
    # Тут мне поле received кажется лишним,
    # так как данная модель должна связывать только уровень и приз.
    # Функция данного класса – показать, какой приз нужно отдать и за какой уровень

# Лучше и логичнее будет создать модель, которая связывает пользователя и призы
class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(null=True, blank=True)


def export_player_data_to_csv(): # Эта функция работает корректно с обновленными классами, показано в проекте
    """Функция для выгрузки данных в SCV файл"""
    print('Выгрузка началась')
    filename = 'player_data.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Player ID', 'Level Title', 'Completed', 'Prize Title'])
        users = Player.objects.prefetch_related('playerlevel_set__level', 'playerprize_set__prize')
        levels = Level.objects.prefetch_related('levelprize_set__prize')
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
