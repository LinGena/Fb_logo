import json
import datetime


def write_to_file(filename, src):
    with open(filename,"w", encoding='utf8') as file:
        file.write(src)


def load_file(filename):
    with open(filename, "r", encoding='utf8') as file:
        src = file.read()
    return src


def write_to_file_json(filename, src):
    with open(filename,"w",encoding='utf8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)


def get_now_datetime():
    return datetime.datetime.now().strftime('%d/%m/%Y, %H:%M')


def load_from_file_json(filename):
    with open(filename, encoding='utf8') as file:
        src=json.load(file)
    return src