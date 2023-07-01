from chapters.linear_algebra import Vector, dot


def sum_of_squares(v: Vector) -> float:
    """Вычисляет сумму возведенных в квадрат элементов v"""
    return dot(v, v)


from typing import Callable


def difference_quotient(f: Callable[[float], float],
                        x: float,
                        h: float) -> float:
    return (f(x + h) - f(x)) / h


# Частное разностное отношение
def partial_difference_quotient(f: Callable[[Vector], float],
                                v: Vector,
                                i: float,
                                h: float) -> float:
    """Возвращает i-е частное разностное отношение функции f в v"""
    w = [v_j + (h if j == i else 0)  # Добавит h только в i-ый элемент v
         for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h


def estimate_gradient(f: Callable[[Vector], float],
                      v: Vector,
                      h: float = 0.0001):
    return [partial_difference_quotient(f, v, i, h)
            for i in range(len(v))]

# Вычислительно ресурсоемко вычислять разностное отношение каждый раз


# Использование Градиента
import random
from chapters.linear_algebra import distance, add, scalar_multiply


def gradient_step(v: Vector, gradient: Vector, step_size: float) -> Vector:
    """Движение с шагом 'step_size' в направлении
       градиента 'gradient' от 'v'"""
    assert len(v) == len(gradient)
    step = scalar_multiply(step_size, gradient)
    return add(v, step)


def sum_of_squares_gradient(v: Vector) -> Vector:
    return [2 * v_i for v_i in v]


# Подобрать случайную отправную точку
v = [random.uniform(-10, 10) for i in range(3)]

for epoch in range(1000):
    grad = sum_of_squares_gradient(v)  # Вычислить градиент в v
    v = gradient_step(v, grad, -0.01)  # Сделать отрицательный градиентный шаг

    print(epoch, v)


assert distance(v, [0, 0, 0]) < 0.00001  # v должно быть близко к 0


# простой пример (поиск углового коэф-та)
# х изменяется в интервале от -50 до 49, у всегда равно 20 * х + 5
inputs = [(x, 20 * x + 5) for x in range(-50, 50)]


# Линейный градиент
def linear_gradient(x: float, y: float, theta: Vector) -> Vector:
    slope, intercept = theta           # Наклон и пересечение
    predicted = slope * x + intercept  # Модельное предсказание
    error = (predicted - y)            # Ошибка равна (предсказание - у)
    squared_error = error ** 2         # Мы минимизируем квадрат ошибки,
    grad = [2 * error * x, 2 * error]  # используя градиент
    return grad


# 1) Начать со случайного значения theta
# 2) Вычислить среднее значение градиентов
# 3) Скорректировать theta в этом направлении
# 4) Повторить

from linear_algebra import vector_mean


# Начать со случайных значений наклона и пересечения
theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

learning_rate = 0.001  # Темп усвоения

for epoch in range(5000):
    # Вычислить среднее значение градиентов
    grad = vector_mean([linear_gradient(x, y, theta) for x, y in inputs])

    # Сделать шаг в этом направлении
    theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)


slope, intercept = theta
assert 19.9 < slope < 20.1, "наклон должен быть равен примерно 20"
assert 4.9 < intercept < 5.1, "пересечение должно быть равным примерно 5"


# мини-пакетный градиентный спуск
from typing import TypeVar, List, Iterator


T = TypeVar('T')  # Это позволяет типизировать "обобщенные" функции


def mini_batches(dataset: List[T],
                 batch_size: int,
                 shuffle: bool = True) -> Iterator[List[T]]:
    """Генерирует мини-пакеты в размере 'batch_size' из набора данных"""
    # Старт индексируется с 0, batch_size, 2 * batch_size ...
    batch_starts = [start for start in range(0, len(dataset), batch_size)]

    if shuffle: random.shuffle(batch_starts)  # Перетасовать пакеты

    for start in batch_starts:
        end = start + batch_size
        yield dataset[start:end]


theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

for epoch in range(1000):
    for batch in mini_batches(inputs, batch_size=20):
        grad = vector_mean([linear_gradient(x, y, theta) for x, y in batch])
        theta = gradient_step(theta, grad, -learning_rate)
    print(epoch, theta)


slope, intercept = theta
assert 19.9 < slope < 20.1, "наклон должен быть равен примерно 20"
assert 4.9 < intercept < 5.1, "пересечение должно быть равным примерно 5"


# Стохастический градиентный спуск
# шаги делаются на основе одного тренировочного примера за раз

theta = [random.uniform(-1, 1), random.uniform(-1, 1)]

for epoch in range(100):
    for x, y in inputs:
        grad = linear_gradient(x, y, theta)
        theta = gradient_step(theta, grad, -learning_rate)
        print(epoch, theta)


slope, intercept = theta
assert 19.9 < slope < 20.1, "наклон должен быть равен примерно 20"
assert 4.9 < intercept < 5.1, "пересечение должно быть равным примерно 5"
