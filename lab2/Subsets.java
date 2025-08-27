import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
 //ใช้ Array กับ ArrayList
public class Subsets {
    // สำหรับเซตของจำนวนเต็ม (เช่น {1,2,3})
    public static void generateSubsets(int[] set) { // รับ array ของจำนวนเต็ม
        int n = set.length; // จำนวนสมาชิกในเซต
        int total = 1 << n; // 2^n เซตย่อย
        for (int i = 0; i < total; i++) { // สำหรับแต่ละเซตย่อย
            StringBuilder sb = new StringBuilder(); // สร้างสตริงสำหรับเซตย่อย
            sb.append("{"); // เริ่มต้นด้วย {
            boolean first = true; // ตัวแปรช่วยจัดการคั่น
            for (int j = 0; j < n; j++) { // สำหรับแต่ละสมาชิก
                if ((i & (1 << j)) > 0) { // ถ้าสมาชิก j อยู่ในเซตย่อยนี้
                    if (!first) // ถ้าไม่ใช่ตัวแรก ให้คั่นด้วยช่องว่าง
                        sb.append(" "); // คั่นด้วยช่องว่าง
                    sb.append(set[j]); // เพิ่มสมาชิก
                    first = false; // เปลี่ยนสถานะว่าไม่ใช่ตัวแรกแล้ว
                }
            }
            sb.append("}"); // ปิดท้ายด้วย }
            System.out.println(sb.toString()); // พิมพ์ผลลัพธ์
        }
        // **ตัดส่วนพิมพ์ singleton sets ออก** ตามที่คุณไม่ต้องการ
    }

    // สำหรับเซตที่สมาชิกเป็นเซตย่อย (เช่น { {1}, {2}, {3} })
    public static void generateSubsetsOfTokens(String[] tokens) { // รับ array ของสตริง
        int n = tokens.length; // number of elements
        int total = 1 << n; // 2^n subsets
        for (int i = 0; i < total; i++) {  // for each subset
            StringBuilder sb = new StringBuilder(); // build subset string
            sb.append("{"); // เริ่มต้นด้วย {
            boolean first = true; // ตัวแปรช่วยจัดการคั่น
            for (int j = 0; j < n; j++) { // for each element
                if ((i & (1 << j)) > 0) { // ถ้า element j อยู่ใน subset นี้
                    if (!first) // คั่นด้วยช่องว่าง
                        sb.append(","); // คั่นด้วย ,
                    sb.append(tokens[j]); // เช่น "{1}"
                    first = false; // เปลี่ยนสถานะว่าไม่ใช่ตัวแรกแล้ว
                }
            }
            sb.append("}"); // ปิดท้ายด้วย }
            System.out.println(sb.toString()); //   พิมพ์ผลลัพธ์
        }
    }

    private static boolean isSetOfSingletonSets(String line) { // ตรวจสอบรูปแบบ {{1},{2},{3}}
        String s = line.replaceAll("\\s+", ""); // ลบช่องว่างทั้งหมด
        return s.matches("\\{(\\{[-]?\\d+})(,\\{[-]?\\d+})*}"); // ตรวจสอบรูปแบบ
    }

    public static void main(String[] args) throws FileNotFoundException { // อ่านไฟล์ SetT.txt
        try (Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\SetT.txt"))) { 
            while (sc.hasNextLine()) { // อ่านทีละบรรทัด
                String line = sc.nextLine().trim(); // อ่านบรรทัดปัจจุบันและตัดช่องว่างข้างหน้า-หลัง
                if (line.equals("{}") || line.isEmpty()) { // กรณีเซตว่าง {}
                    System.out.println("Subsets of {}:"); // พิมพ์หัวข้อ
                    generateSubsets(new int[0]); // พิมพ์เซตว่าง
                    continue; // ข้ามไปบรรทัดถัดไป
                }

                // กรณีเป็นเซตของเซต เช่น {{1},{2},{3}}
                if (isSetOfSingletonSets(line)) { // ตรวจสอบรูปแบบ
                    Pattern p = Pattern.compile("\\{\\s*(-?\\d+)\\s*\\}"); // รูปแบบ {number}
                    Matcher m = p.matcher(line); // สร้าง matcher
                    List<String> tokens = new ArrayList<>(); // เก็บสมาชิกแต่ละตัว
                    while (m.find()) { // หา match
                        String num = m.group(1).trim(); // ดึงตัวเลขออกมา
                        tokens.add("{" + num + "}"); // เก็บในรูปแบบ "{number"
                    }
                    System.out.println("Subsets of " + line + " :"); // พิมพ์หัวข้อ
                    generateSubsetsOfTokens(tokens.toArray(String[]::new)); // พิมพ์เซตย่อย
                    continue; // ข้ามไปบรรทัดถัดไป
                }

                // กรณีปกติ: {1,2,3} → parse เป็น int[]
                String cleaned = line.replaceAll("[{}]", ""); // ลบ {, }
                if (cleaned.isEmpty()) // เซตว่าง
                    continue; // ข้ามไปบรรทัดถัดไป

                String[] parts = cleaned.split(","); // แยกด้วย ,
                int[] arr = new int[parts.length]; // สร้าง array
                for (int i = 0; i < parts.length; i++) { // แปลงเป็น int
                    arr[i] = Integer.parseInt(parts[i].trim()); // แปลงเป็น int
                }

                System.out.println("Subsets of {" + String.join(",", parts) + "} :"); // พิมพ์หัวข้อ
                generateSubsets(arr); // พิมพ์เซตย่อย
            }
        }
    }
}
