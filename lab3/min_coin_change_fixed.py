# min_coin_change_fixed.py

def min_coin_change(amount, coins): #หาจำนวนเหรียญ น้อยที่สุด ที่ใช้ทอนเงิน amount
    """หาจำนวนเหรียญน้อยที่สุด (Bottom-up DP) + ตาราง lookup 2D สำหรับดูว่าเหรียญตัวไหนใช้ในแต่ละขั้นตอน"""
    dp = [float("inf")] * (amount + 1) # สร้างตาราง dp ขนาด amount+1 และกำหนดค่าเริ่มต้นเป็น infinity
    choice = [-1] * (amount + 1)# choice[i] = เหรียญที่เลือกครั้งสุดท้ายสำหรับ i
    dp[0] = 0 # กรณีที่ amount = 0 ต้องใช้เหรียญ 0 เหรียญ

    for i in range(1, amount + 1): #ลูปทุกจำนวนเงิน i ตั้งแต่ 1 ถึง amount
        for c in coins: #ลูปผ่านเหรียญแต่ละตัว
            if i - c >= 0: #ถ้าเหรียญ c สามารถใช้ได้ (ไม่เกินจำนวนเงิน i)
                dp[i] = min(dp[i], dp[i - c] + 1) #อัพเดต dp[i] เป็นค่าที่น้อยที่สุดระหว่างค่าเดิมกับ dp[i-c]+1
                choice[i] = c  # จำว่าเลือกเหรียญ c มาทำ i
    
    used_coins = [] #เก็บเหรียญที่ใช้
    cur = amount #เริ่มจากจำนวนเงินที่ต้องการทอน
    while cur > 0 and choice[cur] != -1: #ถ้ายังมีเงินเหลือและมีเหรียญที่เลือกได้
        used_coins.append(choice[cur]) #เพิ่มเหรียญที่เลือกในรอบนี้ลงในรายการ
        cur -= choice[cur] #ลดจำนวนเงินลงตามเหรียญที่เลือก

    # สร้าง lookup table 2D
    lookup = [[float("inf")] * (amount + 1) for _ in range(len(coins) + 1)]

    # base case
    for i in range(len(coins) + 1):
        lookup[i][0] = 0  # ต้องการเงิน 0 ใช้เหรียญ 0 เหรียญ

    for i in range(1, len(coins) + 1): #ลูปผ่านเหรียญแต่ละตัว
        for j in range(1, amount + 1): #ลูปผ่านจำนวนเงินตั้งแต่ 1 ถึง amount
            if coins[i - 1] <= j: #ถ้าเหรียญตัวนี้สามารถใช้ได้
                lookup[i][j] = min(lookup[i - 1][j], 1 + lookup[i][j - coins[i - 1]]) #เลือกใช้เหรียญตัวนี้หรือไม่ใช้
            else: #ถ้าเหรียญตัวนี้ใช้ไม่ได้
                lookup[i][j] = lookup[i - 1][j] #ไม่ใช้เหรียญตัวนี้

    return dp[amount], used_coins, lookup #คืนค่าจำนวนเหรียญที่ใช้, รายการเหรียญที่ใช้, และตาราง lookup


def run_from_file(filename): #อ่านข้อมูลจากไฟล์และแสดงผลลัพธ์
    import os, sys
    # ตั้งค่า stdout เป็น UTF-8 เพื่อรองรับไทยบน Windows
    if os.name == "nt": # ถ้าเป็น Windows
        import io # รองรับ UTF-8 บน Windows
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8") #รองรับ UTF-8 บน Windows

    with open(filename, "r", encoding="utf-8") as f: #เปิดไฟล์ด้วย encoding UTF-8
        lines = [line.strip() for line in f if line.strip()] #อ่านบรรทัดทั้งหมดในไฟล์และลบช่องว่าง

    for i in range(0, len(lines), 2): #ลูปผ่านบรรทัดทีละ 2 บรรทัด
        amount = int(lines[i]) #จำนวนเงินที่ต้องการทอน
        coins = list(map(int, lines[i + 1].split())) #รายการเหรียญที่มีอยู่

        print("=" * 40) #แสดงเส้นคั่น
        print(f"Amount = {amount}, Coins = {coins}") #แสดงจำนวนเงินและรายการเหรียญ

        min_coins, used_coins, table = min_coin_change(amount, coins) #เรียกใช้ฟังก์ชันหาจำนวนเหรียญน้อยที่สุด

        if min_coins == float("inf"): #ถ้าไม่สามารถทอนเงินได้
            print("ไม่สามารถทอนเงินจำนวนนี้ได้ด้วยเหรียญที่กำหนด") #แสดงข้อความว่าไม่สามารถทอนได้
        else: #ถ้าสามารถทอนได้
            print(f"จำนวนเหรียญน้อยที่สุด = {min_coins}") #แสดงจำนวนเหรียญที่ใช้
            print(f"เหรียญที่ใช้ = {used_coins}") #แสดงรายการเหรียญที่ใช้

        print("Lookup Table (2D):") #แสดงตาราง lookup
        header = ["C\\A"] + list(range(amount + 1)) #หัวตาราง
        print("\t".join(map(str, header))) #แสดงหัวตาราง
        for idx, row in enumerate(table): #แสดงแต่ละแถวในตาราง
            row_display = [str(idx)] + [str(cell) for cell in row] #แปลงค่าทุกค่าในแถวเป็นสตริง
            print("\t".join(row_display)) #แสดงแถวในตาราง


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\3.1.txt")