import sys

INF = float("inf") # ค่าระยะทางเริ่มต้นที่ถือว่า “ไกลมาก” (ไม่มีเส้นทาง)


def solve():
    while True:
        line = sys.stdin.readline() # อ่านบรรทัดจากอินพุต
        if not line: # ถ้าไม่มีบรรทัดให้อ่าน (เช่น EOF) ให้หยุดการทำงานของลูป
            break 

        n, m, q = map(int, line.split()) # แยกตัวเลข n, m, q จากบรรทัดที่อ่านมาและแปลงเป็นจำนวนเต็ม

        # สร้าง matrix
        dist = [[INF] * (n + 1) for _ in range(n + 1)] # สร้างตารางระยะทางเริ่มต้นขนาด n x n โดยใช้ (n + 1) เพื่อให้ index เริ่มจาก 1 (เหมือนในโจทย์ที่นับจุดจาก 1 ถึง n)

        for i in range(1, n + 1): # ตั้งค่าระยะทางจากจุด i ไปยังตัวเองเป็น 0
            dist[i][i] = 0 # ระยะทางจากจุด i ไปยังตัวเองเป็น 0

        # รับ edges
        for _ in range(m):
            u, v, w = map(int, sys.stdin.readline().split())
            dist[u][v] = min(dist[u][v], w) # กรณีที่มีหลายเส้นทางระหว่าง u และ v ให้เก็บเฉพาะเส้นทางที่มีน้ำหนักน้อยที่สุด
            dist[v][u] = min(dist[v][u], w)  # graph นี้เป็น undirected

        # Floyd-Warshall (แบบ Min-Max)
        for k in range(1, n + 1): # วนผ่านทุกจุด k เป็นจุดกลางในการอัพเดตระยะทางระหว่างจุด i และ j
            for i in range(1, n + 1): # วนผ่านทุกจุด i เป็นจุดเริ่มต้น
                for j in range(1, n + 1): # วนผ่านทุกจุด j เป็นจุดปลายทาง
                    dist[i][j] = min(dist[i][j], max(dist[i][k], dist[k][j])) # อัพเดตระยะทางจาก i ไป j โดยพิจารณาเส้นทางผ่าน k ซึ่งจะใช้ค่า max ของ dist[i][k] และ dist[k][j] เพื่อหาค่า min ที่ดีที่สุดสำหรับ dist[i][j]

        # queries
        for _ in range(q): # วนผ่านทุก query เพื่ออ่านจุดเริ่มต้น s และจุดปลายทาง t
            s, t = map(int, sys.stdin.readline().split()) # อ่านจุดเริ่มต้น s และจุดปลายทาง t จากอินพุต
            if dist[s][t] == INF: # ถ้าระยะทางจาก s ไป t ยังคงเป็น INF แสดงว่าไม่มีเส้นทางเชื่อมต่อระหว่าง s และ t
                print("no path") # พิมพ์ "no path" เพื่อแสดงว่าไม่มีเส้นทางเชื่อมต่อระหว่าง s และ t
            else:
                print(dist[s][t]) # ถ้ามีเส้นทางเชื่อมต่อระหว่าง s และ t ให้พิมพ์ระยะทางที่คำนวณได้จากตาราง dist ซึ่งเป็นค่า min-max ที่ดีที่สุดสำหรับเส้นทางจาก s ไป t


if __name__ == "__main__":

    use_file = True  # เปลี่ยนเป็น False ถ้าจะพิมพ์เอง

    if use_file:
        try:
            with open("C:\\Users\\user\\Downloads\\10_example.txt", "r") as f:
                sys.stdin = f
                solve()
        except FileNotFoundError:
            print("ไม่พบไฟล์")
    else:
        solve()
