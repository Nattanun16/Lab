def iterative_sequence(m, n): # สร้างลำดับจาก m..n แบบ iterative
    """
    สร้างลำดับจาก m..n แบบ iterative ให้ผลเหมือนโจทย์
    (โครงสร้าง: ขยายจากลำดับ 0..(n-m) ด้วย evens ก่อน แล้ว odds)
    """
    if n < m: # Base case เมื่อช่วงไม่ถูกต้อง
        return [] # คืนลำดับว่าง
    length = n - m  # ทำงานบนช่วง 0..length แล้วเลื่อน +m ท้ายสุด

    # สร้างลำดับสำหรับช่วง 0..length
    seq = [0] # เริ่มต้นด้วยลำดับที่มีแค่ 0
    while len(seq) < length + 1: # ทำจนกว่าลำดับจะมีขนาด (length+1)
        temp = [] # ชั่วคราวเก็บลำดับใหม่
        # เอาเลขคู่ (x*2) ก่อน
        for x in seq: # วนในลำดับเดิม
            v = x * 2 # สร้างเลขคู่
            if v <= length: # ถ้าไม่เกิน length
                temp.append(v) # เก็บเลขคู่
        # แล้วเอาเลขคี่ (x*2+1)
        for x in seq: # วนในลำดับเดิม
            v = x * 2 + 1 # สร้างเลขคี่
            if v <= length: # ถ้าไม่เกิน length
                temp.append(v) # เก็บเลขคี่
        seq = temp # อัพเดตลำดับเป็นลำดับใหม่

    # เลื่อนค่าทั้งหมดเป็นช่วง m..n
    return [x + m for x in seq] 


# ตัวอย่างทดสอบ
m = int(input("Enter start m: "))
n = int(input("Enter end n: "))
print("Output:", *iterative_sequence(m, n)) # แสดงผลลัพธ์

#Base Case n<m หรือเมื่อ len(seq) == (n-m)+1 ใช้เวลา O(1)
#Recurrence relation คือ T(n) = T(n/2) + O(n) ดังนั้น T(n) = O(n)
#Space Complexity = O(n)
#worst case เกิดเมื่อ n มีค่าใหญ่ที่สุดใน input