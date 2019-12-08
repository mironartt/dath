import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '*7ar99dfpax_d)-p1)uxxi$vd^kj62p9tc0la6hfd2$_=i9h!k'

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1',]

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'dath_db',
      'USER': 'dath_user',
      'PASSWORD': 'dath_password_NDw6zc2JvP',
      'HOST': 'localhost',
      'PORT': '5432',
    }
}

SITE_DOMAIN = 'http://127.0.0.1:8051/'
SITE_NAME = ''

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bebipaks@gmail.com'
EMAIL_HOST_PASSWORD = 'kama89132143636'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
MAIL_FOR_ALERT = 'wwwgigaton@yandex.ru'



"""
134.0.115.198
Логин: root
Пароль: apipT!_TStI4w3

ssh root@134.0.115.198
apipT!_TStI4w3

sshfs root@134.0.115.198:/ /home/truba/sshfs/server_1/

myuser  aa11223344

1.  обновление (под рутом)
apt-get update
apt-get upgrade

2. из-за непоняток с nginx, удалить apache и nginx

service nginx stop
sudo apt-get remove nginx nginx-common
sudo apt-get purge nginx nginx-common
sudo apt-get autoremove
whereis nginx     # проверяю есть ли какие либо оставшиеся папки

service apache2 stop
apt-get purge apache2 apache2-utils apache2.2-bin
apt-get autoremove
whereis apache2     # проверяю есть ли какие либо оставшиеся папки
rm -rf /etc/apache2

3. Ставлю nginx     # если все найс, то при переходи по ip должно быть приветствие от nginx
apt-get install nginx
service apache2 start

4. Cтавлю необходимые пакеты и постгрес
apt-get install python3-dev python3-setuptools python3 python3-pip virtualenvwrapper git nano supervisor python-pip python3-pip uwsgi uwsgi-plugin-python3 -y



nano /etc/apt/sources.list.d/pgdg.list
    deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
apt-get install postgresql-11
apt-get install libpq-dev postgresql-contrib


5. Cоздаю юзера  (ввожу пароль и тд)
adduser myuser

6. Добавляю юзера в судо и нужные группы
sudo adduser myuser www-data

nano /etc/sudoers
myuser  ALL=(ALL:ALL) ALL     # добавляю строчку и сохраняю

7. Даю права на все в папке юзера
sudo chmod 775 -R /home/myuser/


8. создаю нужные bd с нужными юзерами
sudo -u postgres psql
CREATE DATABASE li_battery_db;
CREATE USER li_battery_user WITH password 'li_battery_password';
GRANT ALL ON DATABASE li_battery_db TO li_battery_user;

9. авторизуюсь под созданным юзером
su myuser


10. перехожу в папку юзера качаю проект и поднимаю окружение с модулями. Структура папок: /hoome/myuser/www/ в ней окружение и клон с гита. Не забывать про local_settings.py
cd /home/myuser/
mkdir www
cd /home/myuser/www/

virtualenv -p python3 venv
git clone https://github.com/mironartt/libattery

source venv/bin/activate
cd libattery
mkdir deployment

pip install -r requirements.txt
pip install uwsgi


10.1  тесты если алгоритм рабочий, то они не будут нужны

-создаю тестовый файл
nano test.py
def application(env, start_response):
	start_response('200 OK', [('Content-Type','text/html')])
	return [b"Hello World"]

-тестирую uWSGI
uwsgi --http :8000 --wsgi-file test.py
-Если все работает, нажимаем ctrl-c, завершая процесс


-делаю миграции, создаю суперусера
python manage.py migrate
python manage.py createsuperuser
    admin
    aa11223344


-Тестирую запуск 
python manage.py runserver 0.0.0.0:8080

-собираю статику 
python manage.py collectstatic

-тестирую запус
uwsgi --http :8000 --module __PROJ_NAME___.wsgi



11. Собираю статику, делаю миграции, создаю суперюзера и тестовый запуск.
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
    admin
    aa11223344

uwsgi --http :8000 --module __PROJ_NAME___.wsgi
uwsgi --http :8000 --module libattery.wsgi   # если найс то дальше

+++
12. Конфигурирую nginx

    12.1    Перехожу в deployment
        cd deployment
    12.2 Создаю uwsgi_params
        nano uwsgi_params
    12.3 вставляю в него одно и тоже
        uwsgi_param  QUERY_STRING       $query_string;
        uwsgi_param  REQUEST_METHOD     $request_method;
        uwsgi_param  CONTENT_TYPE       $content_type;
        uwsgi_param  CONTENT_LENGTH     $content_length;
        
        uwsgi_param  REQUEST_URI        $request_uri;
        uwsgi_param  PATH_INFO          $document_uri;
        uwsgi_param  DOCUMENT_ROOT      $document_root;
        uwsgi_param  SERVER_PROTOCOL    $server_protocol;
        uwsgi_param  REQUEST_SCHEME     $scheme;
        uwsgi_param  HTTPS              $https if_not_empty;
        
        uwsgi_param  REMOTE_ADDR        $remote_addr;
        uwsgi_param  REMOTE_PORT        $remote_port;
        uwsgi_param  SERVER_PORT        $server_port;
        uwsgi_param  SERVER_NAME        $server_name;
    12.4 создаю параметры для nginx в my_site_nginx.conf
        nano my_site_nginx.conf
    12.5 вставляю в него 
    
    # the upstream component nginx needs to connect to
	upstream django {
	    server unix:///home/myuser/www/libattery/deployment/uwsgi_nginx.sock; # for a file socket
	    # server 127.0.0.1:8001; # for a web port socket (we'll use this first)
	}

	# configuration of the server
	server {
	    # the port your site will be served on
	    listen      80;
	    # the domain name it will serve for
	    server_name 127.0.0.1 134.0.115.198;    # my_site.ru; # substitute your machine's IP address or FQDN
	    charset     utf-8;

	    # max upload size
	    client_max_body_size 75M;   # adjust to taste

	    # Django media
	    location /media  {
		alias /home/myuser/www/libattery/static_public;  # your Django project's media files - amend as required
	    }

	    location /static {
		alias /home/myuser/www/libattery/static; # your Django project's static files - amend as required
	    }

	    # Finally, send all non-media requests to the Django server.
	    location / {
		uwsgi_pass  django;
		include     /home/myuser/www/libattery/deployment/uwsgi_params; # the uwsgi_params file you installed
	    }
	}

    12.6 перехожу в папку /etc/nginx/  создаю там папку 
        cd /etc/nginx/
        sudo mkdir sites-enabled
    
    12.7 В /etc/nginx/ в файле nginx.conf добавляю после строки:     include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
    
    12.8 создаю ссылку на файл mysite_nginx.conf, чтобы nginx увидел его
        sudo ln -s /home/myuser/www/libattery/deployment/my_site_nginx.conf /etc/nginx/sites-enabled/
        
    12.9 Перезапускаем nginx
    sudo /etc/init.d/nginx restart
    
    12.10 Тестирую статику nginx. Помещаю файл с именем, например, media.png в папку /home/myuser/www/libattery/static_public/HTB1IQBzcRjTBKNjSZFuq6z0HFXaz.jpg_q50.jpg
        http://134.0.115.198/media/HTB1IQBzcRjTBKNjSZFuq6z0HFXaz.jpg_q50.jpg
    
    12.TEST Пробую запустить через сокет
        uwsgi --socket uwsgi_nginx.sock --module libattery.wsgi --chmod-socket=666
        uwsgi --socket uwsgi_nginx.sock --module /home/myuser/www/libattery/libattery/wsgi.py --chmod-socket=666
        
    
    12.11 Создаю файл mysite_uwsgi.ini
        nano /home/myuser/www/libattery/deployment/mysite_uwsgi.ini
        
        #mysite_uwsgi.ini
        [uwsgi]
        
        # Настройки, связанные с Django
        # Корневая папка проекта (полный путь)
        chdir           = /home/myuser/www/libattery
        # Django wsgi файл
        module          = libattery.wsgi
        # полный путь к виртуальному окружению
        home            = /home/myuser/www/venv
        # общие настройки
        # master
        master          = true
        # максимальное количество процессов
        processes       = 10
        # полный путь к файлу сокета
        socket          = /home/myuser/www/libattery/deployment/uwsgi_nginx.sock
        # права доступа к файлу сокета
        chmod-socket    = 666
        # очищать окружение от служебных файлов uwsgi по завершению
        #vacuum          = true
        #env             = DEBUG_MODE=False
        #daemonize=/var/log/uwsgi/my_site.log
        plugins = python3        


    12.12 Пробую запустить глобально 
        sudo uwsgi --ini mysite_uwsgi.ini
        
13. Подключаю вассалов и супервизор
  
    13.1 Перехожу в /etc/uwsgi/
        cd /etc/uwsgi
        
    13.2 Создаю папку для конфигурационных файлов
        sudo mkdir /etc/uwsgi/vassals
    
    13.3 Создаю в ней ссылку на mysite_uwsgi.ini:
        sudo ln -s /home/myuser/www/libattery/deployment/mysite_uwsgi.ini /etc/uwsgi/vassals/
        
    13.4 Создаю файл конфигурации в папке etc/supervisor/conf.d/my_site.conf
        cd /etc/supervisor/conf.d/
        sudo nano supervisord.conf
        
        echo_supervisord_conf > /etc/supervisord.conf      # Непонятная команда     
        
        [program:my_site_libattery]
        command=uwsgi --emperor "/home/myuser/www/libattery/deployment/mysite_uwsgi.ini"
        stdout_logfile=/home/myuser/www/libattery/logs/uwsgi.log
        stderr_logfile=/home/myuser/www/libattery/logs/uwsgi_err.log
        autostart=true
        autorestart=true

      
  
    13.5 Индексирую этот файл под root в папке /etc/supervisor/ или /etc/supervisor/conf.d/
        echo_supervisord_conf > /etc/supervisord.conf      
        
        supervisorctl reread
        supervisorctl update
    
        service supervisor status

14. Финишные проверки

    sudo service supervisor stop
	sudo touch /home/myuser/www/libattery/deployment/mysite_uwsgi.ini
	sudo service supervisor start
    
"""
