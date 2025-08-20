import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Stack;

public class BalanceChecker {
    public static boolean isBalanced(String code) {
        Stack<Character> stack = new Stack<>();
        String opening = "([{";
        String closing = ")]}";

        for (int i = 0; i < code.length(); i++) {
            char c = code.charAt(i);

            // ----- ข้ามคอมเมนต์ (# ทั้งบรรทัด) -----
            if (c == '#') {
                while (i < code.length() && code.charAt(i) != '\n') {
                    i++;
                }
                continue;
            }

            // ----- ข้ามสตริง -----
            if (c == '"' || c == '\'') {
                char quote = c;
                i++;
                while (i < code.length()) {
                    if (code.charAt(i) == quote && code.charAt(i - 1) != '\\') {
                        break;
                    }
                    i++;
                }
                continue;
            }

            // ----- เช็ควงเล็บ -----
            if (opening.indexOf(c) != -1) {
                stack.push(c);
            } else if (closing.indexOf(c) != -1) {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if (!matches(top, c)) return false;
            }
        }
        return stack.isEmpty();
    }

    private static boolean matches(char open, char close) {
        return (open == '(' && close == ')') ||
               (open == '[' && close == ']') ||
               (open == '{' && close == '}');
    }

    public static void main(String[] args) {
        // <<< แก้ตรงนี้เพื่อเปลี่ยนชื่อไฟล์ที่ต้องการรัน >>>
        String filename = "C:\\Users\\user\\Downloads\\test10.py";

        StringBuilder code = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                code.append(line).append("\n");
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
            return;
        }

        if (isBalanced(code.toString())) {
            System.out.println("The file is balanced.");
        } else {
            System.out.println("The file is NOT balanced.");
        }
    }
}