import operator  # นำเข้าโมดูล operator เพื่อใช้ฟังก์ชันทางคณิตศาสตร์
import re # นำเข้าโมดูล re เพื่อใช้ในการแยกสมการเป็น token


class Node:
    def __init__(self, value):  # กำหนดคลาส Node สำหรับเก็บโหนดของ Binary Expression Tree
        self.value = value  # เก็บค่าของโหนด
        self.left = None  # เก็บโหนดลูกซ้าย
        self.right = None  # เก็บโหนดลูกขวา


def is_operator(c):  # ตรวจสอบว่าเป็นตัวดำเนินการหรือไม่
    return c in ["+", "-", "*", "/"]  # ถ้าเป็นตัวดำเนินการจะคืนค่า True


# แปลง Infix → Postfix (ใช้ Shunting Yard)
def infix_to_postfix(expression):  # แปลงนิพจน์จาก infix เป็น postfix
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}  # กำหนดลำดับความสำคัญของตัวดำเนินการ
    output = []  # เก็บผลลัพธ์ของนิพจน์ในรูปแบบ postfix
    stack = []  # เก็บตัวดำเนินการระหว่างการแปลง
    tokens = re.findall(
        r"\d+|[()+\-*/]", expression
    )  # แยกสมการเป็นรายการ โดยเว้นวรรครอบวงเล็บเพื่อให้แยก token ได้ง่าย
    for token in tokens:  # วนลูปผ่านแต่ละ token
        if token.isdigit():  # ถ้าเป็นตัวเลข
            output.append(token)  # ส่งออกไปที่ output ทันที
        elif token == "(":  # ถ้าเป็น '('
            stack.append(token)  # เก็บไว้ใน stack
        elif token == ")":  # ถ้าเป็น ')'
            while stack and stack[-1] != "(":  # ดึงตัวดำเนินการออกจาก stack จนกว่าจะเจอ '('
                output.append(stack.pop())  # ส่งตัวดำเนินการที่ดึงออกไปที่ output
            stack.pop()  # ลบ '(' ออก
        elif is_operator(token):  # ถ้าเป็นตัวดำเนินการ
            while (
                stack
                and stack[-1] != "("
                and precedence[stack[-1]] >= precedence[token]
            ):  # ดึงตัวดำเนินการจาก stack ที่มีลำดับความสำคัญสูงกว่าหรือเท่ากับ token ปัจจุบัน
                output.append(stack.pop())  # ส่งตัวดำเนินการที่ดึงออกไปที่ output
            stack.append(token)  # เก็บ token ปัจจุบันไว้ใน stack
    while stack:  # ถ้า stack ยังไม่ว่าง
        output.append(stack.pop())  # ดึงตัวดำเนินการที่เหลือออกไปที่ output
    return output  # คืนค่านิพจน์ในรูปแบบ postfix


# สร้าง Expression Tree จาก Postfix
def build_expression_tree(
    postfix,
):  # สร้าง Binary Expression Tree จากนิพจน์ในรูปแบบ postfix
    stack = []  # ใช้ stack ในการสร้างต้นไม้
    for token in postfix:  # วนลูปผ่านแต่ละ token ใน postfix
        if not is_operator(token):  # ถ้าเป็นตัวเลข
            stack.append(Node(token))  # สร้างโหนดใหม่และเก็บไว้ใน stack
        else:  # ถ้าเป็นตัวดำเนินการ
            node = Node(token)  # สร้างโหนดใหม่สำหรับตัวดำเนินการ
            node.right = stack.pop()  # ดึงโหนดลูกขวาออกจาก stack
            node.left = stack.pop()  # ดึงโหนดลูกซ้ายออกจาก stack
            stack.append(node)  # เก็บโหนดใหม่ไว้ใน stack
    return stack[-1]  # คืนค่าโหนดรากของต้นไม้


# Traversal
def inorder(node):  # การเดินทางแบบ Inorder
    return (
        inorder(node.left) + [node.value] + inorder(node.right) if node else []
    )  # ถ้าโหนดไม่เป็น None ให้เดินทางซ้าย → โหนดปัจจุบัน → ขวา


def preorder(node):  # การเดินทางแบบ Preorder
    return (
        [node.value] + preorder(node.left) + preorder(node.right) if node else []
    )  # ถ้าโหนดไม่เป็น None ให้เดินทาง โหนดปัจจุบัน → ซ้าย → ขวา


def postorder(node):  # การเดินทางแบบ Postorder
    return (
        postorder(node.left) + postorder(node.right) + [node.value] if node else []
    )  # ถ้าโหนดไม่เป็น None ให้เดินทาง ซ้าย → ขวา → โหนดปัจจุบัน


# คำนวณค่าจาก Postorder โดยใช้ stack
def evaluate_postorder(postfix):  # คำนวณค่าของนิพจน์ในรูปแบบ postfix
    stack = []  # ใช้ stack ในการคำนวณ
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }  # แผนที่ตัวดำเนินการไปยังฟังก์ชันที่เกี่ยวข้อง
    for token in postfix:  # วนลูปผ่านแต่ละ token ใน postfix
        if token not in ops:  # ถ้าเป็นตัวเลข
            stack.append(int(token))  # แปลงเป็นจำนวนเต็มและเก็บไว้ใน stack
        else:  # ถ้าเป็น operator
            b = stack.pop()  # ดึงตัวเลขสองตัวออกจาก stack
            a = stack.pop()  # ดึงตัวเลขสองตัวออกจาก stack
            stack.append(ops[token](a, b))  # คำนวณผลลัพธ์และเก็บไว้ใน stack
    return stack[0]  # คืนค่าผลลัพธ์สุดท้าย


# ฟังก์ชันรวมทุกขั้นตอน
def process_expression(expression):  # ประมวลผลนิพจน์ทางคณิตศาสตร์
    expression = expression.replace("–", "-")
    postfix = infix_to_postfix(expression)  # แปลงนิพจน์เป็น postfix
    tree_root = build_expression_tree(postfix)  # สร้าง Expression Tree
    in_ord = inorder(tree_root)  # ทำ Inorder Traversal
    pre_ord = preorder(tree_root)  # ทำ Preorder Traversal
    post_ord = postorder(tree_root)  # ทำ Postorder Traversal
    value = evaluate_postorder(post_ord)  # คำนวณค่าของนิพจน์
    return in_ord, pre_ord, post_ord, value  # คืนค่าผลลัพธ์ทั้งหมด


# ---------- อ่านไฟล์และแสดงผล ----------
with open("C:\\Users\\user\\Downloads\\lab6_testcase.txt", "r") as f:
    lines = f.readlines()

for expr in lines:  # วนลูปผ่านแต่ละบรรทัดในไฟล์
    expr = expr.strip()  # ลบช่องว่างรอบๆบรรทัด
    if expr:  # ถ้าไม่ใช่บรรทัดว่าง
        in_ord, pre_ord, post_ord, value = process_expression(expr)  # ประมวลผลนิพจน์
        print(f"Expression: {expr}")  # แสดงนิพจน์ต้นฉบับ
        print("Inorder:  ", " ".join(in_ord))  # แสดงผล Inorder
        print("Preorder: ", " ".join(pre_ord))  # แสดงผล Preorder
        print("Postorder:", " ".join(post_ord))  # แสดงผล Postorder
        print("Result:   ", value)  # แสดงผลลัพธ์ของนิพจน์
        print("-" * 40)  # แสดงเส้นคั่นระหว่างผลลัพธ์ของนิพจน์แต่ละบรรทัด
