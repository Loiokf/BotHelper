from Finance import GetInfoAboutRate
from DailyNews import DailyNews
import sqlite3 as sq
from threading import Timer


def update() -> None:
    conn = sq.connect("bot_helper.db")
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {GetInfoAboutRate.table_name()}')
    cur.execute(f'DELETE FROM {DailyNews.table_name()}')
    conn.commit()
    conn.close()
    GetInfoAboutRate.to_db()
    DailyNews.to_db()
    Timer(900, update).start()


if __name__ == '__main__':
    update()
