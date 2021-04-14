import numpy as np
import grav3body


p = list(map(float,input().split()))
X = [p[i] for i in [0,2,4,1,3,5,6,8,10,7,9,11]]
t0=p[12]
#print([x1,x2,x3,y1,y2,y3,vx1,vx2,vx3,vy1,vy2,vy3,T])
#(t0,dm)=grav3body.distance([x1,x2,x3,y1,y2,y3,vx1,vx2,vx3,vy1,vy2,vy3],1.05*T,0.95*T)
  
#print (t0, dm)
#break

s = grav3body.solution(X,t0)

for i in s:
  print("\t".join(map(str,i)))
