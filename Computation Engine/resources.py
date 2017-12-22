import numpy as np

objects = [] # a list of all the objects instantiated into the simulation

class GameObject():
	def __init__(self, mass, radius, pos, V, a):
		self.mass, self.radius = mass, radius
		self.pos, self.V, self.a = pos, V, a

	def distance(self, obj):
    	d = [None, None, None]
    	d[0] = self.pos[0]-obj.pos[0]
    	d[1] = self.pos[1]-obj.pos[1]
    	d[2] = self.pos[2]-obj.pos[2]
    	r = np.sqrt((d[0]**2)+(d[1]**2)+(d[2]**2))
    	return r

    def gravity(self, obj):
    	F = (6.67408e-11 * obj.mass * self.mass) / (self.distance(obj)**2)
		return F

    def get_grav_vector(self, obj):
        Fgrav = gravity(obj.mass, self.mass, self.get_home_radius())
        Fgravx = self.pos[0]/self.distance(obj)*Fgrav
        Fgravy = self.pos[1]/self.distance(obj)*Fgrav
        Fgravz = self.pos[2]/self.distance(obj)*Fgrav
        return [Fgravx, Fgravy, Fgravz]


class Planet(gameObject):
	class Atmosphere:
		def __init__(self, p0, molMass):

			self.p0, self.molMass = p0, molMass

			def pressure(self, T, h):
				g = gravity(super().mass) # check this works, i'm a bit dubious
				P = self.p0 * np.exp((-1 * (self.molMass * g) / (8.3145 * T)) * h)
            	return P

	def __init__(self, mass, radius, pos, V, a, p0, molMass):
		super().__init__(mass, radius, pos, V, a)
		atmosphere = self.atmosphere(p0, molMass)
		

class Rocket(gameObject):
	def __init__(self, mass, length, radius, F, pos, angle, V, a, q, Ve, Pe, Pa, Ae, Cd, Vg):
		super().__init__(mass, raidus, pos, V, a)
		self.length, self.F, self.angle = length, F, angle
		self.q, self.Ve, self.Pe, self.Pa, self.Ae = q, Ve, Pe, Pa, Ae
		self.Cd, self.Vg = Cd, Vg
    def resolve_thrust(self): # yaw, pitch, roll -> x, y, z
        x = self.F*(np.cos(self.angle[0])*np.cos(self.angle[1]))
        y = self.F*(np.sin(self.angle[1]))
        z = self.F*(np.sin(self.angle[0])*np.cos(self.angle[1]))
        return [x, y, z]

    def thrust(self):  # q = rate of ejected mass flow, Ve = exhaust gas ejection speed
    	F = q * Ve + (Pe - Pa) * Ae  # Pe = pressure of exhaust gasses, Pa = pressure of ambient atmosphere
    	return F  # Ae = area of exit

    def drag_area():
    	pass

    def drag(planet, T, h):  # P = Pressure /PA, T = temp(k), Vg = flow velocity of gas
    	F = 0.5 * ((planet.pressure(T, h) / (286 * T)) * (self.Vg ** 2) * self.Cd * drag_area())  # Cd = Coefficient of drag, A = area in drag
    	return F







Earth = Planet(5.972e24, 6371e3, 101325, 0.02896, [0, 0, 0])
zero = [0, 0, 0]

