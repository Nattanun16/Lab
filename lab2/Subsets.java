
public class Subsets {
    public static void generateSubsets(int[] set) {
        int n = set.length;
        int total = 1 << n; // 2^n

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

    public static void main(String[] args) {
        int[] T = { 1, 2, 3 };
        generateSubsets(T);
    }
}