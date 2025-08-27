import operator

# ---------- Node class สำหรับ Expression Tree ----------
class Node:
    def __init__(self, value): # กำหนดคลาส Node สำหรับเก็บโหนดของ Binary Expression Tree
        self.value = value
        self.left = None
        self.right = None

# ---------- ฟังก์ชันช่วย ----------
def is_operator(c):
    return c in ['+', '-', '*', '/']

# แปลง Infix → Postfix (ใช้ Shunting Yard)
def infix_to_postfix(expression):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    output = []
    stack = []
    tokens = expression.replace('(',' ( ').replace(')',' ) ').split()
    for token in tokens:
        if token.isdigit():          # ถ้าเป็นตัวเลข
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # ลบ '(' ออก
        elif is_operator(token):
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

# สร้าง Expression Tree จาก Postfix
def build_expression_tree(postfix):
    stack = []
    for token in postfix:
        if not is_operator(token):
            stack.append(Node(token))
        else:
            node = Node(token)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack[-1]

# Traversal
def inorder(node):
    return inorder(node.left) + [node.value] + inorder(node.right) if node else []

def preorder(node):
    return [node.value] + preorder(node.left) + preorder(node.right) if node else []

def postorder(node):
    return postorder(node.left) + postorder(node.right) + [node.value] if node else []

# คำนวณค่าจาก Postorder โดยใช้ stack
def evaluate_postorder(postfix):
    stack = []
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    for token in postfix:
        if token not in ops:        # ถ้าเป็นตัวเลข
            stack.append(int(token))
        else:                       # ถ้าเป็น operator
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
    return stack[0]

# ฟังก์ชันรวมทุกขั้นตอน
def process_expression(expression):
    postfix = infix_to_postfix(expression)
    tree_root = build_expression_tree(postfix)
    in_ord = inorder(tree_root)
    pre_ord = preorder(tree_root)
    post_ord = postorder(tree_root)
    value = evaluate_postorder(post_ord)
    return in_ord, pre_ord, post_ord, value

# ---------- อ่านไฟล์และแสดงผล ----------
with open("C:\\Users\\user\\Downloads\\lab3_test_case.txt", 'r') as f:
    lines = f.readlines()

for expr in lines:
    expr = expr.strip()
    if expr:  # ถ้าไม่ใช่บรรทัดว่าง
        in_ord, pre_ord, post_ord, value = process_expression(expr)
        print(f"Expression: {expr}")
        print("Inorder:  ", ' '.join(in_ord))
        print("Preorder: ", ' '.join(pre_ord))
        print("Postorder:", ' '.join(post_ord))
        print("Result:   ", value)
        print('-'*40)
