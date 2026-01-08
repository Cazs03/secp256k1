from constantes import G, point_mul, point_add, p, n, inv, Point, history

def big_add(P1: Point, P2: Point) -> tuple:
    x1, y1 = P1
    x2, y2 = P2
    s = (y2 - y1) * inv(x2 - x1) % p
    raw_x = s * s - x1 - x2
    raw_y = s * (x1 - (raw_x % p)) - y1
    x3 = raw_x % p
    y3 = raw_y % p
    big = (raw_x + raw_y - x3 - y3 - s) % p
    return big, (x3, y3), s, raw_x // p, raw_y // p

def big_double(P: Point) -> tuple:
    x1, y1 = P
    s = (3 * x1 * x1) * inv(2 * y1) % p
    raw_x = s * s - 2 * x1
    raw_y = s * (x1 - (raw_x % p)) - y1
    x3 = raw_x % p
    y3 = raw_y % p
    big = raw_x + raw_y - x3 - y3 - (s % p)
    big_add(P, (x3, y3))
    return big, (x3, y3), s, raw_x // p, raw_y // p

def half_point(P: Point) -> Point:
    return point_mul(inv(2, n), P)

def neg_point(P: Point) -> Point:
    return (P[0], (p - P[1]) % p)

k = 76986602635894612984162285505016623229638813641482555458765054502519283612074
P = point_mul(k)
num_bits = 256

bigs_reales = {h.pos: h.big for h in history if h.op == "ADD"}

print(f"k: {k}")
print(f"num_bits: {num_bits}")
print()

R = P
P_i = point_mul(2**255)

for i in range(255, -1, -1):
    bit = (k >> i) & 1

    if bit == 1:
        if i == 0:
            # bit 0 = 1, R ya es G
            print(f"Pos {i}: bit=1, R = G")
        else:
            R_new = point_add(R, neg_point(P_i))
            if R_new is not None:
                big, _, s, ox, oy = big_add(R_new, P_i)
                big_real = bigs_reales.get(i)
                match = big == big_real
                R = R_new
                print(f"Pos {i}: bit=1, big={big}, match={match}")

    if i > 0:
        big_d, P_d, s_d, ox_d, oy_d = big_double(P_i)
        print(f"  big_double: {big_d}")
        P_i = half_point(P_i)

print()
if (k & 1) == 0:
    R = half_point(R)
    print("bit 0 = 0, aplicando half_point")

print(f"R final: {R}")
print(f"G: {G}")
print(f"Llegamos a G: {R == G}")
