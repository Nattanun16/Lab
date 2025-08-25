import operator

# นิยามโครงสร้าง Node ของ Expression Tree
class Node:
    def __init__(self, value):
        self.value = value #ค่าของตัวเลขหรือตัวดำเนินการ
        self.left = None #ชี้ไปยังลูกซ้าย
        self.right = None #ชี้ไปยังลูกขวา

# ตรวจสอบว่าเป็นตัวดำเนินการหรือไม่
def is_operator(c):
    return c in ['+', '-', '*', '/', '^']

# แปลง Infix เป็น Postfix (Shunting-yard algorithm)
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3} # กำหนดลำดับความสำคัญของตัวดำเนินการ
    output = [] # เก็บผลลัพธ์ Postfix
    stack = [] #เก็บเครื่องหมาย
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split() #ตัด string ออกเป็น token (โดยเว้นวรรคเพื่อให้แยกวงเล็บและตัวเลขได้)

    for token in tokens: #วนอ่านแต่ละ token
        if token.isnumeric():  # ถ้าเป็นตัวเลข → ใส่ใน output
            output.append(token)
        elif token == '(': # ถ้าเป็น '(' → ใส่ใน stack
            stack.append(token)
        elif token == ')': # ถ้าเป็น ')' → pop จาก stack ไป output จนเจอ '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # ลบ '(' ออก
        else:  # operator
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]: # pop จาก stack ไป output จนเจอ '(' หรือ operator ที่มีลำดับความสำคัญต่ำกว่า
                output.append(stack.pop())
            stack.append(token) # ใส่ operator ปัจจุบันลง stack

    while stack: # pop เครื่องหมายที่เหลือใน stack ไป output
        output.append(stack.pop())
    return output

# สร้าง Expression Tree จาก Postfix
def construct_tree(postfix):
    stack = [] # ใช้ stack ในการสร้าง tree
    for token in postfix: # วนอ่านแต่ละ token
        if not is_operator(token): # ถ้าเป็นตัวเลข → สร้าง Node และใส่ใน stack
            stack.append(Node(token)) # สร้าง Node และใส่ใน stack
        else: # ถ้าเป็น operator → pop สอง Node จาก stack มาเป็นลูกของ Node ใหม่ แล้วใส่ Node ใหม่กลับใน stack
            right = stack.pop() # pop สอง Node จาก stack
            left = stack.pop() 
            node = Node(token) # สร้าง Node ใหม่
            node.left = left  #กำหนดลูกซ้ายและขวา
            node.right = right #กำหนดลูกซ้ายและขวา
            stack.append(node) # ใส่ Node ใหม่กลับใน stack
    return stack.pop() # Node สุดท้ายใน stack คือ root ของ tree

# Traversal ต่างๆ
def inorder(node): #ใช้ recursion เดิน tree แล้วคืนค่า list ของ traversal
    if node is None: # base case
        return []
    return inorder(node.left) + [node.value] + inorder(node.right) # เดินลูกซ้าย → root → ลูกขวา

def preorder(node): #ใช้ recursion เดิน tree แล้วคืนค่า list ของ traversal
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)

def postorder(node): #ใช้ recursion เดิน tree แล้วคืนค่า list ของ traversal
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value]

# คำนวณค่าจาก Postorder โดยใช้ stack
def evaluate_postorder(postfix): #ใช้ stack ประเมินค่าจาก postfix: ถ้าเจอเลข push, เจอ operator pop 2 ค่า แล้วคำนวณ
    stack = []
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': operator.pow} # mapping ตัวดำเนินการกับฟังก์ชัน
    for token in postfix: 
        if not is_operator(token): # ถ้าเป็นตัวเลข → push ลง stack
            stack.append(float(token)) # แปลงเป็น float เพื่อรองรับการหาร
        else: # ถ้าเป็น operator → pop สองค่า, คำนวณ, แล้ว push ผลลัพธ์ลง stack
            b = stack.pop() 
            a = stack.pop()
            stack.append(ops[token](a, b)) # คำนวณและ push ผลลัพธ์
    return stack.pop()

# --- main program ---
with open("C:\\Users\\user\\Downloads\\Lab_3 example.txt", 'r') as f:
    lines = f.readlines()

for expr in lines: # อ่านแต่ละบรรทัดในไฟล์
    expr = expr.strip() # ลบช่องว่างและ newline
    if not expr: 
        continue # ข้ามบรรทัดว่าง
    postfix = infix_to_postfix(expr) # แปลงเป็น postfix
    tree = construct_tree(postfix) # สร้าง expression tree
    print(f"Expression: {expr}") # แสดงผลลัพธ์
    print("Inorder: ", ' '.join(inorder(tree))) # join list เป็น string โดยมีช่องว่างคั่น
    print("Preorder:", ' '.join(preorder(tree))) # join list เป็น string โดยมีช่องว่างคั่น
    print("Postorder:", ' '.join(postorder(tree))) # join list เป็น string โดยมีช่องว่างคั่น
    print("Result:", evaluate_postorder(postorder(tree))) # ประเมินค่าจาก postorder
    print("------")
