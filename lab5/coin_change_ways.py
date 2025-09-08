# coin_change_ways.py
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def coin_change_ways(amount, coins):
    result = []

    def backtrack(remaining, start, path):
        if remaining == 0:
            result.append(list(path))
            return
        if remaining < 0:
            return
        for i in range(start, len(coins)):
            path.append(coins[i])
            backtrack(remaining - coins[i], i, path)
            path.pop()

    backtrack(amount, 0, [])
    return result


def run_from_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 2):
        amount = int(lines[i])
        coins = list(map(int, lines[i + 1].split()))

        print("=" * 40)
        print(f"Amount = {amount}, Coins = {coins}")

        ways = coin_change_ways(amount, coins)
        print(f"จำนวนวิธีทอน = {len(ways)}")
        for w in ways:
            print(w)


if __name__ == "__main__":
    run_from_file("C:\\Users\\user\\Downloads\\5.1.txt")
