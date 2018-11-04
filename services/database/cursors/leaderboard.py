import services.database.connection as conn


class XP:
    @staticmethod
    def get_leaderboard(guild):
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM xp WHERE guild=?", [guild])

        return cur.fetchall()

    @staticmethod
    def setup():
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS xp (
                    id integer PRIMARY KEY,
                    user text NOT NULL,
                    timestamp INTEGER,
                    xp INTEGER,
                    guild INTEGER
                );
                """)
