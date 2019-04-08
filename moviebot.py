import vk_api
import random
import lxml.html
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": get_random_id()})

def write_new_movie(user_id):
    vk_session.method("messages.send", {"user_id": user_id, "message": get_new_movie(), "random_id": get_random_id()})

def get_new_movie():
    page = requests.get('https://perm.kinoafisha.info/cinema/4283797/').text
    parser = lxml.html.fromstring(page)

    # Получение списка названий фильмов
    movie_name = parser.xpath('.//div[@class = "films_right"]/a/span/span/text()')

    # Получение списка жанров фильмов
    movie_genre = parser.xpath('.//span[@class = "films_info"]/text()')

    # Получение списка ссылок на фильмы
    movie_link = parser.xpath('.//div[@class = "films_right"]/a/@href')

    movie_info = parser.xpath('.//div[@class = "showtimes_cell"]')

    movie_format = []
    movie_time = []
    movie_price = []
    for i in range(len(movie_info)):
        if (i % 2 != 0 and i > 3):

            format = []
            time = []
            temp_time = []
            price = []
            temp_price = []
            flag = 1

            for child in movie_info[i].iter():
                if child.get('class') == "showtimes_format":
                    if (flag == 0):
                        time.append(temp_time)
                        price.append(temp_price)
                        temp_time = []
                        temp_price = []
                    format.append(child.text)
                    flag = 0
                if child.get('class') == "session_time":
                    temp_time.append(child.text)
                if child.get('class') == "session_price":
                    temp_price.append(child.text)

            time.append(temp_time)
            price.append(temp_price)

            movie_format.append(format)
            movie_time.append(time)
            movie_price.append(price)

    mystr = ""

    for i in range(len(movie_name)):
        mystr = mystr + movie_name[i] + "\n" + "Жанр: " + movie_genre[i] + "\n"
        for j in range(len(movie_format[i])):
            mystr = mystr + movie_format[i][j] + ": "
            for k in range(len(movie_time[i][j])):
                try:
                    mystr = mystr + movie_time[i][j][k] + "(" + movie_price[i][j][k] + ") "
                except:
                    mystr = mystr + movie_time[i][j][k] + "(цена не указана) "
            mystr = mystr + "\n"
        mystr = mystr + "Ссылка: " + movie_link[i] + "\n\n"

    return mystr

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

# API-ключ созданный ранее
token = "9bf9a118f6935e61fdc7e437c97a3f767663719de2747b6ba29a6477a86e488b1fa8a7116514c4cb1c616"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Логика ответа
            if request == "привет":
                write_msg(event.user_id, "Привет")
            elif request == "новинки":
                write_header_movie(event.user_id)
            else:
                write_msg(event.user_id, "Я вас не понимаю(((")
