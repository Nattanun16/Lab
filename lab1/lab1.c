#include <stdio.h> // for printf
#include <math.h>

#define MAX_FACTORS 1000 // กำหนดขนาดสูงสุดของอาร์เรย์ที่เก็บตัวประกอบเฉพาะ และป้องกัน overflow

// หาตัวประกอบเฉพาะแบบ naive (trial division)
void prime_factors_naive(unsigned long long n, unsigned long long *count, unsigned long long *factors, unsigned long long *size) // n: จำนวนที่ต้องการหาตัวประกอบเฉพาะ, count: ตัวนับจำนวนการดำเนินการ, factors: อาร์เรย์เก็บตัวประกอบเฉพาะ, size: ขนาดของอาร์เรย์ factors
{
    *size = 0; // เริ่มต้นขนาดเป็น 0
    unsigned long long divisor = 2; // ตัวหารเริ่มต้นที่ 2
    while (n > 1) // ทำจนกว่า n จะลดลงเหลือ 1 หรือถูกแยกหมด
    {
        (*count)++; // เพิ่มตัวนับการดำเนินการ
        if (n % divisor == 0) // ถ้า n หารด้วยตัวหารลงตัว
        {
            factors[(*size)++] = divisor; // เก็บตัวหารลงในอาร์เรย์ factors และเพิ่มขนาด
            n /= divisor; // หาร n ด้วยตัวหาร
        }
        else
        {
            divisor++; // เพิ่มตัวหารขึ้นทีละ 1
        }
    }
}

// ห.ร.ม. แบบ naive
unsigned long long find_gcd1(unsigned long long m, unsigned long long n, unsigned long long *operations) // m: จำนวนแรก, n: จำนวนที่สอง, operations: ตัวนับการดำเนินการ
{
    unsigned long long m_factors[MAX_FACTORS], n_factors[MAX_FACTORS]; // อาร์เรย์เก็บตัวประกอบเฉพาะของ m และ n
    unsigned long long m_size, n_size; // ขนาดของอาร์เรย์ factors

    prime_factors_naive(m, operations, m_factors, &m_size); // หาตัวประกอบเฉพาะของ m
    prime_factors_naive(n, operations, n_factors, &n_size); // หาตัวประกอบเฉพาะของ n

    unsigned long long gcd = 1; // เริ่มต้นห.ร.ม. เป็น 1
    for (unsigned long long i = 0; i < m_size; i++) // วนลูปผ่านตัวประกอบเฉพาะของ m
    {
        for (unsigned long long j = 0; j < n_size; j++) // วนลูปผ่านตัวประกอบเฉพาะของ n เทียบกันกับ m
        {
            if (m_factors[i] == n_factors[j] && n_factors[j] != 0) // ถ้าตัวประกอบเฉพาะตรงกันและยังไม่ถูกใช้
            {
                gcd *= m_factors[i]; // คูณห.ร.ม. ด้วยตัวประกอบเฉพาะนั้น
                n_factors[j] = 0; // ทำเครื่องหมายที่ตัวประกอบเฉพาะของ n ว่าใช้แล้ว
                break; // ออกจากลูปภายใน
            }
        }
        (*operations)++; // เพิ่มตัวนับการดำเนินการ
    }
    return gcd; // คืนค่าห.ร.ม.
}

// หาตัวประกอบเฉพาะโดยใช้ trial division (เวอร์ชันปรับปรุง)
void prime_factors_trial(unsigned long long n, unsigned long long *count, unsigned long long *factors, unsigned long long *size) // n: จำนวนที่ต้องการหาตัวประกอบเฉพาะ, count: ตัวนับจำนวนการดำเนินการ, factors: อาร์เรย์เก็บตัวประกอบเฉพาะ, size: ขนาดของอาร์เรย์ factors
{
    *size = 0; // เริ่มต้นขนาดเป็น 0

    // หารด้วย 2 จนไม่ลงตัว
    while (n % 2 == 0) // ถ้า n หารด้วย 2 ลงตัว (แยก 2 ออกก่อน)
    {
        factors[(*size)++] = 2; // เก็บตัวประกอบเฉพาะ 2
        n /= 2; // หาร n ด้วย 2
        (*count)++; // เพิ่มตัวนับการดำเนินการ
    }

    // หารด้วยจำนวนคี่ตั้งแต่ 3 จนถึง sqrt(n)
    for (unsigned long long i = 3; i * i <= n; i += 2) // เริ่มที่ 3 และเพิ่มทีละ 2 (เฉพาะจำนวนคี่)หยุดเมื่อ i^2 > n
    {
        (*count)++; // เพิ่มตัวนับการดำเนินการ
        while (n % i == 0) // ถ้า n หารด้วย i ลงตัว
        {
            factors[(*size)++] = i; // เก็บตัวประกอบเฉพาะ i
            n /= i; // หาร n ด้วย i
        }
    }

    // ถ้าเหลือเศษ > 1 แปลว่าเป็นจำนวนเฉพาะตัวสุดท้าย
    if (n > 1)
    {
        factors[(*size)++] = n; // เก็บตัวประกอบเฉพาะสุดท้าย
        (*count)++; // เพิ่มตัวนับการดำเนินการ
    }
}

// ห.ร.ม. โดยใช้ trial division
unsigned long long find_gcd2(unsigned long long m, unsigned long long n, unsigned long long *operations) // m: จำนวนแรก, n: จำนวนที่สอง, operations: ตัวนับการดำเนินการ
{
    unsigned long long m_factors[MAX_FACTORS], n_factors[MAX_FACTORS]; // อาร์เรย์เก็บตัวประกอบเฉพาะของ m และ n
    unsigned long long m_size, n_size; // ขนาดของอาร์เรย์ factors

    prime_factors_trial(m, operations, m_factors, &m_size); // หาตัวประกอบเฉพาะของ m
    prime_factors_trial(n, operations, n_factors, &n_size); // หาตัวประกอบเฉพาะของ n

    unsigned long long gcd = 1; // เริ่มต้นห.ร.ม. เป็น 1
    for (unsigned long long i = 0; i < m_size; i++) // วนลูปผ่านตัวประกอบเฉพาะของ m
    {
        for (unsigned long long j = 0; j < n_size; j++) // วนลูปผ่านตัวประกอบเฉพาะของ n เทียบกันกับ m
        {
            if (m_factors[i] == n_factors[j] && n_factors[j] != 0) // ถ้าตัวประกอบเฉพาะตรงกันและยังไม่ถูกใช้
            {
                gcd *= m_factors[i]; // คูณห.ร.ม. ด้วยตัวประกอบเฉพาะนั้น
                n_factors[j] = 0; // ทำเครื่องหมายตัวประกอบเฉพาะของ n ว่าใช้แล้ว
                break; // ออกจากลูปภายใน
            }
        }
        (*operations)++; // เพิ่มตัวนับการดำเนินการ
    }
    return gcd; // คืนค่าห.ร.ม.
}

// Euclidean algorithm
unsigned long long find_gcd3(unsigned long long m, unsigned long long n, unsigned long long *operations)
{
    while (n != 0) // ทำจนกว่า n หรือเศษจะเป็น 0
    {
        (*operations)++; // เพิ่มตัวนับการดำเนินการ
        unsigned long long temp = n; // เก็บค่า n ชั่วคราว
        n = m % n; // คำนวณเศษของ m หาร n
        m = temp; // ย้ายค่า n เดิมไปยัง m (สลับค่าแบบ Euclidean)
    }
    return m; // คืนค่าห.ร.ม.
}

int main(void) // โปรแกรมหลัก
{
    unsigned long long x = 953525754641ULL, y = 658518571823ULL; // กำหนดค่าตัวเลขสองจำนวนที่ต้องการหาห.ร.ม.

    unsigned long long ops1 = 0, ops2 = 0, ops3 = 0; // ตัวนับการดำเนินการสำหรับแต่ละวิธี

    unsigned long long gcd1 = find_gcd1(x, y, &ops1); // หาห.ร.ม. ด้วยวิธีที่ 1
    unsigned long long gcd2 = find_gcd2(x, y, &ops2); // หาห.ร.ม. ด้วยวิธีที่ 2
    unsigned long long gcd3 = find_gcd3(x, y, &ops3); // หาห.ร.ม. ด้วยวิธีที่ 3

    printf("GCD1 = %llu Operations = %llu\n", gcd1, ops1); // แสดงผลลัพธ์ห.ร.ม. และจำนวนการดำเนินการของแต่ละวิธี
    printf("GCD2 = %llu Operations = %llu\n", gcd2, ops2);
    printf("GCD3 = %llu Operations = %llu\n", gcd3, ops3);

    return 0; // จบโปรแกรม
}
