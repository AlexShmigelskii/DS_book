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
