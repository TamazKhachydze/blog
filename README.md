Репозиторий Блога на Django 3.
Установка (для пользователей операционных систем семейства Linux):

Открыть терминал или консоль и перейти в нужную Вам директорию
Прописать команду git clone git@github.com:TamazKhachydze/blog.git

Если Вы используете https, то: git clone https://github.com/TamazKhachydze/blog.git

Прописать следующие команды:


1. python3 -m venv ДиректорияВиртуальногоОкружения
2. source ДиректорияВиртуальногоОкружения/bin/activate
3. Перейти в директорию blog
4. pip install -r requirements.txt
5. python manage.py makemigrations   
6. python manage.py migrate
7. Запустить сервер - python manage.py runserver

Не забудьте создать директорию media, куда будут сохраняться изображения для товара