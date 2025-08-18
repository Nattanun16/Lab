def is_balanced(expression): #สร้างฟังก์ชัน is_balanced(expression) รับสตริงที่ต้องตรวจสอบ
    stack = [] # สร้าง stack ว่างสำหรับเก็บวงเล็บ
    pairs = {")": "(", "]": "[", "}": "{"} # สร้าง dictionary สำหรับจับคู่วงเล็บ

    for ch in expression: #วนลูปผ่านแต่ละตัวอักษรในสตริง
        if ch in "([{":
            stack.append(ch)  # push ลง Stack
        elif ch in ")]}": # ถ้าเจอวงเล็บปิด
            if not stack or stack[-1] != pairs[ch]: #ตรวจสอบว่า stack ต้อง ไม่ว่าง และตัวบนสุด (stack[-1]) ต้องเป็นวงเล็บเปิดที่ตรงคู่กับ ch
                return False # ถ้าไม่ตรง → return False
            stack.pop()  # ถ้าตรง → pop วงเล็บเปิดออกจาก stack (เพราะจับคู่แล้ว)
    return len(stack) == 0 # ถ้า stack ว่างแสดงว่าจับคู่ครบ → return True, ถ้าไม่ว่าง → return False


# ตัวอย่างทดสอบ
print(is_balanced("{[()]}"))  # True
print(is_balanced("([)]"))  # False
