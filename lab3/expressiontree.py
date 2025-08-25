import operator

# นิยามโครงสร้าง Node ของ Expression Tree
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# ตรวจสอบว่าเป็นตัวดำเนินการหรือไม่
def is_operator(c):
    return c in ['+', '-', '*', '/', '^']

# แปลง Infix เป็น Postfix (Shunting-yard algorithm)
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = []
    stack = []
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

    for token in tokens:
        if token.isnumeric():  # ถ้าเป็นตัวเลข
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # ลบ '(' ออก
        else:  # operator
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())
    return output

# สร้าง Expression Tree จาก Postfix
def construct_tree(postfix):
    stack = []
    for token in postfix:
        if not is_operator(token):
            stack.append(Node(token))
        else:
            right = stack.pop()
            left = stack.pop()
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)
    return stack.pop()

# Traversal ต่างๆ
def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)

def preorder(node):
    if node is None:
        return []
    return [node.value] + preorder(node.left) + preorder(node.right)

def postorder(node):
    if node is None:
        return []
    return postorder(node.left) + postorder(node.right) + [node.value]

# คำนวณค่าจาก Postorder โดยใช้ stack
def evaluate_postorder(postfix):
    stack = []
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': operator.pow}
    for token in postfix:
        if not is_operator(token):
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
    return stack.pop()

# --- main program ---
with open("C:\\Users\\user\\Downloads\\Lab_3 example.txt", 'r') as f:
    lines = f.readlines()

for expr in lines:
    expr = expr.strip()
    if not expr:
        continue
    postfix = infix_to_postfix(expr)
    tree = construct_tree(postfix)
    print(f"Expression: {expr}")
    print("Inorder: ", ' '.join(inorder(tree)))
    print("Preorder:", ' '.join(preorder(tree)))
    print("Postorder:", ' '.join(postorder(tree)))
    print("Result:", evaluate_postorder(postorder(tree)))
    print("------")
