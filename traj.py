import numpy as np
import grav3body


p = list(map(float,input().split()))
X = [p[i] for i in [0,2,4,1,3,5,6,8,10,7,9,11]]
t0=p[12]

s = grav3body.solution(X,t0)

for i in s:
  print("\t".join(map(str,i)))
