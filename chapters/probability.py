import enum, random


# Enum - это типизированное множество перечислимых значений
# Мы можем их использовать для того, чтобы сделать код чище описательнее и читабельнее

# Парадокс мальчика и девочки
class Kid(enum.Enum):
    BOY = 0
    GIRL = 1


def random_kid() -> Kid:
    return random.choice([Kid.BOY, Kid.GIRL])


both_girls = 0
older_girl = 0
either_girl = 0

random.seed(0)

for _ in range(1000):
    younger = random_kid()
    older = random_kid()
    if older == Kid.GIRL:
        older_girl += 1
    if older == Kid.GIRL and younger == Kid.GIRL:
        both_girls += 1
    if older == Kid.GIRL or younger == Kid.GIRL:
        either_girl += 1

print("P(both | older): ", both_girls / older_girl)  # ~0.49
print("P(both | either): ", both_girls / either_girl)  # ~0.32


# функция плотности равномерного распределения
def uniform_pdf(x: float) -> float:
    return 1 if 0 <= x < 1 else 0


# (кумулятивная) функция распределения
def uniform_cdf(x: float) -> float:
    """Возвращает вероятность, что равномерно
       распределенная СВ <= x"""
    if x < 0: return 0  # Равномерная величина никогда не бывает меньше 0
    elif x < 1: return x  # Например, P(X <= 0.4) = 0.4
    else: return 1  # Равномерная величина всегда меньше 1


# Нормальное распределение
import math
SQRT_TWO_PI = math.sqrt(2 * math.pi)


# Функция плотности нормального распределения
def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    return math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (SQRT_TWO_PI * sigma)


# (кумулятивная) функция распределения
def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


# инвертирование кумулятивной функции normal_cdf
# чтобы находить значение, соответсвующее указанной вероятности
def inverse_normal_cdf(p: float,
                       mu: float = 0,
                       sigma: float = 1,
                       tolerance: float = 0.00001) -> float:  # задать точность
    """Отыскать приближенную инверсию, используя бинарный поиск"""
    # Если нестандартная, то вычислить стандартную и перешкалировать
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z = -10.0  # normal_cdf(-10) находится близко к 0
    hi_z = 10.0  # normal_cdf(10) находится близко к 1

    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2  # Рассмотреть среднюю точку
        mid_p = normal_cdf(mid_z)  # и значение CDF
        if mid_p < p:
            low_z = mid_z  # Средняя точка слишком низкая, искать выше
        else:
            hi_z = mid_z  # Средняя точка слишком высокая, искать ниже
    return mid_z


# Центральная предельная теорема
# Распределение Бернулли
def bernoulli_trial(p: float) -> int:
    """Возвращает 1 с вероятностью p и 0 с вероятностью 1-p"""
    return 1 if random.random() < p else 0


def binomial(n: int, p: float) -> int:
    """Возвращает сумму из n испытаний bernoulli(p)"""
    return sum(bernoulli_trial(p) for _ in range(n))

# продолжение в probability.ipynb
