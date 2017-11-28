import numpy as np
import matplotlib.pyplot as mpl

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def atmos_pressure(P0, T, h):                        # P0 = Pressure at sea Level
    P = P0*np.exp(((0.02896 * 9.807)/(8.3143*T))*h)  #  T = Temperature of ambient air (K)
    return P

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

heights = []
data = []

for i in range (100000):
    heights.append(i)
    data.append(atmos_pressure(101325, 288.15, i))

mpl.plot(heights, data)
mpl.show()