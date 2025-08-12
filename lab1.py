def prime_factors_naive(n, counter):
    factors = []
    divisor = 2
    while n > 1:
        counter[0] += 1  # นับการเปรียบเทียบหรือการหาร
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    return factors


def find_gcd1(m, n):
    counter = [0]  # ใช้ list เพื่อให้ส่งค่ากลับได้
    m_factors = prime_factors_naive(m, counter)
    n_factors = prime_factors_naive(n, counter)

    # หาค่าที่ซ้ำกัน
    gcd = 1
    for p in m_factors:
        if p in n_factors:
            gcd *= p
            n_factors.remove(p)  # เอาออกเพื่อป้องกันนับซ้ำ
        counter[0] += 1

    return gcd, counter[0]


# ตัวอย่าง
gcd1, ops1 = find_gcd1(60, 48)
print("GCD1 =", gcd1, "Operations =", ops1)


def sieve(limit, counter):
    primes = []
    is_prime = [True] * (limit + 1)
    for p in range(2, limit + 1):
        counter[0] += 1
        if is_prime[p]:
            primes.append(p)
            for multiple in range(p * p, limit + 1, p):
                counter[0] += 1
                is_prime[multiple] = False
    return primes


def prime_factors_sieve(n, primes, counter):
    factors = []
    for p in primes:
        counter[0] += 1
        while n % p == 0:
            counter[0] += 1
            factors.append(p)
            n //= p
        if n == 1:
            break
    return factors


def find_gcd2(m, n):
    counter = [0]
    primes = sieve(max(m, n), counter)
    m_factors = prime_factors_sieve(m, primes, counter)
    n_factors = prime_factors_sieve(n, primes, counter)

    gcd = 1
    for p in m_factors:
        if p in n_factors:
            gcd *= p
            n_factors.remove(p)
        counter[0] += 1

    return gcd, counter[0]


# ตัวอย่าง
gcd2, ops2 = find_gcd2(60, 48)
print("GCD2 =", gcd2, "Operations =", ops2)


def find_gcd3(m, n):
    counter = [0]
    while m != n:
        counter[0] += 1
        if m > n:
            m = m % n
            if m == 0:
                m = n
        else:
            n = n % m
            if n == 0:
                n = m
    return m, counter[0]


# ตัวอย่าง
gcd3, ops3 = find_gcd3(60, 48)
print("GCD3 =", gcd3, "Operations =", ops3)
