# min_coin_change_fixed.py

def min_coin_change(amount, coins): #หาจำนวนเหรียญ น้อยที่สุด ที่ใช้ทอนเงิน amount
    """หาจำนวนเหรียญน้อยที่สุด (Bottom-up DP) + ตาราง lookup 2D สำหรับดูว่าเหรียญตัวไหนใช้ในแต่ละขั้นตอน"""
    dp = [float("inf")] * (amount + 1) # สร้างตาราง dp ขนาด amount+1 และกำหนดค่าเริ่มต้นเป็น infinity
    dp[0] = 0 # กรณีที่ amount = 0 ต้องใช้เหรียญ 0 เหรียญ

    for i in range(1, amount + 1): #ลูปทุกจำนวนเงิน i ตั้งแต่ 1 ถึง amount
        for c in coins:
            if i - c >= 0: #ถ้าเหรียญ c สามารถใช้ได้ (ไม่เกินจำนวนเงิน i)
                dp[i] = min(dp[i], dp[i - c] + 1) #อัพเดต dp[i] เป็นค่าที่น้อยที่สุดระหว่างค่าเดิมกับ dp[i-c]+1

    # สร้าง lookup table 2D
    lookup = [[0] * (amount + 1) for _ in range(len(coins) + 1)] #ตารางขนาด (จำนวนเหรียญ+1) x (amount+1) โดย (len(coins)+1) เป็นแถว, (amount+1) เป็นคอลัมน์
    for i in range(1, len(coins) + 1): #ลูปผ่านเหรียญแต่ละตัว
        for j in range(1, amount + 1): #ลูปผ่านจำนวนเงินตั้งแต่ 1 ถึง amount
            if coins[i - 1] <= j: #ถ้าเหรียญตัวปัจจุบันสามารถใช้ได้ (ไม่เกินจำนวนเงิน j)
                if lookup[i - 1][j] == 0 and j != coins[i - 1]: #ถ้าแถวก่อนหน้ายังไม่มีค่าและ j != coins[i-1]
                    lookup[i][j] = 1 + lookup[i][j - coins[i - 1]] #ให้ใช้เหรียญนี้ + ค่า lookup ก่อนหน้านี้
                else: #ถ้าไม่ใช่
                    lookup[i][j] = min( # เลือกค่าที่ น้อยที่สุด ระหว่าง
                        lookup[i - 1][j] if lookup[i - 1][j] > 0 else float("inf"), # ค่าในแถวก่อนหน้า (ถ้ามีค่า)
                        1 + lookup[i][j - coins[i - 1]], # ค่าใช้เหรียญนี้ + ค่า lookup ก่อนหน้านี้
                    )
            else: #ถ้าเหรียญตัวปัจจุบันไม่สามารถใช้ได้ (มากกว่าจำนวนเงิน j)
                lookup[i][j] = lookup[i - 1][j] #ก็จะใช้ค่าเดิมจากแถวก่อนหน้า

    return dp[amount], lookup #คืนค่าจำนวนเหรียญน้อยที่สุดและตาราง lookup


def run_from_file(filename): #อ่านข้อมูลจากไฟล์และแสดงผลลัพธ์
    import os, sys
    # ตั้งค่า stdout เป็น UTF-8 เพื่อรองรับไทยบน Windows
    if os.name == "nt": 
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    with open(filename, "r", encoding="utf-8") as f: #เปิดไฟล์ด้วย encoding UTF-8
        lines = [line.strip() for line in f if line.strip()] #อ่านบรรทัดทั้งหมดในไฟล์และลบช่องว่าง

    for i in range(0, len(lines), 2): #ลูปผ่านบรรทัดทีละ 2 บรรทัด
        amount = int(lines[i]) #จำนวนเงินที่ต้องการทอน
        coins = list(map(int, lines[i + 1].split())) #รายการเหรียญที่มีอยู่

        print("=" * 40) #แสดงเส้นคั่น
        print(f"Amount = {amount}, Coins = {coins}") #แสดงจำนวนเงินและรายการเหรียญ

        min_coins, table = min_coin_change(amount, coins) #เรียกฟังก์ชันหาจำนวนเหรียญน้อยที่สุดและตาราง lookup
        print(f"จำนวนเหรียญน้อยที่สุด = {min_coins}") #แสดงผลลัพธ์จำนวนเหรียญน้อยที่สุด
        print("Lookup Table:") #แสดงตาราง lookup
        # แสดง header ของคอลัมน์
        header = ["C\\A"] + list(range(amount + 1)) # C\A หมายถึง Coins vs Amount
        print("\t".join(map(str, header))) # แสดง header ของตาราง
        for idx, row in enumerate(table): #ลูปผ่านแต่ละแถวในตาราง lookup
            row_display = [str(idx)] + [str(cell) for cell in row] #เพิ่มหมายเลขแถวด้านหน้า
            print("\t".join(row_display)) #แสดงแต่ละแถวของตาราง lookup


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\5.1.txt")