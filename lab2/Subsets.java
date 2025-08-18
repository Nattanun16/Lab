
public class Subsets {
    public static void generateSubsets(int[] set) {
        int n = set.length; // จำนวนสมาชิกในเซต
        long total = 1 << n; // เลื่อนบิตของเลข 1 ไปซ้าย n ตำแหน่ง (2^n) 

        for (int i = 0; i < total; i++) { 
            //i ทำหน้าที่เป็น ตัวเลขมาสก์บิต (bitmask)
            //total = 1 << n = 2^n → มีทั้งหมด 2^n รอบ
            //i ไล่ตั้งแต่ 0 ถึง 2^n - 1
            //แต่ละค่า i แทนชุดย่อยหนึ่งชุด
            System.out.print("{ ");
            for (int j = 0; j < n; j++) {
                //ใช้ j ไล่สมาชิกของ array set
                //j หมายถึง index ของสมาชิก เช่น j=0 หมายถึง set[0]
                if ((i & (1 << j)) > 0) { //1 << j คือการเลื่อนบิต 1 ไปที่ตำแหน่ง j แล้วทำ AND กับ i
                    //ถ้า i & (1 << j) > 0 แสดงว่า bit ที่ตำแหน่ง j ใน i เป็น 1
                    System.out.print(set[j] + " "); //ถ้าเป็นจริง แสดงว่า set[j] เป็นสมาชิกของชุดย่อยนี้ พิม์พ์สมาชิกนั้น
                }
            }
            System.out.println("}");
        }
    }

    public static void main(String[] args) {
        int[] T = { 1, 2, 3 };
        generateSubsets(T);
    }
}