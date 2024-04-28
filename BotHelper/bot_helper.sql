--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Вс апр 28 19:47:17 2024
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: FinNews
CREATE TABLE IF NOT EXISTS FinNews (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, text TEXT NOT NULL, url TEXT NOT NULL);

-- Таблица: Rates
CREATE TABLE IF NOT EXISTS Rates (id INTEGER PRIMARY KEY AUTOINCREMENT, rate_text TEXT NOT NULL, rate_symbol TEXT NOT NULL, sum_rub TEXT NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
