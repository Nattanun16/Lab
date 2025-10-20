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
    try:
        line1 = input()  # อ่านบรรทัดแรก (อาจเป็น charset หรือ header ที่ไม่ใช้)
    except EOFError:
        return  # ถ้าไม่มีอินพุต ให้หยุดการทำงาน
    line2 = input().strip()  # อ่านบรรทัดที่สอง (ขนาด m และ n) แล้วตัดช่องว่างหัวท้าย
    line3 = input().strip()  # อ่านบรรทัดที่สาม (pattern) แล้วตัดช่องว่างหัวท้าย
    line4 = input().strip()  # อ่านบรรทัดที่สี่ (text) แล้วตัดช่องว่างหัวท้าย

    parts = line2.split()  # แยกขนาด m และ n
    m = int(parts[0])  # แปลงเป็นจำนวนเต็ม
    n = int(parts[1])  # แปลงเป็นจำนวนเต็ม

    pattern = parse_tokens(line3, expected_len=m)  # แปลง pattern เป็นลิสต์โทเค็นหรือตัวอักษร
    text = parse_tokens(line4, expected_len=n)  # แปลง text เป็นลิสต์โทเค็นหรือตัวอักษร

    pi = compute_prefix(pattern)  # คำนวณตาราง prefix function ของ pattern ต้นฉบับ

    lr_positions = kmp_search(pattern, text)  # ค้นหา pattern ใน text จากซ้ายไปขวา (LR)

    # ค้นหา pattern แบบย้อนกลับ (RL)
    pattern_rev = pattern[::-1]  # พลิกลำดับ pattern
    a_positions = kmp_search(pattern_rev, text)  # ค้นใน text
    rl_positions = [a + m - 1 for a in a_positions]  # แปลงเป็นตำแหน่งเริ่มต้น RL

    # รวมผลการค้นหาและจัดเรียงตามตำแหน่ง ถ้าตำแหน่งเท่ากันให้ LR มาก่อน RL
    matches = []  # ลิสต์เก็บผลลัพธ์
    for p in lr_positions:
        matches.append((p, "LR"))  # เพิ่มตำแหน่งและทิศทาง LR
    for p in rl_positions:
        matches.append((p, "RL"))  # เพิ่มตำแหน่งและทิศทาง RL
    matches.sort(
        key=lambda x: (x[0], 0 if x[1] == "LR" else 1)
    )  # จัดเรียงตามตำแหน่ง และถ้าตำแหน่งเท่ากันให้ LR มาก่อน RL

    # output
    print(" ".join(str(x) for x in pi))  # พิมพ์ตาราง prefix function
    print(len(matches))  # พิมพ์จำนวนการแมตช์ที่พบ
    for pos, d in matches:
        print(f"{pos} {d}")  # พิมพ์ตำแหน่งและทิศทางของแต่ละการแมตช์


if __name__ == "__main__":
    main()
