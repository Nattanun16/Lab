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
    file_path = "C:\\Users\\user\\Downloads\\8.8.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines() # อ่านบรรทัดทั้งหมดจากไฟล์
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {file_path}") # แจ้งข้อผิดพลาดถ้าไฟล์ไม่พบ
        return

    if len(lines) < 4: # ตรวจสอบว่ามีบรรทัดครบ 4 บรรทัดหรือไม่
        print("ไฟล์ต้องมีอย่างน้อย 4 บรรทัด (charset, m n, pattern, text)")
        return
    line1 = lines[0].strip()  # เผื่อมี charset
    line2 = lines[1].strip()  # m n line
    line3 = lines[2].strip()  # pattern
    line4 = lines[3].strip()  # text

    parts = line2.split() # แยก m n
    m = int(parts[0]) # แปลง string เป็น integer
    n = int(parts[1]) # แปลง string เป็น integer

    pattern = parse_tokens(line3, expected_len=m) # แปลง pattern เป็นลิสต์โทเค็นหรือตัวอักษร
    text = parse_tokens(line4, expected_len=n) # แปลง text เป็นลิสต์โทเค็นหรือตัวอักษร

    pi = compute_prefix(pattern) # คำนวณตาราง prefix function

    # ค้นหา LR และ RL แบบ naive
    lr_positions = naive_search_lr(pattern, text) # หา match แบบ LR
    rl_positions = naive_search_rl_via_rev(pattern, text)  # หา match แบบ RL

    matches = [] # รวมผลลัพธ์และเรียง
    for p in lr_positions:
        matches.append((p, "LR")) # เพิ่มตำแหน่ง LR
    for p in rl_positions:
        matches.append((p, "RL")) # เพิ่มตำแหน่ง RL
    matches.sort(key=lambda x: (x[0], 0 if x[1] == "LR" else 1)) # จัดเรียงผลลัพธ์ตามตำแหน่ง และถ้าตำแหน่งเท่ากันให้ LR มาก่อน RL

    # แสดงผลทางหน้าจอ
    print(" ".join(str(x) for x in pi)) # พิมพ์ตาราง prefix function
    print(len(matches)) # พิมพ์จำนวน match ที่พบ
    for pos, d in matches:
        print(f"{pos} {d}") # พิมพ์ตำแหน่งและทิศทางของแต่ละการแมตช์


if __name__ == "__main__":
    main()
