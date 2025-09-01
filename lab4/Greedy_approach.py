def greedy(
    grab_string, k
):  # ฟังก์ชัน greedy ที่รับ grab_string สตริงที่มีตัวอักษร G (Grab) และ P (Passenger)
    # และ k :ซึ่งเป็นระยะสูงสุดที่ Grab สามารถรับผู้โดยสารได้ เป็นพารามิเตอร์
    grab_string = list(grab_string)  # แปลงสตริงเป็นลิสต์เพื่อให้ง่ายต่อการจัดการ
    n = len(grab_string)  # หาความยาวของลิสต์
    max_rides = 0  # ตัวแปร max_rides เพื่อเก็บจำนวนผู้โดยสารสูงสุดที่สามารถรับได้ โดยเริ่มต้นที่ 0

    for i in range(n):  # วนลูป ทุกตำแหน่งใน string (index 0 ถึง n-1)
        if (
            grab_string[i] == "G"
        ):  # ถ้าพบผู้โดยสารที่ตำแหน่ง i
            for j in range(
                max(0, i - k), min(n, i + k + 1)
            ):  # พยายามหาผู้โดยสารในช่วง [i-k, i+k] โดย max(0, i-k) เพื่อไม่ให้ออกนอกขอบเขตด้านซ้าย (index < 0) และ min(n, i+k+1) เพื่อไม่ให้ออกนอกขอบเขตด้านขวา (index >= n)
                if grab_string[j] == "P":  # ถ้าพบผู้โดยสารในช่วงที่กำหนด
                    max_rides += 1 # เพิ่ม count ขึ้น 1
                    grab_string[j] = "X"  # ใช้ Grab ไปแล้ว
                    break  # ออกจากลูปการค้นหา ผู้โดยสารสำหรับ Grab คันนี้
    return max_rides  # คืนค่าจำนวนผู้โดยสารสูงสุดที่สามารถรับได้


if __name__ == "__main__":
    with open("C:\\Users\\user\\Downloads\\4.1.1.txt") as f:
        arr = f.readline().strip()
        k = int(f.readline().strip())

    max_passengers = greedy(arr, k)
    print(max_passengers)
