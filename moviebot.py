﻿import vk_api
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

MSG_RESULT_CINEMA_FAMILY = pars.get_new_movie("5192443/")
MSG_RESULT_CINEMA_COLISEUM = pars.get_new_movie("4283797/")
MSG_RESULT_CINEMA_KRISTALL = pars.get_new_movie("8088251/")

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

def create_threads():
	thread_timer = Thread(target = sleep_pars, args = (300, ))
	thread_timer.start()

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
	vk_session.method("messages.send", {"user_id": user_id, "message": pars.parser_listgenre(genre), "random_id": get_random_id()})

def get_message(cinema_id):
	cinema_id.replace("/", "")
	if cinema_id == str(4283797):
		return MSG_RESULT_CINEMA_COLISEUM
	if cinema_id == str(5192443):
		return MSG_RESULT_CINEMA_FAMILY
	if cinema_id == str(8088251):
		return MSG_RESULT_CINEMA_KRISTALL


def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

def change_value_pars():
	MSG_RESULT_CINEMA_FAMILY = pars.get_new_movie("4283797/")
	MSG_RESULT_CINEMA_COLISEUM = pars.get_new_movie("4283797/")
	MSG_RESULT_CINEMA_KRISTALL = pars.get_new_movie("8088251/")


# API-ключ созданный ранее
token = "19b0bec16f37a5ef6754988c36a9759c11a92e4d3a2f6210c2809ab6088921f92b99188cb9d028d7b1695"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)

cinema = {"колизей": "4283797/", "семья": "5192443/", "кристалл": "8088251/"}

create_threads()

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
