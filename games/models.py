from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()
    
    
class Level(models.Model):
    """Уровень"""
    title = models.CharField(max_length=100, verbose_name="Название уровня")
    order = models.IntegerField(default=0, unique=True, verbose_name="Порядковый номер уровня") 

    class Meta:
        verbose_name = 'Уровень',
        verbose_name_plural = 'Уровни'
    
    def __str__(self):
        return self.title


class Prize(models.Model):
    """Приз"""
    title = models.CharField(max_length=100, verbose_name="Название приза")

    class Meta:
        verbose_name = 'Приз',
        verbose_name_plural = 'Призы'
    
    def __str__(self):
        return self.title
    
    
class PlayerLevel(models.Model):
    """Прогресс пользователя на определенном уровне"""
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='levels')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='players')
    completed = models.DateField(verbose_name="Момент прохождения уровня")
    is_completed = models.BooleanField(default=False, verbose_name="Статус прохождения")
    score = models.PositiveIntegerField(default=0, verbose_name="Количество очков")
    
    def assign_prize(self):
        """Присуждение приза"""
        if self.is_completed:
            level_prizes = LevelPrize.objects.filter(level=self.level) # нашли все призы, которые положены за данный уровень
            for level_prize in level_prizes:
                PlayerPrize.objects.create(player=self.player, prize=level_prize.prize, received=timezone.now()) # добавили призы пользователю


class LevelPrize(models.Model):
    """Выдаваемый за прохождение уровня приз"""
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Приз за уровень',
        verbose_name_plural = 'Призы за уровень'
    
    def __str__(self):
        return f'{self.level} – {self.prize}'

class PlayerPrize(models.Model):
    """Призы игрока"""
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Приз игрока',
        verbose_name_plural = 'Призы игрока'
    
    def __str__(self):
        return f'{self.level} – {self.prize}'