import csv
import os
import json


"""Стаитстика: распределение документов по числу данных,
соответсвующих концепту"""


def count_concept(privacy, concept):
    results = {}
    for root, dirs, files in os.walk('./csv'):
        for file in files:
            if file.endswith(".csv"):
                with open(os.path.join(root, file)) as File:
                    reader = csv.reader(File, delimiter=',', quotechar=',',
                                        quoting=csv.QUOTE_MINIMAL)

                    pre_result = []
                    for row in reader:
                        if row[5] == f'{privacy}':
                            r = []
                            for k in range(6, len(row)-2):
                                r.append(row[k])
                            r = ','.join(r)
                            r = r[1:-1]
                            r = r.replace('\"\"', '\"')
                            r = json.loads(r)
                            pre_result.append(r[f'{concept}']['value'])

                    pre_result = {i: pre_result.count(i) for i in pre_result}
                    if file in results.keys():
                        results[file].append(pre_result)
                    else:
                        results[file] = [pre_result, ]

    final = {}
    for file in results:
        keys = []
        for d in results[file]:
            for key in d.keys():
                if key not in keys:
                    keys.append(key)

        count = {}
        for d in results[file]:
            for key in keys:
                count[key] = 0
                if key in d.keys():
                    count[key] = count[key] + d[key]
        final[file] = count

    with open(f'./final_json/{concept}_in_Files.json', 'w') as f:
        f.write(json.dumps(final, indent=4, sort_keys=True))


"""Статистика: Связь между двумя концептами"""


def link_concept(privacy, concept_1, concept_2):
    results = []
    for root, dirs, files in os.walk('./csv'):
        for file in files:
            if file.endswith(".csv"):
                with open(os.path.join(root, file)) as File:
                    reader = csv.reader(File, delimiter=',', quotechar=',',
                                        quoting=csv.QUOTE_MINIMAL)

                    for row in reader:
                        if row[5] == f'{privacy}':
                            r = []
                            for k in range(6, len(row)-2):
                                r.append(row[k])
                            r = ','.join(r)
                            r = r[1:-1]
                            r = r.replace('\"\"', '\"')
                            r = json.loads(r)
                            results.append(f"{r[f'{concept_1}']['value']} \
                                           -{r[f'{concept_2}']['value']}")

    my_dict = {i: results.count(i) for i in results}
    final = {}
    for i in my_dict:
        s = i.split('-')
        if s[0] in final.keys():
            final[s[0]].append({s[1]: my_dict[i]})
        else:
            final[s[0]] = [{s[1]: my_dict[i]}, ]

    with open(f'./final_json/{concept_1}_{concept_2}.json', 'w') as f:
        f.write(json.dumps(final, indent=4, sort_keys=True))


count_concept('First Party Collection/Use', 'Personal Information Type')
count_concept('First Party Collection/Use', 'Purpose')
link_concept(
    'First Party Collection/Use',
    'Personal Information Type',
    'Purpose'
)
