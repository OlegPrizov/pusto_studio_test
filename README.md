# pusto_studio_test

## Описание
Тестовое задание для Pusto Studio. В директории **tasks** есть два файла, где описано решение заданий.
Все остальное необходимо для разворачивания реального проекта и демонстрации.

В проекте имеются 2 доступные команды для демонстрации:
1. python manage.py data_filler – заполняет БД тестовыми данными
2. python manahe.py export_to_csv – сохраняет CSV файл с данными об игроках, их пройденных уровнях и призах

### Описание тестовых данных
1. 4 пользователя:
    1. первый прошел все уровни
    2. второй – только второй уровень
    3. третий – только первый уровень
    4. четвертый не прошел ничего
2. 2 уровня (за первый уровень положен один приз, за второй – два приза)
3. Три приза (XP boost, Time boost, 10 coins)

## Демонстрация
[Нажмите, чтобы перейти к демонстрации](https://drive.google.com/drive/folders/1YYZ96CCMHa3n8VrfJuIcVJGvW7-CgPcb?usp=sharing)

## Установка проекта

1. Скопируйте репозиторий и перейдите в него
```
git clone git@github.com:OlegPrizov/pusto_studio_test.git
cd pusto_studio_test/
```

2. Установите и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
```

3. Установите нужные библиотеки
```
pip install -r requirements.txt
```

4. Создайте и активируйте миграции
```
python manage.py makemigrations
python manage.py migrate
```

5. Заполните БД тестовыми данными
```
python manage.py data_filler
```

6. Выгрузите данные, они появятся в корневой директории проекта
```
python manage.py export to csv
```

## Автор
[Призов Олег](https://github.com/OlegPrizov)