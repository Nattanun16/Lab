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
    visited.add(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v, adj, visited)

def solve():
    """
    ฟังก์ชันหลักในการประมวลผล (อ่านจาก sys.stdin)
    """
    results = [] # ลิสต์สำหรับเก็บคำตอบของแต่ละ test case

    while True:
        try:
            # อ่าน N และ M จาก sys.stdin (ซึ่งจะถูกเปลี่ยนเป็นไฟล์)
            line = sys.stdin.readline().split()
            if not line:
                break # จบการทำงานถ้าไม่มีอินพุต

            N, M = map(int, line)

            # เงื่อนไขสิ้นสุดอินพุต
            if N == 0 and M == 0:
                break

            # สร้าง Adjacency list
            adj_G = [[] for _ in range(N + 1)]
            adj_T = [[] for _ in range(N + 1)]

            for _ in range(M):
                # อ่านข้อมูลถนนจาก sys.stdin
                a, b, c = map(int, sys.stdin.readline().split())
                
                if c == 1: # ทางเดียว: a -> b
                    adj_G[a].append(b)
                    adj_T[b].append(a) # กลับทิศ: b -> a
                elif c == 2: # สองทาง: a <-> b
                    adj_G[a].append(b)
                    adj_G[b].append(a)
                    adj_T[a].append(b)
                    adj_T[b].append(a)

            # --- เริ่มการตรวจสอบ SCC ---
            
            # ถ้า N=1 (โหนดเดียว) ถือว่า strongly connected
            if N <= 1:
                results.append("1")
                continue

            # --- Pass 1: รัน DFS บน G (เริ่มจากโหนด 1) ---
            visited_G = set()
            dfs(1, adj_G, visited_G)
            
            if len(visited_G) != N:
                results.append("0")
                continue 

            # --- Pass 2: รัน DFS บน G_T (เริ่มจากโหนด 1) ---
            visited_T = set()
            dfs(1, adj_T, visited_T)

            if len(visited_T) != N:
                results.append("0")
            else:
                results.append("1")

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
    input_filename = 'C:\\Users\\acer\\OneDrive\\Desktop\\testcases\\test.txt'

    # เก็บ standard input เดิมไว้
    original_stdin = sys.stdin
    
    try:
        # เปิดไฟล์และเปลี่ยน sys.stdin ให้ชี้ไปที่ไฟล์นี้
        # โปรแกรมจะอ่านจากไฟล์นี้แทนการรอรับอินพุตจากคีย์บอร์ด
        sys.stdin = open(input_filename, 'r')
        
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