from django.db import models
from django.utils import timezone

USERNAME_MAX_LENGTH = 100
BOOST_TYPE_MAX_LENGHT = 50

class Player(models.Model): # Лучше создать кастомную модель пользователя от AbstractUser
    """Игрок"""
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Имя пользователя"
    )
    first_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Момент первого входа"
    )

    def record_login(self):
        if not self.first_login:
            self.first_login = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username

class Boost(models.Model):
    """Игровые бусты"""
    BOOST_TYPES = (
        ('xp_boost', 'XP Boost'),
        ('time_boost', 'Time Boost'),
        ('speed_boost', 'Speed Boost'),
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='boosts',
        verbose_name="Игрок"
    )
    type = models.CharField(
        max_length=BOOST_TYPE_MAX_LENGHT,
        choices=BOOST_TYPES,
        verbose_name="Тип буста"
    )
    description = models.TimeField(
        verbose_name="Описание буста"
    )
    quantity = models.IntegerField(
        verbose_name="Количество буста"
    )

    @classmethod
    def award_boost(cls, player, boost_type, quantity=1):
        """Начисление бустов"""
        boost, created = cls.objects.get_or_create(player=player, type=boost_type)
        boost.quantity += quantity
        boost.save()
        return boost

    class Meta:
        verbose_name = 'Игровой буст',
        verbose_name_plural = 'Игровые бусты'

    def __str__(self):
        return f'{self.player} – {self.type}: {self.quantity}'
