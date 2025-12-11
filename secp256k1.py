p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def modinv_p(a):
    return pow(a, p-2, p)

def mul(k):
    x, y = Gx, Gy
    rx, ry = None, None
    while k:
        if k & 1:
            if rx is None:
                rx, ry = x, y
            else:
                s = ((y - ry) * modinv_p(x - rx)) % p
                nx = (s*s - rx - x) % p
                ry = (s*(rx - nx) - ry) % p
                rx = nx
        s = (3*x*x * modinv_p(2*y)) % p
        nx = (s*s - 2*x) % p
        y = (s*(x - nx) - y) % p
        x = nx
        k >>= 1
    return rx, ry

def point_sub(P, Q):
    x2, y2 = Q
    return point_add(P, (x2, (p - y2) % p))

def point_add(P, Q):
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        return None
    s = ((y2 - y1) * modinv_p(x2 - x1)) % p
    nx = (s*s - x1 - x2) % p
    ny = (s*(x1 - nx) - y1) % p
    return (nx, ny)

def half_point(P):
    inv2 = pow(2, n-2, n)
    return mul_point(inv2, P)

def mul_point(k, P):
    rx, ry = None, None
    x, y = P
    while k:
        if k & 1:
            if rx is None:
                rx, ry = x, y
            else:
                s = ((y - ry) * modinv_p(x - rx)) % p
                nx = (s*s - rx - x) % p
                ry = (s*(rx - nx) - ry) % p
                rx = nx
        if k > 1:
            s = (3*x*x * modinv_p(2*y)) % p
            nx = (s*s - 2*x) % p
            y = (s*(x - nx) - y) % p
            x = nx
        k >>= 1
    return rx, ry

def reconstruir_bit1(P):
    # Q + G = P
    Q = point_sub(P, (Gx, Gy))
    s = ((Gy - Q[1]) * modinv_p(Gx - Q[0])) % p
    raw_x = s*s - Q[0] - Gx
    raw_y = s*(Q[0] - P[0]) - Q[1]
    overflow = raw_x // p
    big = (raw_x + raw_y - P[0] - P[1] - s) % p

    # Despejar incógnitas del paso anterior
    # raw_x = s² - Q.x - G.x  →  Q.x = s² - G.x - raw_x
    # raw_y = s*(Q.x - P.x) - Q.y  →  Q.y = s*(Q.x - P.x) - raw_y
    Qx_despejado = (s*s - Gx - overflow*p - P[0]) % p
    Qy_despejado = (s*(Q[0] - P[0]) - raw_y) % p

    return {
        'Q': Q,
        's': s,
        'raw_x': raw_x,
        'raw_y': raw_y,
        'overflow': overflow,
        'big': big,
        'Qx_despejado': Qx_despejado,
        'Qy_despejado': Qy_despejado
    }

def reconstruir_bit0(P):
    # 2Q = P
    Q = half_point(P)
    s = (3 * Q[0] * Q[0] * modinv_p(2 * Q[1])) % p
    raw_x = s*s - 2*Q[0]
    raw_y = s*(Q[0] - P[0]) - Q[1]
    overflow = raw_x // p
    big = (raw_x + raw_y - P[0] - P[1] - s) % p

    # Despejar incógnitas del paso anterior
    # raw_x = s² - 2*Q.x  →  Q.x = (s² - raw_x) / 2
    # raw_y = s*(Q.x - P.x) - Q.y  →  Q.y = s*(Q.x - P.x) - raw_y
    Qx_despejado = ((s*s - overflow*p - P[0]) * modinv_p(2)) % p
    Qy_despejado = (s*(Q[0] - P[0]) - raw_y) % p

    return {
        'Q': Q,
        's': s,
        'raw_x': raw_x,
        'raw_y': raw_y,
        'overflow': overflow,
        'big': big,
        'Qx_despejado': Qx_despejado,
        'Qy_despejado': Qy_despejado
    }

G = (Gx, Gy)

import random
k = random.randint(2**255, 2**256 - 1)
P = mul(k)
last_bit = k & 1

print(f"k = {k}")
print(f"último bit real = {last_bit}")
print()
print(f"P.x = {P[0]}")
print(f"P.y = {P[1]}")
print()

print("=== BIT 1 (Q + G = P) ===")
r1 = reconstruir_bit1(P)
print(f"Q.x = {r1['Q'][0]}")
print(f"Q.y = {r1['Q'][1]}")
print(f"s = {r1['s']}")
print(f"raw_x = {r1['raw_x']}")
print(f"raw_y = {r1['raw_y']}")
print(f"overflow = {r1['overflow']}")
print(f"big = {r1['big']}")
print(f"Qx_despejado = {r1['Qx_despejado']}")
print(f"Qy_despejado = {r1['Qy_despejado']}")
print(f"Qx match = {r1['Q'][0] == r1['Qx_despejado']}")
print(f"Qy match = {r1['Q'][1] == r1['Qy_despejado']}")
print()

print("=== BIT 0 (2Q = P) ===")
r0 = reconstruir_bit0(P)
print(f"Q.x = {r0['Q'][0]}")
print(f"Q.y = {r0['Q'][1]}")
print(f"s = {r0['s']}")
print(f"raw_x = {r0['raw_x']}")
print(f"raw_y = {r0['raw_y']}")
print(f"overflow = {r0['overflow']}")
print(f"big = {r0['big']}")
print(f"Qx_despejado = {r0['Qx_despejado']}")
print(f"Qy_despejado = {r0['Qy_despejado']}")
print(f"Qx match = {r0['Q'][0] == r0['Qx_despejado']}")
print(f"Qy match = {r0['Q'][1] == r0['Qy_despejado']}")
