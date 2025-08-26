import operator

# Node class for Expression Tree
class Node: #กำหนดคลาส Node สำหรับเก็บโหนดของ Binary Expression Tree
    def __init__(self, value): 
        self.value = value #เก็บค่าของโหนด
        self.left = None   #เก็บโหนดลูกซ้าย
        self.right = None #เก็บโหนดลูกขวา

# Function to check if a token is an operator
def is_operator(c): #ตรวจสอบว่าเป็นตัวดำเนินการหรือไม่
    return c in ['+', '-', '*', '/'] #ถ้าเป็นตัวดำเนินการจะคืนค่า True

# Convert infix expression to postfix (using Shunting Yard algorithm)
def infix_to_postfix(expression): #แปลงนิพจน์จาก infix เป็น postfix
    precedence = {'+':1, '-':1, '*':2, '/':2} #กำหนดลำดับความสำคัญของตัวดำเนินการ
    output = [] #เก็บผลลัพธ์ของนิพจน์ในรูปแบบ postfix
    stack = [] #เก็บตัวดำเนินการระหว่างการแปลง
    tokens = expression.replace('(',' ( ').replace(')',' ) ').split() #แยกสมการเป็นรายการ โดยเว้นวรรครอบวงเล็บเพื่อให้แยก token ได้ง่าย
    
    for token in tokens:
        if token.isdigit():
            output.append(token) #ถ้า token เป็นตัวเลข (operand) จะส่งออกไปที่ output ทันที
        elif token == '(': #ถ้า token เป็นวงเล็บเปิด จะเก็บไว้ใน stack
            stack.append(token)
        elif token == ')': #ถ้า token เป็นวงเล็บปิด จะดึงตัวดำเนินการออกจาก stack จนกว่าจะเจอวงเล็บเปิด
            while stack and stack[-1] != '(': #ดึงตัวดำเนินการออกจาก stack จนกว่าจะเจอวงเล็บเปิด
                output.append(stack.pop()) #ส่งตัวดำเนินการที่ดึงออกไปที่ output
            stack.pop() #ดึงวงเล็บเปิดออกจาก stack
        elif is_operator(token): #ถ้า token เป็นตัวดำเนินการ
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]: #ดึงตัวดำเนินการจาก stack ที่มีลำดับความสำคัญสูงกว่าหรือเท่ากับ token ปัจจุบัน
                output.append(stack.pop()) #ส่งตัวดำเนินการที่ดึงออกไปที่ output
            stack.append(token) #เก็บ token ปัจจุบันไว้ใน stack
    while stack: #ถ้า stack ยังไม่ว่าง ให้ดึงตัวดำเนินการที่เหลือออกไปที่ output
        output.append(stack.pop()) #ดึงตัวดำเนินการที่เหลือใน stack ออกไปที่ output
    return output

# Build expression tree from postfix expression
def build_expression_tree(postfix): #สร้าง Binary Expression Tree จากนิพจน์ในรูปแบบ postfix
    stack = [] #เก็บโหนดของต้นไม้ระหว่างการสร้าง
    for token in postfix: #วนลูปผ่านแต่ละ token ในนิพจน์ postfix
        if not is_operator(token): #ถ้า token ไม่ใช่ตัวดำเนินการ (เป็น operand)
            stack.append(Node(token)) #สร้างโหนดใหม่และเก็บไว้ใน stack
        else: #ถ้า token เป็นตัวดำเนินการ
            node = Node(token) #สร้างโหนดใหม่สำหรับตัวดำเนินการ
            node.right = stack.pop() #ดึงโหนดลูกขวาออกจาก stack
            node.left = stack.pop()
            stack.append(node) #เก็บโหนดใหม่ที่มีลูกซ้ายและขวาไว้ใน stack
    return stack[-1]

# Traversals
def inorder(node): #การเดินทางแบบ inorder (ซ้าย, ราก, ขวา)
    if node is None: # ถ้าโหนดเป็น None จะคืนค่าเป็นลิสต์ว่าง
        return []
    return inorder(node.left) + [node.value] + inorder(node.right) #เดินทางไปทางซ้ายก่อน, จากนั้นเพิ่มค่าตัวเอง, แล้วไปทางขวา

def preorder(node):
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right) #Preorder : พิมพ์ค่าตัวเองก่อน → ลูกซ้าย → ลูกขวา

def postorder(node):
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value] #Postorder : ลูกซ้าย → ลูกขวา → พิมพ์ค่าตัวเองทีหลัง

# Evaluate expression tree using postorder traversal
def evaluate_postorder(postfix):
    stack = [] #เก็บค่าระหว่างการประเมินผล
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv} #กำหนดฟังก์ชันสำหรับตัวดำเนินการแต่ละตัว
    for token in postfix: #วนลูปผ่านแต่ละ token ในนิพจน์ postfix
        if token not in ops: #ถ้า token ไม่ใช่ตัวดำเนินการ (เป็น operand)
            stack.append(int(token)) #แปลง token เป็นจำนวนเต็มและเก็บไว้ใน stack
        else: #ถ้า token เป็นตัวดำเนินการ
            b = stack.pop() #ดึงค่าล่าสุดสองค่าออกจาก stack
            a = stack.pop() 
            stack.append(ops[token](a, b)) #ประเมินผลโดยใช้ฟังก์ชันที่ตรงกับตัวดำเนินการและเก็บผลลัพธ์ไว้ใน stack
    return stack[0] #ค่าที่เหลือใน stack คือผลลัพธ์สุดท้าย

# Main Program
def process_expression(expression): #ฟังก์ชันหลักในการประมวลผลนิพจน์
    postfix = infix_to_postfix(expression) #แปลงนิพจน์จาก infix เป็น postfix
    tree_root = build_expression_tree(postfix) #สร้าง Binary Expression Tree จากนิพจน์ postfix
    in_ord = inorder(tree_root) #ทำการเดินทางแบบ inorder, preorder, postorder และประเมินผล
    pre_ord = preorder(tree_root) 
    post_ord = postorder(tree_root)
    value = evaluate_postorder(post_ord) #ประเมินผลโดยใช้ postorder
    return in_ord, pre_ord, post_ord, value #คืนค่าผลลัพธ์ทั้งหมด

# Read file and process
with open("C:\\Users\\user\\Downloads\\Lab_3 example.txt", 'r') as f:
    lines = f.readlines()

for expr in lines:
    expr = expr.strip() #ลบช่องว่างและตัวขึ้นบรรทัดใหม่
    if expr:
        in_ord, pre_ord, post_ord, value = process_expression(expr) #ประมวลผลนิพจน์
        print(f"Expression: {expr}") #แสดงผลลัพธ์
        print("Inorder:", ' '.join(in_ord)) #แสดงผลลัพธ์การเดินทางแบบ inorder
        print("Preorder:", ' '.join(pre_ord)) #แสดงผลลัพธ์การเดินทางแบบ preorder
        print("Postorder:", ' '.join(post_ord)) #แสดงผลลัพธ์การเดินทางแบบ postorder
        print("Result:", value) #แสดงผลลัพธ์การประเมินผล
        print('-'*40) #แสดงเส้นคั่นระหว่างผลลัพธ์ของแต่ละนิพจน์
