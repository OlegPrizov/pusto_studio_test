from django.core.management.base import BaseCommand

from ...models import User, Level, Prize, PlayerLevel, LevelPrize

USERS = (
    ('first user', 'firstuser@gmail.com'),
    ('second user', 'seconduser@gmail.com'),
    ('third user', 'thirduser@gmail.com'),
    ('fourth user', 'fourthuser@gmail.com'),
    )

LEVELS = (
    ('first level', 1),
    ('second level', 2)
)

PRIZES = (
    'XP boost',
    'Time boost',
    '10 coins'
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Загрузка началась')
        for user in USERS:
            User.objects.create(username=user[0], email=user[1])
        for level in LEVELS:
            Level.objects.create(title=level[0], order=level[1])
        for prize in PRIZES:
            Prize.objects.create(title=prize)
        user_1 = User.objects.get(id=1)
        user_2 = User.objects.get(id=2)
        user_3 = User.objects.get(id=3)
        user_4 = User.objects.get(id=4)
        level_1 = Level.objects.get(id=1)
        level_2 = Level.objects.get(id=2)
        prize_1 = Prize.objects.get(id=1)
        prize_2 = Prize.objects.get(id=2)
        prize_3 = Prize.objects.get(id=3)
        PlayerLevel.objects.create(player=user_1, level=level_1, completed='2024-08-01', is_completed=True, score=100)
        PlayerLevel.objects.create(player=user_1, level=level_2, completed='2024-08-02', is_completed=True, score=200)
        PlayerLevel.objects.create(player=user_2, level=level_2, completed='2024-08-01', is_completed=True, score=50)
        PlayerLevel.objects.create(player=user_3, level=level_1, completed='2024-08-01', is_completed=True, score=80)
        LevelPrize.objects.create(level=level_1, prize=prize_1)
        LevelPrize.objects.create(level=level_2, prize=prize_2)
        LevelPrize.objects.create(level=level_2, prize=prize_3)
        for object in PlayerLevel.objects.all():
            object.assign_prize()
        print('Загрузка закончилась')
