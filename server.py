from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import os

from database import init_db, update_bot, get_bots

app = Flask(__name__)

init_db()


@app.route("/bot_activity", methods=["POST"])
def bot_activity():

    data = request.json

    bot_id = data["bot_id"]
    status = data["status"]

    now = datetime.utcnow().isoformat()

    update_bot(bot_id, status, now)

    return jsonify({"ok": True})


@app.route("/")
def dashboard():

    rows = get_bots()

    bots = []

    for r in rows:

        last = datetime.fromisoformat(r[2])

        online = datetime.utcnow() - last < timedelta(minutes=1)

        bots.append({
            "id": r[0],
            "status": r[1],
            "last_seen": r[2],
            "online": online
        })

    return render_template("dashboard.html", bots=bots)


port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=port)
