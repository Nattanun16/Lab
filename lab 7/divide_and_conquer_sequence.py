def divide_and_conquer_sequence(n):
    if n == 0:
        return [0]
    evens = divide_and_conquer_sequence(n // 2)
    odds = [x * 2 + 1 for x in evens if x * 2 + 1 <= n]
    evens = [x * 2 for x in evens if x * 2 <= n]
    return evens + odds


def iterative_sequence(n):
    # แบบไม่ใช้ Divide and Conquer
    # ใช้วิธีจำลองการสร้างลำดับด้วยการแบ่งเลขคู่/คี่แบบวนลูป
    result = [0]
    while len(result) <= n:
        temp = []
        for x in result:
            if x * 2 <= n:
                temp.append(x * 2)
        for x in result:
            if x * 2 + 1 <= n:
                temp.append(x * 2 + 1)
        result = temp
    return result


def main():
    # 🔹 ใส่ path เต็มของไฟล์ Test Case ตรงนี้
    path = r"C:\Users\Nattanun\Documents\TestCase.txt" #ใส่ path ของไฟล์ที่ต้องการอ่านข้อมูล

    with open(path, "r") as f:
        cases = [int(line.strip()) for line in f if line.strip().isdigit()]

    for n in cases:
        div_seq = divide_and_conquer_sequence(n)
        iter_seq = iterative_sequence(n)

        print(f"n = {n}")
        print("Divide & Conquer :", " ".join(map(str, div_seq)))
        print("Non-D&C         :", " ".join(map(str, iter_seq)))
        print("-" * 40)


if __name__ == "__main__":
    main()