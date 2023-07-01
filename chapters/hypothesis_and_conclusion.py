import random
from typing import Tuple
import math


# Аппроксимация биномиальной случайной величины нормальным распределением
def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    """Возвращает mu и sigma, соответствующие binomial(n, p)"""
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    return mu, sigma


from chapters.probability import normal_cdf

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


from chapters.probability import inverse_normal_cdf


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


# P-значения
# Двустороннее p-значение
def two_sided_p_value(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
       Насколько правдоподобно увидеть значение, как минимум, такое же
       предельное, что и x (в любом направлении), если наши значения
       поступают из N(mu, sigma)?
    """
    if x >= mu:
        # х больше, чем среднее, поэтому хвост везде больше, чем х
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # х меньше, чем среднее, поэтому хвост везде меньше, чем х
        return 2 * normal_probability_below(x, mu, sigma)


upper_p_value = normal_probability_above
lower_p_value = normal_probability_below


from typing import List


def run_experiment() -> List[bool]:
    """Подбрасывает уравновешенную монету 1000 раз,
       Истина = орлы, Ложь = решки"""
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment: List[bool]) -> bool:
    """Использование 5%-ных уровней значимости"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531


random.seed(0)
experiments = [run_experiment() for _ in range(1000)]

num_rejections = len([experiment
                      for experiment in experiments
                      if reject_fairness(experiment)])


assert num_rejections == 46, f'{num_rejections}'


# Проведение А/В тестирования
# оценочные параметры
def estimated_parameters(N: int, n: int) -> Tuple[float, float]:
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma


# проверка, что p_a и p_b одинаковы (p_a - p_b = 0)
def a_b_test_statistic(N_A: int, n_A: int, N_B: int, n_B: int) -> float:
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A**2 + sigma_B**2)


# Байесов вывод
# бета-распределение
def B(alpha: float, beta: float) -> float:
    """Нормализирующая константа, чтобы полная
       вероятность в суме составляла 1"""
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)


def beta_pdf(x: float, alpha: float, beta: float) -> float:
    if x <= 0 or x >= 1:  # за пределами [0, 1] нет веса
        return 0
    return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)
