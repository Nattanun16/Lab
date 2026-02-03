import math
import matplotlib.pyplot as plt
import os


def dist(p1, p2): 
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def cost(polygon, i, j, k): # คำนวณเส้นรอบรูปของสามเหลี่ยมที่สร้างจากจุด i, j, k
    p1, p2, p3 = polygon[i], polygon[j], polygon[k] # ดึงพิกัดของจุดทั้งสาม
    return dist(p1, p2) + dist(p2, p3) + dist(p3, p1) # ผลรวมของความยาวด้านทั้งสาม


def sort_polygon_points(points):
    cx = sum(p[0] for p in points) / len(points) # ค่า x เฉลี่ย
    cy = sum(p[1] for p in points) / len(points) # ค่า y เฉลี่ย

    def angle(p):
        return math.atan2(p[1] - cy, p[0] - cx)

    return sorted(points, key=angle)


def triangulation(polygon, find_max=False):
    n = len(polygon)
    dp = [[0] * n for _ in range(n)]
    tri = [[-1] * n for _ in range(n)]

    for l in range(3, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float("-inf") if find_max else float("inf")
            for k in range(i + 1, j):
                val = dp[i][k] + dp[k][j] + cost(polygon, i, k, j)
                if (find_max and val > dp[i][j]) or (not find_max and val < dp[i][j]):
                    dp[i][j] = val
                    tri[i][j] = k

    solution = []

    def get_solution(i, j):
        if j <= i + 1:
            return
        k = tri[i][j]
        if k == -1:
            return
        solution.append((i, k, j))
        get_solution(i, k)
        get_solution(k, j)

    get_solution(0, n - 1)
    return dp[0][n - 1], solution


def read_polygon_from_file(filename):
    polygon = []
    if not os.path.exists(filename):
        print(f"Error: File not found at {filename}")
        return []

    with open(filename, "r") as f:
        lines = f.readlines()
        # บรรทัดแรกคือจำนวนจุด (n)
        try:
            n = int(lines[0].strip())
            # อ่านบรรทัดถัดไปตามจำนวน n
            for line in lines[1 : n + 1]:
                parts = line.strip().split()
                if len(parts) >= 2:
                    polygon.append((float(parts[0]), float(parts[1])))
        except ValueError:
            print("Error: Invalid file format.")
            return []

    # เรียงจุดให้ถูกต้องก่อนส่งกลับ
    return sort_polygon_points(polygon)



def visualize_results(polygon, min_sol, min_cost, max_sol, max_cost): # แสดงผลลัพธ์การแบ่งสามเหลี่ยมด้วยกราฟ
    # สร้างหน้าต่างกราฟ 1 แถว 2 คอลัมน์ (ซ้าย=Min, ขวา=Max)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6)) # ขนาดกราฟ

    titles = [f"Minimum Cost: {min_cost:.4f}", f"Maximum Cost: {max_cost:.4f}"]
    solutions = [min_sol, max_sol] # คำตอบทั้งสองแบบ

    for idx, ax in enumerate(axes): # วนลูปสร้างกราฟทั้งสอง
        sol = solutions[idx] # คำตอบที่ต้องการแสดงผล (min หรือ max)  

        # 1. วาดจุดและเส้นขอบของ Polygon (สีดำหนา)
        x_coords = [p[0] for p in polygon] + [polygon[0][0]]  # วนกลับมาจุดแรก
        y_coords = [p[1] for p in polygon] + [polygon[0][1]] # วนกลับมาจุดแรก
        ax.plot(
            x_coords, # พิกัด x
            y_coords, # พิกัด y
            "k-o", # สีดำ จุดกลม
            linewidth=2, # ความหนาเส้น
            markersize=8, # ขนาดจุด
            label="Polygon Boundary", # ชื่อเส้น
        )

        # ใส่ตัวเลขกำกับจุด (0, 1, 2, ...)
        for i, p in enumerate(polygon): # วนลูปแต่ละจุด
            ax.text(p[0], p[1] + 0.3, f"P{i}", fontsize=12, ha="center", color="blue") # แสดงตัวเลขกำกับจุด

        # 2. วาดเส้นแบ่งสามเหลี่ยม (สีแดงเส้นประ)
        # เราจะวาดสามเหลี่ยมทุกรูปที่ได้จากคำตอบ
        for i, j, k in sol: # สำหรับแต่ละสามเหลี่ยมที่ได้จากคำตอบ
            pts = [polygon[i], polygon[j], polygon[k], polygon[i]]  # จุด 3 จุดวนกลับมาที่เดิม
            tx = [p[0] for p in pts] # พิกัด x
            ty = [p[1] for p in pts] # พิกัด y
            ax.plot(tx, ty, "r--", alpha=0.7, linewidth=1)  # เส้นประสีแดง

        ax.set_title(titles[idx], fontsize=14, fontweight="bold") # ตั้งชื่อกราฟ
        ax.set_aspect("equal")  # ให้สัดส่วนภาพจริง
        ax.grid(True, linestyle=":", alpha=0.6) # เส้นตาราง

    plt.tight_layout() # จัดระยะกราฟให้พอดี
    plt.show() # แสดงกราฟ


# --- Main Program ---
if __name__ == "__main__":
    filename = "C:\\Users\\user\\Downloads\\1.1_ex.txt"

    print(f"Reading data from: {filename}")
    polygon = read_polygon_from_file(filename)

    if polygon:
        # คำนวณหาคำตอบ
        min_cost, min_sol = triangulation(polygon, find_max=False) # หา min triangulation
        max_cost, max_sol = triangulation(polygon, find_max=True) # หา max triangulation

        # แสดงผลตัวเลข
        print("-" * 30) # แยกผลลัพธ์
        print(f"Minimum Cost: {min_cost:.4f}")
        for i, k, j in min_sol: # สำหรับแต่ละสามเหลี่ยมที่ได้จากคำตอบ
            print(f"  Triangle: ({polygon[i]}, {polygon[k]}, {polygon[j]})") # แสดงพิกัดของสามเหลี่ยม

        print("-" * 30)
        print(f"Maximum Cost: {max_cost:.4f}")
        for i, k, j in max_sol: 
            print(f"  Triangle: ({polygon[i]}, {polygon[k]}, {polygon[j]})") 

        # วาดกราฟ
        print("-" * 30)
        print("Plotting results...")
        visualize_results(polygon, min_sol, min_cost, max_sol, max_cost) # แสดงผลลัพธ์การแบ่งสามเหลี่ยมด้วยกราฟ
    else:
        print("Failed to load polygon data.")
