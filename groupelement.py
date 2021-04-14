import numpy as np
import grav3body

p = list(map(float,input().split()))

X = [p[i] for i in [0,2,4,1,3,5,6,8,10,7,9,11]]
t0=p[12]


s = grav3body.solution(X,t0)

ovp = 0
ta = [0]
seq = [2]
seq = []
for i in range(len(s)):
    t = s[i][0]
    x = s[i][1:4]
    y = s[i][4:7]
    rx=x[1]-x[0]
    ry=y[1]-y[0]
    lx=2*x[2]-x[1]-x[0]
    ly=2*y[2]-y[1]-y[0]
    vp = rx * ly - ry * lx
    if (ovp * vp) < 0:
        a = (x[1]-x[0])*(x[1]-x[0])+(y[1]-y[0])*(y[1]-y[0])
        b = (x[2]-x[0])*(x[2]-x[0])+(y[2]-y[0])*(y[2]-y[0])
        c = (x[1]-x[2])*(x[1]-x[2])+(y[1]-y[2])*(y[1]-y[2])
        if a>b and a>c:
            seq += [2]
            ta += [t]
        if b>a and b>c:
            seq += [3]
            ta += [t]
        if c>a and c>b:
            seq += [1]
            ta += [t]
    ovp = vp
if seq[-1]!=seq[0] or (len(seq)%2==0):
    seq += [seq[0]]
print(seq)
n = len(seq)
for i in range(n-1):
    for j in range(len(seq)-1):
        if seq[j]==seq[j+1]:
          seq = seq[:j]+seq[j+2:]
          if j==0:
              seq[-1]=seq[0]
          if j==len(seq):
              seq[0]=seq[-1]
          break
print(seq)
  
om = {(1,2):"F",(1,3):"FA",(2,1):"B",(2,3):"A",(3,1):"EB",(3,2):"E"}
em = {(1,2):"D",(1,3):"DG",(2,1):"H",(2,3):"G",(3,1):"CH",(3,2):"C"}
hc = ""
offset = 0
for i in range(len(seq)-1):
   if(seq[i]!=seq[i+1]):
       if (i+offset)%2 == 0:
           hc += om[(seq[i],seq[i+1])]
       else:
           hc += em[(seq[i],seq[i+1])]
   else:
       offset += 1
       print("Multiple - seg:", seq[i])

hc2c={"AC":"a","GE":"A","BD":"b","HF":"B", "CA":"a","EG":"A","DB":"b","FH":"B"}

fg = ""
tmp = hc[:]
shift = False
print(tmp)
for i in range(0,len(tmp),2):
    if tmp[i:i+2] not in hc2c:
        shift = True
        print("shift")
if shift:
    tmp = tmp[1:]+tmp[0]
print(tmp)
while tmp != "":
    fg += hc2c[tmp[:2]]
    tmp = tmp[2:]
print("".join(map(str,seq)),fg)
