from collections import Counter
from typing import List
from random import randint

Vector = List[float]

num_friends = [randint(1, 101) for _ in range(204)]


# Среднее значение
def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


def _median_odd(xs: List[float]) -> float:
    """Если len(xs) является нечетнрй,
       то медиана - средний элемент"""
    return sorted(xs)[len(xs) // 2]


def _median_even(xs: List[float]) -> float:
    """Если len(xs) является четнрй, то она является средним значением
       двух средних значений"""
    sorted_xs = sorted(xs)
    hi_midpoint = len(xs) // 2
    return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2


def median(v: List[float]) -> float:
    """Отыскивает 'ближайшее к середине' значение v"""
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)


assert median([1, 10, 2, 9, 5]) == 5
assert median([1, 9, 2, 10]) == (2 + 9) / 2

print(median(num_friends))


# Квантиль - значение, ниже которого располагается определенный процентиль данных
def quantile(xs: List[float], p: float) -> float:
    """Возвращает значение p-го процентиля xs"""
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]

print(quantile(num_friends, 0.10))
print(quantile(num_friends, 0.25))
print(quantile(num_friends, 0.75))
print(quantile(num_friends, 0.90))


def mode(xs: List[float]) -> List[float]:
    """Возвращает список, т. к. может быть больше одной моды"""
    counts = Counter(xs)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items()
            if count == max_count]


print(mode(num_friends))
