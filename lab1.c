#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define MAX_LIMIT 1000000

// -------------------------------------------
// Prime factorization (naive method)
void prime_factors_naive(long long n, int *operations, long long factors[], int *size)
{
    *size = 0;
    for (long long i = 2; i <= n; i++)
    {
        while (n % i == 0)
        {
            factors[(*size)++] = i;
            n /= i;
            (*operations)++;
        }
    }
}

// -------------------------------------------
// Prime factorization (sieve method)
bool sieve[MAX_LIMIT + 1];

void generate_sieve()
{
    for (int i = 0; i <= MAX_LIMIT; i++)
        sieve[i] = true;
    sieve[0] = sieve[1] = false;
    for (int i = 2; i * i <= MAX_LIMIT; i++)
    {
        if (sieve[i])
        {
            for (int j = i * i; j <= MAX_LIMIT; j += i)
            {
                sieve[j] = false;
            }
        }
    }
}

void prime_factors_sieve(long long n, int *operations, long long factors[], int *size)
{
    *size = 0;
    for (long long i = 2; i <= n && i <= MAX_LIMIT; i++)
    {
        if (sieve[i])
        {
            while (n % i == 0)
            {
                factors[(*size)++] = i;
                n /= i;
                (*operations)++;
            }
        }
    }
    if (n > 1)
    { // เหลือ prime ใหญ่กว่าขอบเขต sieve
        factors[(*size)++] = n;
        (*operations)++;
    }
}

// -------------------------------------------
// GCD methods

// Method 1: Naive prime factorization
long long find_gcd1(long long m, long long n, int *operations)
{
    long long m_factors[64], n_factors[64];
    int m_size, n_size;
    int ops_m = 0, ops_n = 0;

    prime_factors_naive(m, &ops_m, m_factors, &m_size);
    prime_factors_naive(n, &ops_n, n_factors, &n_size);

    *operations = ops_m + ops_n;

    long long gcd = 1;
    for (int i = 0; i < m_size; i++)
    {
        for (int j = 0; j < n_size; j++)
        {
            if (m_factors[i] == n_factors[j])
            {
                gcd *= m_factors[i];
                n_factors[j] = -1; // mark used
                break;
            }
        }
    }
    return gcd;
}

// Method 2: Sieve prime factorization
long long find_gcd2(long long m, long long n, int *operations)
{
    long long m_factors[64], n_factors[64];
    int m_size, n_size;
    int ops_m = 0, ops_n = 0;

    prime_factors_sieve(m, &ops_m, m_factors, &m_size);
    prime_factors_sieve(n, &ops_n, n_factors, &n_size);

    *operations = ops_m + ops_n;

    long long gcd = 1;
    for (int i = 0; i < m_size; i++)
    {
        for (int j = 0; j < n_size; j++)
        {
            if (m_factors[i] == n_factors[j])
            {
                gcd *= m_factors[i];
                n_factors[j] = -1; // mark used
                break;
            }
        }
    }
    return gcd;
}

// Method 3: Euclidean algorithm
long long find_gcd3(long long m, long long n, int *operations)
{
    *operations = 0;
    while (n != 0)
    {
        (*operations)++;
        long long temp = n;
        n = m % n;
        m = temp;
    }
    return m;
}

// -------------------------------------------
// Main program
int main()
{
    long long m, n;
    printf("Enter two positive integers: ");
    scanf("%lld %lld", &m, &n);

    generate_sieve();

    int ops1, ops2, ops3;
    long long gcd1 = find_gcd1(m, n, &ops1);
    long long gcd2 = find_gcd2(m, n, &ops2);
    long long gcd3 = find_gcd3(m, n, &ops3);

    printf("\nGCD by Naive Prime Factorization = %lld (operations: %d)\n", gcd1, ops1);
    printf("GCD by Sieve Prime Factorization = %lld (operations: %d)\n", gcd2, ops2);
    printf("GCD by Euclidean Algorithm = %lld (operations: %d)\n", gcd3, ops3);

    return 0;
}
