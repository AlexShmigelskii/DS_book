from typing import Tuple
import math


# Аппроксимация биномиальной случайной величины нормальным распределением
def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    """Возвращает mu и sigma, соответствующие binomial(n, p)"""
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    return mu, sigma


from probability import normal_cdf

# Нормальная функция CDF (normal_cdf) - это вероятность,
# что переменная лежит ниже порога
normal_probability_below = normal_cdf


# Она лежит выше порога, если она не ниже порога
def normal_probability_above(lo: float,
                             mu: float = 0,
                             sigma: float = 1) -> float:
    """Вероятность, что N(mu, sigma) выше, чем lo"""
    return 1 - normal_cdf(lo, mu, sigma)


# Она лежит между, если она меньше, чем hi, но выше чем lo
def normal_probability_between(lo: float,
                               hi: float,
                               mu: float = 0,
                               sigma: float = 1) -> float:
    """Вероятность, что N(mu, sigma) лежит между lo и hi"""
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


# Она лежит за пределами, если она не лежит между
def normal_probability_outside(lo: float,
                               hi: float,
                               mu: float = 0,
                               sigma: float = 1) -> float:
    """Вероятность, что N(mu, sigma) не лежит между lo и hi"""
    return 1 - normal_probability_between(lo, hi, mu, sigma)


from probability import inverse_normal_cdf


# Верхняя граница
def normal_upper_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    """Возвращает z, для которой P(Z <= z) = вероятность"""
    return inverse_normal_cdf(probability, mu, sigma)


# Нижняя граница
def normal_lower_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    """Возвращает z, для которой P(Z >= z) = вероятность"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


# Двусторонняя граница
def normal_two_sided_bounds(probability: float,
                            mu: float = 0,
                            sigma: float = 1) -> Tuple[float, float]:
    """Возвращает симметрические (вокруг среднего) границы,
       которые содержат указанную вероятность"""
    tail_probability = (1 - probability) / 2

    # Верхняя граница должна иметь хвостовую tail_probability выше ее
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    # Нижняя граница должна иметь хвостовую tail_probability ниже ее
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound


mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)

# Принимаем значимость = 5%

# (469, 531)
lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)


# 95%-ные границы, основанные на допущении, что p = 0.5
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

# Фактические mu и sigma, основанные на p = 0.55
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

# Ошибка 2-го рода означает, что нам не удалось отклонить нулевую гипотезу,
# что произойдет, когда Х все еще внутри нашего исходного интервала
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability  # ~0.8865

hi = normal_upper_bound(0.95, mu_0, sigma_0)
# равно 526 (< 531, т. к. нам нужно больше вероятности в верхнем хвосте)

type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
power = 1 - type_2_probability  # ~0.9364
