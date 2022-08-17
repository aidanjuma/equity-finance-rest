from enum import Enum


class AssetType(Enum):
    STOCK = 'stock'
    INDEX = 'index'
    FUTURE = 'future'
    CURRENCY = 'currency'
