import sys

# เพิ่มขีดจำกัดความลึกของ recursion สำหรับ DFS
# (จำเป็นสำหรับกราฟที่มีความลึกมาก)
sys.setrecursionlimit(200000)


def dfs(u, adj, visited):
    """
    ฟังก์ชันมาตรฐาน Depth-First Search
    u: โหนดปัจจุบัน
    adj: Adjacency list ของกราฟ (G หรือ G_Transpose)
    visited: set ของโหนดที่เคยเยี่ยมชมแล้ว
    """
    visited.add(u)  # ทำเครื่องหมายโหนด u ว่าเยี่ยมชมแล้ว แล้วเพิ่มลงใน set
    for v in adj[u]:  # วนผ่านโหนดทุกเพื่อนบ้าน v ของโหนด u
        if v not in visited:  # ถ้าโหนด v ยังไม่เคยเยี่ยมชม
            dfs(v, adj, visited)  # เรียกตัวเองแบบ recursive (มาตรฐาน DFS) ซ้ำที่โหนด v


def solve():
    """
    ฟังก์ชันหลักในการประมวลผล (อ่านจาก sys.stdin) และเก็บผลลัพธ์เพื่อพิมพ์ทีเดียวตอนท้าย
    """
    results = []  # ลิสต์สำหรับเก็บคำตอบของแต่ละ test case

    while True:  # วนลูปอ่าน test case จนกว่าจะเจอ EOF
        try:
            # อ่าน N และ M จาก sys.stdin (ซึ่งจะถูกเปลี่ยนเป็นไฟล์)
            line = (
                sys.stdin.readline().split()
            )  # อ่านบรรทัดถัดมา (string) แล้ว .split() เพื่อแยกเป็น token list
            if not line:
                break  # จบการทำงานถ้าไม่มีอินพุต

            N, M = map(
                int, line
            )  # แปลง token list เป็นจำนวนเต็มสองค่า N (จำนวนโหนด) และ M (จำนวนขอบ)

            # เงื่อนไขสิ้นสุดอินพุต
            if N == 0 and M == 0:
                break  # ถ้าพบ 0 0 ตามรูปแบบของปัญหาให้หยุดอ่าน (เป็นสัญญาณสิ้นสุดชุดข้อมูล)

            # สร้าง Adjacency list
            adj_G = [[] for _ in range(N + 1)]  # Adjacency list ของกราฟทิศทางปกติ
            adj_T = [
                [] for _ in range(N + 1)
            ]  # Adjacency list ของกราฟทิศทางผกผัน (Transpose)

            for _ in range(M):
                # อ่านข้อมูลถนนจาก sys.stdin
                a, b, c = map(
                    int, sys.stdin.readline().split()
                )  # a: จุดเริ่มต้น, b: จุดปลายทาง, c: ประเภทถนน (1 = ทางเดียว a -> b, 2 = สองทาง a <-> b)
                if c == 1:  # ทางเดียว: a -> b
                    adj_G[a].append(b)  # ปกติ: a -> b
                    adj_T[b].append(a)  # กลับทิศ: b -> a
                elif c == 2:  # สองทาง: a <-> b
                    adj_G[a].append(b)  # ปกติ: a -> b
                    adj_G[b].append(a)  # ปกติ: b -> a
                    adj_T[a].append(b)  # กลับทิศ: a -> b
                    adj_T[b].append(a)  # กลับทิศ: b -> a

            # --- เริ่มการตรวจสอบ SCC ---

            # ถ้า N=1 (โหนดเดียว) ถือว่า strongly connected แล้วใส่ "1" ใน results แล้ว continue ไปกรณีถัดไป
            if N <= 1:
                results.append("1")
                continue

            # --- Pass 1: รัน DFS บน G (เริ่มจากโหนด 1) ---
            visited_G = set() # set สำหรับเก็บโหนดที่เยี่ยมชมในกราฟ G
            dfs(1, adj_G, visited_G) # เรียก DFS เริ่มจากโหนด 1

            if len(visited_G) != N: # ถ้าไม่สามารถเยี่ยมชมโหนดทั้งหมดได้
                results.append("0") # ใส่ "0" ใน results แล้ว continue ไปเคสถัดไป
                continue

            # --- Pass 2: รัน DFS บน G_T (เริ่มจากโหนด 1) ---
            visited_T = set() # set สำหรับเก็บโหนดที่เยี่ยมชมในกราฟ G_Transpose
            dfs(1, adj_T, visited_T) # เรียก DFS เริ่มจากโหนด 1

            if len(visited_T) != N: # ถ้าไม่สามารถเยี่ยมชมโหนดทั้งหมดได้
                results.append("0") # ใส่ "0" ใน results แล้ว continue ไปเคสถัดไป
            else: # ถ้าเยี่ยมชมโหนดทั้งหมดได้ทั้งสองรอบ
                results.append("1") # ใส่ "1" ใน results

        except EOFError:
            break
        except Exception as e:
            # print(f"Error: {e}", file=sys.stderr) # สำหรับ debug
            break

    # พิมพ์คำตอบทั้งหมดออกทางหน้าจอ (Standard Output)
    print("\n".join(results))


# --- ส่วนหลักในการรันโปรแกรม ---
if __name__ == "__main__":

    # ชื่อไฟล์อินพุตที่ต้องการอ่าน
    input_filename = "C:\\Users\\user\\Downloads\\Extra9.6.txt"

    # เก็บ standard input เดิมไว้
    original_stdin = sys.stdin

    try:
        # เปิดไฟล์และเปลี่ยน sys.stdin ให้ชี้ไปที่ไฟล์นี้
        # โปรแกรมจะอ่านจากไฟล์นี้แทนการรอรับอินพุตจากคีย์บอร์ด
        sys.stdin = open(input_filename, "r")

        # เรียกฟังก์ชัน solve()
        solve()

    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ '{input_filename}'", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        # ไม่ว่าจะเกิดอะไรขึ้น คืนค่า sys.stdin กลับเป็นเหมือนเดิม
        # (สำคัญหากโปรแกรมนี้ถูก import ไปใช้ที่อื่น)
        if sys.stdin is not original_stdin:
            sys.stdin.close()
        sys.stdin = original_stdin
