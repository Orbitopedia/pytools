from scipy.integrate import odeint,ode
import time
import numpy as np
import math

def hamilton(t,y):
  xx=y[0:3]
  xy=y[3:6]
  vx=y[6:9]
  vy=y[9:12]
  ret=list(vx)+list(vy)+[0.,0.,0.,0.,0.,0.]
  for i in range(3):
    for j in range(3):
      if i!=j:
        ret[6+i]=ret[6+i]+(xx[j]-xx[i])/math.pow((xx[j]-xx[i])*(xx[j]-xx[i])+(xy[j]-xy[i])*(xy[j]-xy[i]),3./2)
        ret[9+i]=ret[9+i]+(xy[j]-xy[i])/math.pow((xx[j]-xx[i])*(xx[j]-xx[i])+(xy[j]-xy[i])*(xy[j]-xy[i]),3./2)
  return ret


def dist2(y1,y2):
  return sum([(i-j)**2 for i,j in zip(y1,y2)])

def norm2(y):
  return sum([i**2 for i in y])

def kenergy(y):
  return sum([x*x for x in y[6:]]) 

def penergy(y):
  p=0.
  for i in range(3):
    for j in range(3):
      if j>i:
        p=p-1.0/math.sqrt((y[j]-y[i])*(y[j]-y[i])+(y[j+3]-y[i+3])*(y[j+3]-y[i+3]))
  return p

def energy(y):
  return penergy(y)+penergy(y)

def solution(y0,t0):
  sol=[]
  def outf(t,y):
    sol.append([t]+list(y)+[kenergy(y),penergy(y),energy(y)])
    if kenergy(y)>1e10:
      return -1
    else:
      return 0      
  r = ode(hamilton).set_integrator('dopri5',rtol=1e-15,max_step=0.001,nsteps=2000000)
  r.set_initial_value(y0, 0)
  r.set_solout(outf)
  r.integrate(t0)
  return sol

class Distancer:
  def __init__(self,y0,tm):
    self.oy=[]
    self.ot=-1
    self.smd=0
    self.mmd=100
    self.mmt=0
    self.started=False
    self.y0=y0
    self.tm=tm
  def outf(self,t,y):
    ym=y
    if self.ot>-1:
      x2=dist2(ym,self.oy)
      x02=dist2(self.y0,self.oy)
      xx0=sum([(ym[i]-self.oy[i])*(self.y0[i]-self.oy[i]) for i in range(12)])      
      md=np.sqrt(x02-xx0*xx0/x2)
      mt=(t-self.ot)*xx0/x2
      self.started=self.started or (md<self.smd)
      self.smd=md
      if self.started and (md<self.mmd) and (mt>0) and (mt+self.ot)<t and (t>self.tm):
        self.mmd=md
        self.mmt=self.ot+mt
    self.oy=np.copy(ym)
    self.ot=t
    if kenergy(ym)>1e10:
      return -1
    else:
      return 0      
        
def distance(y0,t0,tm):
  d=Distancer(y0,tm)
  r = ode(hamilton).set_integrator('dopri5',rtol=1e-15,max_step=0.001,nsteps=2000000)
  r.set_initial_value(y0, 0)
  r.set_solout(d.outf)
  r.integrate(t0)
  return d.mmt,d.mmd
