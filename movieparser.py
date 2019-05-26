import lxml.html
import requests

def parser_listgenre(word):
    page = requests.get('https://perm.kinoafisha.info/cinema/4283797/').text
    parser = lxml.html.fromstring(page)
    # название фильма
    movie_name = parser.xpath('.//div[@class = "films_right"]/a/span/span/text()')
    # жанр фильма
    movie_genre = parser.xpath('.//span[@class = "films_info"]/text()')

    return_movie = []
    print(movie_genre)
    for i in movie_genre:
        print("=====",i,"====")
        temp = list(i.split(', '))
        print(temp)
        print((i))
        result = list(set(temp) & set(word))
        print(result)
        if(len(result)==len(word)):
            index = movie_genre.index(i)
            return_movie.append(movie_name[index] + " [" + movie_genre[index] + "]\n")


    print(return_movie)
    return_movie = set(return_movie)
    str = ""
    for i in return_movie:
        str+= i + "\n"
    if str=="":
        str = "Я не смог найти фильмы с данным жанром";
    return str


def get_new_movie(cinema_id):
	
    page = requests.get('https://perm.kinoafisha.info/cinema/' + cinema_id).text
    
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