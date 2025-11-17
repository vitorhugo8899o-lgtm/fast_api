from enum import Enum


class TypeProcuct(str, Enum):
    shirt = 'shirt'
    pants = 'pants'
    cap = 'cap'
    backpack = 'backpack'


class PartnerBrands(str, Enum):
    Oakley = 'Oakley'
    Nike = 'Nike'
    Adidas = 'Adidas'
    Tilibra = 'Tilibra'


class Size(str, Enum):
    G = 'G'
    M = 'M'
    P = 'P'
    PP = 'PP'
