import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Subsets {
    public static void generateSubsets(int[] set) { //ถ้า set มี n ตัว → จะมี subset ทั้งหมด 2^n แบบ
        int n = set.length;
        int total = 1 << n;
        for (int i = 0; i < total; i++) {
            //ใช้ค่า i เป็นตัวแทน subset
            StringBuilder sb = new StringBuilder();
            sb.append("{");
            boolean first = true;
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) > 0) { //ถ้า bit ตำแหน่ง j ของ i เป็น 1 → เอา set[j] มาใส่ใน subset
                    if (!first)
                        sb.append(" ");
                    sb.append(set[j]);
                    first = false;
                }
            }
            sb.append("}");
            System.out.println(sb.toString());
        }

        // กรณีพิเศษ: พิมพ์ singleton sets ในรูปแบบ {{1},{2},...}
        if (n > 0) { //ถ้า set ไม่ว่าง → สร้าง output แบบ singleton sets เช่น ถ้า {1,2,3} → ได้ {{1},{2},{3}} และใช้ , คั่นระหว่างแต่ละ subset
            StringBuilder singles = new StringBuilder();
            singles.append("{");
            for (int i = 0; i < n; i++) {
                singles.append("{").append(set[i]).append("}");
                if (i < n - 1)
                    singles.append(",");
            }
            singles.append("}");
            System.out.println(singles.toString());
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\SetT.txt")); //เปิดไฟล์เพื่ออ่านชุดข้อมูล
        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (line.equals("{}") || line.isEmpty()) { //ถ้าเป็น {} หรือบรรทัดว่าง → แสดงว่าไม่มีชุดข้อมูล ให้แสดงผล subset ของ empty set
                System.out.println("Subsets of {}:");
                generateSubsets(new int[0]);
                continue;
            }

            // ลบ { และ }
            line = line.replaceAll("[{}]", ""); //กรณี input มี element
            if (line.isEmpty())
                continue;

            String[] parts = line.split(",");
            int[] arr = new int[parts.length];
            for (int i = 0; i < parts.length; i++) {
                arr[i] = Integer.parseInt(parts[i].trim());
            } //ตัด { และ } ออก split ด้วย , แล้วแปลงเป็น int[]

            System.out.println("Subsets of {" + String.join(",", parts) + "} :");
            generateSubsets(arr);
        }
        sc.close();
    }
}