class Node():
  def __init__(self,board,space,pre,cost,heuristic=None,hash_value=None):
    self.state=1 # 1:open, 2:close
    self.board=board
    self.pre=pre
    self.space=space
    self.cost=cost # 初期位置からこの場面までの実コスト
    self.heuristic=heuristic# この場面からゴールまでの推定コスト（ヒューリスティック値）
    if heuristic is None:
      self.heuristic=get_heuristic(board) 
    self.hash_value=hash_value
    if hash_value is None: # この場面を一意に表すハッシュ値
      self.hash_value=get_hash_value(self.board)
    self.score=self.heuristic+self.cost

  # スコアの大小比較のための関数
  def __lt__(self,other):
    return self.score < other.score

b=10**9+7
h=pow(2,61)-1
def get_hash_value(board):
  ret=0
  for i in range(len(board)):
    ret+=board[i]*pow(b,len(board)-i-1,h)
    ret%=h
  return ret

def get_heuristic(board):
  ret=0
  for i in range(3):
    for j in range(3):
      t=board[i*3+j]-1
      if t<0:continue
      ti,tj=divmod(t,3)
      ret+=abs(i-ti)+abs(j-tj)
  return ret

# スペースを動かした時の[場面、実コスト、ヒューリステック値、ハッシュ値]を返す。
# 指定された方向へ動かせない場合Noneを返す
def move_piece(node,direction):
  next_board=node.board[:]
  space=node.space
  i,j=space
  di,dj=direction
  ni,nj=i+di,j+dj
  if not(0<=ni<3 and 0<=nj<3):return None
  t=next_board[ni*3+nj]
  ti,tj=divmod(t-1,3)

  # heuristic
  next_heuristic=node.heuristic
  next_heuristic-=abs(ti-ni)+abs(tj-nj)
  next_heuristic+=abs(ti-i)+abs(tj-j)

  # board
  next_board[i*3+j]=t
  next_board[ni*3+nj]=0

  # hash_value
  next_hash_value=node.hash_value
  next_hash_value-=t*pow(b,len(next_board)-(ni*3+nj)-1,h)
  next_hash_value+=t*pow(b,len(next_board)-(i*3+j)-1,h)
  next_hash_value%=h
  return next_board,node.cost+1,next_heuristic,next_hash_value

from heapq import heappop,heappush
def A_star(ep):
  open_set={}
  for i in range(9):
    if ep.board[i]==0:space=divmod(i,3)
  start=Node(ep.board,space,None,0,None,None)
  open_set[start.hash_value]=start
  Node_list=[start]
  route=[]
  while Node_list:
    node=heappop(Node_list)
    if open_set[node.hash_value].score<node.score:continue
    if node.heuristic==0:
      route.append(node)
      break
    i,j=node.space
    for direction in ((0,1),(0,-1),(1,0),(-1,0)):
      di,dj=direction
      ni,nj=i+di,j+dj
      if not (0<=ni<3 and 0<=nj<3):continue
      next_space=ni,nj
      ret=move_piece(node,direction)
      if ret is not None:
        next_board,next_cost,next_heuristic,next_hash_value=ret
        if next_hash_value in open_set:
          if open_set[next_hash_value].score>next_cost+next_heuristic:
            pass
          else:
            continue
        next_node=Node(next_board,next_space,node.hash_value,next_cost,next_heuristic,next_hash_value)
        open_set[next_hash_value]=next_node
        heappush(Node_list,next_node)
    node.state=2
  
  if route:
    while True:
      route.append(open_set[route[-1].pre])
      if route[-1].pre is None:break
    route.reverse()
    return route
  else:
    return None


import random
from random import randint
class eight_puzzle():
  def __init__(self,board=None,seed=None):
    if seed is not None:random.seed(seed)
    self.seed=seed

    if board is not None:
      self.board=board
      for i in range(9):
        if board[i]==0:
          self.space=divmod(i,3)
    else:
      board=[i+1 for i in range(9)]
      board[-1]=0  
      now=8
      pre=-1
      dirctions=[[0,1],[0,-1],[1,0],[-1,0]]
      for _ in range(100):
        i,j=divmod(now,3)
        di,dj=dirctions[randint(0,3)]
        ni,nj=i+di,j+dj
        if 0<=ni<3 and 0<=nj<3 and ni*3+nj!=pre:
          board[now],board[ni*3+nj]=board[ni*3+nj],board[now]
          pre=now
          now=ni*3+nj    
      self.board=board
      self.space=now

# test
if __name__=='__main__1':
  #ep=eight_puzzle([1,2,3,4,5,6,8,7,0])
  ep=eight_puzzle()
  route=A_star(ep)
  if route is not None:
    for x in route:
      print(*x.board[0:3])
      print(*x.board[3:6])
      print(*x.board[6:9])
      print('↓')
    print(f'{len(route)} hands')
  else:
    print('not goal')
# test
if __name__=='__main__':
  hands=0
  for i in range(100):
    ep=eight_puzzle()
    ret=A_star(ep)
    if ret is not None:
      hands=max(hands,len(ret)-1)
    else:
      print(ep.board)
      break
  print(f'max {hands} hands')
