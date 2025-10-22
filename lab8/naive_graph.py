import sys
import matplotlib.pyplot as plt  # ใช้สำหรับสร้างกราฟ

def parse_tokens(line, expected_len=None):
    parts = line.strip().split()
    if expected_len is not None and len(parts) == 1 and len(parts[0]) == expected_len:
        return list(parts[0])
    return parts


def compute_prefix(pat):
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
    m = len(pat)
    n = len(text)
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


def naive_search_rl_via_rev(pat, text):
    pat_rev = pat[::-1]
    m = len(pat)
    n = len(text)
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


def visualize_prefix(pattern, pi):
    """แสดงตารางและกราฟของ prefix function"""
    print("\n📊 Prefix Function Table (KMP π)")
    print("Index   :", " ".join(f"{i:>2}" for i in range(len(pattern))))
    print("Pattern :", " ".join(f"{c:>2}" for c in pattern))
    print("π value :", " ".join(f"{p:>2}" for p in pi))

    # วาดกราฟแท่งของ prefix function
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(pi)), pi, tick_label=pattern, color='skyblue', edgecolor='black')
    plt.title("KMP Prefix Function (π Table)")
    plt.xlabel("Pattern characters")
    plt.ylabel("π value")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # แสดงค่าตัวเลขบนกราฟ
    for i, val in enumerate(pi):
        plt.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


def visualize_matches(text, pattern, lr_positions, rl_positions):
    """แสดงกราฟตำแหน่ง Match ทั้งแบบ LR และ RL"""
    n = len(text)
    plt.figure(figsize=(10, 3))
    plt.title("ตำแหน่งการ Match ของ Pattern ใน Text")

    # Plot text บนแกน x
    plt.plot(range(1, n + 1), [0]*n, 'ko', markersize=4, label="Text")

    # Plot ตำแหน่ง match
    for p in lr_positions:
        plt.plot(p, 0, 'go', markersize=10, label="LR Match" if p == lr_positions[0] else "")
    for p in rl_positions:
        plt.plot(p, 0, 'ro', markersize=10, label="RL Match" if p == rl_positions[0] else "")

    plt.yticks([])
    plt.xlabel("ตำแหน่งในข้อความ (Text index)")
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
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
    lr_positions = naive_search_lr(pattern, text)
    rl_positions = naive_search_rl_via_rev(pattern, text)

    matches = []
    for p in lr_positions:
        matches.append((p, "LR"))
    for p in rl_positions:
        matches.append((p, "RL"))
    matches.sort(key=lambda x: (x[0], 0 if x[1] == "LR" else 1))

    # แสดงผลข้อความ
    print(" ".join(str(x) for x in pi))
    print(len(matches))
    for pos, d in matches:
        print(f"{pos} {d}")

    # ✅ แสดง Visualization
    visualize_prefix(pattern, pi)
    visualize_matches(text, pattern, lr_positions, rl_positions)


if __name__ == "__main__":
    main()
