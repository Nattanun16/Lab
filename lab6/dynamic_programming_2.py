import math

def dist(p1, p2):  # ใช้คำนวณระยะทางระหว่างจุด p1 และ p2
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])  # ใช้สูตร sqrt((x2 - x1)^2 + (y2 - y1)^2)

def cost(polygon, i, j, k):  # คำนวณเส้นรอบรูปของสามเหลี่ยมที่สร้างจากจุด i, j, k
    p1, p2, p3 = polygon[i], polygon[j], polygon[k]  # ดึงพิกัดของจุดทั้งสาม
    return dist(p1, p2) + dist(p2, p3) + dist(p3, p1) # ผลรวมของความยาวด้านทั้งสาม

def sort_polygon_points(points): # เรียงจุดพิกัดให้เป็น polygon ที่ถูกต้อง (ตามเข็มนาฬิกา)
    # คำนวณจุดศูนย์กลาง (centroid) ของจุดทั้งหมด
    cx = sum(p[0] for p in points) / len(points) # ค่า x เฉลี่ย
    cy = sum(p[1] for p in points) / len(points) # ค่า y เฉลี่ย

    # เรียงจุดตามมุม polar angle รอบ centroid (ตามเข็มนาฬิกา)
    def angle(p):
        return math.atan2(p[1] - cy, p[0] - cx) # คำนวณมุม polar angle โดยใช้มุม atan2() เพื่อหามุมของแต่ละจุดรอบจุดศูนย์กลาง
    return sorted(points, key=angle) # เรียงจุดตามมุมนั้น (จาก 0 องศาไป 360 องศา)

def triangulation(polygon, find_max=False):
    """
    Dynamic Programming หาค่า min/max triangulation cost
    """
    n = len(polygon) # จำนวนจุดใน polygon
    dp = [[0]*n for _ in range(n)] # ตาราง dp สำหรับเก็บค่า min/max cost ของ polygon ช่วง i ถึง j
    tri = [[-1]*n for _ in range(n)]  # เก็บจุดแบ่ง (k) ที่ให้ค่า min/max

    for l in range(3, n+1): # l = ความยาวของ polygon ที่กำลังพิจารณา (เริ่มจาก 3 จุดขึ้นไป)
        for i in range(n - l + 1): # i = จุดเริ่มต้นของ subpolygon โดย n-l+1 มีไว้เพื่อให้ไม่เกินขอบเขต
            j = i + l - 1 # j = จุดสิ้นสุดของ subpolygon และ i+l-1 = จำนวนจุด - 1
            dp[i][j] = float('-inf') if find_max else float('inf') # กำหนดค่าเริ่มต้นเป็น -inf สำหรับหา max และ inf สำหรับหา min
            for k in range(i+1, j):  # ทดลองแบ่ง polygon ที่ k ระหว่าง i กับ j
                val = dp[i][k] + dp[k][j] + cost(polygon, i, k, j) # ค่า cost ของสามเหลี่ยมที่สร้างจาก i, k, j
                if (find_max and val > dp[i][j]) or (not find_max and val < dp[i][j]): # อัพเดตค่า dp[i][j] ถ้าพบค่าใหม่ที่ดีกว่า
                    dp[i][j] = val # อัพเดตค่า dp[i][j]
                    tri[i][j] = k #เก็บค่า k ที่ใช้แบ่งนั้นไว้ใน tri[i][j] เพื่อไว้ reconstruct solution(ไล่ย้อนกลับเพื่อสร้างคำตอบจริง)

    # reconstruct solution  คือ ใช้ tri ที่เก็บจุดแบ่ง (k) มาไล่ย้อนดูว่า polygon ถูกแบ่งเป็นสามเหลี่ยมแบบไหนบ้าง
    solution = [] # เก็บผลลัพธ์ของการแบ่งสามเหลี่ยม
    def get_solution(i, j): # ฟังก์ชันช่วยในการสร้างคำตอบจริงโดยการไล่ย้อนกลับจาก tri
        if j <= i + 1: # ถ้า j <= i+1 หมายความว่า polygon มีจุดน้อยกว่า 3 จุด ไม่สามารถแบ่งได้
            return
        k = tri[i][j] # ดึงจุดแบ่ง k จาก tri
        if k == -1: # ถ้า k = -1 หมายความว่าไม่มีการแบ่ง
            return
        solution.append((i, k, j)) # เพิ่มสามเหลี่ยมที่สร้างจาก i, k, j ลงใน solution
        get_solution(i, k) # ไล่ย้อนกลับไปทางซ้าย
        get_solution(k, j) # ไล่ย้อนกลับไปทางขวา

    get_solution(0, n-1) # เริ่มไล่ย้อนกลับจาก polygon ทั้งหมด (0 ถึง n-1)
    return dp[0][n-1], solution # คืนค่าค่า min/max cost และ solution ที่ได้

def read_polygon_from_file(filename):  # อ่านพิกัดจุดจากไฟล์ Test Case
    polygon = [] # เก็บพิกัดจุดของ polygon
    with open(filename, 'r') as f:
        lines = f.readlines() # อ่านทุกบรรทัดในไฟล์
        n = int(lines[0].strip())  # บรรทัดแรก = จำนวนจุด
        for line in lines[1:n+1]:  # อ่านเฉพาะ n บรรทัดถัดไป
            parts = line.strip().split() # แยกพิกัด x, y
            if len(parts) == 2: # ถ้ามีพิกัดครบ 2 ค่า
                polygon.append((float(parts[0]), float(parts[1]))) # เพิ่มพิกัด (x, y) ลงในรายการ polygon

    # เรียงพิกัดให้เป็น polygon ที่ถูกต้องก่อนคำนวณ
    polygon = sort_polygon_points(polygon) # เรียงพิกัดให้เป็น polygon ที่ถูกต้อง
    return polygon # คืนค่ารายการพิกัดจุดของ polygon

def print_solution(polygon, triangles): # แสดงผลลัพธ์การแบ่งสามเหลี่ยม
    print("Triangulation:") 
    for (i, k, j) in triangles: # สำหรับแต่ละสามเหลี่ยมที่ได้จากการแบ่ง
        print(f"  Triangle: ({polygon[i]}, {polygon[k]}, {polygon[j]})") # แสดงพิกัดของสามเหลี่ยม

if __name__ == "__main__":
    filename = "C:\\Users\\user\\Downloads\\1.1.txt"
    polygon = read_polygon_from_file(filename)

    min_cost, min_sol = triangulation(polygon, find_max=False) # หา min triangulation
    max_cost, max_sol = triangulation(polygon, find_max=True) # หา max triangulation

    print(f"Minimum triangulation cost: {min_cost:.4f}")
    print_solution(polygon, min_sol) # แสดงผลลัพธ์การแบ่งสามเหลี่ยมสำหรับ min cost
    print("\n" + "-"*50)
    print(f"Maximum triangulation cost: {max_cost:.4f}")
    print_solution(polygon, max_sol) # แสดงผลลัพธ์การแบ่งสามเหลี่ยมสำหรับ max cost
