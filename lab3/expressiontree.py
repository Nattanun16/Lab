import operator

# Node class for Expression Tree
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Function to check if a token is an operator
def is_operator(c):
    return c in ['+', '-', '*', '/']

# Convert infix expression to postfix (using Shunting Yard algorithm)
def infix_to_postfix(expression):
    precedence = {'+':1, '-':1, '*':2, '/':2}
    output = []
    stack = []
    tokens = expression.replace('(',' ( ').replace(')',' ) ').split()
    
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif is_operator(token):
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

# Build expression tree from postfix expression
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

# Traversals
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

# Evaluate expression tree using postorder traversal
def evaluate_postorder(postfix):
    stack = []
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    for token in postfix:
        if token not in ops:
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
    return stack[0]

# Main Program
def process_expression(expression):
    postfix = infix_to_postfix(expression)
    tree_root = build_expression_tree(postfix)
    in_ord = inorder(tree_root)
    pre_ord = preorder(tree_root)
    post_ord = postorder(tree_root)
    value = evaluate_postorder(post_ord)
    return in_ord, pre_ord, post_ord, value

# Read file and process
with open("C:\\Users\\user\\Downloads\\Lab_3 example.txt", 'r') as f:
    lines = f.readlines()

for expr in lines:
    expr = expr.strip()
    if expr:
        in_ord, pre_ord, post_ord, value = process_expression(expr)
        print(f"Expression: {expr}")
        print("Inorder:", ' '.join(in_ord))
        print("Preorder:", ' '.join(pre_ord))
        print("Postorder:", ' '.join(post_ord))
        print("Result:", value)
        print('-'*40)
