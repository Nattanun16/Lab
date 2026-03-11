import sys
import matplotlib.pyplot as plt  # สำหรับทำกราฟ


def parse_tokens(line, expected_len=None): 
    parts = line.strip().split()  
    if expected_len is not None and len(parts) == 1 and len(parts[0]) == expected_len:
        return list(parts[0]) 
    return parts 


def compute_prefix(
    pat,
): 
    m = len(pat) 
    pi = [0] * m  
    k = 0  
    for q in range(1, m): 
        while k > 0 and pat[k] != pat[q]: 
            k = pi[k - 1]  
        if pat[k] == pat[q]:  
            k += 1  
        pi[q] = k 
    return pi  


def naive_search_lr(pat, text): 
    m, n = len(pat), len(text)  
    res = []  
    for s in range(0, n - m + 1):  
        ok = True  
        for j in range(m):  
            if text[s + j] != pat[j]:  
                ok = False
                break  
        if ok: 
            res.append(s + 1)  
    return res  


def naive_search_rl_via_rev(
    pat, text
):  
    pat_rev = pat[::-1]  
    m, n = len(pat), len(text)  
    res_a = []  
    for s in range(0, n - m + 1):  
        ok = True
        for j in range(m):
            if text[s + j] != pat_rev[j]:
                ok = False
                break  
        if ok:  
            res_a.append(s + 1)
    return [a + m - 1 for a in res_a]


def plot_prefix_table(pi): # ฟังก์ชันสำหรับวาดกราฟของตาราง prefix function (pi)
    plt.figure(figsize=(8, 4)) # กำหนดขนาดของกราฟ
    plt.plot(range(1, len(pi) + 1), pi, marker="o", linestyle="-", color="blue") # วาดกราฟเส้นของค่า pi ตามตำแหน่งของ pattern
    plt.title("Prefix Function Table (pi)") 
    plt.xlabel("Pattern Position")
    plt.ylabel("Prefix Length")
    plt.grid(True) # เพิ่มเส้นตารางเพื่อให้อ่านค่าบนกราฟได้ง่ายขึ้น
    plt.xticks(range(1, len(pi) + 1)) # กำหนดตำแหน่งของแกน x ให้ตรงกับตำแหน่งของ pattern
    plt.show() 


def plot_match_positions(matches, n): # ฟังก์ชันสำหรับวาดกราฟตำแหน่งที่พบ match ใน text
    plt.figure(figsize=(10, 4)) # กำหนดขนาดของกราฟ
    positions = [pos for pos, _ in matches] # ดึงตำแหน่งที่พบ match ออกมา
    directions = [1 if d == "LR" else -1 for _, d in matches] # กำหนดค่า y สำหรับทิศทาง LR เป็น 1 และ RL เป็น -1
    colors = ["green" if d == "LR" else "red" for _, d in matches] # กำหนดสีสำหรับทิศทาง LR เป็นเขียวและ RL เป็นแดง

    plt.scatter(positions, directions, c=colors, s=100) # วาดจุดบนกราฟตามตำแหน่งและทิศทาง
    plt.yticks([-1, 1], ["RL", "LR"]) # กำหนดค่า y และป้ายชื่อสำหรับทิศทาง
    plt.xticks(range(1, n + 1)) # กำหนดตำแหน่งของแกน x ให้ตรงกับความยาวของ text
    plt.title("Match Positions in Text")
    plt.xlabel("Text Position (1-based)")
    plt.grid(True) # เพิ่มเส้นตารางเพื่อให้อ่านค่าบนกราฟได้ง่ายขึ้น
    plt.show()


def main():
    file_path = "C:\\Users\\user\\Downloads\\7_example.txt"
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
    print(" ".join(str(x) for x in pi)) # พิมพ์ตาราง prefix function
    print(len(matches)) # พิมพ์จำนวน match ที่พบ
    for pos, d in matches: # พิมพ์ตำแหน่งและทิศทางของแต่ละการแมตช์
        print(f"{pos} {d}") # เพิ่มการ Visualize

    # เพิ่มการ Visualize
    plot_prefix_table(pi) # วาดกราฟของตาราง prefix function
    plot_match_positions(matches, n) # วาดกราฟตำแหน่งที่พบ match ใน text


if __name__ == "__main__":
    main()
