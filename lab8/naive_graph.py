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


def plot_prefix_table(pi):
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(pi) + 1), pi, marker="o", linestyle="-", color="blue")
    plt.title("Prefix Function Table (pi)")
    plt.xlabel("Pattern Position")
    plt.ylabel("Prefix Length")
    plt.grid(True)
    plt.xticks(range(1, len(pi) + 1))
    plt.tight_layout()
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
    plot_prefix_table(pi)
    plot_match_positions(matches, n)


if __name__ == "__main__":
    main()
