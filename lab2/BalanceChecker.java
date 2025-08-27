import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Stack;

public class BalanceChecker { // ตรวจสอบความสมดุลของวงเล็บในโค้ด Python
    public static boolean isBalanced(String code) { // รับสตริงโค้ด Python
        Stack<Character> stack = new Stack<>(); // สแต็กสำหรับเก็บวงเล็บเปิด
        String opening = "([{"; // วงเล็บเปิด
        String closing = ")]}"; // วงเล็บปิด

        for (int i = 0; i < code.length(); i++) { // วนลูปตรวจสอบตัวอักษรในโค้ด
            char c = code.charAt(i); // ตัวอักษรปัจจุบัน

            // ----- ข้ามคอมเมนต์ (# ทั้งบรรทัด) -----
            if (c == '#') { // ข้ามไปจนถึงจบบรรทัด
                while (i < code.length() && code.charAt(i) != '\n') { // จนกว่าจะเจอบรรทัดใหม่
                    i++; // ข้ามตัวอักษร
                }
                continue; // ข้ามไปตรวจสอบตัวถัดไป
            }

            // ----- ข้ามสตริง -----
            if (c == '"' || c == '\'') { // ข้ามไปจนกว่าจะเจอเครื่องหมายปิดสตริง
                char quote = c; // จำเครื่องหมายเปิดสตริง
                i++; // ข้ามเครื่องหมายเปิดสตริง
                while (i < code.length()) { // วนลูปจนกว่าจะเจอเครื่องหมายปิดสตริง
                    if (code.charAt(i) == quote && code.charAt(i - 1) != '\\') { // เจอเครื่องหมายปิดสตริงที่ไม่ใช่ \"
                        break; // ออกจากลูป
                    }
                    i++; // ข้ามตัวอักษรในสตริง
                }
                continue; // ข้ามไปตรวจสอบตัวถัดไป
            }

            // ----- เช็ควงเล็บ -----
            if (opening.indexOf(c) != -1) { // ถ้าเป็นวงเล็บเปิด
                stack.push(c); // เก็บลงสแต็ก
            } else if (closing.indexOf(c) != -1) { // ถ้าเป็นวงเล็บปิด
                if (stack.isEmpty()) return false; // ถ้าสแต็กว่าง แสดงว่าไม่สมดุล
                char top = stack.pop(); // เอาวงเล็บเปิดสุดท้ายออกจากสแต็ก
                if (!matches(top, c)) return false; // ถ้าไม่ตรงกัน แสดงว่าไม่สมดุล
            }
        }
        return stack.isEmpty(); // ถ้าสแต็กว่าง แสดงว่าสมดุล
    }

    private static boolean matches(char open, char close) { // ตรวจสอบว่าคู่วงเล็บตรงกันหรือไม่
        return (open == '(' && close == ')') || // ตรงกันถ้าเป็น (), [], {}
               (open == '[' && close == ']') || // ตรงกันถ้าเป็น (), [], {}
               (open == '{' && close == '}'); // ตรงกันถ้าเป็น (), [], {}
    }

    public static void main(String[] args) { 
        // <<< แก้ตรงนี้เพื่อเปลี่ยนชื่อไฟล์ที่ต้องการรัน >>>
        String filename = "C:\\Users\\user\\Downloads\\test10.py";

        StringBuilder code = new StringBuilder(); // เก็บโค้ดจากไฟล์
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) { // อ่านไฟล์
            String line; // ตัวแปรเก็บบรรทัดปัจจุบัน
            while ((line = br.readLine()) != null) { // อ่านทีละบรรทัด
                code.append(line).append("\n"); // เพิ่มบรรทัดลงในโค้ด
            }
        } catch (IOException e) { // จัดการข้อผิดพลาดในการอ่านไฟล์
            System.out.println("Error reading file: " + e.getMessage()); // แสดงข้อความผิดพลาด
            return; // ออกจากโปรแกรม
        }

        if (isBalanced(code.toString())) { // ตรวจสอบความสมดุลของวงเล็บ
            System.out.println("The file is balanced."); // แสดงผลถ้าสมดุล
        } else { // ถ้าไม่สมดุล
            System.out.println("The file is NOT balanced."); // แสดงผลถ้าไม่สมดุล
        }
    }
}