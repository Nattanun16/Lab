import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Subsets {
    public static void generateSubsets(int[] set) {
        int n = set.length;
        int total = 1 << n;
        for (int i = 0; i < total; i++) {
            System.out.print("{ ");
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) > 0) {
                    System.out.print(set[j] + " ");
                }
            }
            System.out.println("}");
        }
    }

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(new File("test_set.txt"));
        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (line.equals("{}") || line.isEmpty()) {
                System.out.println("Subsets of {}:");
                generateSubsets(new int[0]);
                continue;
            }

            // ลบ { และ }
            line = line.replaceAll("[{}]", "");
            if (line.isEmpty()) continue;

            String[] parts = line.split(",");
            int[] arr = new int[parts.length];
            for (int i = 0; i < parts.length; i++) {
                arr[i] = Integer.parseInt(parts[i].trim());
            }

            System.out.println("Subsets of {" + String.join(",", parts) + "} :");
            generateSubsets(arr);
        }
        sc.close();
    }
}