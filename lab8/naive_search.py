import sys  # นำเข้าโมดูล sys สำหรับการจัดการอินพุตและเอาต์เอาท์


def parse_tokens(line, expected_len=None):  # แปลงบรรทัดข้อความเป็นลิสต์ของโทเค็น (คำหรืออักขระ)
    parts = line.strip().split()  # ตัดช่องว่างหัวท้ายแล้วแยกคำตามเว้นวรรค
    if (
        expected_len is not None and len(parts) == 1 and len(parts[0]) == expected_len
    ):  # ถ้า expected_len กำหนดมา และลิสต์มีโทเค็นเดียวซึ่งความยาวตรงกับ expected_len
        return list(parts[0])  # คืนลิสต์ตัวอักษรทีละตัว
    return parts  # คืนลิสต์โทเค็นปกติ


def compute_prefix(pat):  # คำนวณตาราง prefix function (pi) ของ pattern สำหรับ KMP
    m = len(pat)  # ความยาวของ pattern
    pi = [0] * m  # สร้างลิสต์ขนาด m โดยมีค่าเริ่มต้นเป็น 0
    k = 0  # ตัวชี้ความยาวของ prefix ที่แมตช์มากที่สุด
    for q in range(1, m):  # วนตำแหน่ง q ตั้งแต่ 1 ถึง m-1
        while k > 0 and pat[k] != pat[q]:  # ถ้าไม่แมตช์
            k = pi[k - 1]  # ย้อน k ตามค่า pi ก่อนหน้า
        if pat[k] == pat[q]:  # ถ้าแมตช์
            k += 1  # เพิ่มความยาว prefix
        pi[q] = k  # บันทึกค่า prefix function ที่ตำแหน่ง q
    return pi  # คืนค่าตาราง prefix function


def naive_search_lr(pat, text):  # ค้นหา pattern ใน text แบบ naive จากซ้ายไปขวา
    m = len(pat)  # ความยาวของ pattern
    n = len(text)  # ความยาวของ text
    res = []  # เก็บตำแหน่งที่พบ match (1-based)
    for s in range(0, n - m + 1):  # วนตำแหน่งเริ่มต้น s ใน text
        ok = True  # สมมติว่าแมตช์ได้
        for j in range(m):  # วนตำแหน่ง j ใน pattern
            if text[s + j] != pat[j]:  # ถ้าไม่แมตช์/ถ้ามีตัวอักษรไม่ตรงกัน
                ok = False  # ยกเลิกการแมตช์
                break
        if ok:  # ถ้าแมตช์ได้
            res.append(s + 1)  # บันทึกตำแหน่งเริ่มต้น (1-based)
    return res  # คืนค่าลิสต์ตำแหน่งที่พบ match


def naive_search_rl_via_rev(
    pat, text
):  # ค้นหา pattern แบบย้อนกลับ (Right-to-Left) โดยการพลิก pattern ก่อน
    pat_rev = pat[::-1]  # พลิกลำดับ pattern
    m = len(pat)  # ความยาวของ pattern
    n = len(text)  # ความยาวของ text
    res_a = []  # เก็บตำแหน่งเริ่มต้นของ match กับ pat_rev (1-based)
    for s in range(0, n - m + 1):  # วนตำแหน่งเริ่มต้น s ใน text
        ok = True
        for j in range(m):  # วนตำแหน่ง j ใน pat_rev
            if text[s + j] != pat_rev[j]:  # ถ้าไม่แมตช์
                ok = False  # ยกเลิกการแมตช์
                break
        if ok:  # ถ้าแมตช์ได้
            res_a.append(s + 1)  # เก็บตำแหน่งของ pat_rev ใน text
    return [a + m - 1 for a in res_a]  # แปลง a ให้เป็นตำแหน่งเริ่มต้นของการแมตช์ย้อนกลับใน text


def main():
    try:
        line1 = input() # อ่านบรรทัดแรก (มักเป็น header หรือ charset line)
    except EOFError:
        return # จบโปรแกรมถ้าไม่มีอินพุต
    line2 = input().strip() # อ่านบรรทัดที่สอง (ขนาด m และ n) แล้วตัดช่องว่างหัวท้าย
    line3 = input().strip() # อ่านบรรทัดที่สาม (pattern) แล้วตัดช่องว่างหัวท้าย
    line4 = input().strip() # อ่านบรรทัดที่สี่ (text) แล้วตัดช่องว่างหัวท้าย

    parts = line2.split() # แยกขนาด m และ n
    m = int(parts[0]) # แปลงจำนวนโทเค็นใน pattern เป็นจำนวนเต็ม
    n = int(parts[1]) # แปลงจำนวนโทเค็นใน text เป็นจำนวนเต็ม

    pattern = parse_tokens(line3, expected_len=m) # แปลง pattern เป็นลิสต์โทเค็นหรือตัวอักษร
    text = parse_tokens(line4, expected_len=n) # แปลง text เป็นลิสต์โทเค็นหรือตัวอักษร

    pi = compute_prefix(pattern)  # คำนวณตาราง prefix function

    lr_positions = naive_search_lr(pattern, text) # ค้นหา pattern ใน text จากซ้ายไปขวา (LR)
    rl_positions = naive_search_rl_via_rev(pattern, text) # ค้นหา pattern แบบย้อนกลับ (RL)

    matches = []  # ลิสต์เก็บรวมผลลัพธ์ทั้ง LR และ RL
    for p in lr_positions:
        matches.append((p, "LR")) # บันทึกตำแหน่งและทิศทาง LR
    for p in rl_positions:
        matches.append((p, "RL"))  # บันทึกตำแหน่งและทิศทาง RL
    matches.sort(key=lambda x: (x[0], 0 if x[1] == "LR" else 1)) # จัดเรียงผลลัพธ์ตามตำแหน่ง และถ้าตำแหน่งเท่ากันให้ LR มาก่อน RL

    print(" ".join(str(x) for x in pi)) # พิมพ์ตาราง prefix function
    print(len(matches)) # พิมพ์จำนวนครั้งที่พบ pattern
    for pos, d in matches:
        print(f"{pos} {d}") # พิมพ์ตำแหน่งและทิศทางของแต่ละการแมตช์


if __name__ == "__main__":
    main()
