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


def dot(v: Vector, w: Vector) -> float:
    """Вычисляет v_i * w_i + ... + v_n * w_n"""
    assert len(v) == len(w), "векторы должны иметь одинаковую длину"

    return sum(v_i * w_i for v_i, w_i in zip(v, w))


assert dot([1, 2, 3], [4, 5, 6]) == 32


def sum_of_squares(v: Vector) -> float:
    """Возвращает v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


assert sum_of_squares([1, 2, 3]) == 14


import math


def magnitude(v: Vector) -> float:
    """Возвращает магнитуду (длину) вектора v"""
    return math.sqrt(sum_of_squares(v))


assert magnitude([3, 4]) == 5


# Вычисление евклидова расстояния
# def squared_distance(v: Vector, w: Vector) -> float:
#     """Вычисляет (v_1 - w_1) ** 2 + ... (v_n - w_n) ** 2"""
#     return sum_of_squares(subtract(v, w))
#
#
# def distance(v: Vector, w: Vector) -> float:
#     """Вычисляет расстояние между v и w"""
#     return math.sqrt(squared_distance(v, w))


# эквивалентная функция
def distance(v: Vector, w: Vector) -> float:
    return magnitude(subtract(v, w))


# Matrix
from typing import Tuple

Matrix = List[List[float]]


def shape(A: Matrix) -> Tuple[int, int]:
    """Возвращает (число строк А, число столбцов А)"""
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0  # Число элементов в первой строке
    return num_rows, num_cols


assert shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)


def get_row(A: Matrix, i: int) -> Vector:
    """Возвращает i-ю строку А (как тип Vector)"""
    return A[i]


def get_col(A: Matrix, j: int) -> Vector:
    """Возвращает j-й столбец А (как тип Vector)"""
    return [A_i[j] for A_i in A]


from typing import Callable


def make_matrix(num_rows: int,
                num_cols: int,
                entry_fn: Callable[[int, int], float]) -> Matrix:
    """
    Возвращает матрицу размера num_rows х num_cols,
    чей (i, j)-й элемент является функцией entry_fn(i, j)
    """
    return [[entry_fn(i, j)
             for j in range(num_cols)]
            for i in range(num_rows)]


# Единичная матрица
def identity_matrix(n: int) -> Matrix:
    """Возвращает (n x n) - единичную матрицу"""
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)


assert identity_matrix(5) == [[1, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 1]]



