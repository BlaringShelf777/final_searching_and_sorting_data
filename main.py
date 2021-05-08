import re

with open('Dados_clean/minirating.csv', encoding='utf8') as dados:
    i = 0
    for line in dados:
        parsed = re.findall(r'(.*),(.*),(.*),', line)
        print(i + 1, parsed)
        i += 1
        if i > 1:
            break