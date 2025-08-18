#include <stdio.h>
#include <math.h>

#define MAX_FACTORS 1000

// หาตัวประกอบเฉพาะแบบ naive (trial division)
void prime_factors_naive(unsigned long long n, unsigned long long *count, unsigned long long *factors, unsigned long long *size) {
    *size = 0;
    unsigned long long divisor = 2;
    while (n > 1) {
        (*count)++;
        if (n % divisor == 0) {
            factors[(*size)++] = divisor;
            n /= divisor;
        } else {
            divisor++;
        }
    }
}

// ห.ร.ม. แบบ naive
unsigned long long find_gcd1(unsigned long long m, unsigned long long n, unsigned long long *operations) {
    unsigned long long m_factors[MAX_FACTORS], n_factors[MAX_FACTORS];
    unsigned long long m_size, n_size;

    prime_factors_naive(m, operations, m_factors, &m_size);
    prime_factors_naive(n, operations, n_factors, &n_size);

    unsigned long long gcd = 1;
    for (unsigned long long i = 0; i < m_size; i++) {
        for (unsigned long long j = 0; j < n_size; j++) {
            if (m_factors[i] == n_factors[j] && n_factors[j] != 0) {
                gcd *= m_factors[i];
                n_factors[j] = 0;
                break;
            }
        }
        (*operations)++;
    }
    return gcd;
}

// หาตัวประกอบเฉพาะโดยใช้ trial division (เวอร์ชันปรับปรุง)
void prime_factors_trial(unsigned long long n, unsigned long long *count, unsigned long long *factors, unsigned long long *size) {
    *size = 0;

    // หารด้วย 2 จนไม่ลงตัว
    while (n % 2 == 0) {
        factors[(*size)++] = 2;
        n /= 2;
        (*count)++;
    }

    // หารด้วยจำนวนคี่ตั้งแต่ 3 จนถึง sqrt(n)
    for (unsigned long long i = 3; i * i <= n; i += 2) {
        (*count)++;
        while (n % i == 0) {
            factors[(*size)++] = i;
            n /= i;
        }
    }

    // ถ้าเหลือเศษ > 1 แปลว่าเป็น prime ตัวสุดท้าย
    if (n > 1) {
        factors[(*size)++] = n;
        (*count)++;
    }
}

// ห.ร.ม. โดยใช้ trial division
unsigned long long find_gcd2(unsigned long long m, unsigned long long n, unsigned long long *operations) {
    unsigned long long m_factors[MAX_FACTORS], n_factors[MAX_FACTORS];
    unsigned long long m_size, n_size;

    prime_factors_trial(m, operations, m_factors, &m_size);
    prime_factors_trial(n, operations, n_factors, &n_size);

    unsigned long long gcd = 1;
    for (unsigned long long i = 0; i < m_size; i++) {
        for (unsigned long long j = 0; j < n_size; j++) {
            if (m_factors[i] == n_factors[j] && n_factors[j] != 0) {
                gcd *= m_factors[i];
                n_factors[j] = 0;
                break;
            }
        }
        (*operations)++;
    }
    return gcd;
}

// Euclidean algorithm
unsigned long long find_gcd3(unsigned long long m, unsigned long long n, unsigned long long *operations) {
    while (n != 0) {
        (*operations)++;
        unsigned long long temp = n;
        n = m % n;
        m = temp;
    }
    return m;
}

int main(void) {
    unsigned long long x = 953525754641ULL, y = 658518571823ULL;

    unsigned long long ops1 = 0, ops2 = 0, ops3 = 0;

    unsigned long long gcd1 = find_gcd1(x, y, &ops1);
    unsigned long long gcd2 = find_gcd2(x, y, &ops2);
    unsigned long long gcd3 = find_gcd3(x, y, &ops3);

    printf("GCD1 = %llu Operations = %llu\n", gcd1, ops1);
    printf("GCD2 = %llu Operations = %llu\n", gcd2, ops2);
    printf("GCD3 = %llu Operations = %llu\n", gcd3, ops3);

    return 0;
}
