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

    public static void main(String[] args) throws FileNotFoundException {
        // อ่านไฟล์ .py ที่ชื่อ test_balance.py
        Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\test2.py"));
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) {
            sb.append(sc.nextLine());
        }
        sc.close();

        String input = sb.toString();
        if (isBalanced(input)) {
            System.out.println("The file is balanced.");
        } else {
            System.out.println("The file is NOT balanced.");
        }
    }
}