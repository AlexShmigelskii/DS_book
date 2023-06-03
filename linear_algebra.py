from typing import List

Vector = List[float]


def add(v: Vector, w: Vector) -> Vector:
    """Складывает соответсвующие элементы"""
    assert len(v) == len(w), " векторы должны иметь одинаковую длину"

    return [v_i + w_i for v_i, w_i in zip(v, w)]


assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]


def subtract(v: Vector, w: Vector) -> Vector:
    "Вычитает соответсвующте элементы"
    assert len(v) == len(w), "векторы должны иметь одинаковую длину"

    return [v_i - w_i for v_i, w_i in zip(v, w)]


assert subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]


def vector_sum(vectors: List[Vector]) -> Vector:
    """Суммирует все соответсвующие элементы"""
    assert vectors, "Векторы не предоставлены!"

    length = len(vectors[0])

    assert all(len(v) == length for v in vectors), "векторы должны иметь одинаковую длину"

    return [sum(vector[i] for vector in vectors)
            for i in range(length)]


assert vector_sum([[1, 2], [3, 4], [5, 6], [7, 8]]) == [16, 20]


def scalar_multiply(c: float, v: Vector) -> Vector:
    """Умножает каждый элемент на c"""
    return [c * v_i for v_i in v]


assert scalar_multiply(2, [1, 2, 3]) == [2, 4, 6]


def vector_mean(vectors: List[Vector]) -> Vector:
    """Вычисляет поэлементное среднее арифметическое"""
    n = len(vectors)

    return scalar_multiply(1/n, vector_sum(vectors))


assert vector_mean([[1, 2], [3, 4], [5, 6]]) == [3, 4]




