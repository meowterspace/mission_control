
import numpy as np



# In[5]:

def distance(base, obj):
    d = [None, None, None]
    d[0] = base.pos[0]-obj.pos[0]
    d[1] = base.pos[1]-obj.pos[1]
    d[2] = base.pos[2]-obj.pos[2]
    r = np.sqrt((d[0]**2)+(d[1]**2)+(d[2]**2))
    return r

# coding: utf-8

# In[1]:

import numpy as np


# In[2]:

def drag(P, T, Vg, Cd, A):  # P = Pressure /PA, T = temp(k), Vg = flow velocity of gas

    F = 0.5 * ((P / (286 * T)) * (Vg ** 2) * Cd * A)  # Cd = Coefficient of drag, A = area in drag
    return F


def gravity(M, m, r):
	
	F = (6.67408e-11 * M * m) / (r**2)
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
        Fgrav = gravity(obj.mass, self.mass, self.get_home_radius())
        #Fgravx = Fgrav*(np.sqrt((self.pos[0]**2)/(self.get_home_radius()**2)))
        #Fgravy = Fgrav*(np.sqrt((self.pos[1]**2)/(self.get_home_radius()**2)))
        #Fgravz = Fgrav*(np.sqrt((self.pos[2]**2)/(self.get_home_radius()**2)))
        Fgravx = self.pos[0]/self.get_home_radius()*Fgrav
        Fgravy = self.pos[1]/self.get_home_radius()*Fgrav
        Fgravz = self.pos[2]/self.get_home_radius()*Fgrav
        #if Fgravx**2+Fgravy**2+Fgravz**2 != Fgrav**2: print("BAD")
        return [Fgravx, Fgravy, Fgravz]
    
    def resolve_thrust(self): # yaw, pitch, roll -> x, y, z
        x = self.F*(np.cos(self.angle[0])*np.cos(self.angle[1]))
        y = self.F*(np.sin(self.angle[1]))
        z = self.F*(np.sin(self.angle[0])*np.cos(self.angle[1]))
        return [x, y, z]
    
class planet:
    class atmosphere:
        def __init__(self):
        	pass
        def atmos_pressure(P0, Mm, T, h):  # P0 = Pressure at sea Level
            P = P0 * np.exp((-1 * (Mm * 9.807) / (8.3145 * T)) * h)
            return P
    
    def __init__(self, mass, radius, p0, molMass, pos):
        self.mass, self.radius, self.p0, self.molMass, self.pos = (mass, radius, p0, molMass, pos)
        atmosphere = self.atmosphere()
        


# In[12]:

objects = []
Earth = planet(5.972e24, 6371e3, 101325, 0.02896, [0, 0, 0])
objects.append(Earth)

saturnv = rocket()


# In[59]:

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = plt.axes(projection='3d')

# ---- SIM > Rocket moving through atmosphere
"""
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
    print                                     #Something meant to go here?
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
"""

# In[ ]:
# ---- SIM > Orbit (hopefully)
saturnv.mass = 500
saturnv.a = [0, 0, 0]
saturnv.F = 0
saturnv.pos = [0, 6779e3, 0] # 408km above Earth's surface
saturnv.V = [7800, 0, 0]


print("{{{a = "+str(type(saturnv.a).__name__)+"}}}")
print("{{{"+str(type(saturnv.V).__name__)+"}}}")
#print("{{{"+str(type(F).__name__)+"}}}")

DATA = []
bob = []


for j in range(100000):  #issue[372] increase &  see object flyyyyyyy into deep space
	F = gravity(Earth.mass, saturnv.mass, saturnv.get_home_radius())
	F = saturnv.get_grav_vector(Earth)
	F = [-F[0],-F[1],-F[2]]
	for i in range(3):
		saturnv.a[i] = (F[i] / saturnv.mass)
		saturnv.V[i] = saturnv.V[i] + saturnv.a[i]*0.1 # 0.1 = tick
		saturnv.pos[i] = saturnv.pos[i] + saturnv.V[i]*0.1
	x = saturnv.pos
	DATA.append([x[0], x[1], x[2]])



DATA = np.array(DATA)
DATA = np.transpose(DATA)
print('-------------------------')
print(DATA)
ax.plot(DATA[0], DATA[1], DATA[2], '-b')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()

plt.plot(DATA[0], DATA[1], '-b')
plt.show()


print(distance(saturnv, Earth))

