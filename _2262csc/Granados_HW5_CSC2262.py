import numpy as np
import matplotlib.pyplot as plt

y = np.array([3, 4, 1, 4, 1, 4, 0, 0, 0, 0, 0, 0])
A= np.array([[0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
             [0 ,0,0,0,27,9,3,1,0,0,0,0],
             [0 ,0,0,0,0,0,0,0,216,36,6,1],
             [27 ,9,3,1,0,0,0,0,0,0,0,0],
             [0 ,0,0,0,216,36,6,1,0,0,0,0],
             [0 ,0,0,0,0,0,0,0,512,64,8,1],
             [27 ,2,1,0,-27,-2,-1,0,0,0,0,0],
             [0 ,0,0,0,108,2,1,0,-108,-2,-1,0],
             [18 ,2,0,0,-18,-2,0,0,0,0,0,0],
             [0 ,0,0,0,36,2,0,0,-36,-2,0,0],
             [0 ,2,0,0,0,0,0,0,0,0,0,0],
             [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,48 ,2 ,0 ,0]])
b = np.dot(np.linalg.inv(A),y)
def S(x_val, i):
    return b[i] * (x_val - x[i])**3 + b[i+1] * (x_val - x[i])**2 + b[i+1] * (x_val - x[i]) +b[i+1]

x = np.linspace(0,10,100)
conditions = [x < x[i+1] for i in range(len(x)-1)]

yy = np.piecewise(x,conditions,[lambda x_val: S(x_val, i) for i in range(len(x)-1)])