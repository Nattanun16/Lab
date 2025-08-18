import java.util.*;

public class EvaluateExpression {
    public static int precedence(char op) {
        if (op == '+' || op == '-')
            return 1;
        if (op == '*' || op == '/')
            return 2;
        return 0;
    }

    public static int applyOp(int a, int b, char op) {
        switch (op) {
            case '+' -> {
                return a + b;
            }
            case '-' -> {
                return a - b;
            }
            case '*' -> {
                return a * b;
            }
            case '/' -> {
                return a / b;
            }
        }
        return 0;
    }

    public static int evaluate(String expr) {
        Stack<Integer> values = new Stack<>();
        Stack<Character> ops = new Stack<>();
        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);

            if (Character.isWhitespace(ch))
                continue;

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
                ops.pop(); // remove '('
            } else { // operator
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) {
                    int b = values.pop();
                    int a = values.pop();
                    values.push(applyOp(a, b, ops.pop()));
                }
                ops.push(ch);
            }
        }

        while (!ops.isEmpty()) {
            int b = values.pop();
            int a = values.pop();
            values.push(applyOp(a, b, ops.pop()));
        }

        return values.pop();
    }

    public static void main(String[] args) {
        String expr = "10 + 2 * (6 - 4)";
        System.out.println(expr + " = " + evaluate(expr));
    }
}
