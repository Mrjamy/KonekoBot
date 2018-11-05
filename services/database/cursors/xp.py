import time
import services.database.connection as conn


class XP:
    @staticmethod
    def get_xp(user: int, guild: int):
        connection = conn.create_connection("services/database/xp.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM xp WHERE user=? AND guild=?", [user, guild])

        return cur.fetchone()

    @staticmethod
    def add_xp_to_user(user: int, guild: int, xp: int, timestamp: float):
        db = conn.create_connection("services/database/xp.db")
        cursor = db.cursor()
        cursor.execute("""
            UPDATE xp 
            SET xp = ?, 
                timestamp = ?
            WHERE 
                guild = ? AND 
                user = ?""", [xp, timestamp, guild, user])
        db.commit()
        db.close()

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
        db = conn.create_connection("services/database/xp.db")
        cursor = db.cursor()

        ts = time.time()

        sql = "SELECT xp, timestamp FROM xp WHERE guild=? AND user=?"
        cursor.execute(sql, [guild, user])
        data = cursor.fetchone()
        # if object does not exist, create it
        if len(data) == 0:
            sql = "INSERT INTO xp (user, timestamp, xp, guild) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, [user, ts, 100, guild])
        # if stored object exist and we need update it
        else:
            sql = "UPDATE xp SET xp = ? WHERE guild = ? AND user = ?"
            cursor.execute(sql, [100, guild, user])
        db.commit()
        db.close()
