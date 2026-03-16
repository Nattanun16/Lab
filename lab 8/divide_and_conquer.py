def divide_and_conquer_sequence(m, n):
    """สร้างลำดับแบบ Divide and Conquer จาก m ถึง n"""
    if n < m: # Base case เมื่อช่วงไม่ถูกต้อง
        return [] # คืนลำดับว่าง

    if m == n: # Base case เมื่อช่วงมีค่าเดียว
        return [m] # คืนลำดับที่มีค่าเดียวคือ m

    # เรียกแบบเดิมแต่ยืดขอบช่วงโดยเลื่อนเลข
    length = n - m # ความยาวของช่วง
    prev = divide_and_conquer_sequence(0, length) # เรียกฟังก์ชันแบบเดิมกับช่วง 0 ถึง length

    # ปรับค่ากลับให้เริ่มที่ m
    return [x + m for x in prev] # เลื่อนค่าทั้งหมดเป็นช่วง m..n


def base_divide_and_conquer(n):
    """ลำดับตั้งแต่ 0 ถึง n (ต้นแบบที่ใช้ภายใน)"""
    if n == 0: 
        return [0] # Base case
    prev = base_divide_and_conquer(n // 2) # เรียกตัวเองกับ n//2
    evens = [x * 2 for x in prev if x * 2 <= n] # สร้างเลขคู่
    odds = [x * 2 + 1 for x in prev if x * 2 + 1 <= n] # สร้างเลขคี่
    return evens + odds # รวมเลขคู่และเลขคี่


# ใช้ base_divide_and_conquer ภายในเพื่อให้ผลลัพธ์ตรงตามโจทย์
def divide_and_conquer_sequence(m, n): # สร้างลำดับจาก m..n แบบ Divide and Conquer
    if n < m: # Base case เมื่อช่วงไม่ถูกต้อง
        return [] # คืนลำดับว่าง
    seq = base_divide_and_conquer(n - m) # สร้างลำดับจาก 0..(n-m)
    return [x + m for x in seq] # เลื่อนค่าทั้งหมดเป็นช่วง m..n


# 🔹 ตัวอย่างทดสอบ
m = int(input("Enter start m: "))
n = int(input("Enter end n: "))

seq = divide_and_conquer_sequence(m, n) # สร้างลำดับจาก m..n
print("Output:", *seq) # แสดงผลลัพธ์
#Base Case n==0 ใช้เวลา O(1)
#Recursive Case n>0 เรียกตัวเอง 1 ครั้งกับ n//2 และทำงาน O(n)
#เวลารวม T(n) = T(n/2) + O(n) ดังนั้น T(n) = O(n)
#Space Complexity = O(n)