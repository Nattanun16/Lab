import sys

sys.setrecursionlimit(200000) # เพิ่มขีดจำกัดการเรียกซ้ำของฟังก์ชัน


# --- DFS มาตรฐาน ---
def dfs(u, adj, visited, stack=None, collect=None): # u: โหนดปัจจุบัน, adj: กราฟในรูป adjacency list, visited: เซ็ตโหนดที่เยี่ยมชมแล้ว
    visited.add(u) # ทำเครื่องหมายว่าโหนด u ถูกเยี่ยมชมแล้ว
    if collect is not None: # เก็บโหนดที่อยู่ใน component ปัจจุบัน
        collect.append(u) # เพิ่มโหนด u ลงในลิสต์ collect
    for v in adj[u]: # วนผ่านโหนดเพื่อนบ้านของ u
        if v not in visited: # ถ้าโหนด v ยังไม่ถูกเยี่ยมชม
            dfs(v, adj, visited, stack, collect) # เรียก DFS ซ้ำที่โหนด v
    if stack is not None: # ถ้ามีสแตกสำหรับเก็บลำดับการสิ้นสุด
        stack.append(u) # เพิ่มโหนด u ลงในสแตกหลังจากเยี่ยมชมเสร็จ


# --- ฟังก์ชันหลัก ---
def solve():
    results = [] # เก็บผลลัพธ์ของแต่ละเคส
    case_num = 1 # ตัวนับเคส

    while True: # วนลูปอ่านเคสจนกว่าจะเจอจุดสิ้นสุด
        try: # อ่านจำนวนโหนดและขอบ
            line = sys.stdin.readline().split() # อ่านบรรทัดและแยกเป็นโทเค็น
            if not line: # ถ้าว่าง แสดงว่า EOF
                break
            N, M = map(int, line) # แปลงเป็นจำนวนเต็ม
            if N == 0 and M == 0: # ถ้าเจอ 0 0 แสดงว่าเป็นจุดสิ้นสุด
                break

            adj_G = [[] for _ in range(N + 1)] # กราฟทิศทางเดิม
            adj_T = [[] for _ in range(N + 1)] # กราฟทิศทางกลับด้าน

            for _ in range(M): # อ่านขอบทั้งหมด
                a, b, c = map(int, sys.stdin.readline().split()) # อ่านขอบ a -> b และทิศทาง c
                if c == 1:  # one way
                    adj_G[a].append(b) # เพิ่มขอบจาก a ไป b
                    adj_T[b].append(a) # เพิ่มขอบกลับด้านจาก b ไป a
                elif c == 2:  # two way
                    adj_G[a].append(b) # เพิ่มขอบจาก a ไป b
                    adj_G[b].append(a) # เพิ่มขอบจาก b ไป a
                    adj_T[a].append(b) # เพิ่มขอบกลับด้านจาก a ไป b
                    adj_T[b].append(a) # เพิ่มขอบกลับด้านจาก b ไป a

            # ----- ตรวจว่า strongly connected ไหม -----
            visited_G = set() # เซ็ตโหนดที่เยี่ยมชมในกราฟเดิม
            dfs(1, adj_G, visited_G) # เริ่ม DFS จากโหนด 1 ในกราฟเดิม
            if len(visited_G) != N: # ถ้าไม่เยี่ยมชมครบทุกโหนด
                strongly = False # ไม่ใช่ strongly connected
            else: # ตรวจกราฟกลับด้าน
                visited_T = set() # เซ็ตโหนดที่เยี่ยมชมในกราฟกลับด้าน
                dfs(1, adj_T, visited_T) # เริ่ม DFS จากโหนด 1 ในกราฟกลับด้าน
                strongly = len(visited_T) == N # ถ้าเยี่ยมชมครบทุกโหนดในกราฟกลับด้านก็เป็น strongly connected

            # ถ้า strongly connected แล้ว
            if strongly:
                results.append("1") # บันทึกผลลัพธ์
                continue # ไปเคสถัดไป

            # ----- หา Strongly Connected Components (SCCs) -----
            visited = set() # เซ็ตโหนดที่เยี่ยมชม
            stack = [] # สแตกเก็บลำดับการสิ้นสุดของโหนด
            for i in range(1, N + 1): # วนผ่านโหนดทั้งหมด
                if i not in visited: # ถ้ายังไม่ถูกเยี่ยมชม
                    dfs(i, adj_G, visited, stack) # เรียก DFS เพื่อเติมสแตก

            visited.clear() # ล้างเซ็ตเยี่ยมชมเพื่อใช้ใหม่
            scc_list = [] # ลิสต์เก็บ SCCs
            scc_id = [0] * (N + 1) # เก็บรหัส SCC ของแต่ละโหนด
            curr_id = 0 # ตัวนับรหัส SCC
            while stack: # วนจนกว่าสแตกจะว่าง
                node = stack.pop() # ดึงโหนดจากสแตก
                if node not in visited: # ถ้ายังไม่ถูกเยี่ยมชม
                    collect = [] # ลิสต์เก็บโหนดใน SCC ปัจจุบัน
                    dfs(node, adj_T, visited, collect=collect) # เรียก DFS ในกราฟกลับด้านเพื่อเก็บ SCC
                    curr_id += 1 # เพิ่มรหัส SCC
                    for x in collect: # กำหนดรหัส SCC ให้โหนดใน component นี้
                        scc_id[x] = curr_id # กำหนดรหัส SCC ให้โหนด x
                    scc_list.append(collect) # เพิ่ม component นี้ลงในลิสต์ SCCs

            # ----- สร้างกราฟย่อ -----
            scc_count = curr_id # จำนวน SCC ทั้งหมด
            outdeg = [0] * (scc_count + 1) # เก็บ outdegree ของแต่ละ SCC
            indeg = [0] * (scc_count + 1) # เก็บ indegree ของแต่ละ SCC

            for u in range(1, N + 1): # วนผ่านโหนดทั้งหมด
                for v in adj_G[u]: # วนผ่านโหนดเพื่อนบ้านของ u
                    if scc_id[u] != scc_id[v]: # ถ้า u กับ v อยู่คนละ SCC
                        outdeg[scc_id[u]] += 1 # เพิ่ม outdegree ของ SCC ที่ u อยู่
                        indeg[scc_id[v]] += 1 # เพิ่ม indegree ของ SCC ที่ v อยู่

            sources = sum(1 for i in range(1, scc_count + 1) if indeg[i] == 0) # นับจำนวน SCC ที่เป็น source
            sinks = sum(1 for i in range(1, scc_count + 1) if outdeg[i] == 0) # นับจำนวน SCC ที่เป็น sink
            edges_needed = max(sources, sinks)

            # ----- แสดงผล -----
            print(f"Case #{case_num}: 0 (Not strongly connected)") # แสดงผลเคสปัจจุบัน
            print(f"  SCCs found ({scc_count} total):") # แสดงจำนวน SCCs ที่พบ
            for i, comp in enumerate(scc_list, start=1): # แสดงแต่ละ SCC
                print(f"    Component {i}: {sorted(comp)}") # แสดงโหนดใน component นั้นๆ

            print(f"  -> ต้องเพิ่ม edge อย่างน้อย {edges_needed} เส้น") # แสดงจำนวน edge ที่ต้องเพิ่ม

            # เพื่อให้เห็นภาพ จะเชื่อม source → sink แบบง่ายที่สุด
            if edges_needed > 0: # ถ้าต้องเพิ่ม edge
                sources_list = [i for i in range(1, scc_count + 1) if indeg[i] == 0] # รายการ SCC ที่เป็น source
                sinks_list = [i for i in range(1, scc_count + 1) if outdeg[i] == 0] # รายการ SCC ที่เป็น sink
                new_edges = [] # ลิสต์เก็บ edge ที่จะแนะนำให้เพิ่ม
                for i in range(edges_needed): # วนเพิ่ม edge ตามจำนวนที่ต้องการ
                    u_comp = sinks_list[i % len(sinks_list)] # เลือก SCC ที่เป็น sink
                    v_comp = sources_list[i % len(sources_list)] # เลือก SCC ที่เป็น source
                    new_edges.append((scc_list[u_comp - 1][0], scc_list[v_comp - 1][0])) # เพิ่ม edge จากโหนดใน sink ไปยังโหนดใน source

                print("  แนะนำให้เพิ่ม edge:") # แสดง edge ที่แนะนำให้เพิ่ม
                for a, b in new_edges:
                    print(f"    {a} -> {b}") # แสดง edge ที่แนะนำให้เพิ่ม

            print() # บรรทัดว่างระหว่างเคส
            case_num += 1 # เพิ่มตัวนับเคส

        except EOFError:
            break
        except Exception as e: # จับข้อผิดพลาดทั่วไป
            print(f"Error: {e}", file=sys.stderr) # แสดงข้อผิดพลาดไปยัง stderr
            break


# --- ส่วนหลักในการรัน ---
if __name__ == "__main__":
    input_filename = "C:\\Users\\user\\Downloads\\Extra9.6.txt"
    original_stdin = sys.stdin # เก็บ stdin เดิมไว้
    try:
        sys.stdin = open(input_filename, "r") # เปลี่ยน stdin ไปอ่านจากไฟล์
        solve() # เรียกฟังก์ชันแก้ปัญหา
    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ '{input_filename}'", file=sys.stderr) # แสดงข้อผิดพลาดถ้าไฟล์ไม่พบ
    finally:
        if sys.stdin is not original_stdin: # ปิดไฟล์ถ้าเปิดขึ้นมา
            sys.stdin.close() # ปิดไฟล์ stdin
        sys.stdin = original_stdin # คืนค่า stdin เดิม
