import java.util.*;

public class BalancedBrackets { 
    public static boolean isBalanced(String str) { //เมธอดหลัก isBalanced คืนค่า true/false ว่าสมดุลไหม
        Stack<Character> stack = new Stack<>(); //สร้าง Stack<Character> สำหรับเก็บวงเล็บเปิดที่เจอ
        for (char ch: str.toCharArray()) { //วนลูปผ่านตัวอักษรในสตริง
            //.toCharArray() แปลงสตริงเป็นอาร์เรย์ของตัวอักษร
            if (ch == '(' || ch == '[' || ch == '{') { //ถ้าเป็น วงเล็บเปิด ให้ push ลงสแตก
                stack.push(ch);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                if (stack.isEmpty()) return false; //ถ้าสต็กว่าง หมายถึงมีปิดก่อนเปิด false ทันที
                char top = stack.pop(); //ไม่ว่าง ให้เอาของบนสุดออกมาตรวจ
                if ((ch == ')' && top != '(') ||
                    (ch == ']' && top != '[') ||
                    (ch == '}' && top != '{')) {
                    return false; //ตรวจว่าคู่ที่ pop ออกมาตรงกับชนิดวงเล็บปิดหรือไม่ ถ้าไม่ตรง → ลำดับการซ้อนผิด → false
                }
            }
        }
        return stack.isEmpty(); //หลังวนครบทุกตัวอักษร ถ้า สแตกยังไม่ว่าง แปลว่ายังมีวงเล็บเปิดที่ไม่ถูกปิด false ทันที
        //ถ้า สแตกว่าง แปลว่าทุกวงเล็บเปิดถูกปิดหมดแล้ว → true
    }

    public static void main(String[] args) {
        String input = "Hello, World!";
        System.out.println("The file is " + (isBalanced(input) ? "Balanced" : "Not Balanced"));
    }
}
