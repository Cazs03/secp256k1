import constantes
from constantes import *

def calcular_big(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    s = (y2 - y1) * inv(x2 - x1) % p
    raw_x = s * s - x1 - x2
    raw_y = s * (x1 - (raw_x % p)) - y1
    x3 = raw_x % p
    y3 = raw_y % p
    big = (raw_x + raw_y - x3 - y3 - s) % p
    overflow_x = raw_x // p
    overflow_y = raw_y // p
    return big, (x3, y3), s, overflow_x, overflow_y, x1, y1, x3, y3

def half_point(P):
    inv2 = inv(2, n)
    return point_mul(inv2, P)

print(f"k: {k}")
print(f"k binario (255-250): {bin(k)[2:8]}")
P = point_mul(k)

history_debug = history.copy()
bigs_reales = {h.pos: h.big for h in history_debug}

# POS 255: bit siempre = 1
P_255 = point_mul(2**255)
R_255 = point_add(P, (P_255[0], (p - P_255[1]) % p))
big_255, punto_255, s_255, overflow_x_255, overflow_y_255, x1_255, y1_255, x3_255, y3_255 = calcular_big(R_255, P_255)

print(f"\n--- POS 255 (bit=1 gratis) ---")
print(f"R_255.x (x1): {x1_255}")
print(f"R_255.y (y1): {y1_255}")
print(f"P_255.x (x2): {P_255[0]}")
print(f"P_255.y (y2): {P_255[1]}")
print(f"x3 (=P.x): {x3_255}")
print(f"y3 (=P.y): {y3_255}")
print(f"s: {s_255}")
print(f"overflow_x: {overflow_x_255}")
print(f"overflow_y: {overflow_y_255}")
print(f"big: {big_255}")

# POS 254
P_254 = half_point(P_255)
bit_254_real = 1 if bigs_reales.get(254) else 0

print(f"\n--- POS 254 (bit real = {bit_254_real}) ---")

# Camino A: bit=1
R_254_A = point_add(R_255, (P_254[0], (p - P_254[1]) % p))
big_254_A, punto_254_A, s_254_A, overflow_x_254_A, overflow_y_254_A, x1_254_A, y1_254_A, x3_254_A, y3_254_A = calcular_big(R_254_A, P_254)

print(f"\nCamino A (bit=1):")
print(f"  R_254_A.x (x1): {x1_254_A}")
print(f"  R_254_A.y (y1): {y1_254_A}")
print(f"  P_254.x (x2): {P_254[0]}")
print(f"  P_254.y (y2): {P_254[1]}")
print(f"  x3: {x3_254_A}")
print(f"  y3: {y3_254_A}")
print(f"  s: {s_254_A}")
print(f"  overflow_x: {overflow_x_254_A}")
print(f"  overflow_y: {overflow_y_254_A}")
print(f"  big: {big_254_A}")

# Camino B: bit=0
big_254_B, punto_254_B, s_254_B, overflow_x_254_B, overflow_y_254_B, x1_254_B, y1_254_B, x3_254_B, y3_254_B = calcular_big(R_255, P_254)

print(f"\nCamino B (bit=0):")
print(f"  R_255.x (x1): {x1_254_B}")
print(f"  R_255.y (y1): {y1_254_B}")
print(f"  P_254.x (x2): {P_254[0]}")
print(f"  P_254.y (y2): {P_254[1]}")
print(f"  x3: {x3_254_B}")
print(f"  y3: {y3_254_B}")
print(f"  s: {s_254_B}")
print(f"  overflow_x: {overflow_x_254_B}")
print(f"  overflow_y: {overflow_y_254_B}")
print(f"  big: {big_254_B}")

print(f"\n--- VERIFICACIÓN ---")
print(f"big_254 real: {bigs_reales.get(254)}")
print(f"big_254_A == real: {big_254_A == bigs_reales.get(254)}")
print(f"big_254_B == real: {big_254_B == bigs_reales.get(254)}")
