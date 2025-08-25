import java.io.*;
import java.util.*;

class Node { //สร้าง class Node เก็บค่าของ expression tree
    String value;
    Node left, right;

    Node(String value) {
        this.value = value;
    }
}

public class ExpressionTreeLab3 {

    // ตรวจสอบว่าเป็น operator หรือไม่
    private static boolean isOperator(String s) { //ตรวจสอบว่าเป็น operator หรือไม่
        return "+-*/^".contains(s); // ถ้า s เป็นตัวใดตัวหนึ่งใน "+-*/^" จะคืนค่า true
    }

    // กำหนดลำดับความสำคัญ operator
    private static int precedence(String op) { // กำหนดลำดับความสำคัญของ operator
        return switch (op) {
            case "+", "-" -> 1; // + และ - มีลำดับความสำคัญต่ำสุด
            case "*", "/" -> 2; // * และ / มีลำดับความสำคัญสูงกว่า + และ -
            case "^" -> 3; // ^ มีลำดับความสำคัญสูงสุด
            default -> 0; // กรณีอื่นๆ คืนค่า 0
        };
    }

    // แปลง infix เป็น postfix (Shunting-yard algorithm)
    private static List<String> infixToPostfix(String expr) { //ใช้ stack และ list เก็บผลลัพธ์ postfix
        List<String> output = new ArrayList<>();
        Stack<String> stack = new Stack<>();
        String[] tokens = expr.replace("(", " ( ").replace(")", " ) ").trim().split("\\s+"); //แบ่ง expression ออกเป็น token โดยใช้เว้นวรรค

        for (String token : tokens) { 
            if (token.matches("\\d+")) { //ตรวจสอบว่า token เป็นตัวเลข
                output.add(token); //ถ้าเป็นตัวเลขให้เพิ่มลงใน output
            } else if (token.equals("(")) { //ถ้าเป็น ( ให้ push ลง stack
                stack.push(token);
            } else if (token.equals(")")) { //ถ้าเป็น ) ให้ pop จาก stack ไป output จนเจอ (
                while (!stack.isEmpty() && !stack.peek().equals("(")) { // pop จาก stack ไป output จนเจอ (
                    output.add(stack.pop()); // pop จาก stack แล้วเพิ่มลง output
                }
                stack.pop(); // ลบ (
            } else if (isOperator(token)) { //ถ้าเป็น operator
                while (!stack.isEmpty() && !stack.peek().equals("(") && // pop จาก stack ไป output จนเจอ ( หรือ operator ที่มีลำดับความสำคัญต่ำกว่า
                        precedence(stack.peek()) >= precedence(token)) { //ถ้า operator บน stack มีลำดับความสำคัญมากกว่าหรือเท่ากับ token ปัจจุบัน
                    output.add(stack.pop()); // pop จาก stack แล้วเพิ่มลง output
                }
                stack.push(token); // push operator ปัจจุบันลง stack
            }
        }
        while (!stack.isEmpty()) { // pop เครื่องหมายที่เหลือใน stack ไป output
            output.add(stack.pop()); // pop จาก stack แล้วเพิ่มลง output
        }
        return output;
    }

    // สร้าง Expression Tree จาก postfix
    private static Node constructTree(List<String> postfix) { //ประเมินค่า postfix
        Stack<Node> stack = new Stack<>(); //ใช้ stack เก็บ node ของ tree
        for (String token : postfix) { //วนลูปแต่ละ token ใน postfix
            if (!isOperator(token)) { //ถ้า token เป็นตัวเลข
                stack.push(new Node(token)); //สร้าง node ใหม่แล้ว push ลง stack
            } else { //ถ้า token เป็น operator
                Node right = stack.pop(); //pop สอง node จาก stack (ขวาก่อนซ้าย)
                Node left = stack.pop(); //pop สอง node จาก stack (ขวาก่อนซ้าย)
                Node node = new Node(token); //สร้าง node ใหม่สำหรับ operator
                node.left = left; //กำหนดลูกซ้าย
                node.right = right; //กำหนดลูกขวา
                stack.push(node); //push node ใหม่ลง stack
            }
        }
        return stack.pop(); //node สุดท้ายใน stack คือ root ของ tree
    }

    // Traversals
    private static void inorder(Node root, List<String> result) { //ใช้ recursion เดิน tree แล้วเพิ่มค่าใน list result
        if (root != null) { // base case
            inorder(root.left, result); // เดินลูกซ้าย
            result.add(root.value); // เพิ่มค่าของ root ลงใน result
            inorder(root.right, result); // เดินลูกขวา
        }
    }

    private static void preorder(Node root, List<String> result) { //ใช้ recursion เดิน tree แล้วเพิ่มค่าใน list result
        if (root != null) { // base case
            result.add(root.value); // เพิ่มค่าของ root ลงใน result
            preorder(root.left, result); // เดินลูกซ้าย
            preorder(root.right, result); // เดินลูกขวา
        }
    }

    private static void postorder(Node root, List<String> result) { //ใช้ recursion เดิน tree แล้วเพิ่มค่าใน list result
        if (root != null) { // base case
            postorder(root.left, result); // เดินลูกซ้าย
            postorder(root.right, result);  // เดินลูกขวา
            result.add(root.value); // เพิ่มค่าของ root ลงใน result
        }
    }

    // ประเมินค่าจาก postfix
    private static double evaluatePostfix(List<String> postfix) { //ใช้ stack ประเมินค่าจาก postfix: ถ้าเจอเลข push, เจอ operator pop 2 ค่า แล้วคำนวณ
        Stack<Double> stack = new Stack<>(); //ใช้ stack เก็บค่าชั่วคราว
        for (String token : postfix) { //วนลูปแต่ละ token ใน postfix
            if (!isOperator(token)) { //ถ้า token เป็นตัวเลข
                stack.push(Double.valueOf(token)); //แปลงเป็น double แล้ว push ลง stack
            } else { //ถ้า token เป็น operator
                double b = stack.pop(); //pop สองค่า (ขวาก่อนซ้าย)
                double a = stack.pop(); //pop สองค่า (ขวาก่อนซ้าย)
                switch (token) { //คำนวณตาม operator แล้ว push ผลลัพธ์ลง stack
                    case "+" -> stack.push(a + b); //ถ้าเป็น + ให้บวก a กับ b แล้ว push ผลลัพธ์ลง stack
                    case "-" -> stack.push(a - b); //ถ้าเป็น - ให้ลบ a กับ b แล้ว push ผลลัพธ์ลง stack
                    case "*" -> stack.push(a * b);
                    case "/" -> stack.push(a / b);
                    case "^" -> stack.push(Math.pow(a, b)); //ใช้ Math.pow สำหรับยกกำลัง
                }
            }
        }
        return stack.pop(); //ค่าที่เหลือใน stack คือผลลัพธ์สุดท้าย
    }

    public static void main(String[] args) { 
        String inputFile = "C:\\Users\\user\\Downloads\\Lab_3 example.txt"; // หรือกำหนด path เต็ม
        try (BufferedReader br = new BufferedReader(new FileReader(inputFile))) { //อ่านไฟล์
            String expr; //เก็บ expression แต่ละบรรทัด
            while ((expr = br.readLine()) != null) { //อ่านทีละบรรทัดจนกว่าจะหมดไฟล์
                expr = expr.trim(); //ลบช่องว่างข้างหน้าและข้างหลัง
                if (expr.isEmpty()) //ข้ามบรรทัดว่าง
                    continue;

                List<String> postfix = infixToPostfix(expr); //แปลง infix เป็น postfix
                Node tree = constructTree(postfix); //สร้าง expression tree จาก postfix

                List<String> in = new ArrayList<>(); //เก็บผลลัพธ์ inorder
                List<String> pre = new ArrayList<>(); //เก็บผลลัพธ์ preorder
                List<String> post = new ArrayList<>(); //เก็บผลลัพธ์ postorder
                inorder(tree, in); //เรียก inorder
                preorder(tree, pre); //เรียก preorder
                postorder(tree, post); //เรียก postorder

                System.out.println("Expression: " + expr);
                System.out.println("Inorder: " + String.join(" ", in)); //แสดงผลลัพธ์ inorder โดยใช้ String.join เพื่อรวม list เป็น string เดียวโดยมีช่องว่างคั่น
                System.out.println("Preorder: " + String.join(" ", pre)); //แสดงผลลัพธ์ preorder โดยใช้ String.join เพื่อรวม list เป็น string เดียวโดยมีช่องว่างคั่น
                System.out.println("Postorder: " + String.join(" ", post)); //แสดงผลลัพธ์ postorder โดยใช้ String.join เพื่อรวม list เป็น string เดียวโดยมีช่องว่างคั่น
                System.out.println("Result: "
                        + (evaluatePostfix(post) % 1 == 0 ? (int) evaluatePostfix(post) : evaluatePostfix(post))); //แสดงผลลัพธ์การประเมินค่า โดยตรวจสอบว่าผลลัพธ์เป็นจำนวนเต็มหรือไม่ ถ้าใช่ให้แสดงเป็น integer
                System.out.println("------"); //คั่นระหว่าง expression แต่ละบรรทัด
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage()); //แสดงข้อความผิดพลาดถ้าอ่านไฟล์ไม่ได้
        }
    }
}
