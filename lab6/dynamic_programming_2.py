import math

def dist(p1, p2): #ใช้คำนวณระยะทางระหว่างจุด p1 และ p2
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1]) #ใช้สูตร ระยะทาง = sqrt((x2 - x1)^2 + (y2 - y1)^2)

def cost(polygon, i, j, k): #คำนวณเส้นรอบรูปของสามเหลี่ยมที่สร้างจากจุด i, j, k
    p1, p2, p3 = polygon[i], polygon[j], polygon[k] #ดึงพิกัดของจุดทั้งสาม
    return dist(p1, p2) + dist(p2, p3) + dist(p3, p1) #คืนค่าระยะทางรวมของสามเหลี่ยม = น้ำหนักของสามเหลี่ยมนั้น

def min_triangulation_cost(polygon): #หาค่าต่ำสุดของการแบ่งรูปหลายเหลี่ยมเป็นสามเหลี่ยมโดยใช้ Dynamic Programming
    n = len(polygon) #จำนวนจุดในรูปหลายเหลี่ยม
    dp = [[0] * n for _ in range(n)] #สร้างตาราง dp ขนาด n x n เพื่อเก็บค่าต่ำสุดของการแบ่งรูปหลายเหลี่ยม โดยเริ่มจากจุด i ถึง j และกำหนดค่าเริ่มต้นเป็น 0

    # l = ความยาวของ subpolygon (จำนวนจุด)
    for l in range(3, n + 1): #พิจารณาขนาดของ subpolygon ตั้งแต่ 3 ถึง n โดย l คือจำนวนจุดใน subpolygonท ที่ต้อง >= 3 ถึงจะสร้างสามเหลี่ยมได้
        for i in range(n - l + 1): #ลูปผ่านจุดเริ่มต้น i ของ subpolygon
            j = i + l - 1 #คำนวณจุดสิ้นสุด j ของ subpolygon
            dp[i][j] = float('inf') #กำหนดค่าเริ่มต้นเป็น infinity เพื่อหาค่าต่ำสุด
            for k in range(i + 1, j): #หาค่า minimu cost ของ subpolugon โดยแบ่ง polugon ที่อยู่ระหว่าง i ถึง j ด้วย k
                val = dp[i][k] + dp[k][j] + cost(polygon, i, k, j) #ส่วนซ้าย คือ dp[i][k] ส่วนขวา คือ dp[k][j] และส่วนกลาง คือ สามเหลี่ยม (i,j,k) แล้วเอาทั้งหมดมาบวกกัน
                if val < dp[i][j]: #ถ้าค่าที่คำนวณได้น้อยกว่าค่าปัจจุบันใน dp[i][j]
                    dp[i][j] = val #เก็บค่าทรี่เล็กที่สุดไว้ใน dp[i][j]

    return dp[0][n - 1] #คืนค่าค่าต่ำสุดของการแบ่งรูปหลายเหลี่ยมทั้งหมด (จากจุด 0 ถึง n-1)

def read_polygon_from_file(filename): #อ่านพิกัดจุดจากไฟล์
    polygon = [] #เก็บพิกัดจุดของรูปหลายเหลี่ยม
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split() #แยกพิกัด x และ y
            if len(parts) == 2: #ถ้ามีพิกัดครบทั้ง x และ y
                polygon.append((float(parts[0]), float(parts[1]))) #เพิ่มพิกัด (x, y) ลงในรายการ polygon
    return polygon #คืนค่ารายการพิกัดจุดของรูปหลายเหลี่ยม

if __name__ == "__main__":
    filename = "C:\\Users\\user\\Downloads\\Lab_6_Example.txt"  # ชื่อไฟล์เทสเคส
    polygon = read_polygon_from_file(filename)
    result = min_triangulation_cost(polygon)
    print(f"Minimum triangulation cost: {result:.4f}")
