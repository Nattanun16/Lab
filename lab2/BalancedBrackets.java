import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Stack;

public class BalancedBrackets {
    public static boolean isBalanced(String str) {
        Stack<Character> stack = new Stack<>();
        for (char ch : str.toCharArray()) {
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                if (stack.isEmpty()) return false;
                char top = stack.pop();
                if ((ch == ')' && top != '(') ||
                        (ch == ']' && top != '[') ||
                        (ch == '}' && top != '{')) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }

    public static String removeCommentsAndStrings(String code) {
        StringBuilder cleaned = new StringBuilder();
        boolean inString = false;
        char stringChar = 0;
        for (int i = 0; i < code.length(); i++) {
            char ch = code.charAt(i);

            // จัดการ comment (# ...)
            if (!inString && ch == '#') {
                while (i < code.length() && code.charAt(i) != '\n') {
                    i++;
                }
                continue;
            }

            // จัดการ string ('...' หรือ "...")
            if (!inString && (ch == '"' || ch == '\'')) {
                inString = true;
                stringChar = ch;
                continue;
            } else if (inString && ch == stringChar) {
                inString = false;
                continue;
            }

            // ถ้าไม่อยู่ใน string ให้เก็บตัวอักษร
            if (!inString) {
                cleaned.append(ch);
            }
        }
        return cleaned.toString();
    }


    public static void main(String[] args) throws FileNotFoundException {
        // อ่านไฟล์ .py ที่ชื่อ test_balance.py
        Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\test10.py"));
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) {
            sb.append(sc.nextLine());
        }
        sc.close();

        String input = sb.toString();
        input = removeCommentsAndStrings(input);
        if (isBalanced(input)) {
            System.out.println("The file is balanced.");
        } else {
            System.out.println("The file is NOT balanced.");
        }
    }
}