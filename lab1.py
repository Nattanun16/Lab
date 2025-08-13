def prime_factors_naive(n, counter): #รับตัวเลข n และตัวนับ counter (อยู่ใน list เพื่อส่งกลับได้)
    factors = []
    divisor = 2
    while n > 1:
        counter[0] += 1  # นับการเปรียบเทียบหรือการหาร
        if n % divisor == 0: #ถ้า n หารด้วย divisor ลงตัว ให้เก็บ divisor เป็นตัวประกอบและหารออก
            factors.append(divisor) # เจอตัวประกอบ
            n //= divisor # หารออกไป
        else: #ถ้าไม่ลงตัว ให้เพิ่ม divisor ทีละ 1
            divisor += 1 # ลองตัวหารถัดไป
    return factors # ส่งกลับลิสต์ตัวประกอบที่ได้


def find_gcd1(m, n): #ห.ร.ม. โดยการแยกตัวประกอบแบบ naive
    counter = [0]  # ใช้ list เพื่อให้ส่งค่ากลับได้
    m_factors = prime_factors_naive(m, counter) #เรียกฟังก์ชันแยกตัวประกอบจำนวนเฉพาะแบบง่ายกับ m
    n_factors = prime_factors_naive(n, counter)  #เรียกฟังก์ชันแยกตัวประกอบจำนวนเฉพาะแบบง่ายกับ n และใช้ตัวนับ counter ชุดเดิม (จึงสะสมรวม)

    # หาค่าที่ซ้ำกัน
    gcd = 1 # เริ่มต้นห.ร.ม. เป็น 1
    for p in m_factors: #วนดูทีละตัวประกอบจากฝั่ง m
        if p in n_factors: #เช็คว่า p ตัวนี้มีอยู่ในลิสต์ตัวประกอบของ n ด้วยไหม โดยถ้ามี แปลว่า p เป็น “ตัวประกอบร่วม” อย่างน้อยหนึ่งตัว
            gcd *= p #ถ้าเป็นตัวประกอบร่วม ก็คูณ p เข้าไปในผลลัพธ์ gcd
            n_factors.remove(p)  # เอาออกเพื่อป้องกันนับซ้ำ
        counter[0] += 1

    return gcd, counter[0] # ส่งกลับห.ร.ม. และจำนวนการดำเนินการที่นับได้


# ตัวอย่าง
gcd1, ops1 = find_gcd1(742271756, 606228865)
print("GCD1 =", gcd1, "Operations =", ops1)


def sieve(limit): # ใช้ Sieve of Eratosthenes เพื่อหาตัวเลขเฉพาะ
    primes = []
    is_prime = [True] * (limit + 1) # สร้างลิสต์ที่บอกว่าตัวเลขแต่ละตัวเป็นเฉพาะหรือไม่
    for p in range(2, limit + 1): # เริ่มจาก 2 ถึง limit
         
        if is_prime[p]: # ถ้า p ยังเป็นจำนวนเฉพาะ
            primes.append(p) # เก็บ p ลงในลิสต์ primes
            for multiple in range(p * p, limit + 1, p): # เริ่มตัดเลขที่เป็นพหุคูณของ p
                
                is_prime[multiple] = False #ตัดเลขที่เป็นพหุคูณของ p ออกจากการเป็นจำนวนเฉพาะ
    return primes # ส่งกลับลิสต์ของจำนวนเฉพาะที่พบ


def prime_factors_sieve(n, primes, counter): # ใช้ Sieve of Eratosthenes เพื่อหาตัวประกอบเฉพาะของ n
    factors = []
    for p in primes: #วนดูจำนวนเฉพาะที่ได้จาก Sieve
        counter[0] += 1
        while n % p == 0: # ถ้า n หารด้วย p ลงตัว
            counter[0] += 1
            factors.append(p) # เก็บ p เป็นตัวประกอบ
            n //= p # หาร n ออกไป
        if n == 1:
            break
    return factors


def find_gcd2(m, n): #ห.ร.ม. โดยใช้ Sieve of Eratosthenes
    counter = [0]
    primes = sieve(max(m, n)) # สร้างลิสต์จำนวนเฉพาะที่ใช้ในการแยกตัวประกอบ
    m_factors = prime_factors_sieve(m, primes, counter) # แยกตัวประกอบเฉพาะของ m
    n_factors = prime_factors_sieve(n, primes, counter) # แยกตัวประกอบเฉพาะของ n

    gcd = 1 # เริ่มต้นห.ร.ม. เป็น 1
    for p in m_factors: #วนดูทีละตัวประกอบจากฝั่ง m
        if p in n_factors: #เช็คว่า p ตัวนี้มีอยู่ในลิสต์ตัวประกอบของ n ด้วยไหม
            gcd *= p #ถ้าเป็นตัวประกอบร่วม ก็คูณ p เข้าไปในผลลัพธ์ gcd
            n_factors.remove(p) # เอาออกเพื่อป้องกันนับซ้ำ
        counter[0] += 1

    return gcd, counter[0] # ส่งกลับห.ร.ม. และจำนวนการดำเนินการที่นับได้


# ตัวอย่าง
gcd2, ops2 = find_gcd2(742271756, 606228865)
print("GCD2 =", gcd2, "Operations =", ops2)


def find_gcd3(m, n): #ห.ร.ม. โดยใช้วิธี Euclidean algorithm (แบบใช้ modulus)
    counter = [0] # ใช้ list เพื่อให้ส่งค่ากลับได้
    while m != n: #solving until m and n are equal
        counter[0] += 1
        if m > n: 
            m = m % n # หาร m ด้วย n และเก็บเศษไว้ใน m
            if m == 0:
                m = n
        else:
            n = n % m # หาร n ด้วย m และเก็บเศษไว้ใน n
            if n == 0:
                n = m
    return m, counter[0] # ส่งกลับห.ร.ม. และจำนวนการดำเนินการที่นับได้


# ตัวอย่าง
gcd3, ops3 = find_gcd3(742271756, 606228865)
print("GCD3 =", gcd3, "Operations =", ops3)
