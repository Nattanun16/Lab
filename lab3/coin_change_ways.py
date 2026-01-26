import sys, io

# รองรับ UTF-8 บน Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def coin_change_ways_list(amount, coins):
    """แจกแจงวิธีทอนเงินทุกวิธี (Backtracking/Top-down recursive)"""
    result = [] #เก็บผลลัพธ์วิธีทอนเงินทั้งหมด

    def backtrack(remaining, start, path): #ฟังก์ชันช่วยในการทำ Backtracking
        if remaining == 0: #ถ้าทอนเงินครบตามจำนวนที่ต้องการ
            result.append(list(path)) #เก็บวิธีทอนเงินที่เจอ
            return #ออกจากฟังก์ชัน
        if remaining < 0:  #ถ้าทอนเงินเกินจำนวนที่ต้องการ
            return #ออกจากฟังก์ชัน
        for i in range(start, len(coins)): #ลูปผ่านเหรียญแต่ละตัว เริ่มจากตำแหน่ง start (เพื่อไม่ให้ซ้ำวิธีเดิม) และ len(coins) (เพื่อให้ใช้เหรียญได้ทุกตัว)
            path.append(coins[i]) #เพิ่มเหรียญตัวนี้ในวิธีทอนเงินปัจจุบัน
            backtrack(remaining - coins[i], i, path) #recursive, ใช้เหรียญตัวเดิมซ้ำได้
            path.pop() #เอาเหรียญตัวนี้ออกจากวิธีทอนเงินปัจจุบัน (backtrack) เพื่อ explore วิธีถัดไป

    backtrack(amount, 0, []) #เริ่มต้น backtracking ด้วยจำนวนเงินที่ต้องการ, ตำแหน่งเริ่มต้น 0, และวิธีทอนเงินว่างเปล่า
    return result #คืนค่ารายการวิธีทอนเงินทั้งหมด


def coin_change_ways_dp(amount, coins):
    """หาจำนวนวิธีทอนเงินด้วย DP (Bottom-up)"""
    dp = [0] * (amount + 1) # สร้างตาราง dp ขนาด amount+1 และกำหนดค่าเริ่มต้นเป็น 0
    dp[0] = 1 # กรณีที่ amount = 0 มีวิธีทอนเงิน 1 วิธี คือ ไม่ใช้เหรียญเลย

    for c in coins: #ลูปผ่านเหรียญแต่ละตัว
        for i in range(c, amount + 1): #ลูปผ่านจำนวนเงินตั้งแต่ค่าเหรียญ c ถึง amount
            dp[i] += dp[i - c] #อัพเดต dp[i] โดยเพิ่มจำนวนวิธีทอนเงินที่ได้จากการใช้เหรียญ c

    return dp[amount] #คืนค่าจำนวนวิธีทอนเงินที่ต้องการ


def run_from_file(filename): #อ่านข้อมูลจากไฟล์และแสดงผลลัพธ์
    with open(filename, "r", encoding="utf-8") as f: #เปิดไฟล์ด้วย encoding UTF-8
        lines = [line.strip() for line in f if line.strip()] #อ่านบรรทัดทั้งหมดในไฟล์และลบช่องว่าง

    for i in range(0, len(lines), 2): #ลูปผ่านบรรทัดทีละ 2 บรรทัด
        amount = int(lines[i]) #จำนวนเงินที่ต้องการทอน
        coins = list(map(int, lines[i + 1].split())) #รายการเหรียญที่มีอยู่

        print("=" * 40) #แสดงเส้นคั่น
        print(f"Amount = {amount}") #แสดงจำนวนเงินที่ต้องการทอน
        print(f"coins [] = {coins}") #แสดงรายการเหรียญที่มีอยู่

        if amount <= 20:
            # ใช้ Backtracking แจกแจงทุกวิธี
            ways = coin_change_ways_list(amount, coins) #เรียกใช้ฟังก์ชันแจกแจงวิธีทอนเงิน
            print(f"Ways to make change = {len(ways)}") #แสดงจำนวนวิธีทอนเงินที่เจอ
            print(" ".join("{" + ",".join(map(str, w)) + "}" for w in ways)) #แสดงวิธีทอนเงินทั้งหมดในรูปแบบที่กำหนด
        else:
            # ใช้ DP คำนวณจำนวนวิธี
            ways = coin_change_ways_dp(amount, coins) #เรียกใช้ฟังก์ชันหาจำนวนวิธีทอนเงิน
            print(f"Ways to make change = {ways} (too many to list)") #แสดงจำนวนวิธีทอนเงินที่เจอ พร้อมข้อความว่า "too many to list"


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\3.1.txt")
