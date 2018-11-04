import services.database.connection as conn


class XP:
    @staticmethod
    def xp_by_user(user, guild):
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM xp WHERE user=? AND guild=?", (user, guild))

        return cur.fetchone()

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
