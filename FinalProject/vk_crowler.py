import vk
import sqlite3
import os
import re
from vk.exceptions import VkAPIError


DOMAIN = "living.poets"
ACCESS_TOKEN = "29677f9e65cdf02279fa930a3b6c1d7e2c921aacbb8a8c5ae86b3d3ff40322b6f5a3f9b068ac152b64a"
SESSION = vk.Session(access_token=ACCESS_TOKEN)

API = vk.API(SESSION, v=5.95)

name_of_bd = "live_poems.bd"


def take_posts():
    posts_l = []
    poems_raw = []
    offset = 0
    while offset < 300:
        posts_raw = API.wall.get(domain=DOMAIN, count=100, offset=offset, filter=all)
        if not posts_raw["items"]:
            break
        posts_l.extend(posts_raw["items"])
        offset += 100
        print(offset)
    num = 0
    for i in posts_l:
        text = i["text"]
        if ("#жыанкета" not in text) and ("#жыафиша" not in text) and ("#жыдрузья" not in text) and \
                ("#про_вжывую" not in text) and ("#жыфакт" not in text) and ("#жыновости" not in text)\
                and ("#жырадио" not in text) and ("#жыцитата" not in text) \
                and ("#жыпремия" not in text) and ("#живыепоэты" in text):
            poems_raw.append(text)
            num += 1
    return poems_raw


def process_poems(poems):
    poems_parsed = []
    for i in poems:
        try:
            poem = i.split("\n\n")
            author = poem[0]
            if "id" in author:
                author = re.match(r"\[id\d+\|(.*?)\]", author).group(1)
            elif "club" in author:
                author = re.match(r"\[club\d+\|(.*?)\]", author).group(1)
            if len(author.split()) >= 6:
                continue
            if len(poem[1].split("\n")) == 1:
                text = "\n".join(poem[2:-1])
            else:
                text = "\n".join(poem[1:-1])
            poems_parsed.append((author, text))
        except AttributeError:
            continue
    return poems_parsed


def create_bd():
    conn = sqlite3.connect(name_of_bd)
    c = conn.cursor()
    c.execute("CREATE TABLE poets (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, poet TEXT NOT NULL UNIQUE);")
    c.execute("CREATE TABLE poems (line TEXT NOT NULL, author INT NOT NULL )")
    conn.commit()


def fill_bd(poems_p):
    conn = sqlite3.connect(name_of_bd)
    c = conn.cursor()

    authors_in_bd = []

    for i in poems_p:
        try:
            if i[0] not in authors_in_bd:
                try:
                    c.execute("INSERT INTO poets (poet) VALUES (?)", (i[0],))
                    authors_in_bd.append(i[0])
                # ловим ошибку уникальности - авторы не должны встречаться дважды, и если мы дозаполняем бд повторно
                # может появиться IntegrityError
                except sqlite3.IntegrityError:
                    print("poet is in the bd already!")
            text = i[1].split("\n")
            c.execute("SELECT id FROM poets WHERE poet == (?)", (format(i[0]),))
            index_author = c.fetchone()

            lines_of_author = get_poems_of_author(index_author[0])

            for t in text:
                if detect_bad_line(t) == False:
                    if t != "" and t not in lines_of_author:
                        c.execute("INSERT INTO poems VALUES (?,?)", (t, index_author[0]))
        except sqlite3.OperationalError:
            print("Ошибка на: ")
            print(i)
            continue
    conn.commit()


def get_poems_of_author(id_author):
    conn = sqlite3.connect(name_of_bd)
    c = conn.cursor()

    c.execute("SELECT line FROM poems WHERE author == (?)", (id_author,))
    lines_of_author = c.fetchall()
    lines_of_author = [i[0] for i in lines_of_author]
    return lines_of_author


# не все строки - строки стихотворения. Это может быть "Перевод с ____ языка: переводчик", или например номер строфы I
# а еще это все же современная поэзия, и строки в одно слово для нее нормальны - но нам не очень хочется выдавать их
# как ответ пользователю
def detect_bad_line(line):
    if re.match("Перевод со? [а-я]+:", line) is not None:
        return True
    if re.match("[а-яА-Я]", line) is None:
        return True
    if len(line.split()) <= 2:
        return True
    return False


def main():
    try:
        poems = take_posts()
    except VkAPIError:
        global ACCESS_TOKEN
        global SESSION
        global API
        ACCESS_TOKEN = input("Not a valid token! Input another one: ")
        SESSION = vk.Session(access_token=ACCESS_TOKEN)
        API = vk.API(SESSION, v=5.95)
        poems = take_posts()
    if not os.path.exists(name_of_bd):
        create_bd()

    poems_p = process_poems(poems)
    fill_bd(poems_p)


main()
