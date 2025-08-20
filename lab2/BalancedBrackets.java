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
        boolean inSingleLineComment = false;
        boolean inMultiLineComment = false;
        boolean inSingleQuoteString = false;
        boolean inDoubleQuoteString = false;
        boolean inTripleSingleQuote = false;
        boolean inTripleDoubleQuote = false;
        
        int i = 0;
        int n = code.length();
        
        while (i < n) {
            char ch = code.charAt(i);
            
            // Handle triple quotes first (for multi-line strings)
            if (!inSingleLineComment && !inMultiLineComment) {
                if (i + 2 < n) {
                    String triple = code.substring(i, i + 3);
                    if (triple.equals("'''") && !inDoubleQuoteString && !inTripleDoubleQuote) {
                        inTripleSingleQuote = !inTripleSingleQuote;
                        i += 3;
                        continue;
                    } else if (triple.equals("\"\"\"") && !inSingleQuoteString && !inTripleSingleQuote) {
                        inTripleDoubleQuote = !inTripleDoubleQuote;
                        i += 3;
                        continue;
                    }
                }
            }
            
            // Handle single and double quotes (only if not in triple quotes)
            if (!inSingleLineComment && !inMultiLineComment && !inTripleSingleQuote && !inTripleDoubleQuote) {
                if (ch == '\'' && !inDoubleQuoteString) {
                    inSingleQuoteString = !inSingleQuoteString;
                    i++;
                    continue;
                } else if (ch == '"' && !inSingleQuoteString) {
                    inDoubleQuoteString = !inDoubleQuoteString;
                    i++;
                    continue;
                }
            }
            
            // Handle comments (only if not in any string)
            if (!inSingleQuoteString && !inDoubleQuoteString && !inTripleSingleQuote && !inTripleDoubleQuote) {
                if (i + 1 < n) {
                    String twoChars = code.substring(i, i + 2);
                    if (twoChars.equals("# ")) {
                        inSingleLineComment = true;
                    }
                }
                
                if (ch == '\n') {
                    inSingleLineComment = false;
                    inMultiLineComment = false;
                }
            }
            
            // Only append characters that are not in comments or strings
            if (!inSingleLineComment && !inMultiLineComment && 
                !inSingleQuoteString && !inDoubleQuoteString && 
                !inTripleSingleQuote && !inTripleDoubleQuote) {
                cleaned.append(ch);
            }
            
            i++;
        }
        
        return cleaned.toString();
    }

    public static void main(String[] args) throws FileNotFoundException {
        // เปลี่ยนเป็นไฟล์ที่ต้องการทดสอบ
        Scanner sc = new Scanner(new File("test8.py"));
        StringBuilder sb = new StringBuilder();
        while (sc.hasNextLine()) {
            sb.append(sc.nextLine()).append("\n"); // เพิ่ม newline ทุกบรรทัด
        }
        sc.close();

        String input = sb.toString();
        System.out.println("Original code:");
        System.out.println(input);
        
        String cleaned = removeCommentsAndStrings(input);
        System.out.println("Cleaned code (only brackets):");
        System.out.println(cleaned);
        
        if (isBalanced(cleaned)) {
            System.out.println("The file is balanced.");
        } else {
            System.out.println("The file is NOT balanced.");
        }
    }
}