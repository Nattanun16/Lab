# coin_change_ways.py
import sys, io # ตั้งค่า stdout เป็น UTF-8 เพื่อรองรับไทยบน Windows

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def coin_change_ways(amount, coins): 
    """หาจำนวนวิธีทอนเงิน (Backtracking)"""
    result = [] #เก็บ ทุกวิธีการทอนเงิน ที่หาได้

    def backtrack(remaining, start, path): # เป็นฟังก์ชัน recursive สำหรับค้นหาทุกวิธีทอนเงิน โดย remaining = จำนวนเงินที่เหลือ, start = ตำแหน่งเริ่มต้นใน coins, path = วิธีการทอนเงินปัจจุบัน
        if remaining == 0: #เงินครบแล้ว
            result.append(list(path)) #บันทึกวิธีนี้ลง result
            return
        if remaining < 0: #เงินเกิน
            return #หยุดการค้นหา
        for i in range(start, len(coins)): #เลือกเหรียญ coins[i] เพิ่มเข้า path
            path.append(coins[i]) #เพิ่มเหรียญเข้า path
            backtrack(remaining - coins[i], i, path) #เรียก backtrack ซ้ำ โดยลดจำนวนเงินที่เหลือ และยังคงเริ่มที่เหรียญเดิม (i) เพื่อให้สามารถใช้เหรียญซ้ำได้
            path.pop() #นำเหรียญออกจาก path เพื่อกลับไปลองเหรียญถัดไป (เอาเหรียญออกหลังกลับจาก recursion (backtracking))

    backtrack(amount, 0, []) #เริ่มต้นการค้นหาด้วยจำนวนเงินเต็ม, เริ่มที่เหรียญตัวแรก, และ path ว่าง
    return result #คืนค่าทุกวิธีการทอนเงินที่หาได้


def run_from_file(filename):
    with open(filename, "r") as f: #อ่านข้อมูลจากไฟล์
        lines = [line.strip() for line in f if line.strip()] #ลบบรรทัดว่าง

    for i in range(0, len(lines), 2): #อ่านข้อมูลทีละ 2 บรรทัด (บรรทัดแรกเป็นจำนวนเงิน, บรรทัดที่สองเป็นรายการเหรียญ)
        amount = int(lines[i]) #จำนวนเงิน
        coins = list(map(int, lines[i + 1].split())) #coin คือ list รายการเหรียญ

        print("=" * 40) # แสดงเส้นคั่น
        print(f"Amount = {amount}, Coins = {coins}") # แสดงจำนวนเงินและรายการเหรียญ

        ways = coin_change_ways(amount, coins) #หา วิธีทอนเงิน
        print(f"จำนวนวิธีทอน = {len(ways)}") # แสดงจำนวนวิธีทอนเงินที่หาได้
        for w in ways: # แสดงแต่ละวิธีทอนเงิน
            print(w) # แสดงวิธีทอนเงิน


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\5.1.txt")
