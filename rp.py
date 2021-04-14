import numpy as np
import grav3body


p = list(map(float,input().split()))
X = [p[i] for i in [0,2,4,1,3,5,6,8,10,7,9,11]]
t0=p[12]

(t0,dm)=grav3body.distance(X,1.05*t0,0.95*t0)
  
print (t0, dm)

