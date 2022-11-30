import os
import sys
import argparse
import time
import numpy as np
import math
import random
import re
import min_conflict

INF = 1000000000

def floyd(n, cst):
    dis = np.copy(cst)
    for i in range(n):
        dis[i][i] = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
    return dis

def path_scanning(n, dpt, cap, cst, dis, dmd):
    free = []
    dpt = dpt-1
    for i in range(n):
        for j in range(i+1, n):
            if dmd[i][j] != 0:
                free.append((i, j, dmd[i][j]))
    m = len(free)
    for i in range(m):
        e = free[i]
        free.append((e[1], e[0], e[2]))
    k = -1
    R = []
    load = []
    cost = []
    while len(free) > 0:
        k = k+1; R.append([]); load.append(0); cost.append(0); i = dpt
        while len(free) > 0:
            min_d, min_u = INF, -1
            m = len(free) // 2
            for u in range(m*2):
                e = free[u]
                if load[k]+e[2] <= cap:
                    if dis[i][e[0]] < min_d:
                        min_d = dis[i][e[0]]
                        min_u = u
                    elif dis[i][e[0]] == min_d and random.randint(0, 1) == 0:
                        min_u = u
            if min_d == INF:
                break
            # print(min_u, free[min_u])
            e = free[min_u]
            R[k].append(e)
            load[k] = load[k] + e[2]
            cost[k] = cost[k] + min_d + cst[e[0]][e[1]]
            i = e[1]
            # print('beg', free)
            if min_u >= m:
                free.remove(free[min_u])
                free.remove(free[min_u-m])
            else:
                free.remove(free[min_u+m])
                free.remove(free[min_u])
            # print('end', free)
        cost[k] = cost[k] + dis[i][dpt]
    k = k+1
    return k, R, load, cost

def file_input(args):
    f = open(args.file)
    file_dict = {}
    cst = np.full((200, 200), INF, dtype=int)
    dmd = np.zeros((200, 200), dtype=int)
    pos = 0
    while True:
        s = f.readline()
        if s.find('END') != -1:
            break
        if pos < 8:
            ss = re.split(r' : ', s.strip())
            file_dict[ss[0]] = ss[1]
        if pos > 8:
            ss = re.split(r'[ ]+', s.strip())
            u = int(ss[0])
            v = int(ss[1])
            c = int(ss[2])
            s = int(ss[3])
            cst[u][v] = cst[v][u] = c
            dmd[u][v] = dmd[v][u] = s
        # print(ss)
        # input(s)
        pos += 1
    return file_dict, cst, dmd

def print_out(k, R, cost):
    sum = 0
    print('s ', end='')
    for i in range(k):
        print('0', end=',')
        for e in R[i]:
            print("(%d,%d)" % (e[0]+1, e[1]+1), end=',')
        if i == k-1:
            print('0', end='')
        else:
            print('0', end=',')
        sum = sum + cost[i]
    print('\nq %d' % sum)

def main():
    argparser = argparse.ArgumentParser(description="CARP Solver")
    argparser.add_argument(
        '-t', '--termination',
        metavar='T',
        default=60,
        help='A positive number which indicates how many seconds in your algorithm can spend on this instance'
    )
    argparser.add_argument(
        '-s', '--seed',
        metavar='S',
        default='114514',
        help='The random seed used in this run'
    )
    argparser.add_argument(
        'file',
        type=str,
        default='sample.dat',
        help='The input file name'
    )
    args = argparser.parse_args()
    # print(args.file, args.seed, args.termination)
    start = time.time()
    # abaaba

    file_dict, cst, dmd = file_input(args)
    # print(file_dict)
    n = int(file_dict['VERTICES'])
    dpt = int(file_dict['DEPOT'])
    cap = int(file_dict['CAPACITY'])

    cst = cst[1:n+1, 1:n+1]
    dmd = dmd[1:n+1, 1:n+1]
    # print(cst)
    dis = floyd(n, cst)
    # print(cst)
    # print(dis)
    k, R, load, cost = path_scanning(n, dpt, cap, cst, dis, dmd)
    print_out(k, R, cost)
    k, R, load, cost = min_conflict.min_conflict(n, dpt, cap, k, R, load, cost, cst, dmd, dis)
    print_out(k, R, cost)
    run_time = (time.time()-start)
    pass

if __name__ == "__main__":
    main()