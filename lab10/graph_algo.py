#!/usr/bin/env python3
import sys


def main():
    data = input().strip().split()  # อ่านข้อมูลทั้งหมดจาก stdin
    if not data:  # ถ้าไม่มี Data ให้หยุดทำงาน
        return
    it = iter(data)  # สร้าง iterator จากลิสต์ เพื่อใช้ next(it) ดึงค่าทีละตัว
    try:
        n = int(next(it))  # จำนวนโหนด(จำนวนจุด)
        E = int(next(it))  # จำนวนเส้นเชื่อม (edges)
        k = int(next(it))  # จำนวนคู่จุดที่ต้องตอบคำถาม
    except StopIteration:  # ถ้าไม่มีข้อมูลเพียงพอ ให้หยุดทำงาน(Input ไม่ครบ)
        return

    INF = 10**15  # ค่าระยะทางเริ่มต้นที่ถือว่า “ไกลมาก” (ไม่มีเส้นทาง)
    # 1-based indexing
    dist = [
        [INF] * (n + 1) for _ in range(n + 1)
    ]  # สร้างตารางระยะทางเริ่มต้นขนาด n x n โดยใช้ (n + 1) เพื่อให้ index เริ่มจาก 1 (เหมือนในโจทย์ที่นับจุดจาก 1 ถึง n)
    for i in range(1, n + 1):  # ตั้งค่า dist[i][i] = 0 เพราะระยะทางจากจุดหนึ่งถึงตัวมันเองเป็น 0
        dist[i][i] = 0

    for _ in range(E):  # อ่านข้อมูลเส้นเชื่อมทั้งหมด
        try:
            u = int(next(it))  # จุดเริ่มต้นของเส้นเชื่อม
            v = int(next(it))  # จุดปลายทางของเส้นเชื่อม
            w = int(next(it))  # น้ำหนัก (cost) ของเส้นเชื่อม(ระดับเสียง)
        except StopIteration:  # ถ้าไม่มีข้อมูลเพียงพอ ให้หยุดทำงาน(Input ไม่ครบ)
            break
        # undirected graph (ตามตัวอย่าง) — ถ้าเป็น directed ให้ลบบรรทัดที่ mirror ออก
        if w < dist[u][v]:  # ตรวจว่า w น้อยกว่าค่าที่มีอยู่เดิมไหม (ป้องกันข้อมูลซ้ำ)
            dist[u][v] = w  # อัพเดตระยะทางจาก u ไป v (เนื่องจากเป็นกราฟไม่มีทิศทาง)
            dist[v][u] = w  # อัพเดตระยะทางจาก v ไป u (เนื่องจากเป็นกราฟไม่มีทิศทาง)

    # Floyd–Warshall แบบ minimax
    for mid in range(1, n + 1):  # วนทุกจุด mid เพื่อพิจารณาเป็น จุดผ่านกลาง (intermediate node)
        for i in range(1, n + 1): # วนทุกจุด i
            if dist[i][mid] == INF:
                continue # ถ้าไม่มีทางไป mid ให้ข้าม
            for j in range(1, n + 1): # วนทุกจุด j
                if dist[mid][j] == INF:
                    continue # ถ้าไม่มีทางจาก mid ไป j ให้ข้าม
                # cost of path i -...- mid -...- j is max(dist[i][mid], dist[mid][j])
                via = max(dist[i][mid], dist[mid][j]) # คำนวณค่าสูงสุดของเส้นทางผ่าน mid
                if via < dist[i][j]: # ถ้าค่าที่คำนวณได้น้อยกว่าค่าที่มีอยู่เดิม
                    dist[i][j] = via # อัพเดตระยะทางจาก i ไป j

    out_lines = [] # เก็บผลลัพธ์การตอบคำถาม
    for _ in range(k): # อ่านคำถาม k คู่
        try:
            a = int(next(it)) # จุดเริ่มต้น
            b = int(next(it)) # จุดปลายทาง
        except StopIteration: # ถ้าไม่มีข้อมูลเพียงพอ ให้หยุดทำงาน(Input ไม่ครบ)
            break
        if dist[a][b] == INF: # ถ้าไม่มีเส้นทางจาก a ไป b
            out_lines.append("no path") # บันทึกผลลัพธ์ว่าไม่มีเส้นทาง
        else:
            out_lines.append(str(dist[a][b])) # บันทึกผลลัพธ์เป็นค่าระยะทางที่น้อยที่สุด

    sys.stdout.write("\n".join(out_lines)) # แสดงผลลัพธ์ทั้งหมดในครั้งเดียว


if __name__ == "__main__":
    main()
