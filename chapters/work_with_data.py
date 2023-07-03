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


