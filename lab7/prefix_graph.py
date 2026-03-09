import sys
import matplotlib.pyplot as plt  # สำหรับทำกราฟ


def parse_tokens(line, expected_len=None):  # แปลงสตริงบรรทัดให้เป็นลิสต์ของโทเค็น
    parts = line.strip().split()  # ตัดช่องว่างหัวท้ายแล้วแยกคำตามเว้นวรรค
    if expected_len is not None and len(parts) == 1 and len(parts[0]) == expected_len:
        return list(parts[0])  # แยกโทเค็นนั้นเป็นลิสต์ของตัวอักษร
    return parts  # คืนลิสต์ของโทเค็นตามที่แยกได้


def compute_prefix(
    pat,
):  # คำนวณตาราง prefix function (pi) สำหรับ pattern ใน KMP algorithm
    m = len(pat)  # ความยาวของ pattern
    pi = [0] * m  # สร้างลิสต์ค่า prefix โดยให้เริ่มต้นเป็น 0 ทั้งหมด
    k = 0  # ตัวชี้ความยาว match ที่ยาวที่สุดจนถึงปัจจุบัน
    for q in range(1, m):  # วนตั้งแต่ตำแหน่งที่สองจนถึงสุดของ pattern
        while k > 0 and pat[k] != pat[q]:  # ถ้าไม่ตรงกัน
            k = pi[k - 1]  # ย้อนกลับไปตามค่า pi
        if pat[k] == pat[q]:  # ถ้าตรงกัน
            k += 1  # เพิ่มความยาว match
        pi[q] = k  # กำหนดค่า pi ที่ตำแหน่ง q เป็นความยาว match ปัจจุบัน
    return pi  # คืนค่าตาราง prefix function


def naive_search_lr(pat, text):  # ค้นหา pattern ใน text แบบ naive จากซ้ายไปขวา
    m, n = len(pat), len(text)  # ความยาวของ pattern และ text
    res = []  # ลิสต์เก็บตำแหน่งที่พบ pattern
    for s in range(0, n - m + 1):  # วนผ่านแต่ละตำแหน่งเริ่มต้นใน text
        ok = True  # สมมติว่าแมตช์ได้
        for j in range(m):  # วนผ่านแต่ละตัวอักษรใน pattern
            if text[s + j] != pat[j]:  # ถ้าไม่แมตช์
                ok = False
                break  # ออกจากลูป
        if ok:  # ถ้าแมตช์ได้
            res.append(s + 1)  # บันทึกตำแหน่งเริ่มต้น (1-based)
    return res  # คืนค่าลิสต์ตำแหน่งที่พบ pattern


def naive_search_rl_via_rev(
    pat, text
):  # ค้นหา pattern แบบย้อนกลับ (Right-to-Left) โดยการพลิก pattern ก่อน
    pat_rev = pat[::-1]  # พลิกลำดับ pattern
    m, n = len(pat), len(text)  # ความยาวของ pattern และ text
    res_a = []  # ลิสต์เก็บตำแหน่งที่พบ pattern พลิก
    for s in range(0, n - m + 1):  # วนผ่านแต่ละตำแหน่งเริ่มต้นใน text
        ok = True  # สมมติว่าแมตช์ได้
        for j in range(m):  # วนผ่านแต่ละตัวอักษรใน pattern พลิก
            if text[s + j] != pat_rev[j]:  # ถ้าไม่แมตช์
                ok = False
                break  # ออกจากลูป
        if ok:  # ถ้าแมตช์ได้
            res_a.append(s + 1)  # บันทึกตำแหน่งเริ่มต้น (1-based)
    return [a + m - 1 for a in res_a]  # แปลงเป็นตำแหน่งเริ่มต้นของการแมตช์ย้อนกลับ


def plot_prefix_table(pi):
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(pi) + 1), pi, marker="o", linestyle="-", color="blue")
    plt.title("Prefix Function Table (pi)")
    plt.xlabel("Pattern Position")
    plt.ylabel("Prefix Length")
    plt.grid(True)
    plt.xticks(range(1, len(pi) + 1))
    plt.show()


def plot_match_positions(matches, n):
    plt.figure(figsize=(10, 4))
    positions = [pos for pos, _ in matches]
    directions = [1 if d == "LR" else -1 for _, d in matches]
    colors = ["green" if d == "LR" else "red" for _, d in matches]

    plt.scatter(positions, directions, c=colors, s=100)
    plt.yticks([-1, 1], ["RL", "LR"])
    plt.xticks(range(1, n + 1))
    plt.title("Match Positions in Text")
    plt.xlabel("Text Position (1-based)")
    plt.grid(True)
    plt.show()


def main():
    file_path = "C:\\Users\\user\\Downloads\\8.1.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
    except FileNotFoundError:
        print(f"ไม่พบไฟล์: {file_path}")
        return

    if len(lines) < 4:
        print("ไฟล์ต้องมีอย่างน้อย 4 บรรทัด (charset, m n, pattern, text)")
        return

    line1 = lines[0].strip()
    line2 = lines[1].strip()
    line3 = lines[2].strip()
    line4 = lines[3].strip()

    parts = line2.split()
    m = int(parts[0])
    n = int(parts[1])

    pattern = parse_tokens(line3, expected_len=m)
    text = parse_tokens(line4, expected_len=n)

    pi = compute_prefix(pattern)

    # ค้นหา LR และ RL
    lr_positions = naive_search_lr(pattern, text)
    rl_positions = naive_search_rl_via_rev(pattern, text)

    matches = []
    for p in lr_positions:
        matches.append((p, "LR"))
    for p in rl_positions:
        matches.append((p, "RL"))
    matches.sort(key=lambda x: (x[0], 0 if x[1] == "LR" else 1))

    # แสดงผล
    print(" ".join(str(x) for x in pi))
    print(len(matches))
    for pos, d in matches:
        print(f"{pos} {d}")

    # เพิ่มการ Visualize
    plot_prefix_table(pi)
    plot_match_positions(matches, n)


if __name__ == "__main__":
    main()
