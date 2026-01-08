import random
from typing import Tuple, Optional, List

Point = Tuple[int, int]
OptionalPoint = Optional[Point]
p: int = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n: int = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx: int = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy: int = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G: Point = (Gx, Gy)
k: int = random.randint(2**255, 2**256 - 1)

class H:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
    def __repr__(self):
        return '\n'.join(f"{key}: {val}" for key, val in self.__dict__.items())

history: List[H] = []
history_double: List[H] = []

def inv(x: int, m: int = p) -> int:
    return pow(x, m - 2, m)

def point_mul(k: int, P: OptionalPoint = None) -> OptionalPoint:
    history.clear()
    history_double.clear()
    if P is None: P = G
    R: OptionalPoint = None
    bit_pos = 0
    while k:
        bit = k & 1
        if bit:
            if R is None:
                R = P
                history.append(H(op="INIT", bit=1, pos=bit_pos, x1=None, y1=None, x2=P[0], y2=P[1], x3=P[0], y3=P[1], big=None, overflow=None, s=None))
            else:
                x1, y1 = R
                x2, y2 = P
                s = (y2 - y1) * inv(x2 - x1) % p
                raw_x = s * s - x1 - x2
                raw_y = s * (x1 - (raw_x % p)) - y1
                x3 = raw_x % p
                y3 = raw_y % p
                overflow = raw_x // p
                big = (raw_x + raw_y - x3 - y3 - s) % p
                history.append(H(op="ADD", bit=1, pos=bit_pos, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, big=big, overflow=overflow, s=s))
                R = (x3, y3)

        x1, y1 = P
        s = (3 * x1 * x1) * inv(2 * y1) % p
        raw_x = s * s - 2 * x1
        raw_y = s * (x1 - (raw_x % p)) - y1
        big_double = raw_x + raw_y - (raw_x % p) - (raw_y % p) - s % p
        history_double.append(H(op="DOUBLE", pos=bit_pos, x1=x1, y1=y1, big_double=big_double))

        P = (raw_x % p, raw_y % p)
        k >>= 1
        bit_pos += 1
    return R

def point_add(P: OptionalPoint, Q: OptionalPoint) -> OptionalPoint:
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if y1 != y2: return None
        s = (3 * x1 * x1) * inv(2 * y1) % p
    else:
        s = (y2 - y1) * inv(x2 - x1) % p
    raw_x = s * s - x1 - x2
    raw_y = s * (x1 - (raw_x % p)) - y1
    return (raw_x % p, raw_y % p)

__all__ = [
    'p', 'n', 'Gx', 'Gy', 'G',
    'Point', 'OptionalPoint',
    'history', 'history_double', 'H',
    'inv', 'point_add', 'point_mul', 'k'
]
