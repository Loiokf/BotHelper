import requests
from bs4 import BeautifulSoup
import datetime


def get_news_titles(topic):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.rbc.ru/{topic}/{current_date}"

    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "Error: failed to connect to the website"

    soup = BeautifulSoup(page.content, 'html.parser')

    news_titles = []
    for title in soup.find_all('a', class_='news-feed__item__title'):
        news_titles.append(title.text)

    if not news_titles:
        return "Error: no news found for this topic and date"

    return news_titles


topic = input("Enter topic: ")
titles = get_news_titles(topic)

if type(titles) == str:
    print(titles)
else:
    for title in titles:
        print(title)