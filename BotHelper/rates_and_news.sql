CREATE TABLE Rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_text TEXT NOT NULL,
    rate_symbol TEXT NOT NULL,
    sum_rub REAL NOT NULL
);

CREATE TABLE FinNews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    url TEXT NOT NULL
);