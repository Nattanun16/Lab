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

    public static double applyOp(double a, double b, char op) {
        return switch (op) {
            case '+' -> a + b;
            case '-' -> a - b;
            case '*' -> a * b;
            case '/' -> a / b;
            default -> 0;
        };
    }

    public static double evaluate(String expr) {
        Stack<Double> values = new Stack<>();
        Stack<Character> ops = new Stack<>();

        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);

            if (Character.isWhitespace(ch)) continue;

            // ตรวจจับตัวเลข (รวมถึงติดลบและทศนิยม)
            if (Character.isDigit(ch) || ch == '.' ||
                    (ch == '-' && (i == 0 || expr.charAt(i - 1) == '(' || "+-*/".indexOf(expr.charAt(i - 1)) != -1))) {

                boolean negative = false;
                if (ch == '-') {
                    negative = true;
                    i++;
                }

                double val = 0;
                boolean decimalFound = false;
                double decimalDiv = 10;

                while (i < expr.length() && (Character.isDigit(expr.charAt(i)) || expr.charAt(i) == '.')) {
                    if (expr.charAt(i) == '.') {
                        decimalFound = true;
                        i++;
                        continue;
                    }
                    int digit = expr.charAt(i) - '0';
                    if (!decimalFound) {
                        val = val * 10 + digit;
                    } else {
                        val += digit / decimalDiv;
                        decimalDiv *= 10;
                    }
                    i++;
                }

                if (negative) val = -val;
                values.push(val);
                i--; // for-loop จะเพิ่ม i อีกที
            }
            else if (ch == '(') {
                ops.push(ch);
            }
            else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    double b = values.pop();
                    double a = values.pop();
                    values.push(applyOp(a, b, ops.pop()));
                }
                ops.pop(); // ลบ '('
            }
            else { // operator
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) {
                    double b = values.pop();
                    double a = values.pop();
                    values.push(applyOp(a, b, ops.pop()));
                }
                ops.push(ch);
            }
        }

        while (!ops.isEmpty()) {
            double b = values.pop();
            double a = values.pop();
            values.push(applyOp(a, b, ops.pop()));
        }

        return values.pop();
    }

    public static void main(String[] args) throws FileNotFoundException {
        // อ่านไฟล์ที่เก็บ expression
        StringBuilder sb = new StringBuilder();
        try (Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\2_Expression.txt"))) {
            while (sc.hasNextLine()) {
                sb.append(sc.nextLine()).append("\n");
            }
        }

        String expr = sb.toString().trim();
        System.out.println("Expression: " + expr);
        System.out.println("Result = " + evaluate(expr));
    }
}
