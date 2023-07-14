import random
from typing import List, Dict
from collections import Counter
import math
import matplotlib.pyplot as plt


def bucketsize(point: float, bucket_size: float) -> float:
    """Округлить точку до следующего наименьшего кратного
       размера интервала bucket_size """
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points: List[float], bucket_size: float) -> Dict[float, int]:
    """Разбивает точки на интервалы и подсчитывает
        их количество в каждом интервале"""
    return Counter(bucketsize(point, bucket_size) for point in points)


def plot_histogram(points: List[float], bucket_size: float, title: str=''):
    histogram = make_histogram(points, bucket_size)
    plt.bar(list(histogram.keys()),
            list(histogram.values()),
            width=bucket_size)
    plt.title(title)
    plt.show()


from chapters.linear_algebra import Matrix, Vector, make_matrix
from chapters.statistics import correlation


def correlation_matrix(data: List[Vector]) -> Matrix:
    """Возвращает матрицу размера len(data) x len(data),
       (i, j)-й элемент которой является корреляцией между data[i] и data[j]"""
    def correlation_ij(i: int, j: int) -> float:
        return correlation(data[i], data[j])

    return make_matrix(len(data), len(data), correlation_ij)


# Применение типизированных именованных кортежей
import datetime


# проблемный вариант, связанный с лишней занимаемой памятью и вероятностью присвоить лишнее (несуществующее) значение
stock_price = {'closing_price': 102.06,
               'date': datetime.date(2014, 8, 29),
               'symbol': 'AAPL'}


# Альтернатива - именованный кортеж
from collections import namedtuple

StockPrice = namedtuple('StockPrice', ['symbol', 'date', 'closing_price'])
price = StockPrice('MSFT', datetime.date(2018, 12, 14), 106.03)

assert price.symbol == 'MSFT'
assert price.closing_price == 106.03


from typing import NamedTuple


class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self) -> bool:
        """Это класс, и поэтому мы также можем добавлять методы"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']


price = StockPrice('MSFT', datetime.date(2018, 12, 14), 106.03)

assert price.symbol == 'MSFT'
assert price.closing_price == 106.03
assert price.is_high_tech()


from dataclasses import dataclass

# Имеет ту же проблему с "случайными" ключами, что и словари
@dataclass
class StockPrice2:
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self) -> bool:
        """Это класс, и поэтому мы также можем добавлять методы"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']


price2 = StockPrice2('MSFT', datetime.date(2018, 12, 14), 106.03)

assert price.symbol == 'MSFT'
assert price.closing_price == 106.03
assert price.is_high_tech()


# Очистка и конвертирование
from dateutil.parser import parse


def parse_row(row: List[str]) -> StockPrice:
    symbol, date, closing_price = row
    return StockPrice(symbol=symbol,
                      date=parse(date).date(),
                      closing_price=float(closing_price))


# Тестируем функцию
stock = parse_row(["MSFT", "2018-12-14", "106.03"])


assert stock.symbol == 'MSFT'
assert stock.closing_price == 106.03
assert stock.date == datetime.date(2018, 12, 14)


from typing import Optional
import re


def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    symbol, date_, closing_price_ = row

    # Символ акции должен состоять из прописных букв
    if not re.match(r"^[A-Z]+$", symbol):
        return None

    try:
        date = parse(date_).date()
    except ValueError:
        return None

    try:
        closing_price = float(closing_price_)
    except ValueError:
        return None

    return StockPrice(symbol, date, closing_price)


# Должно вернуть None в случае ошибок
assert try_parse_row(["MSFT0", "2018-12-14", "106.03"]) is None
assert try_parse_row(["MSFT", "2018-12--14", "106.03"]) is None
assert try_parse_row(["MSFT", "2018-12-14", "x"]) is None

# Но должно вернуть то же, что и раньше, если данные хорошие
assert try_parse_row(["MSFT", "2018-12-14", "106.03"]) == stock


data = [
    StockPrice(symbol='MSFT',
               date=datetime.date(2018, 12, 24),
               closing_price=106.03),
]

# Максимальная цена акции AAPL
max_aapl_price = max([stock_price.closing_price
                     for stock_price in data
                     if stock_price.symbol == "AAPL"], default=0)

# Максимальная цена всех акций
from collections import defaultdict


max_prices: Dict[str, float] = defaultdict(lambda : float('-inf'))

for sp in data:
    symbol, closing_price = sp.symbol, sp.closing_price
    if closing_price > max_prices[symbol]:
        max_prices[symbol] = closing_price


# Максимальное/Минимальное однодневное процентное изменение
from typing import List
from collections import defaultdict


# Собрать цены по символу
prices: Dict[str, List[StockPrice]] = defaultdict(list)

for sp in data:
    prices[sp.symbol].append(sp)

# Упорядочить по дате
prices = {symbol: sorted(symbol_prices)
          for symbol, symbol_prices in prices.items()}


# Эти цены можно использовать для вычисления последовательности изменений день ко дню
def pct_change(yesterday: StockPrice, today: StockPrice) -> float:
    return today.closing_price / yesterday.closing_price - 1


class DailyChange(NamedTuple):
    symbol: str
    date: datetime.date
    pct_change: float


def day_over_day_changes(prices: List[StockPrice]) -> List[DailyChange]:
    """Предполагает. что цены только для одной акции и упорядочены"""
    return [DailyChange(symbol=today.symbol,
                        date=today.date,
                        pct_change=pct_change(yesterday, today))
            for yesterday, today in zip(prices, prices[1:])]


# И собираем их все
all_changes = [change
               for symbol_prices in prices.values()
               for change in day_over_day_changes(symbol_prices)]

max_change = max(all_changes, key=lambda change: change.pct_change, default=0)
min_change = min(all_changes, key=lambda change: change.pct_change, default=0)


# среднедневное изменение по месяцу
changes_by_month: List[DailyChange] = {month: [] for month in range(1, 13)}

for change in all_changes:
    changes_by_month[change.date.month].append(change)

# avg_daily_change = {
#     month: sum(change.pct_change for change in changes) / len(changes)
#     for month, changes in changes_by_month.items()
# }


# Шкалирование
from chapters.linear_algebra import distance


a_to_b = distance([63, 150], [67, 160])        # 10.77
a_to_c = distance([63, 150], [70, 171])        # 22.14
b_to_c = distance([67, 160], [70, 171])        # 11.40

a_to_b = distance([160, 150], [170.2, 160])    # 14.28
a_to_c = distance([160, 150], [177.8, 171])    # 27.53
b_to_c = distance([170.2, 160], [177.8, 171])  # 13.37

from typing import Tuple

from chapters.linear_algebra import vector_mean
from chapters.statistics import standard_deviation


def scale(data: List[Vector]) -> Tuple[Vector, Vector]:
    """Возвращает среднее значение и стандартное отклонение
       для каждой позиции"""
    dim = len(data[0])

    means = vector_mean(data)
    stdevs = [standard_deviation([vector[i] for vector in data])
              for i in range(dim)]

    return means, stdevs


from chapters.linear_algebra import distance

a_to_b = distance([63, 150], [67, 160])        # 10.77
a_to_c = distance([63, 150], [70, 171])        # 22.14
b_to_c = distance([67, 160], [70, 171])        # 11.40

a_to_b = distance([160, 150], [170.2, 160])    # 14.28
a_to_c = distance([160, 150], [177.8, 171])    # 27.53
b_to_c = distance([170.2, 160], [177.8, 171])  # 13.37

from typing import Tuple

from chapters.linear_algebra import vector_mean
from chapters.statistics import standard_deviation


def scale(data: List[Vector]) -> Tuple[Vector, Vector]:
    """returns the means and standard deviations for each position"""
    dim = len(data[0])

    means = vector_mean(data)
    stdevs = [standard_deviation([vector[i] for vector in data])
              for i in range(dim)]

    return means, stdevs

vectors = [[-3, -1, 1], [-1, 0, 1], [1, 1, 1]]
means, stdevs = scale(vectors)
assert means == [-1, 0, 1]
assert stdevs == [2, 1, 0]


def rescale(data: List[Vector]) -> List[Vector]:
    """
    Шкалирует входные данные так, чтобы каждый столбец
    имел нулевое среднее значение и станартное отклонение, равное 1
    (оставляет позицию как есть, если ее стандартное отклонение равно 0)
    """
    dim = len(data[0])
    means, stdevs = scale(data)

    # Make a copy of each vector
    rescaled = [v[:] for v in data]

    for v in rescaled:
        for i in range(dim):
            if stdevs[i] > 0:
                v[i] = (v[i] - means[i]) / stdevs[i]

    return rescaled

means, stdevs = scale(rescale(vectors))
assert means == [0, 0, 1]
assert stdevs == [1, 1, 0]



# библиотека tqdm
import tqdm

for i in tqdm.tqdm(range(100)):
    # Делать что-то медленное
    _ = [random.random() for _ in range(1000000)]


def primes_up_to(n: int) -> List[int]:
    primes = [2]

    with tqdm.trange(3, n) as t:
        for i in t:
            # i является простым, если нет меньшего простого, которое делит его
            i_is_prime = not any(i % p == 0 for p in primes)
            if i_is_prime:
                primes.append(i)
            t.set_description(f"{len(primes)} простых")

    return primes


my_primes = primes_up_to(100_000)


# Снижение размерности
from chapters.linear_algebra import subtract


def se_mean(data: List[Vector]) -> List[Vector]:
    """Перецентрировать данные, чтобы иметь среднее,
       равное 0, в каждой размерности"""
    mean = vector_mean(data)
    return [subtract(vector, mean) for vector in data]


from chapters.linear_algebra import magnitude


def direction(w: Vector) -> Vector:
    mag = magnitude(w)
    return [w_i / mag for w_i in w]


from chapters.linear_algebra import dot


def directional_variance(data: List[Vector], w: Vector) -> float:
    """Возвращает дисперсию x в направлении w"""
    w_dir = direction(w)
    return sum(dot(v, w_dir) ** 2 for v in data)


def directional_variance_gradient(data: List[Vector], w: Vector) -> Vector:
    """Градиент направленной дисперсии по отношению к w"""
    w_dir = direction(w)
    return [sum(2 * dot(v, w_dir) * v[i] for v in data)
            for i in range(len(w))]

