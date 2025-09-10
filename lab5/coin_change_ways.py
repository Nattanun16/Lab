import sys, io

# รองรับ UTF-8 บน Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def coin_change_ways_dp(amount, coins):
    """หาจำนวนวิธีทอนเงินด้วย DP (Bottom-up)"""
    dp = [0] * (amount + 1) # สร้างตาราง dp ขนาด amount+1
    dp[0] = 1  # วิธีทอน 0 = 1 (ไม่ใช้เหรียญเลย)

    for c in coins:  # ลูปเหรียญทีละตัว
        for i in range(c, amount + 1): # ลูปจำนวนเงินตั้งแต่ c ถึง amount
            dp[i] += dp[i - c] # อัพเดต dp[i] โดยเพิ่มจำนวนวิธีทอนที่ได้จากการใช้เหรียญ c หรือก็คือ จำนวนวิธีทอนเงิน i = จำนวนวิธีทอนเงิน (i-c) + วิธีอื่นที่มีอยู่แล้ว

    return dp[amount] # คืนค่าจำนวนวิธีทอนเงิน amount


def run_from_file(filename): # อ่านข้อมูลจากไฟล์และแสดงผลลัพธ์
    with open(filename, "r", encoding="utf-8") as f: # เปิดไฟล์ด้วย encoding UTF-8
        lines = [line.strip() for line in f if line.strip()] # อ่านบรรทัดทั้งหมดในไฟล์และลบช่องว่าง

    for i in range(0, len(lines), 2): # ลูปผ่านบรรทัดทีละ 2 บรรทัด
        amount = int(lines[i]) # จำนวนเงินที่ต้องการทอน
        coins = list(map(int, lines[i + 1].split())) # รายการเหรียญที่มีอยู่

        print("=" * 40) # แสดงเส้นคั่น
        print(f"Amount = {amount}, Coins = {coins[:10]}{'...' if len(coins) > 10 else ''}") # แสดงจำนวนเงินและรายการเหรียญ (ถ้ามากกว่า 10 เหรียญจะแสดงแค่ 10 ตัวแรก)
        ways = coin_change_ways_dp(amount, coins) # เรียกใช้ฟังก์ชันหาจำนวนวิธีทอนเงิน
        print(f"จำนวนวิธีทอน = {ways}") # แสดงจำนวนวิธีทอนเงิน


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\5.1.txt")
