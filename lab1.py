# ตัวแปรสำหรับนับจำนวน operation
op_count = 0


def prime_factors_naive(x):
    global op_count
    factors = []
    divisor = 2
    while x > 1:
        op_count += 1  # basic operation
        while x % divisor == 0:
            factors.append(divisor)
            x //= divisor
            op_count += 1
        divisor += 1
    return factors


def prime_factors_sieve(x):
    global op_count
    # สร้าง sieve
    sieve = [True] * (x + 1)
    sieve[0] = sieve[1] = False
    primes = []
    for i in range(2, x + 1):
        if sieve[i]:
            primes.append(i)
            for j in range(i * i, x + 1, i):
                sieve[j] = False
                op_count += 1
    # แยกตัวประกอบโดยใช้ primes
    factors = []
    for p in primes:
        while x % p == 0:
            factors.append(p)
            x //= p
            op_count += 1
    return factors


def FindGCD1(m, n):
    global op_count
    op_count = 0
    fm = prime_factors_naive(m)
    fn = prime_factors_naive(n)
    common = []
    for p in fm:
        if p in fn:
            common.append(p)
            fn.remove(p)
            op_count += 1
    result = 1
    for c in common:
        result *= c
        op_count += 1
    return result, op_count


def FindGCD2(m, n):
    global op_count
    op_count = 0
    fm = prime_factors_sieve(m)
    fn = prime_factors_sieve(n)
    common = []
    for p in fm:
        if p in fn:
            common.append(p)
            fn.remove(p)
            op_count += 1
    result = 1
    for c in common:
        result *= c
        op_count += 1
    return result, op_count


def FindGCD3(m, n):
    global op_count
    op_count = 0
    while m != n:
        op_count += 1
        if m > n:
            m = m % n
        else:
            n = n % m
        if m == 0 or n == 0:
            return m + n, op_count
    return m, op_count


# ตัวอย่างการทดสอบ
if __name__ == "__main__":
    m, n = 48, 18
    print("FindGCD1:", FindGCD1(m, n))
    print("FindGCD2:", FindGCD2(m, n))
    print("FindGCD3:", FindGCD3(m, n))
