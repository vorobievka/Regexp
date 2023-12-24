import csv
import re
from datetime import datetime

pattern_fio = r"\w+"
pattern_phone = r"(\+7|8)(.+)?(\d{3})(.+)?(\d{3})(-)?(\d{2})(-)?(\d{2})(.+)?(доб.)\s(\d{4})?(\))?"
substitute = r"+7(\3)\5-\7-\9 доб.\12"


def open_file(path, text):
    with open(path, "a", encoding='utf-8') as f:
        f.write(text)


def logger(path):
    path = path

    def __logger(old_function):
        def new_function(*args, **kwargs):
            dt = datetime.today()
            nonlocal path
            print(f"Вызвана функция {old_function.__name__} в {dt.hour}:{dt.minute} с аргументами {args}, {kwargs}")
            open_file(path, f"Вызвана функция {old_function.__name__} в {dt.hour}:{dt.minute} с аргументами {args}, {kwargs} \n")
            result = old_function(*args, **kwargs)
            print(f"Функция {old_function.__name__} вернула {result} ")
            open_file(path, f"Функция {old_function.__name__} вернула {result} \n")
            return result

        return new_function

    return __logger


def read_phonebook():
    try:
        with open("phonebook_raw.csv", encoding='utf-8') as f:
            rows = csv.DictReader(f, delimiter=",")
            contacts_list = list(rows)
            return contacts_list
    except(Exception,):
        print("An exception occurred")


def write_phonebook(contacts_list):
    fieldnames = [i for i in contacts_list[0]]
    try:
        with open("phonebook.csv", "w", newline='') as f:
            datawriter = csv.DictWriter(f, fieldnames=fieldnames)
            datawriter.writeheader()
            for row in contacts_list:
                datawriter.writerow(row)
    except(Exception,):
        print("An exception occurred")


@logger("app.log")
def remake_fio_phone(row):
    lastname = re.findall(pattern_fio, row.get('lastname'))
    firstname = re.findall(pattern_fio, row.get('firstname'))
    surname = re.findall(pattern_fio, row.get('surname'))
    fio = [lastname, firstname, surname]
    list_fio = []
    for x in fio:
        for y in x:
            list_fio.append(y)
    if len(list_fio) < 3:
        list_fio.append("")

    phone_string = re.sub(pattern_phone, substitute, row.get('phone'))

    phone = phone_string.split(' ')[0]
    if len(phone_string.split(' ')) == 2:
        extension = phone_string.split(' ')[1]
        if extension != 'доб.':
            phone = phone + " " + extension

    row.update({'phone': phone})
    row.update({'lastname': list_fio[0]})
    row.update({'firstname': list_fio[1]})
    row.update({'surname': list_fio[2]})

    return "Modifications done"

def set_unique_row(contacts_list):
    contacts_list_modified = []
    contacts_list_uniq = {}
    for row in contacts_list:
        key = row.get('lastname') + "_" + row.get('firstname')
        if key not in contacts_list_uniq:
            contacts_list_uniq.update({key: row})
        else:
            t = contacts_list_uniq.get(key)
            for k in t:
                if t.get(k) == '':
                    t.update({k: row.get(k)})
    for key in contacts_list_uniq:
        contacts_list_modified.append(contacts_list_uniq.get(key))
    return contacts_list_modified


def main():
    contacts_list = read_phonebook()
    for row in contacts_list:
        remake_fio_phone(row)
        contacts_list = set_unique_row(contacts_list)
    write_phonebook(contacts_list)


if __name__ == '__main__':
    main()
