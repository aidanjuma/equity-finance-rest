from enum import Enum


class AssetType(str, Enum):
    STOCK = 'stock'
    INDEX = 'index'
    FUTURE = 'future'
    CURRENCY = 'currency'
    CRYPTOCURRENCY = 'cryptocurrency'
