import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Stack;

public class EvaluateExpression {
    public static int precedence(char op) {
        if (op == '+' || op == '-') return 1;
        if (op == '*' || op == '/') return 2;
        return 0;
    }

    public static int applyOp(int a, int b, char op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/':
                if (b == 0) throw new ArithmeticException("Divide by zero");
                return a / b;
        }
        return 0;
    }

    public static int evaluate(String expr) {
        Stack<Integer> values = new Stack<>();
        Stack<Character> ops = new Stack<>();

        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);
            if (Character.isWhitespace(ch)) continue;

            if (Character.isDigit(ch)) {
                int val = 0;
                while (i < expr.length() && Character.isDigit(expr.charAt(i))) {
                    val = val * 10 + (expr.charAt(i) - '0');
                    i++;
                }
                values.push(val);
                i--;
            } else if (ch == '(') {
                ops.push(ch);
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    int b = values.pop();
                    int a = values.pop();
                    values.push(applyOp(a, b, ops.pop()));
                }
                ops.pop();
            } else { // operator
                // handle unary minus เช่น -3 หรือ ( -2 )
                if (ch == '-' && (i == 0 || expr.charAt(i-1) == '(' || "+-*/".indexOf(expr.charAt(i-1)) != -1)) {
                    // unary minus: อ่านเลขถัดไปเป็นค่าติดลบ
                    i++;
                    int val = 0;
                    while (i < expr.length() && Character.isDigit(expr.charAt(i))) {
                        val = val * 10 + (expr.charAt(i) - '0');
                        i++;
                    }
                    values.push(-val);
                    i--;
                } else {
                    while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) {
                        int b = values.pop();
                        int a = values.pop();
                        values.push(applyOp(a, b, ops.pop()));
                    }
                    ops.push(ch);
                }
            }
        }

        while (!ops.isEmpty()) {
            int b = values.pop();
            int a = values.pop();
            values.push(applyOp(a, b, ops.pop()));
        }
        return values.pop();
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(new File("test_expression.txt"));
        while (sc.hasNextLine()) {
            String expr = sc.nextLine().trim();
            if (expr.isEmpty()) continue;
            try {
                int result = evaluate(expr);
                System.out.println(expr + " = " + result);
            } catch (Exception e) {
                System.out.println(expr + " -> Error: " + e.getMessage());
            }
        }
        sc.close();
    }
}