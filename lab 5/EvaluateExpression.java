import java.io.File; // สำหรับจัดการไฟล์
import java.io.FileNotFoundException; // สำหรับจัดการข้อผิดพลาดเมื่อหาไฟล์ไม่เจอ
import java.util.Scanner; // สำหรับอ่านไฟล์
import java.util.Stack; // สำหรับใช้สแต็ก

public class EvaluateExpression { // ประเมินผลนิพจน์ทางคณิตศาสตร์จากไฟล์

    public static int precedence(char op) { // กำหนดลำดับความสำคัญของ operator
        if (op == '+' || op == '-')
            return 1; // ความสำคัญของ + และ - คือ 1
        if (op == '*' || op == '/')
            return 2; // ความสำคัญของ * และ / คือ 2
        return 0; // กรณีอื่นๆ ความสำคัญคือ 0
    }

    public static double applyOp(double a, double b, char op) { // ประเมินผล a, op, b
        return switch (op) { // ใช้ switch expression
            case '+' -> a + b;
            case '-' -> a - b;
            case '*' -> a * b;
            case '/' -> a / b;
            default -> 0;
        };
    }

    public static double evaluate(String expr) { // ประเมินผลนิพจน์
        Stack<Double> values = new Stack<>(); // สแต็กเก็บตัวเลข
        Stack<Character> ops = new Stack<>(); // สแต็กเก็บ operator

        for (int i = 0; i < expr.length(); i++) { // วนลูปผ่านแต่ละตัวอักษรในนิพจน์
            char ch = expr.charAt(i); // ตัวอักษรปัจจุบัน

            if (Character.isWhitespace(ch))
                continue; // ข้ามช่องว่าง

            // ตรวจจับตัวเลข (รวมถึงติดลบและทศนิยม)
            if (Character.isDigit(ch) || ch == '.' ||
                    (ch == '-' && (i == 0 || expr.charAt(i - 1) == '(' || "+-*/".indexOf(expr.charAt(i - 1)) != -1))) { // ลบถ้าเป็นลบหน้าตัวเลข

                boolean negative = false; // ตรวจสอบว่าลบหรือไม่
                if (ch == '-') { // ถ้าเป็นลบ
                    negative = true; // ตั้งค่าว่าลบ
                    i++; // ข้ามเครื่องหมายลบ
                }

                double val = 0; // ตัวแปรเก็บค่าตัวเลข
                boolean decimalFound = false; // ตรวจสอบว่าพบจุดทศนิยมหรือไม่
                double decimalDiv = 10; // ตัวหารสำหรับทศนิยม

                while (i < expr.length() && (Character.isDigit(expr.charAt(i)) || expr.charAt(i) == '.')) { // อ่านตัวเลขและจุดทศนิยม
                    if (expr.charAt(i) == '.') { // ถ้าพบจุดทศนิยม
                        decimalFound = true; // ตั้งค่าว่าพบจุดทศนิยม
                        i++; // ข้ามจุดทศนิยม
                        continue; // ข้ามไปประมวลผลตัวถัดไป
                    }
                    int digit = expr.charAt(i) - '0'; // แปลงตัวอักษรเป็นตัวเลข
                    if (!decimalFound) { // ถ้ายังไม่พบจุดทศนิยม
                        val = val * 10 + digit; // สร้างตัวเลขเต็ม
                    } else {// ถ้าพบจุดทศนิยมแล้ว
                        val += digit / decimalDiv; // เพิ่มค่าทศนิยม
                        decimalDiv *= 10; // เพิ่มตัวหารทศนิยม
                    }
                    i++; // ไปตัวอักษรถัดไป
                }

                if (negative)
                    val = -val; // ถ้าลบ ให้ลบค่าตัวเลข
                values.push(val); // เก็บตัวเลขในสแต็ก
                i--; // ลดค่า i เพราะลูปจะเพิ่มค่า i อีกครั้ง
            } else if (ch == '(') { // ถ้าเจอ '('
                ops.push(ch); // เก็บ '(' ในสแต็ก
            } else if (ch == ')') { // ถ้าเจอ ')'
                while (!ops.isEmpty() && ops.peek() != '(') { // ประเมินผลจนเจอ '('
                    double b = values.pop(); // ตัวที่สอง
                    double a = values.pop(); // ตัวที่หนึ่ง
                    values.push(applyOp(a, b, ops.pop())); // ประเมินผลและเก็บผลลัพธ์กลับในสแต็ก
                }
                if (!ops.isEmpty())
                    ops.pop(); // เอา '(' ออกจากสแต็ก
            } else { // operator
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) { // ประเมินผลตามลำดับความสำคัญ
                    double b = values.pop(); // ตัวที่สอง
                    double a = values.pop(); // ตัวที่หนึ่ง
                    values.push(applyOp(a, b, ops.pop())); // ประเมินผลและเก็บผลลัพธ์กลับในสแต็ก
                }
                ops.push(ch); // เก็บ operator ปัจจุบันในสแต็ก
            }
        }

        while (!ops.isEmpty()) { // ประเมินผลที่เหลือในสแต็ก
            double b = values.pop(); // ตัวที่สอง
            double a = values.pop(); // ตัวที่หนึ่ง
            values.push(applyOp(a, b, ops.pop())); // ประเมินผลและเก็บผลลัพธ์กลับในสแต็ก
        }

        return values.pop(); // ผลลัพธ์สุดท้าย
    }

    public static void main(String[] args) throws FileNotFoundException {
        // อ่านไฟล์ที่เก็บ expression //
        String path = args.length > 0 ? args[0] : "C:\\Users\\user\\Downloads\\2_Expression.txt";
        try (Scanner sc = new Scanner(new File(path))) { // อ่านไฟล์
            int lineNo = 0; // ตัวนับบรรทัด
            while (sc.hasNextLine()) { // อ่านทีละบรรทัด
                String line = sc.nextLine().trim(); // อ่านบรรทัดปัจจุบันและตัดช่องว่างข้างหน้า-หลัง
                lineNo++; // เพิ่มตัวนับบรรทัด
                if (line.isEmpty())
                    continue; // ข้ามบรรทัดว่าง
                System.out.println("Expression (line " + lineNo + "): " + line);
                try {
                    double result = evaluate(line); // ประเมินผลนิพจน์
                    System.out.println("Result = " + result); // แสดงผลลัพธ์
                } catch (Exception e) {
                    System.out.println("Error evaluating line " + lineNo + ": " + e.getMessage()); // แสดงข้อความผิดพลาด
                }
                System.out.println(); // เว้นบรรทัด
            }
        }
    }
}