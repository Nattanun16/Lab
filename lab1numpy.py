import matplotlib.pyplot as plt
import numpy as np
import time

# ---------------------------------------------------
# วิธีที่ 1: Prime Factorization (Naive)
# ---------------------------------------------------
def prime_factors_naive(n, counter):
    factors = []
    divisor = 2
    while n > 1:
        counter[0] += 1
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    return factors

def find_gcd1(m, n):
    counter = [0]
    m_factors = prime_factors_naive(m, counter)
    n_factors = prime_factors_naive(n, counter)
    gcd = 1
    for p in m_factors:
        if p in n_factors:
            gcd *= p
            n_factors.remove(p)
        counter[0] += 1
    return gcd, counter[0]

# ---------------------------------------------------
# วิธีที่ 2: Prime Factorization (with Sieve)
# ---------------------------------------------------
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

# ---------------------------------------------------
# วิธีที่ 3: Euclidean Algorithm
# ---------------------------------------------------
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

# ---------------------------------------------------
# ข้อมูลตัวเลข (คู่ m, n)
# ---------------------------------------------------
pairs = [
    (30,15),(20,72),(72,88),(58,77),(92,80),(286,544),(985,716),(839,433),
    (471,561),(269,749),(1888,1224),(3164,6996),(6253,5431),(4390,2874),
    (5017,7615),(76241,57606),(74766,64553),(12322,50440),(34726,92155),
    (14785,19817),(672270,431511),(694404,256785),(975922,532283),
    (279392,946230),(906443,392685),(2226412,8648878),(6061228,5546440),
    (1691980,1414558),(3234496,7268362),(8356954,3705742),(81786288,61052652),
    (21535993,91675657),(26586591,78851391),(68575643,45017255),(45991767,77583796),
    (459917672,775837965),(265865917,788513914),(685756433,450172557),(785756437,102475659),
    (504857673,354879547),(4737418245,9465215337),(7384184877,6565315335),
    (6531741823,8795491761),(5865583711,9535851393),(6954464645,8017257569),
    (84184418245,65310172575),(58659151391,85756451391),(57564301725,74851857673),
    (59917672487,88512663377),(65315344641,98418485851),(789176724879,659151396733),
    (659117416437,946585181391),(653184188245,758331017965),(841818235337,767318488245),
    (953525754641,658518571823)
]

# ---------------------------------------------------
# รันการทดลอง
# ---------------------------------------------------
ops1, ops2, ops3 = [], [], []

for m, n in pairs:
    _, c1 = find_gcd1(m, n)
    _, c2 = find_gcd2(m, n)
    _, c3 = find_gcd3(m, n)
    ops1.append(c1)
    ops2.append(c2)
    ops3.append(c3)

# ---------------------------------------------------
# วาดกราฟ
# ---------------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(ops1, label="Prime Factorization (Naive)", marker="o")
plt.plot(ops2, label="Prime Factorization (Sieve)", marker="s")
plt.plot(ops3, label="Euclidean Algorithm", marker="^")
plt.xlabel("Test Case Index")
plt.ylabel("Operation Count")
plt.title("Comparison of GCD Methods")
plt.legend()
plt.grid(True)
plt.savefig("gcd_methods_comparison.png", dpi=300)
plt.show()
