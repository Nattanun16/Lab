import sys # นำเข้าโมดูล sys สำหรับการจัดการอินพุตและเอาต์พุต


def parse_tokens(
    line, expected_len=None
):  # แปลงสตริงบรรทัดให้เป็นลิสต์ของโทเค็น โดยถ้า expected_len กำหนดมา และลิสต์มีโทเค็นเดียวซึ่งความยาวตรงกับ expected_len ให้แยกโทเค็นนั้นเป็นลิสต์ของตัวอักษร
    parts = line.strip().split()  # ตัดช่องว่างหัวท้ายแล้วแยกคำตามเว้นวรรค
    if expected_len is not None and len(parts) == 1 and len(parts[0]) == expected_len:
        return list(
            parts[0]
        )  # ถ้า expected_len ไม่ใช่ None และลิสต์มีโทเค็นเดียวซึ่งความยาวตรงกับ expected_len ให้แยกโทเค็นนั้นเป็นลิสต์ของตัวอักษร
    return parts  # ถ้าไม่ใช่ ให้คืนลิสต์ของโทเค็นตามที่แยกได้


def compute_prefix(
    pat,
):  # คำนวณตาราง prefix function (pi) สำหรับ pattern ใน KMP algorithm
    m = len(pat)  # ความยาวของ pattern
    pi = [0] * m  # สร้างลิสต์ค่า prefix โดยให้เริ่มต้นเป็น 0 ทั้งหมด
    k = 0  # ตัวชี้ความยาว match ที่ยาวที่สุดจนถึงปัจจุบัน
    for q in range(1, m):  # วนตั้งแต่ตำแหน่งที่สองจนถึงสุดของ pattern
        while k > 0 and pat[k] != pat[q]:
            k = pi[k - 1]  # ถ้าไม่ตรงกัน ให้ย้อนกลับไปตามค่า pi
        if pat[k] == pat[q]:
            k += 1  # ถ้าตรงกัน ให้เพิ่มความยาว match
        pi[q] = k  # กำหนดค่า pi ที่ตำแหน่ง q เป็นความยาว match ปัจจุบัน
    return pi  # คืนค่าตาราง prefix function


def kmp_search(pat, text):  # ค้นหา pattern ใน text โดยใช้ KMP algorithm
    m = len(pat)  # ความยาวของ pattern
    n = len(text)  # ความยาวของ text
    pi = compute_prefix(pat)  # คำนวณตาราง prefix function ของ pattern
    q = 0  # จำนวนตัวที่แมตช์ในปัจจุบัน
    results = []  # ลิสต์เก็บตำแหน่งที่พบ pattern
    for i in range(n):  # วนผ่านแต่ละตัวอักษรใน text
        while q > 0 and pat[q] != text[i]:
            q = pi[q - 1]  # ถ้าไม่ตรงกัน ให้ย้อนกลับไปตามค่า pi
        if pat[q] == text[i]:
            q += 1  # ถ้าตรงกัน ให้เพิ่มจำนวนตัวที่แมตช์
        if q == m:  # ถ้าแมตช์ครบทั้ง pattern
            results.append(i - m + 2)  # บันทึกตำแหน่งเริ่มต้น (1-based)
            q = pi[q - 1]  # เตรียม q สำหรับการค้นหาต่อไป
    return results  # คืนค่าลิสต์ตำแหน่งที่พบ pattern


def main():
    file_path = "C:\\Users\\user\\Downloads\\8.7.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines() # อ่านบรรทัดทั้งหมดจากไฟล์
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {file_path}") # แจ้งข้อผิดพลาดถ้าไฟล์ไม่พบ
        return # ออกจากโปรแกรม
    if len(lines) < 4:
        print("ไฟล์ต้องมี 4 บรรทัด: charset, m n, pattern, text")
        return # ออกจากโปรแกรมถ้าบรรทัดไม่ครบ

    line2 = lines[1].strip()  # m n line
    line3 = lines[2].strip()  # pattern
    line4 = lines[3].strip()  # text

    m, n = map(int, line2.split()) # แยกค่า m และ n จากบรรทัดที่สอง
    pattern = parse_tokens(line3, expected_len=m) # แปลง pattern เป็นลิสต์โทเค็นหรือตัวอักษร
    text = parse_tokens(line4, expected_len=n) # แปลง text เป็นลิสต์โทเค็นหรือตัวอักษร

    # คำนวณ prefix table
    pi = compute_prefix(pattern) # คำนวณตาราง prefix function
    print(" ".join(str(x) for x in pi)) # พิมพ์ตาราง prefix function

    # หา match แบบ LR
    text_extended = text + text  # ขยาย text ให้ wrap-around ได้
    lr_all = kmp_search(pattern, text_extended)  # ค้นหา pattern ใน text ขยาย
    lr_mapped = sorted({((p - 1) % n) + 1 for p in lr_all}) # แปลงตำแหน่งให้เป็นในช่วง 1 ถึง n และลบซ้ำ
    

    # หา match แบบ RL
    pattern_rev = pattern[::-1] # พลิกลำดับ pattern
    rl_all = kmp_search(pattern_rev, text_extended) # ค้นหา pattern พลิกใน text ขยาย
    rl_mapped = sorted({((p + m - 2) % n) + 1 for p in rl_all}) # แปลงตำแหน่งให้เป็นในช่วง 1 ถึง n และลบซ้ำ


    # รวมผลลัพธ์และเรียง
    matches = [(p, "LR") for p in lr_mapped] + [(p, "RL") for p in rl_mapped] # รวมผลลัพธ์
    matches.sort(key=lambda x: (x[0], 0 if x[1] == "LR" else 1)) # จัดเรียงผลลัพธ์ตามตำแหน่ง และถ้าตำแหน่งเท่ากันให้ LR มาก่อน RL

    print(len(matches)) # พิมพ์จำนวน match ที่พบ
    for pos, d in matches: # พิมพ์ตำแหน่งและทิศทางของแต่ละการแมตช์
        print(f"{pos} {d}")

if __name__ == "__main__":
    main()
