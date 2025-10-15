def divide_and_conquer_sequence(m, n):
    """สร้างลำดับแบบ Divide and Conquer จาก m ถึง n"""
    if n < m:
        return []

    if m == n:
        return [m]

    # เรียกแบบเดิมแต่ยืดขอบช่วงโดยเลื่อนเลข
    length = n - m
    prev = divide_and_conquer_sequence(0, length)

    # ปรับค่ากลับให้เริ่มที่ m
    return [x + m for x in prev]


def base_divide_and_conquer(n):
    """ลำดับตั้งแต่ 0 ถึง n (ต้นแบบที่ใช้ภายใน)"""
    if n == 0:
        return [0]
    prev = base_divide_and_conquer(n // 2)
    evens = [x * 2 for x in prev if x * 2 <= n]
    odds = [x * 2 + 1 for x in prev if x * 2 + 1 <= n]
    return evens + odds


# ใช้ base_divide_and_conquer ภายในเพื่อให้ผลลัพธ์ตรงตามโจทย์
def divide_and_conquer_sequence(m, n):
    if n < m:
        return []
    seq = base_divide_and_conquer(n - m)
    return [x + m for x in seq]


# 🔹 ตัวอย่างทดสอบ
m = int(input("Enter start m: "))
n = int(input("Enter end n: "))

seq = divide_and_conquer_sequence(m, n)
print("Output:", *seq)
#Base Case n==0 ใช้เวลา O(1)
#Recursive Case n>0 เรียกตัวเอง 1 ครั้งกับ n//2 และทำงาน O(n)
#เวลารวม T(n) = T(n/2) + O(n) ดังนั้น T(n) = O(n)
#Space Complexity = O(n)
#worst case เกิดเมื่อ n-m ใหญ่ที่สุด 
#Complexity = O(n-m+1)
#Space complexity = O(n-m+1)