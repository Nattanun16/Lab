from itertools import permutations # นำเข้า permutations จากไลบรารี itertools เพื่อใช้สำหรับสร้างชุด การเรียงลำดับที่เป็นไปได้ทั้งหมด ของ Passengers


def brute_force(grab_string, k): # ฟังก์ชัน brute_force ที่รับ grab_string สตริงที่มีตัวอักษร G (Grab) และ P (Passenger) 
    #และ k :ซึ่งเป็นระยะสูงสุดที่ Grab สามารถรับผู้โดยสารได้ เป็นพารามิเตอร์
    n = len(arr)
    grabs = [i for i, c in enumerate(grab_string) if c == "G"] #ใช้ list comprehension เพื่อสร้างลิสต์ grabs ที่เก็บ ตำแหน่ง index ของตัวอักษร G
    passengers = [i for i, c in enumerate(grab_string) if c == "P"] #ใช้ list comprehension เพื่อสร้างลิสต์ passengers ที่เก็บ ตำแหน่ง index ของตัวอักษร P

    max_rides = 0 # ตัวแปร max_rides เพื่อเก็บจำนวนผู้โดยสารสูงสุดที่สามารถรับได้ โดยเริ่มต้นที่ 0
    solutions = set() #เก็บชุดของการจับคู่ (Grab–Passenger) ที่ทำให้ได้ max_rides

    # ลองทุกการเรียงลำดับผู้โดยสาร
    for perm in permutations(passengers, min(len(grabs), len(passengers))): #ใช้ permutations เพื่อสร้างการเรียงลำดับที่เป็นไปได้ทั้งหมด ของผู้โดยสาร โดยจำนวนผู้โดยสารที่พิจารณาจะถูกจำกัดโดยจำนวนของ Grab หรือ Passenger ที่มีอยู่
        used = set() #เก็บตำแหน่งของผู้โดยสารที่ถูกจับคู่แล้วใน การเรียงลำดับปัจจุบัน
        count = 0 # ตัวแปร count เพื่อเก็บจำนวนผู้โดยสารที่สามารถรับได้ใน การเรียงลำดับปัจจุบัน
        for g, p in zip(grabs, perm): #เอา Grab แต่ละตัว (g) ไปจับคู่กับ Passenger (p) ตามลำดับที่ได้จาก perm
            if abs(g - p) <= k:  # ตรวจสอบว่าระยะห่างระหว่าง Grab และ Passenger ไม่เกิน k
                count += 1 #ถ้าใช่ เพิ่ม count ขึ้น 1
                used.add(p) #บันทึกตำแหน่งของผู้โดยสารที่ถูกจับคู่แล้ว
        if count > max_rides: #ถ้าจำนวนผู้โดยสารที่จับคู่ได้ใน การเรียงลำดับปัจจุบัน (count) มากกว่า max_rides ที่บันทึกไว้
            max_rides = count #อัปเดต max_rides เป็น count ใหม่
            solutions = {perm} #รีเซ็ต solutions เป็นชุดใหม่ที่มีเพียง การเรียงลำดับปัจจุบัน (perm)
        elif count == max_rides: #ถ้า count เท่ากับ max_rides
            solutions.add(perm) #เพิ่ม การเรียงลำดับปัจจุบัน (perm) ลงในชุด solutions

    return len(solutions), max_rides #คืนค่าจำนวนชุดของการจับคู่ที่ทำให้ได้ max_rides และค่า max_rides
if __name__ == "__main__": #ถ้าไฟล์นี้ถูกเรียกใช้โดยตรง (ไม่ใช่การนำเข้าเป็นโมดูล)
    with open("C:\\Users\\user\\Downloads\\4.1.1.txt") as f: #เปิดไฟล์ที่มีข้อมูลอินพุต
        arr = f.readline().strip() #อ่านบรรทัดแรกของไฟล์และลบช่องว่างที่ไม่จำเป็นออก
        k = int(f.readline().strip()) #อ่านบรรทัดที่สองของไฟล์และแปลงเป็นจำนวนเต็ม

    num_solutions, max_passengers = brute_force(arr, k) #เรียกใช้ฟังก์ชัน brute_force กับข้อมูลที่อ่านมา
    print(num_solutions) #แสดงผลจำนวนชุดของการจับคู่ที่ทำให้ได้ max_rides
    print(max_passengers) #แสดงผลจำนวนผู้โดยสารสูงสุดที่สามารถขึ้น Grab ได้ ด้วยวิธี Brute-force
