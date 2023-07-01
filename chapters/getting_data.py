# egrep.py
import sys, re

# sys.argv - список аргументов командной строки
# sys.argv[0] - имя самой программы
# sys.argv[1] - регулярное выражение, указываемое в командной строке
regex = sys.argv[1]

# Для каждой строки, переданной сценарию
for line in sys.stdin:
    # Если она соответствует регулярному выражению regex,
    # то записать ее в stdout
    if re.search(regex, line):
        sys.stdout.write(line)


# Подсчет строк (line_count.py)
import sys


count = 0
for line in sys.stdin:
    count += 1

# Печать выводится на консоль sys.stdout
print(count)

# Подсчёт строк, в которых содержатся числа

# Пример использования для Windows:
'type Somefile.txt | python egrep.py "[0-9]" | python line_count.py'

# Пример использования для UNIX-подобных систем:
'cat Somefile.txt | python egrep.py "[0-9]" | python line_count.py'

# "|" означает, что выход команды слева надо использовать в качестве входа команды справа


# Наиболее распространенные слова (most_common_words.py)
import sys
from collections import Counter


# Передать число слов в качестве первого аргумента
try:
    num_words = int(sys.argv[1])

except:
    print("Применение: most_common_words.py num_words")
    sys.exit(1)  # Ненулевой код выхода сигнализирует об ошибке

counter = Counter(word.lower()                      # Перевести в нижний регистр
                  for line in sys.stdin
                  for word in line.strip().split()  # Разбить строку по пробелам
                  if word)                          # Пропустить "пустые" слова

for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")


# Чтение файлов
# 'r' - только чтение (read-only)
file_for_reading = open('reading_file.txt', 'r')
file_for_reading2 = open('reading_file.txt')

# 'w' - пишет в файл. Сотрет файл, если он уже существует (write)
file_for_writing = open('reading_file.txt', 'w')

# 'a' - дополняет файл (append)
file_for_appending = open('reading_file.txt', 'a')

# не забывать закрывать файл в конце работы
file_for_writing.close()

# Чтобы не париться насчёт закрытия файла, можно пользоваться конструкцией
with open('reading_file.txt', 'r') as f:
    data = '...'

# в этой строке кода файл f уже закрыт, поэтому не следует пытаться использовать его


# чтение файла целиком
starts_with_hash = 0

with open('input.txt', 'r') as f:
    for line in f:                 # Просмотреть каждую строку файла, используя
        if re.match("^#", line):   # regex для проверки, начинается ли она с "#"
            starts_with_hash += 1  # Если да, добавляем 1 в счётчик


# Файлы с разделителями
import csv


"""
6/20/2014   AAPL    90
6/20/2014   MSFT    41
6/20/2014   FB      64
"""


with open('file.txt', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')  # Если поля разделены символом табуляции
    for row in reader:
        date = row[0]
        symbol = float(row[1])
        closing_price = row[2]

"""
date:symbol:closing_price
6/20/2014:AAPL:90
6/20/2014:MSFT:41
6/20/2014:FB:64
"""

# Файл имеет заголовки
with open('file.txt', 'rb') as f:
    colon_reader = csv.DictReader(f, delimiter=':')  # Если поля разделены символом ":"
    for dict_row in colon_reader:
        date = row["date"]
        symbol = row["symbol"]
        closing_price = float(row["closing_price"])


# Запись данных с разделителями
today_prices = {"AAPL": 90.91, "MSFT": 41.68, "FB": 64.6}

with open('file.txt', 'wb') as f:
    writer = csv.writer(f, delimiter=',')
    for stock, price in today_prices.items():
        writer.writerow([stock, price])

