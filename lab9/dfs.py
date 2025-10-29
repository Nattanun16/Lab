import sys

sys.setrecursionlimit(200000)


# --- DFS มาตรฐาน ---
def dfs(u, adj, visited, stack=None, collect=None):
    visited.add(u)
    if collect is not None:
        collect.append(u)
    for v in adj[u]:
        if v not in visited:
            dfs(v, adj, visited, stack, collect)
    if stack is not None:
        stack.append(u)


# --- ฟังก์ชันหลัก ---
def solve():
    results = []
    case_num = 1

    while True:
        try:
            line = sys.stdin.readline().split()
            if not line:
                break
            N, M = map(int, line)
            if N == 0 and M == 0:
                break

            adj_G = [[] for _ in range(N + 1)]
            adj_T = [[] for _ in range(N + 1)]

            for _ in range(M):
                a, b, c = map(int, sys.stdin.readline().split())
                if c == 1:  # one way
                    adj_G[a].append(b)
                    adj_T[b].append(a)
                elif c == 2:  # two way
                    adj_G[a].append(b)
                    adj_G[b].append(a)
                    adj_T[a].append(b)
                    adj_T[b].append(a)

            # ----- ตรวจว่า strongly connected ไหม -----
            visited_G = set()
            dfs(1, adj_G, visited_G)
            if len(visited_G) != N:
                strongly = False
            else:
                visited_T = set()
                dfs(1, adj_T, visited_T)
                strongly = len(visited_T) == N

            # ถ้า strongly connected แล้ว
            if strongly:
                results.append("1")
                continue

            # ----- หา Strongly Connected Components (SCCs) -----
            visited = set()
            stack = []
            for i in range(1, N + 1):
                if i not in visited:
                    dfs(i, adj_G, visited, stack)

            visited.clear()
            scc_list = []
            scc_id = [0] * (N + 1)
            curr_id = 0
            while stack:
                node = stack.pop()
                if node not in visited:
                    collect = []
                    dfs(node, adj_T, visited, collect=collect)
                    curr_id += 1
                    for x in collect:
                        scc_id[x] = curr_id
                    scc_list.append(collect)

            # ----- สร้างกราฟย่อ -----
            scc_count = curr_id
            outdeg = [0] * (scc_count + 1)
            indeg = [0] * (scc_count + 1)

            for u in range(1, N + 1):
                for v in adj_G[u]:
                    if scc_id[u] != scc_id[v]:
                        outdeg[scc_id[u]] += 1
                        indeg[scc_id[v]] += 1

            sources = sum(1 for i in range(1, scc_count + 1) if indeg[i] == 0)
            sinks = sum(1 for i in range(1, scc_count + 1) if outdeg[i] == 0)
            edges_needed = max(sources, sinks)

            # ----- แสดงผล -----
            print(f"Case #{case_num}: 0 (Not strongly connected)")
            print(f"  SCCs found ({scc_count} total):")
            for i, comp in enumerate(scc_list, start=1):
                print(f"    Component {i}: {sorted(comp)}")

            print(f"  -> ต้องเพิ่ม edge อย่างน้อย {edges_needed} เส้น")

            # เพื่อให้เห็นภาพ จะเชื่อม source → sink แบบง่ายที่สุด
            if edges_needed > 0:
                sources_list = [i for i in range(1, scc_count + 1) if indeg[i] == 0]
                sinks_list = [i for i in range(1, scc_count + 1) if outdeg[i] == 0]
                new_edges = []
                for i in range(edges_needed):
                    u_comp = sinks_list[i % len(sinks_list)]
                    v_comp = sources_list[i % len(sources_list)]
                    new_edges.append((scc_list[u_comp - 1][0], scc_list[v_comp - 1][0]))

                print("  แนะนำให้เพิ่ม edge:")
                for a, b in new_edges:
                    print(f"    {a} -> {b}")

            print()
            case_num += 1

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break


# --- ส่วนหลักในการรัน ---
if __name__ == "__main__":
    input_filename = "C:\\Users\\user\\Downloads\\Extra9.5.txt"
    original_stdin = sys.stdin
    try:
        sys.stdin = open(input_filename, "r")
        solve()
    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ '{input_filename}'", file=sys.stderr)
    finally:
        if sys.stdin is not original_stdin:
            sys.stdin.close()
        sys.stdin = original_stdin
