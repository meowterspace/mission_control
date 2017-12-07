
# coding: utf-8

# In[1]:

import numpy as np


# In[2]:

def drag(P, T, Vg, Cd, A):  # P = Pressure /PA, T = temp(k), Vg = flow velocity of gas

    F = 0.5 * ((P / (286 * T)) * (Vg ** 2) * Cd * A)  # Cd = Coefficient of drag, A = area in drag
    return F


def gravity(M, m, r):  # P = Pressure, T = temp(k), Vg = flow velocity of gas
    F = (6.67408e-11 * M * m) / (r ** 2)  # Cd = Coefficient of drag, A = area in drag
    return F


def thrust(q, Ve, Pe, Pa, Ae):  # q = rate of ejected mass flow, Ve = exhaust gas ejection speed
    F = q * Ve + (Pe - Pa) * Ae  # Pe = pressure of exhaust gasses, Pa = pressure of ambient atmosphere
    return F  # Ae = area of exit


# In[11]:

class rocket:
    def __init__(self):
        mass = length = radius = F = None
        pos = angle = S = U = V = a = [None, None, None]
        
    def get_home_radius(self):
        radius = np.sqrt((self.pos[0]**2)+(self.pos[1]**2)+(self.pos[2]**2))
        return radius
    
    def get_grav_vector(self, obj):
        Fgrav = gravity(obj.mass, self.mass, self.get_home_radius)
        Fgravx = Fgrav*(np.sqrt((selfpos[0]**2)/(self.get_home_radius**2)))
        Fgravy = Fgrav*(np.sqrt((selfpos[1]**2)/(self.get_home_radius**2)))
        Fgravz = Fgrav*(np.sqrt((selfpos[2]**2)/(self.get_home_radius**2)))
        return [Fgravx, Fgravy, Fgravz]
    
    def resolve_thrust(self): # yaw, pitch, roll -> x, y, z
        x = self.F*(np.cos(self.angle[0])*np.cos(self.angle[1]))
        y = self.F*(np.sin(self.angle[1]))
        z = self.F*(np.sin(self.angle[0])*np.cos(self.angle[1]))
        return [x, y, z]
    
class planet:
    class atmosphere:
        def __init__(self):
        
        def atmos_pressure(P0, Mm, T, h):  # P0 = Pressure at sea Level
            P = P0 * np.exp((-1 * (Mm * 9.807) / (8.3145 * T)) * h)
            return P
    
    def __init__(self, mass, radius, p0, molMass):
        self.mass, self.radius, self.p0, self.molMass = (mass, radius, p0, molMass)
        atmosphere = self.atmosphere()


# In[12]:

objects = []
Earth = planet(5.972e24, 6371e3, 101325, 0.02896)
objects.append(Earth)

saturnv = rocket()


# In[59]:

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = plt.axes(projection='3d')

saturnv.F = 500
saturnv.pos = [0, 6371e3, 0]
saturnv.angle = [0, 90, 0]
saturnv.angle = np.radians(saturnv.angle)
x = []
y = []
z = []
for i in range(10):
    F = saturnv.resolve_thrust()
    saturnv.pos[0] = saturnv.pos[0] + F[0]
    print
    saturnv.pos[1] = saturnv.pos[1] + F[1]
    saturnv.pos[2] = saturnv.pos[2] + F[2]
    x.append(saturnv.pos[0])
    y.append(saturnv.pos[1])
    z.append(saturnv.pos[2])
    #saturnv.angle[0] = saturnv.angle[0]+np.radians(0.01)
    #saturnv.angle[1] = saturnv.angle[1]+np.radians(1)

print(F)
ax.plot(x, y, z, '-b')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()


# In[ ]:


