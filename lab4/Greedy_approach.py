def greedy(grab_string, k):
    n = len(grab_string)
    taken = [False] * n
    max_rides = 0

    for i in range(n):
        if grab_string[i] == "G":
            # พยายามหาผู้โดยสารในช่วง [i-k, i+k]
            for j in range(max(0, i - k), min(n, i + k + 1)):
                if grab_string[j] == "P" and not taken[j]:
                    taken[j] = True
                    max_rides += 1
                    break
    print(max_rides)
