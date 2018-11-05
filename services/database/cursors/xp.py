import time
import services.database.connection as conn


class XP:
    @staticmethod
    def xp_by_user(user: int, guild: int):
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM xp WHERE user=? AND guild=?", [user, guild])

        return cur.fetchone()

    @staticmethod
    def setup():
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS xp (
                    id integer PRIMARY KEY,
                    user INTEGER NOT NULL,
                    timestamp INTEGER,
                    xp INTEGER,
                    guild INTEGER
                );
                """)

    @staticmethod
    def test_data(guild, user):
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()

        ts = time.time()

        sql = "SELECT * FROM xp WHERE guild=? AND user=?"
        cur.execute(sql, [guild, user])
        data = cur.fetchall()
        # if object does not exist, create it
        if len(data) == 0:
            sql = "INSERT INTO xp (user, timestamp, xp, guild) VALUES (?, ?, ?, ?)"
            cur.execute(sql, [user, ts, 100, guild])
        # if stored object exist and we need update it
        else:
            sql = "UPDATE xp SET xp = ? WHERE guild = ? AND user = ?"
            cur.execute(sql, [100, guild, user])
