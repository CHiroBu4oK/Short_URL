import sqlite3

class Database():
    def __init__(self):
        conn=sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS urls (
            short_url TEXT PRIMARY KEY,
            original_url TEXT NOT NULL
        )""")
        conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS url_visitors (
            visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT,
            country TEXT,
            ip_address TEXT,
            visit_time TIMESTAMP,
            FOREIGN KEY (short_url) REFERENCES urls(short_url)
        )""")
        conn.commit()

        conn.close()

    @staticmethod
    def save_url(short_path: str, original_path: str):
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)",
                       (short_path, original_path))
        conn.commit()
        conn.close()

    @staticmethod
    def get_original_url(short_url: str):
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_path = ?",
                       (short_url,))
        url = cursor.fetchone()
        conn.close()
        if url:
            return url[0]
        else:
            return None

    @staticmethod
    def save_visit(short_url: str, country: str, ip_address: str, visit_time: str):
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO url_visitors (short_url, country, ip_address, visit_time) VALUES (?, ?, ?, ?)",
                       (short_url, country, ip_address, visit_time))
        conn.commit()
        conn.close()

    @staticmethod
    def get_stats(short_url: str):
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM url_visits WHERE short_url = ?",
                       (short_url,))
        count = cursor.fetchone()
        conn.close()
        if count:
            return count[0]
        else:
            return None

