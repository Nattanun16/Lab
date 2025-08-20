import java.util.*;

public class EvaluateExpression {
    public static int precedence(char op) { //คืนค่าลำดับความสำคัญของโอเปอเรเตอร์
        if (op == '+' || op == '-')
            return 1;
        if (op == '*' || op == '/')
            return 2;
        return 0;
    }

    public static int applyOp(int a, int b, char op) { //รับตัวเลขสองตัว a และ b กับเครื่องหมาย op แล้วคำนวณผล
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
                continue; //ถ้าเป็นช่องว่าง → ข้าม

            if (Character.isDigit(ch)) {
                int val = 0; //สร้างตัวแปร val เพื่อสะสมค่าตัวเลขนั้น
                while (i < expr.length() && Character.isDigit(expr.charAt(i))) {
                    //Character.isDigit(expr.charAt(i)) ตรวจว่ายังเป็นตัวเลขอยู่หรือไม่
                    //expr.charAt(i) คืนตัวอักษรที่ตำแหน่ง i
                    val = val * 10 + (expr.charAt(i) - '0'); //(expr.charAt(i) - '0') แปลงตัวอักษรให้เป็นค่าตัวเลขจริง
                    i++; //เลื่อนไปอ่านตัวอักษรถัดไป
                }
                values.push(val); //นำค่าตัวเลขที่ได้เก็บไว้ใน stack Values
                i--; //ลดค่า i ลง 1 เพราะลูป for จะเพิ่มค่า i ขึ้นอีก 1 ในรอบถัดไป
            } else if (ch == '(') {
                ops.push(ch); //ถ้าเป็นวงเล็บเปิด ให้เก็บไว้ใน stack ops
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') { //.peek() คืนค่าโอเปอเรเตอร์ตัวบนสุดของ stack ops โดยไม่ลบออก
                    int b = values.pop(); //นำค่าตัวเลขตัวบนสุดของ stack values ออกมา
                    int a = values.pop(); //นำค่าตัวเลขตัวถัดไปออกมา
                    values.push(applyOp(a, b, ops.pop())); //นำโอเปอเรเตอร์ตัวบนสุดของ stack ops ออกมาและคำนวณผลกับค่าตัวเลขที่นำออกมา แล้วเก็บผลลัพธ์ไว้ใน stack values
                }
                ops.pop(); // remove '('
            } else { // operator
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) { //ถ้า stack ops ไม่ว่างและโอเปอเรเตอร์ตัวบนสุดมีลำดับความสำคัญมากกว่าหรือเท่ากับโอเปอเรเตอร์ ch
                    //นำค่าตัวเลขสองตัวบนสุดของ stack values ออกมาและคำนวณผลลัพธ์ด้วยโอเปอเรเตอร์ตัวบนสุดของ stack ops
                    int b = values.pop();
                    int a = values.pop();
                    values.push(applyOp(a, b, ops.pop())); //นำผลลัพธ์ที่ได้เก็บไว้ใน stack values
                }
                ops.push(ch); //นำโอเปอเรเตอร์ ch เก็บไว้ใน stack ops
            }
        }

        while (!ops.isEmpty()) {
            int b = values.pop();
            int a = values.pop();
            values.push(applyOp(a, b, ops.pop())); //นำโอเปอเรเตอร์ตัวบนสุดของ stack ops ออกมาและคำนวณผลกับค่าตัวเลขที่นำออกมา แล้วเก็บผลลัพธ์ไว้ใน stack values
        }

        return values.pop(); //ผลลัพธ์สุดท้ายจะอยู่ที่ตัวบนสุดของ stack values
    }

    public static void main(String[] args) {
        String expr = "(1 + 2) * 3";
        System.out.println(expr + " = " + evaluate(expr));
    }
}
