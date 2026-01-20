def greedy(
    grab_string, k
):  # ฟังก์ชัน greedy ที่รับ grab_string สตริงที่มีตัวอักษร G (Grab) และ P (Passenger)
    # และ k :ซึ่งเป็นระยะสูงสุดที่ Grab สามารถรับผู้โดยสารได้ เป็นพารามิเตอร์
    grabs = [i for i, c in enumerate(grab_string) if c == "G"] # ใช้ list comprehension เพื่อสร้างลิสต์ grabs ที่เก็บ ตำแหน่ง index ของตัวอักษร G
    passengers = [i for i, c in enumerate(grab_string) if c == "P"] # ใช้ list comprehension เพื่อสร้างลิสต์ passengers ที่เก็บ ตำแหน่ง index ของตัวอักษร P

    used = set() # เซ็ต used เพื่อเก็บ Passenger ที่ถูกใช้แล้ว
    count = 0 # ตัวแปร count เพื่อเก็บจำนวนผู้โดยสารที่สามารถรับได้

    for g in grabs: # วนลูปผ่าน Grab แต่ละคัน
        # หา Passenger ที่อยู่ในระยะ และยังไม่ถูกใช้
        candidates = [p for p in passengers if p not in used and abs(g - p) <= k] # ใช้ list comprehension เพื่อสร้างลิสต์ candidates ที่เก็บ Passenger ที่ยังไม่ถูกใช้ และอยู่ในระยะที่ Grab สามารถรับได้

        if candidates: 
            # เลือก Passenger ที่อยู่ซ้ายที่สุด
            chosen = min(candidates)
            used.add(chosen) # ทำเครื่องหมาย Passenger ว่าได้ถูกใช้แล้ว
            count += 1 # เพิ่มจำนวนผู้โดยสารที่รับได้

    return count # คืนค่าจำนวนผู้โดยสารสูงสุดที่สามารถรับได้


if __name__ == "__main__":
    with open("C:\\Users\\user\\Downloads\\2.1.3.txt") as f:
        arr = f.readline().strip()
        k = int(f.readline().strip())

    max_passengers = greedy(arr, k)  # เรียกใช้ฟังก์ชัน greedy กับข้อมูลที่อ่านมา
    print(max_passengers)  # แสดงผลจำนวนผู้โดยสารสูงสุดที่สามารถขึ้น Grab ได้ ด้วยวิธี Greedy
