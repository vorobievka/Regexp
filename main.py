from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

if __name__ == '__main__':

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        # rows = csv.reader(f, delimiter=",")
        rows = csv.DictReader(f, delimiter=",")
        contacts_list = list(rows)

    ## 1. Выполните пункты 1-3 задания.
    ## Ваш код
    contacts_list2 = []
    contact_list_uniq = {}

    for i in contacts_list:
        lastname = i.get('lastname')
        firstname = i.get('firstname')
        surname = i.get('surname')
        pattern = r"\w+"
        patter_phone = r"(\+7|8)((\(|\s\()|(\s))?(\d{3})(\) |\)|-)?(\d{3})(-)?(\d{2})(-)?(\d{2})(( доб. )|( \(доб. ))?(\d{4})?(\))?"
        substitude = r"+7(\5)\7-\9-\11 доб.\15"
        result1 = re.findall(pattern, lastname)
        result2 = re.findall(pattern, firstname)
        result3 = re.findall(pattern, surname)
        list = [result1, result2, result3]
        list_fio = []
        for x in list:
            for y in x:
                list_fio.append(y)
        if len(list_fio) < 3:
            list_fio.append("")

        ph = re.sub(patter_phone, substitude, i.get('phone'))
        u = ph.split(' ')
        phone = u[0]
        p = ""
        r = ""
        if len(u) == 2:
            p = u[0]
            r = u[1]
            if r != 'доб.':
                phone = u[0] + " " + u[1]

        i.update({'phone': phone});
        i.update({'lastname': list_fio[0]});
        i.update({'firstname': list_fio[1]});
        i.update({'surname': list_fio[2]});

        key = i.get('lastname') + "_" + i.get('firstname')

        if key not in contact_list_uniq:
            contact_list_uniq.update({key: i})
        else:
            t = contact_list_uniq.get(key)
            for k in t:
                if t.get(k) == '':
                    t.update({k: i.get(k)})
        list_fio = []

    for key in contact_list_uniq:
        contacts_list2.append(contact_list_uniq.get(key))

    fieldnames = []
    for h in contacts_list2[0]:
        fieldnames.append(h)

    ## 2. Сохраните получившиеся данные в другой файл.
    ## Код для записи файла в формате CSV:

    with open("phonebook.csv", "w", newline='') as f:
        datawriter = csv.DictWriter(f, fieldnames=fieldnames)

        ## Вместо contacts_list подставьте свой список:
        datawriter.writeheader()
        for row in contacts_list2:
            datawriter.writerow(row)
