import java.io.*;
import java.util.*;

class Node {
    String value;
    Node left, right;

    Node(String value) {
        this.value = value;
    }
}

public class ExpressionTreeLab3 {

    // ตรวจสอบว่าเป็น operator หรือไม่
    private static boolean isOperator(String s) {
        return "+-*/^".contains(s);
    }

    // กำหนดลำดับความสำคัญ operator
    private static int precedence(String op) {
        return switch (op) {
            case "+", "-" -> 1;
            case "*", "/" -> 2;
            case "^" -> 3;
            default -> 0;
        };
    }

    // แปลง infix เป็น postfix (Shunting-yard algorithm)
    private static List<String> infixToPostfix(String expr) {
        List<String> output = new ArrayList<>();
        Stack<String> stack = new Stack<>();
        String[] tokens = expr.replace("(", " ( ").replace(")", " ) ").trim().split("\\s+");

        for (String token : tokens) {
            if (token.matches("\\d+")) {
                output.add(token);
            } else if (token.equals("(")) {
                stack.push(token);
            } else if (token.equals(")")) {
                while (!stack.isEmpty() && !stack.peek().equals("(")) {
                    output.add(stack.pop());
                }
                stack.pop(); // ลบ (
            } else if (isOperator(token)) {
                while (!stack.isEmpty() && !stack.peek().equals("(") &&
                        precedence(stack.peek()) >= precedence(token)) {
                    output.add(stack.pop());
                }
                stack.push(token);
            }
        }
        while (!stack.isEmpty()) {
            output.add(stack.pop());
        }
        return output;
    }

    // สร้าง Expression Tree จาก postfix
    private static Node constructTree(List<String> postfix) {
        Stack<Node> stack = new Stack<>();
        for (String token : postfix) {
            if (!isOperator(token)) {
                stack.push(new Node(token));
            } else {
                Node right = stack.pop();
                Node left = stack.pop();
                Node node = new Node(token);
                node.left = left;
                node.right = right;
                stack.push(node);
            }
        }
        return stack.pop();
    }

    // Traversals
    private static void inorder(Node root, List<String> result) {
        if (root != null) {
            inorder(root.left, result);
            result.add(root.value);
            inorder(root.right, result);
        }
    }

    private static void preorder(Node root, List<String> result) {
        if (root != null) {
            result.add(root.value);
            preorder(root.left, result);
            preorder(root.right, result);
        }
    }

    private static void postorder(Node root, List<String> result) {
        if (root != null) {
            postorder(root.left, result);
            postorder(root.right, result);
            result.add(root.value);
        }
    }

    // ประเมินค่าจาก postfix
    private static double evaluatePostfix(List<String> postfix) {
        Stack<Double> stack = new Stack<>();
        for (String token : postfix) {
            if (!isOperator(token)) {
                stack.push(Double.valueOf(token));
            } else {
                double b = stack.pop();
                double a = stack.pop();
                switch (token) {
                    case "+" -> stack.push(a + b);
                    case "-" -> stack.push(a - b);
                    case "*" -> stack.push(a * b);
                    case "/" -> stack.push(a / b);
                    case "^" -> stack.push(Math.pow(a, b));
                }
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        String inputFile = "C:\\Users\\user\\Downloads\\Lab_3 example.txt"; // หรือกำหนด path เต็ม
        try (BufferedReader br = new BufferedReader(new FileReader(inputFile))) {
            String expr;
            while ((expr = br.readLine()) != null) {
                expr = expr.trim();
                if (expr.isEmpty())
                    continue;

                List<String> postfix = infixToPostfix(expr);
                Node tree = constructTree(postfix);

                List<String> in = new ArrayList<>();
                List<String> pre = new ArrayList<>();
                List<String> post = new ArrayList<>();
                inorder(tree, in);
                preorder(tree, pre);
                postorder(tree, post);

                System.out.println("Expression: " + expr);
                System.out.println("Inorder: " + String.join(" ", in));
                System.out.println("Preorder: " + String.join(" ", pre));
                System.out.println("Postorder: " + String.join(" ", post));
                System.out.println("Result: "
                        + (evaluatePostfix(post) % 1 == 0 ? (int) evaluatePostfix(post) : evaluatePostfix(post)));
                System.out.println("------");
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
    }
}
