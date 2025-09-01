from itertools import permutations # นำเข้า permutations จากไลบรารี itertools เพื่อใช้สำหรับสร้างชุด การเรียงลำดับที่เป็นไปได้ทั้งหมด ของ Passengers


def brute_force(grab_string, k): # ฟังก์ชัน brute_force ที่รับ grab_string สตริงที่มีตัวอักษร G (Grab) และ P (Passenger) 
    #และ k :ซึ่งเป็นระยะสูงสุดที่ Grab สามารถรับผู้โดยสารได้ เป็นพารามิเตอร์
    grabs = [i for i, c in enumerate(grab_string) if c == "G"] #ใช้ list comprehension เพื่อสร้างลิสต์ grabs ที่เก็บ ตำแหน่ง index ของตัวอักษร G
    passengers = [i for i, c in enumerate(grab_string) if c == "P"] #ใช้ list comprehension เพื่อสร้างลิสต์ passengers ที่เก็บ ตำแหน่ง index ของตัวอักษร P

    max_rides = 0 # ตัวแปร max_rides เพื่อเก็บจำนวนผู้โดยสารสูงสุดที่สามารถรับได้ โดยเริ่มต้นที่ 0
    solutions = set() #เก็บชุดของการจับคู่ (Grab–Passenger) ที่ทำให้ได้ max_rides

    # ลองทุกการเรียงลำดับผู้โดยสาร
    for perm in permutations(passengers, min(len(grabs), len(passengers))): #ใช้ permutations เพื่อสร้างการเรียงลำดับที่เป็นไปได้ทั้งหมด ของผู้โดยสาร โดยจำนวนผู้โดยสารที่พิจารณาจะถูกจำกัดโดยจำนวนของ Grab หรือ Passenger ที่มีอยู่
        count = 0 # ตัวแปร count เพื่อเก็บจำนวนผู้โดยสารที่สามารถรับได้ใน การเรียงลำดับปัจจุบัน
        pairs = [] #เก็บคู่ (grab, passenger) ที่จับคู่กัน
        for g, p in zip(grabs, perm): #เอา Grab แต่ละตัว (g) ไปจับคู่กับ Passenger (p) ตามลำดับที่ได้จาก perm
            if abs(g - p) <= k:  # ตรวจสอบว่าระยะห่างระหว่าง Grab และ Passenger ไม่เกิน k
                count += 1 #ถ้าใช่ เพิ่ม count ขึ้น 1
                pairs.append((g, p)) #เพิ่มคู่ (g, p) ลงในลิสต์ pairs
        if count > max_rides: #ถ้าจำนวนผู้โดยสารที่จับคู่ได้ใน การเรียงลำดับปัจจุบัน (count) มากกว่า max_rides ที่บันทึกไว้
            max_rides = count #อัปเดต max_rides เป็น count ใหม่
            solutions = {tuple(sorted(pairs))} #รีเซ็ตชุด solutions ให้เก็บเฉพาะชุดปัจจุบัน โดยใช้ tuple(sorted(pairs)) เพื่อให้แน่ใจว่าชุดของคู่ (grab, passenger) ถูกจัดเรียงในลำดับที่แน่นอน (ใช้ tuple(sorted(pairs)) เพื่อจัดลำดับคู่ให้ไม่ซ้ำ)
        elif count == max_rides: #ถ้า count เท่ากับ max_rides
            solutions.add(tuple(sorted(pairs))) #เพิ่ม solution นี้เข้าไปใน solutions

    print(len(solutions))  # จำนวนวิธีที่ทำให้ได้ผู้โดยสารสูงสุด
    print(max_rides)  # จำนวนผู้โดยสารสูงสุด
