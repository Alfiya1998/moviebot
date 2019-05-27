import vk_api
import random
import lxml.html
import requests
import json
import re
import time
import movieparser as pars
from threading import Thread
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

my_genre = ["биография","военный", 'ужасы','семейный', 'триллер', 'комедия','боевик', 'фантастика', 'фэнтези',"приключение","мелодрама" , "драма"]

genre_msg = ""
for i in my_genre:
  genre_msg += i + "\n"

ID_FAMILY = "5192443"
ID_COLISEUM = "4283797"
ID_KRISTALL = "8088251"
MSG_RESULT_CINEMA_FAMILY = pars.get_new_movie(ID_FAMILY)
MSG_RESULT_CINEMA_COLISEUM = pars.get_new_movie(ID_COLISEUM)
MSG_RESULT_CINEMA_KRISTALL = pars.get_new_movie(ID_KRISTALL)

#MSG_RESULT_GENRE = pars.all_genres() here change

def find_genre(listword):
  wordlist=re.sub("[^\w]", " ", listword).split()
  result  = list(set(wordlist) & set(my_genre))
  return result


def sleep_pars(time_sleep):
	while True:
		print("start_timer")
		time.sleep(time_sleep)
		change_value_pars()
		print("pars site")

def create_thread():
	thread_timer = Thread(target = sleep_pars, args = (300, ))
	thread_timer.start()
	return thread_timer

keyboard = {
    "one_time": None,
    "buttons": [
      [{
        "action": {
          "type": "text",
          "payload": "{\"button\": \"1\"}",
          "label": "Колизей"
        },
        "color": "positive"
      },
     {
        "action": {
          "type": "text",
          "payload": "{\"button\": \"2\"}",
          "label": "СемьЯ"
        },
        "color": "positive"
      },
      {
        "action": {
          "type": "text",
          "payload": "{\"button\": \"3\"}",
          "label": "Кристалл"
        },
        "color": "positive"
      }],
     [{
        "action": {
          "type": "text",
          "payload": "{\"button\": \"4\"}",
          "label": "Поиск по жанру"
        },
        "color": "primary"
      }]
    ]
  }

def write_msg(user_id, message):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": get_random_id()})

def write_new_movie(user_id, keyboard, cinema_id):
    vk_session.method("messages.send", {"user_id": user_id, "message": get_message(cinema_id), "random_id": get_random_id(), "keyboard": keyboard})

def write_recomendet(user_id, genre):
	vk_session.method("messages.send", {"user_id": user_id, "message": MSG_RESULT_GENRE[genre], "random_id": get_random_id()})

def get_message(cinema_id):
	if cinema_id == ID_COLISEUM:
		return MSG_RESULT_CINEMA_COLISEUM
	if cinema_id == ID_FAMILY:
		return MSG_RESULT_CINEMA_FAMILY
	if cinema_id == ID_KRISTALL:
		return MSG_RESULT_CINEMA_KRISTALL


def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def change_value_pars():
	MSG_RESULT_CINEMA_FAMILY = pars.get_new_movie(ID_FAMILY)
	MSG_RESULT_CINEMA_COLISEUM = pars.get_new_movie(ID_COLISEUM)
	MSG_RESULT_CINEMA_KRISTALL = pars.get_new_movie(ID_KRISTALL)

	#MSG_RESULT_GENRE = pars.all_genres() here change


# API-ключ созданный ранее
token = "19b0bec16f37a5ef6754988c36a9759c11a92e4d3a2f6210c2809ab6088921f92b99188cb9d028d7b1695"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)

cinema = {"колизей": ID_COLISEUM, "семья": ID_FAMILY, "кристалл": ID_KRISTALL} 

create_thread()

for event in longpoll.listen():

    # Если пришло новое сообщение и если оно имеет метку для меня( то есть бота)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower().replace(" ", "")

        # Логика ответа
        if request == "привет":
            write_msg(event.user_id, "Привет! Я чат-бот, который позволит тебе узнать расписания сеансов в городе Пермь на сегодня. Для начала работы, напишите любой из кинотеатров: Колизей, СемьЯ, Кристалл.")
        elif request == "колизей" or request == "семья" or request == "кристалл":
            write_new_movie(event.user_id, json.dumps(keyboard, ensure_ascii=False), cinema[request])
        elif request == "поискпожанру":
        	write_msg(event.user_id, "Для поиска фильма по жанру напишите один из перечисленных жанров:\n{0}".format(genre_msg))
        elif request in my_genre:
        	listtem = find_genre(request)
        	write_recomendet(event.user_id, listtem)
        else:
            write_msg(event.user_id, "Проверьте введенное слово, вы, кажется, ошиблись :)")
