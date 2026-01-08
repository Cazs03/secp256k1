from constantes import *

P_list = [G]
for i in range(256):
    x1, y1 = P_list[-1]
    s = (3 * x1 * x1) * inv(2 * y1) % p
    raw_x = s * s - 2 * x1
    raw_y = s * (x1 - (raw_x % p)) - y1
    P_list.append((raw_x % p, raw_y % p))

P_pub = point_mul(k)

print(f"P_pub.x = {P_pub[0]}")
print()

def backward_step(R, P_i):
    return point_add(R, (P_i[0], (p - P_i[1]) % p))

def forward_step(R, P_i):
    return point_add(R, P_i)

R_255 = backward_step(P_pub, P_list[255])

print(f"R_255.x = {R_255[0]}")
print()

N = 4

bits_atras = [1, 0, 1, 0]
print(f"Camino hacia atrás: {''.join(map(str, bits_atras))}")

R_medio = R_255
for i, bit in enumerate(bits_atras):
    pos = 254 - i
    if bit == 1:
        R_medio = backward_step(R_medio, P_list[pos])

print(f"R_medio.x = {R_medio[0]}")
print()

print("=" * 60)
print("Todos los caminos hacia adelante con TODAS las x intermedias:")
print("=" * 60)
print()

for combo in range(2**N):
    bits_adelante = [(combo >> i) & 1 for i in range(N)]

    print(f"Adelante: {''.join(map(str, bits_adelante))}")
    print(f"  Inicio: x = {R_medio[0]}")

    R_test = R_medio
    for i in range(N-1, -1, -1):
        pos = 254 - i
        if bits_adelante[i] == 1:
            R_test = forward_step(R_test, P_list[pos])
        print(f"  Paso {N-1-i} (bit={bits_adelante[i]}, pos={pos}): x = {R_test[0]}")

    marca = ""
    if R_test[0] == R_255[0]:
        marca = " <-- R_255.x ✓"

    print(f"  Final: x = {R_test[0]}{marca}")
    print()
