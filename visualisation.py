import matplotlib.pyplot as plt

# # График
# years = [i for i in range(1950, 2011, 10)]
# gdp = [300, 500, 1034.3, 2829, 5987, 10284, 15000]
#
# plt.plot(years, gdp, color='green', marker='x', linestyle='solid')
#
# plt.title('Номинальный ВВП')
#
# plt.ylabel('Млрд $')
#
# plt.show()

# # Столбчатая диаграмма
# movies = ['Энни Холл', 'Бен-Гур', 'Касабланка', 'Ганди', 'Вестсайдская история']
# num_oscars = [5, 11, 3, 8, 10]
#
# plt.bar(range(len(movies)), num_oscars)
# plt.title('Мои любимые фильмы')
# plt.ylabel('Число наград')
# plt.xticks(range(len(movies)), movies)
#
# plt.show()

# # Гистограмма сгруппированых числовых значений
# from collections import  Counter
#
# grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
#
# # Сгруппировать оценки подецильно
# # но разместить 100 вместе с отметками 90 и выше
# histogram = Counter(min(grade // 10 * 10, 90) for grade in grades)
#
# plt.bar([x for x in histogram.keys()],  # Сдвигаем столбцы вправо на 5
#         histogram.values(),  # Назначаем каждому столбцу правильную высоту
#         10,                  # Назначаем каждому столбцу ширину 10
#         edgecolor=(0, 0, 0)  # черные края для каждого столбца
#         )
# plt.axis([-5, 105, 0, 5])    # Ось х от -5 до 105
#                              # Ось у от 0 до 5
# plt.xticks([10 * i for i in range(11)])  # Метки по оси: 0, 10, ..., 100
# plt.xlabel("Дециль")
# plt.ylabel("Число студентов")
# plt.title('Распределение оценок за экзамен ')
# plt.show()

# # Линейные графики
# variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]  # Дисперсия
# bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]  # Квадрат смещения
# # Суммарная ошибка
# total_error = [x + y for x, y, in zip(variance, bias_squared)]
# xs = [i for i, _ in enumerate(variance)]
#
# # Зеленая сплошная линия
# plt.plot(xs, variance, 'g-', label='дисперсия')
# # Красная штрихпунктирная
# plt.plot(xs, bias_squared, 'r-.', label='смещение^2')
# # Синяя пунктирная
# plt.plot(xs, total_error, 'b:', label='суммарная ошибка')
# # loc=9 - легенда будет по середине
# plt.legend(loc=9)
# plt.xlabel('Сложность модели')
# plt.title('Компромисс между смещением и дисперсией')
# plt.show()


# Диаграммы рассеяния
friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

plt.scatter(friends, minutes)

# Назначаем метку каждой точке
for label, friend_count, minute_count in zip(labels, friends, minutes):
    plt.annotate(label,
                 xy=(friend_count, minute_count),  # Задать метку
                 xytext=(5, 5),  # немного сместить
                 textcoords='offset points')

plt.title('Число минут против числа друзей')
plt.ylabel('Число минут, проводимых на сайте ежедневно')
plt.xlabel('Число друзей')
plt. show()

