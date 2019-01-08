Smirnov Test Bot
================

Smirnov Test Bot - это первый тестовый бот Антона Смирнова в рамках обучения на программе `Learn Python`_.
Бот умеет отправлять фотографии из папок, принимать координаты и контакты пользователя, а также общаться при помощи API `Dialogflow`_.

Установка
---------

Создайте виртуальное окружение и активируйте его. Затем выполните в вирутальном окружении:

.. code-block:: text

    pip install -r requirements.txt

Положите картинки в папку images. Название файлов картинок для кнопки "Прислать котика" должно начинаться с tar, а "Прислать бегемотика" с bad.
Все файлы с картнками должны иметь разрешение .jpg или .jpeg

Настройка
---------

Создайте файл settings.py и добавьте туда следующие настройки:

.. code-block:: python 

    PROXY = {'proxy_url': 'socks5://ВАШ_SOCKS5_ПРОКСИ:1080',
        'urllib3_proxy_kwargs': {'username': 'ЛОГИН', 'password': 'ПАРОЛЬ'}}


    API_KEY = "Api ключ, который вы получите от BotFather"

    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']  

    API_AI = 'Api ключ, который вы получите при регистрации в Dialogflow'

Запуск
------

В активированном виртуальном окружении выполните:

.. code-block:: text

    python bot2.py


.. _Learn Python: https://learn.python.ru/
.. _Dialogflow: https://dialogflow.com/