import sqlite3

DB = "bots.db"

def init_db():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS bots(
        bot_id TEXT PRIMARY KEY,
        status TEXT,
        last_seen TEXT
    )
    """)

    conn.commit()
    conn.close()


def update_bot(bot_id, status, time):

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    INSERT INTO bots(bot_id,status,last_seen)
    VALUES(?,?,?)
    ON CONFLICT(bot_id) DO UPDATE SET
    status=?,
    last_seen=?
    """,(bot_id,status,time,status,time))

    conn.commit()
    conn.close()


def get_bots():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    bots = c.execute("SELECT bot_id,status,last_seen FROM bots").fetchall()

    conn.close()

    return bots