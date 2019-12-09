# dath

db : 
    'NAME': 'dath_db',
    'USER': 'dath_user',
    'PASSWORD': 'dath_password_NDw6zc2JvP',


ЛОКАЛЬНОЕ РАЗВЕРТЫВАНИЕ

1. Создать postgres bd
    # для работы нужна установленная postgresql (https://www.postgresql.org/download/linux/ubuntu/)
    # создавть можно из под psql: sudo -u postgres psql
    CREATE DATABASE dath_db;
    CREATE USER dath_user WITH password 'dath_password_NDw6zc2JvP';
    GRANT ALL ON DATABASE dath_db TO dath_user;
    
2. Создать виртуалку
    в консоли:
    virtualenv -p python3 venv
    
3. Активировать виртуалку
    source venv/bin/activate
   
4.  Установить зависимости (~path корневая папка проекта)
    pip install -r requirements.txt
    

5.  Выполнить миграции (~path корневая папка проекта)
    python manage.py migrate


-Запустить локальный сервер (~path корневая папка проекта)
    python manage.py runserver 8000
    
-Вход в панель администратора:
    создать суперюзера:
        python manage.py createsuperuser
    войти под созданными логином и паролем
        http://localhost:8000/admin/
        
-для тестирования создать карты и юзеров если нужно
    python manage.py create_test_obj
    создасться 10 и 100 карточек и юзеров с рандомными данными
    
Валидация:
