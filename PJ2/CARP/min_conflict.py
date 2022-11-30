import random

def min_conflict(n, dpt, cap, k, R, load, cost, cst, dmd, dis):
    T = 0
    while True:
        T += 1
        if T > 10000:
            break
        ri = random.randint(0, k-1)
        rj = random.randint(0, len(R[ri])-1)
        e1 = R[ri][rj]
        p1 = R[ri][rj-1] if rj != 0 else (0, dpt)
        s1 = R[ri][rj+1] if rj != len(R[ri])-1 else (dpt, 0)
        for i in range(k):
            if i != ri:
                for j in range(len(R[i])):
                    e2 = R[i][j]
                    p2 = R[i][j-1] if j != 0 else (0, dpt)
                    s2 = R[i][j+1] if j != len(R[i])-1 else (dpt, 0)
                    if load[ri] - e1[2] + e2[2] > cap or load[i] - e2[2] + e1[2] > cap:
                        continue
                    if dis[p1[1]][e2[0]] + dis[e2[1]][s1[0]] + dis[p2[1]][e1[0]] + dis[e1[1]][s2[0]] < dis[p1[1]][e1[0]] + dis[e1[1]][s1[0]] + dis[p2[1]][e2[0]] + dis[e2[1]][s2[0]]:
                        load[ri] = load[ri] - e1[2] + e2[2]
                        cost[ri] = cost[ri] - dis[p1[1]][e1[0]] - dis[e1[1]][s1[0]] - cst[e1[0:2]] + dis[p1[1]][e2[0]] + dis[e2[1]][s1[0]] + cst[e2[0:2]]
                        load[i] = load[i] - e2[2] + e1[2]
                        cost[i] = cost[i] - dis[p2[1]][e2[0]] - dis[e2[1]][s2[0]] - cst[e2[0:2]] + dis[p2[1]][e1[0]] + dis[e1[1]][s2[0]] + cst[e1[0:2]]
                        print(cost[ri], cost[i])
    return k, R, load, cost      
