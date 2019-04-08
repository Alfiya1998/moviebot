import vk_api
import random
import lxml.html
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message):
    vk_session.method("messages.send", {"user_id": user_id, "message": message, "random_id": get_random_id()})

def write_header_movie(user_id):
    vk_session.method("messages.send", {"user_id": user_id, "message": get_header_movie(), "random_id": get_random_id()})

def get_header_movie():
    page = requests.get('https://perm.kinoafisha.info/cinema/4283797/').text
    parser = lxml.html.fromstring(page)

    # Íàçâàíèå ôèëüìà
    path_movie_name = ".films_right > a > span > span"
    movie_name = []
    for i in parser.cssselect(path_movie_name):
        movie_name.append(i.text)

    # Æàíð ôèëüìà
    path_movie_info = ".films_info"
    movie_info = []
    for i in parser.cssselect(path_movie_info):
        movie_info.append(i.text)

    # Ññûëêà íà ôèëüì
    movie_link = parser.xpath('.//div[@class = "films_right"]/a/@href')

    mystr = ""
    for i in range(len(movie_name)):
        mystr = mystr + movie_name[i] + "\n" + "Æàíð: " + movie_info[i] + "\n" + "Ññûëêà: " + movie_link[i] + "\n\n"

    return mystr

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])

# API-êëþ÷ ñîçäàííûé ðàíåå
token = "9bf9a118f6935e61fdc7e437c97a3f767663719de2747b6ba29a6477a86e488b1fa8a7116514c4cb1c616"

# Àâòîðèçóåìñÿ êàê ñîîáùåñòâî
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():

    # Åñëè ïðèøëî íîâîå ñîîáùåíèå
    if event.type == VkEventType.MESSAGE_NEW:

        # Åñëè îíî èìååò ìåòêó äëÿ ìåíÿ( òî åñòü áîòà)
        if event.to_me:

            # Ñîîáùåíèå îò ïîëüçîâàòåëÿ
            request = event.text

            # Ëîãèêà îòâåòà
            if request == "ïðèâåò":
                write_msg(event.user_id, "Ïðèâåò")
            elif request == "íîâèíêè":
                write_header_movie(event.user_id)
            else:
                write_msg(event.user_id, "ß âàñ íå ïîíèìàþ(((")
