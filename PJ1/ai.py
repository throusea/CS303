from turtle import screensize
import numpy as np
import random
import time
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
inf = 998244353
random.seed(0)
stable_list_row = [(0, 1), (0, 6), (7, 1), (7, 6)]
stable_list_col = [(1, 0), (6, 0), (6, 7), (1, 7)]
#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out, variable, env):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need to add your decision to your candidate_list. The system will get the end of your candidate_list as your decision.
        self.candidate_list = []
        self.dirx = [1,-1,0,0,1,1,-1,-1]
        self.diry = [0,0,1,-1,1,-1,1,-1]
        self.variable = variable
        self.env = env
    
    def get_candidate_list(self, color, chessboard):
        candidate_list = []
        op_clr = -color
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for pos in idx:
            tem_pos = [0, 0]
            for j in range(8):
                tem_pos[0] = pos[0]
                tem_pos[1] = pos[1]
                op_clr_cnt = 0
                flag = True
                while True:
                    tem_pos[0] = tem_pos[0] + self.dirx[j]
                    tem_pos[1] = tem_pos[1] + self.diry[j]
                    if tem_pos[0] >= self.chessboard_size or tem_pos[1] >= self.chessboard_size:
                        flag = False
                        break
                    if tem_pos[0] < 0 or tem_pos[1] < 0 or chessboard[tem_pos[0]][tem_pos[1]] == COLOR_NONE:
                        flag = False
                        break
                    if chessboard[tem_pos[0]][tem_pos[1]] == color:
                        break
                    if chessboard[tem_pos[0]][tem_pos[1]] == op_clr:
                        op_clr_cnt += 1
                    
                if flag == True and op_clr_cnt > 0:
                    candidate_list.append(pos)
                    break

        return candidate_list
    
    def play(self, color, node, chessboard):
        idx = []
        temp_chessboard = np.copy(chessboard)
        if node == ():
            return temp_chessboard
        temp_chessboard[node[0]][node[1]] = color
        for i in range(8):
            tx = node[0]
            ty = node[1]
            flag = True
            while True:
                tx = tx + self.dirx[i]
                ty = ty + self.diry[i]
                if  tx < 0 or ty < 0 or tx >= self.chessboard_size or ty >= self.chessboard_size or chessboard[tx][ty] == COLOR_NONE:
                    flag = False
                    break
                idx.append((tx, ty))
                if chessboard[tx][ty] == color:
                    break
            if flag == True:
                for j in range(len(idx)):
                    temp_chessboard[idx[j][0]][idx[j][1]] = color
            idx.clear()
        return temp_chessboard
    
    def eval(self, color, slted_nodes:list, chessboard, candidate_list):
        pl_cnt = len(np.where(chessboard == self.color)[0])
        op_cnt = len(np.where(chessboard == -self.color)[0])
        
        t = pl_cnt+op_cnt
        v = np.copy(self.variable); v[0] = v[0]/32/32
        s = op_cnt-pl_cnt
        k = len(candidate_list) if color == self.color else -len(candidate_list)
        c = self.chessboard_size*self.chessboard_size
        # print(chessboard)
        # print(k)
        if t == 64 or (k == 0 and len(self.get_candidate_list(-color, chessboard)) == 0):
            if s > 0:
                return inf-1
            elif s < 0:
                return -inf+1
            else:
                return 0
        else:
            env_score = 0; bonus = 0
            for (o, clr) in slted_nodes:
                env_score = env_score + (-self.env[o[0]][o[1]] if clr == self.color else self.env[o[0]][o[1]])
            # print('envscore', env_score)
            if t > 30:
                if chessboard[0][0] == COLOR_NONE and chessboard[0][1] == chessboard[1][0] == chessboard[1][1] and chessboard[0][1] != COLOR_NONE:
                    bonus += 20 if chessboard[0][1] == self.color else -20
                if chessboard[0][7] == COLOR_NONE and chessboard[0][6] == chessboard[1][7] == chessboard[1][6] and chessboard[0][6] != COLOR_NONE:
                    bonus += 20 if chessboard[0][6] == self.color else -20
                if chessboard[7][0] == COLOR_NONE and chessboard[6][0] == chessboard[7][1] == chessboard[6][1] and chessboard[6][0] != COLOR_NONE:
                    bonus += 20 if chessboard[6][0] == self.color else -20
                if chessboard[7][7] == COLOR_NONE and chessboard[7][6] == chessboard[6][7] == chessboard[7][7] and chessboard[7][6] != COLOR_NONE:
                    bonus += 20 if chessboard[7][6] == self.color else -20
                
            score = (v[0]*t*t-c*v[0]*t+v[1])*s+(-v[0]*t*t+c*v[0]*t+v[2]-v[1])*k+(1-v[2])*env_score+bonus
            print('slt', slted_nodes, k, score)
            # for st_node in stable_list_row:
            #     if st_node[0] == node[0] and chessboard[st_node] == -self.color:
            #         score -= 20
            # for st_node in stable_list_col:
            #     if st_node[1] == node[1] and chessboard[st_node] == -self.color:
            #         score -= 20
            return score
    
    def maximize(self, color, slted_nodes, opcand_list, chessboard, depth, alpha, beta):
        # print("max", chessboard)
        candidate_list = self.get_candidate_list(color, chessboard)
        ept_cnt = len(np.where(chessboard == COLOR_NONE)[0])
        # print(candidate_list)
        if (ept_cnt > 10 and depth >= 5) or (len(candidate_list) == 0 and len(self.get_candidate_list(-color, chessboard)) == 0):
            return ((), self.eval(color, slted_nodes, chessboard, opcand_list))
        if len(candidate_list) == 0 and len(self.get_candidate_list(-color, chessboard)) != 0:
            return self.minimize(-color, slted_nodes, opcand_list, chessboard, depth, alpha, beta)
        maxNode, maxUtility = (), -inf
        for node in candidate_list:
            slted_nodes.append((node, color))
            _, utility = self.minimize(-color, slted_nodes, opcand_list, self.play(color, node, chessboard), depth+1, alpha, beta)
            slted_nodes.pop(-1)
            if utility > maxUtility:
                maxNode, maxUtility = node, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
            
        return (maxNode, maxUtility)

    def minimize(self, color, slted_nodes, opcand_list, chessboard, depth, alpha, beta):
        # print("min", chessboard)
        candidate_list = self.get_candidate_list(color, chessboard)
        ept_cnt = len(np.where(chessboard == COLOR_NONE)[0])
        if (ept_cnt > 10 and depth >= 5) or (len(candidate_list) == 0 and len(self.get_candidate_list(-color, chessboard)) == 0):
            return ((), self.eval(color, slted_nodes, chessboard, opcand_list))
        if len(candidate_list) == 0 and len(self.get_candidate_list(-color, chessboard)) != 0:
            return self.maximize(-color, slted_nodes, opcand_list, chessboard, depth, alpha, beta)
        minNode, minUtility = (), inf
        for node in candidate_list:
            slted_nodes.append((node, color))
            if depth == 2:
                _, utility = self.maximize(-color, slted_nodes, candidate_list, self.play(color, node, chessboard), depth+1, alpha, beta)
            else:
                _, utility = self.maximize(-color, slted_nodes, opcand_list, self.play(color, node, chessboard), depth+1, alpha, beta)
            slted_nodes.pop(-1)
            if utility < minUtility:
                minNode, minUtility = node, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility
        return (minNode, minUtility)

    # The input is the current chessboard. Chessboard is a numpy array.
    def go(self, chessboard):
        self.candidate_list.clear()
        self.candidate_list = self.get_candidate_list(self.color, chessboard)
        if len(self.candidate_list) > 0:
            node, _ = self.maximize(self.color, [], [], chessboard, 1, -inf, inf)
            self.candidate_list.append(node)
        return self.candidate_list

class RandomAI(AI):
    def go(self, chessboard):
        self.candidate_list.clear()
        self.candidate_list = self.get_candidate_list(self.color, chessboard)
        if len(self.candidate_list) > 0:
            node = random.choice(self.candidate_list)
            self.candidate_list.append(node)
        return self.candidate_list