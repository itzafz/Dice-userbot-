import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def alive():
    return "alive"

def run_server():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_server, daemon=True).start()

while True:
    print("started...")
    os.system("python3 bot.py")
    print("exited...")