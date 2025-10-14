def divide_and_conquer_sequence(n): # แบบใช้ Divide and Conquer
    # ใช้วิธีแบ่งปัญหาเป็นปัญหาย่อยโดยการสร้างลำดับจาก n//2
    if n == 0: # Base case
        return [0] # เริ่มต้นด้วยลำดับที่มีเพียง 0
    # แบ่งปัญหาเป็นปัญหาย่อย
    evens = divide_and_conquer_sequence(n // 2) # สร้างลำดับสำหรับเลขคู่
    # รวมผลลัพธ์จากปัญหาย่อย
    odds = [x * 2 + 1 for x in evens if x * 2 + 1 <= n] # สร้างลำดับสำหรับเลขคี่
    evens = [x * 2 for x in evens if x * 2 <= n] # สร้างลำดับสำหรับเลขคู่
    return evens + odds # รวมลำดับเลขคู่และเลขคี่


def iterative_sequence(n): 
    # แบบไม่ใช้ Divide and Conquer
    # ใช้วิธีจำลองการสร้างลำดับด้วยการแบ่งเลขคู่/คี่แบบวนลูป
    result = [0] # เริ่มต้นด้วยลำดับที่มีเพียง 0
    while len(result) <= n: # ทำจนกว่าความยาวของลำดับจะเกิน n
        temp = [] # สร้างลำดับชั่วคราว
        for x in result: # สร้างลำดับเลขคู่ก่อน
            if x * 2 <= n: # ตรวจสอบว่าเลขคู่ไม่เกิน n
                temp.append(x * 2) # เพิ่มเลขคู่ลงในลำดับชั่วคราว
        for x in result: # สร้างลำดับเลขคี่
            if x * 2 + 1 <= n: # ตรวจสอบว่าเลขคี่ไม่เกิน n
                temp.append(x * 2 + 1) # เพิ่มเลขคี่ลงในลำดับชั่วคราว
        result = temp # อัปเดตลำดับหลักด้วยลำดับชั่วคราว
    return result #[:n + 1] # คืนค่าลำดับที่มีความยาว n+1


def main():
    # 🔹 ใส่ path เต็มของไฟล์ Test Case ตรงนี้
    path = r"C:\Users\Nattanun\Documents\TestCase.txt" #ใส่ path ของไฟล์ที่ต้องการอ่านข้อมูล

    with open(path, "r") as f: 
        cases = [int(line.strip()) for line in f if line.strip().isdigit()] # อ่านข้อมูลจากไฟล์และเก็บเป็นรายการของจำนวนเต็ม

    for n in cases: 
        div_seq = divide_and_conquer_sequence(n) # เรียกใช้ฟังก์ชันแบบ Divide and Conquer
        iter_seq = iterative_sequence(n) # เรียกใช้ฟังก์ชันแบบไม่ใช้ Divide and Conquer

        print(f"n = {n}") # แสดงค่า n
        print("Divide & Conquer :", " ".join(map(str, div_seq))) # แสดงผลลัพธ์จากฟังก์ชันแบบ Divide and Conquer
        print("Non-D&C         :", " ".join(map(str, iter_seq))) # แสดงผลลัพธ์จากฟังก์ชันแบบไม่ใช้ Divide and Conquer
        print("-" * 40)


if __name__ == "__main__":
    main()