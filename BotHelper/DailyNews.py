"""from bs4 import BeautifulSoup
from urllib.request import urlopen
from models import Parser, News, ABC
import sqlite3 as sq


class DailyNews(Parser, ABC):
    URL = "https://www.rbc.ru/short_news"
    soup = BeautifulSoup(urlopen(URL).read(), "html.parser")

    @classmethod
    def get_news_text_exception(cls, url: str, _class: str) -> str:
        text_soup = BeautifulSoup(urlopen(url).read(), "html.parser")
        try:
            article_title = text_soup.find("div", attrs={"class": _class})
            result = article_title.find("span").text.replace("\n", "")
            if len(result) < 150:
                return " "
            return result
        except AttributeError:
            return " "

    @classmethod
    def get_news_text(cls, url: str) -> str:
        _class = ["article__text article__text_free", "article__text__overview"]
        first_title, second_title = cls.get_news_text_exception(url, _class[0]), cls.get_news_text_exception(url,
                                                                                                             _class[1])
        if first_title == second_title:
            return first_title
        if first_title == str():
            return second_title
        return first_title
        print(first_title)
        print(second_title)

    @classmethod
    def get_data(cls) -> list[News]:
        all_news: list[News] = []
        news_list, news_url_list = cls.soup.find_all("span", attrs={"class": "item__title rm-cm-item-text "
                                                                             "js-rm-central-column-item-text"}), \
            cls.soup.find_all("a", attrs={"class": "item__link rm-cm-item-link js-rm-central-column-item-link"})
        for news, url in zip(news_list, news_url_list):
            news = str(news)
            news_obj = News(
                title=news[42 + 68:len(news) - 68],
                text=cls.get_news_text(url.get("href")),
                url=url.get("href")
            )
            all_news.append(news_obj)
        return all_news
        print(news_obj)

    @classmethod
    def to_db(cls) -> None:
        news: list[News] = cls.get_data()
        conn = sq.connect("bot_helper.db")
        cur = conn.cursor()
        for news_obj in news:
            sql_request = f"INSERT INTO FinNews(title, text, url) " \
                          f"VALUES('{news_obj.title}', '{news_obj.text}', '{news_obj.url}')"
            cur.execute(sql_request)
            conn.commit()
        conn.close()

    @classmethod
    def table_name(cls) -> str:
        return 'FinNews'
"""

import sqlite3
import requests
from bs4 import BeautifulSoup


class DailyNews():
    # Создать соединение с базой данных
    conn = sqlite3.connect('finnews.db')
    # Создать курсор
    cur = conn.cursor()

    # Создать таблицу FinNews, если она еще не существует
    cur.execute("""
    CREATE TABLE IF NOT EXISTS FinNews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        url TEXT NOT NULL
    )
    """)

    # URL-адрес веб-сайта с новостями
    url = 'https://www.rbc.ru/finances/'

    # Получить HTML-код веб-сайта
    response = requests.get(url)
    html = response.text

    # Создать объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Найти все заголовки новостей
    news_headers = soup.find_all('a', class_='main__feed__link')

    # Итерировать по заголовкам новостей
    for header in news_headers:
        # Получить заголовок новости
        title = header.text.strip()

        # Получить URL-адрес новости
        url = header['href']

        # Получить полный текст новости
        news_page = requests.get(url)
        news_html = news_page.text
        news_soup = BeautifulSoup(news_html, 'html.parser')
        news_text = news_soup.find('div', class_='article__text').text.strip()

        # Вставить новость в базу данных
        query = """
        INSERT INTO FinNews(title, text, url) 
        VALUES (?, ?, ?)
        """
        data = (title, news_text, url)
        print(cur.execute(query, data))

    # Сохранить изменения в базе данных
    conn.commit()

    # Закрыть курсор и соединение
    cur.close()
    conn.close()