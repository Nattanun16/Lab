import math

MAX_FACTORS = 1000


# หาตัวประกอบเฉพาะแบบ naive (trial division)
def prime_factors_naive(n, operations):
    factors = []
    divisor = 2

    while n > 1:
        operations[0] += 1
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1

    return factors


# ห.ร.ม. แบบ naive
def find_gcd1(m, n, operations):
    m_factors = prime_factors_naive(m, operations)
    n_factors = prime_factors_naive(n, operations)

    gcd = 1
    for i in range(len(m_factors)):
        for j in range(len(n_factors)):
            if m_factors[i] == n_factors[j] and n_factors[j] != 0:
                gcd *= m_factors[i]
                n_factors[j] = 0
                break
        operations[0] += 1

    return gcd


# หาตัวประกอบเฉพาะโดยใช้ trial division (เวอร์ชันปรับปรุง)
def prime_factors_trial(n, operations):
    factors = []

    # หารด้วย 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
        operations[0] += 1

    # หารด้วยจำนวนคี่
    i = 3
    while i * i <= n:
        operations[0] += 1
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # ถ้าเหลือ prime ตัวสุดท้าย
    if n > 1:
        factors.append(n)
        operations[0] += 1

    return factors


# ห.ร.ม. โดยใช้ trial division
def find_gcd2(m, n, operations):
    m_factors = prime_factors_trial(m, operations)
    n_factors = prime_factors_trial(n, operations)

    gcd = 1
    for i in range(len(m_factors)):
        for j in range(len(n_factors)):
            if m_factors[i] == n_factors[j] and n_factors[j] != 0:
                gcd *= m_factors[i]
                n_factors[j] = 0
                break
        operations[0] += 1

    return gcd


# Euclidean algorithm
def find_gcd3(m, n, operations):
    while n != 0:
        operations[0] += 1
        m, n = n, m % n
    return m


def main():
    x = 953_525_754_641
    y = 658_518_571_823

    ops1 = [0]
    ops2 = [0]
    ops3 = [0]

    gcd1 = find_gcd1(x, y, ops1)
    gcd2 = find_gcd2(x, y, ops2)
    gcd3 = find_gcd3(x, y, ops3)

    print(f"GCD1 = {gcd1} Operations = {ops1[0]}")
    print(f"GCD2 = {gcd2} Operations = {ops2[0]}")
    print(f"GCD3 = {gcd3} Operations = {ops3[0]}")


if __name__ == "__main__":
    main()
