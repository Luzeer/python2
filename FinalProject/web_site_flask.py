from flask import Flask
from flask import request, render_template
import sqlite3
import random
import re


app = Flask(__name__)


@app.route("/")
def index():
    conn = sqlite3.connect('live_poems.bd')
    c = conn.cursor()

    if request.args:
        line = request.args["line_input"]
        rhyme, author = find_rhyme(line)
        return render_template("main.html", poem_line=rhyme, author=author, line="Вы ввели: {}".format(line))
    return render_template("main.html", poem_line="", author="", line="")


def find_rhyme(line):
    conn = sqlite3.connect("live_poems.bd")
    c = conn.cursor()

    c.execute("SELECT line FROM poems")
    lines = c.fetchall()
    lines = [i[0] for i in lines]

    ending = re.sub("[.,?!\-—:;)(\"\' ]", "", line)[-3:]

    appr_lines = [i for i in lines if re.sub("[.,?!\-—:;)(\"\' ]", "", i).endswith(ending)]

    if "я" in ending or "ю" in ending or "ё" in ending:
        ending = ending.replace("я", "а").replace("ю", "у").replace("ё", "о")
        appr_lines.extend([i for i in lines if re.sub("[.,?!\-—:;)(\"\' ]", "", i).endswith(ending)])


    if len(appr_lines) != 0:
        res = appr_lines[random.randint(0, len(appr_lines) - 1)]

        c.execute("SELECT poet FROM poets INNER JOIN poems ON poets.id == poems.author WHERE line==(?)", (res,))
        author = c.fetchone()[0]
        return res, author
    else:
        return "ой, стихотворения с такой рифмой не найдено:(", "создатель сайта"


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
