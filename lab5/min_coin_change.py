# min_coin_change_fixed.py

def min_coin_change(amount, coins):
    """หาจำนวนเหรียญน้อยที่สุด (Bottom-up DP) + ตาราง lookup"""
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if i - c >= 0:
                dp[i] = min(dp[i], dp[i - c] + 1)

    # สร้าง lookup table 2D
    lookup = [[0] * (amount + 1) for _ in range(len(coins) + 1)]
    for i in range(1, len(coins) + 1):
        for j in range(1, amount + 1):
            if coins[i - 1] <= j:
                if lookup[i - 1][j] == 0 and j != coins[i - 1]:
                    lookup[i][j] = 1 + lookup[i][j - coins[i - 1]]
                else:
                    lookup[i][j] = min(
                        lookup[i - 1][j] if lookup[i - 1][j] > 0 else float("inf"),
                        1 + lookup[i][j - coins[i - 1]],
                    )
            else:
                lookup[i][j] = lookup[i - 1][j]

    return dp[amount], lookup


def run_from_file(filename):
    import os, sys
    # ตั้งค่า stdout เป็น UTF-8 เพื่อรองรับไทยบน Windows
    if os.name == "nt":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 2):
        amount = int(lines[i])
        coins = list(map(int, lines[i + 1].split()))

        print("=" * 40)
        print(f"Amount = {amount}, Coins = {coins}")

        min_coins, table = min_coin_change(amount, coins)
        print(f"จำนวนเหรียญน้อยที่สุด = {min_coins}")
        print("Lookup Table:")
        # แสดง header ของคอลัมน์
        header = ["C\\A"] + list(range(amount + 1))
        print("\t".join(map(str, header)))
        for idx, row in enumerate(table):
            row_display = [str(idx)] + [str(cell) for cell in row]
            print("\t".join(row_display))


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\5.1.txt")