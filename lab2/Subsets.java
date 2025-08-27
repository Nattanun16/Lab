import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Subsets {
    // สำหรับเซตของจำนวนเต็ม (เช่น {1,2,3})
    public static void generateSubsets(int[] set) {
        int n = set.length;
        int total = 1 << n;
        for (int i = 0; i < total; i++) {
            StringBuilder sb = new StringBuilder();
            sb.append("{");
            boolean first = true;
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) > 0) {
                    if (!first)
                        sb.append(" ");
                    sb.append(set[j]);
                    first = false;
                }
            }
            sb.append("}");
            System.out.println(sb.toString());
        }
        // **ตัดส่วนพิมพ์ singleton sets ออก** ตามที่คุณไม่ต้องการ
    }

    // สำหรับเซตที่สมาชิกเป็นเซตย่อย (เช่น { {1}, {2}, {3} })
    public static void generateSubsetsOfTokens(String[] tokens) {
        int n = tokens.length;
        int total = 1 << n;
        for (int i = 0; i < total; i++) {
            StringBuilder sb = new StringBuilder();
            sb.append("{");
            boolean first = true;
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) > 0) {
                    if (!first)
                        sb.append(",");
                    sb.append(tokens[j]); // เช่น "{1}"
                    first = false;
                }
            }
            sb.append("}");
            System.out.println(sb.toString());
        }
    }

    private static boolean isSetOfSingletonSets(String line) {
        String s = line.replaceAll("\\s+", "");
        return s.matches("\\{(\\{[-]?\\d+})(,\\{[-]?\\d+})*}");
    }

    public static void main(String[] args) throws FileNotFoundException {
        try (Scanner sc = new Scanner(new File("C:\\Users\\user\\Downloads\\SetT.txt"))) {
            while (sc.hasNextLine()) {
                String line = sc.nextLine().trim();
                if (line.equals("{}") || line.isEmpty()) {
                    System.out.println("Subsets of {}:");
                    generateSubsets(new int[0]);
                    continue;
                }

                // กรณีเป็นเซตของเซต เช่น {{1},{2},{3}}
                if (isSetOfSingletonSets(line)) {
                    Pattern p = Pattern.compile("\\{\\s*(-?\\d+)\\s*\\}");
                    Matcher m = p.matcher(line);
                    List<String> tokens = new ArrayList<>();
                    while (m.find()) {
                        String num = m.group(1).trim();
                        tokens.add("{" + num + "}");
                    }
                    System.out.println("Subsets of " + line + " :");
                    generateSubsetsOfTokens(tokens.toArray(new String[0]));
                    continue;
                }

                // กรณีปกติ: {1,2,3} → parse เป็น int[]
                String cleaned = line.replaceAll("[{}]", "");
                if (cleaned.isEmpty())
                    continue;

                String[] parts = cleaned.split(",");
                int[] arr = new int[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    arr[i] = Integer.parseInt(parts[i].trim());
                }

                System.out.println("Subsets of {" + String.join(",", parts) + "} :");
                generateSubsets(arr);
            }
        }
    }
}
