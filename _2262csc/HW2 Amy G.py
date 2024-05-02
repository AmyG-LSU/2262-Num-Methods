#AmyGranados
import numpy as np
import matplotlib.pyplot as plt
import math as m
#below is the equation x^J/J!
# j is the degree to which you need to find to meaning how many times each x has to be mulitplied to
def p_x(x,j):
    result = [1]
    for k in range(1, j+1):
        result = x ** k/ m.factorial(k)
    return result

x = np.linspace(-3,10, 100)

appx3rd = p_x(x,3)
appx12rd = p_x(x,12)

plt.plot(x,appx3rd, color= 'g')
plt.plot(x,appx12rd, color= 'r')
plt.ylim((-3, 10))
plt.xlabel("x", size=16)
plt.ylabel("y", size=16)
plt.title("3rd and 12th order Taylor Approximations of e^x: AMY GRANADOS", size=16)
plt.legend(("$p_3(x;0)$", "$p_12(x;0)$"))
plt.show()

plt.savefig("AmyGranadosHW2Q3.png")






