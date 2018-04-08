import numpy as np

OBJECTS = [] # a list of all the objects instantiated into the simulation

data = {
  'p_acc' : [None, None, None],    #player accelleration
  'p_vel' : [None, None, None], #player velocity
  'p_pos' : [None, None, None],    #player position
  'p_ang' : [None, None, None],    #player angle
  'p_fue' : '',    #player fuel              <<<<< ADD IN TO GAME
  'p_thm' : 0,    #player thrust multiplyer <<<<< ADD IN TO GAME
  'p_sta' : True,    #player status            <<<<< ^
  'p_orb' : False,    #player orbit 
}

def resolve(vector):
    r = np.sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))

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
        Fgrav = self.gravity(obj)
        Fgravx = self.pos[0]/self.distance(obj)*Fgrav
        Fgravy = self.pos[1]/self.distance(obj)*Fgrav
        Fgravz = self.pos[2]/self.distance(obj)*Fgrav
        return [Fgravx, Fgravy, Fgravz]

    def collision_test(self, object): #rocket, planet
        if (self.length > self.radius):
            brad = self.length
        else:
            brad = self.radius
        d = self.distance(object) - brad - object.radius
        if (d == 0):
            if (np.mod(resolve(self.V)-resolve(object.V)) < 10):
                velocity_ratio = [None, None, None]
                velocity_ratio[0] = self.v[0] / resolve(self.V)
                velocity_ratio[1] = body.v[1] / resolve(self.V)
                velocity_ratio[2] = body.v[2] / resolve(self.V)
                pb = self.mass * resolve(self.V)
                po = object.mass * resolve(object.V)
                vr = (pb + po) / (object.mass + self.mass)
                self.V = [vr*velocity_ratio[0], vr*velocity_ratio[1], vr*velocity_ratio[2]]
                object.V = [vr*velocity_ratio[0], vr*velocity_ratio[1], vr*velocity_ratio[2]]
            elif (d < 0):
                #die
                pass
            else:
                # die
                pass


class Planet(GameObject):
    class Atmosphere(GameObject):
        def __init__(self, mass, radius, pos, V, a, p0, molMass):
            super().__init__(mass, radius, pos, V, a)
            self.mass, self.p0, self.molMass = mass, p0, molMass
        
        def pressure(self, T, h):
            g = (self.mass*6.67408e-11)/(self.radius+h) # check this works, i'm a bit dubious
            P = self.p0 * np.exp((-1 * (self.molMass * g) / (8.3145 * T)) * h)
            return P

    def __init__(self, mass, radius, pos, V, a, p0, molMass):
        super().__init__(mass, radius, pos, V, a)
        atmosphere = self.Atmosphere(mass, radius, pos, V, a, p0, molMass)
        self.atmosphere = atmosphere

        
class Rocket(GameObject):
    def __init__(self, mass, length, radius, F, pos, angle, V, a, q, Ve, Pe, Cd, Vg, Ae, Fuel):
        super().__init__(mass, radius, pos, V, a)
        self.length, self.F, self.angle = length, F, angle
        self.q, self.Ve, self.Pe, self.Ae = q, Ve, Pe, Ae
        self.Cd, self.Vg, self.fuel = Cd, Vg, Fuel
        self.thm = 0;
    def resolve_thrust(self): # yaw, pitch, roll -> x, y, z
        x = self.F*(np.cos(self.angle[0])*np.cos(self.angle[1]))
        y = self.F*(np.sin(self.angle[1]))
        z = self.F*(np.sin(self.angle[0])*np.cos(self.angle[1]))
        return [x, y, z]

    def thrust(self, planet):  # q = rate of ejected mass flow, Ve = exhaust gas ejection speed

        F = self.q * self.Ve + (self.Pe - planet.atmosphere.pressure(285, self.distance(planet)-planet.radius)) * self.Ae  # Pe = pressure of exhaust gasses, Pa = pressure of ambient atmosphere   !! SET TO 285K STATIC <FF024EA5.xxc>
                                                              
        return F  # Ae = area of exit

    def drag_area(V, a, r, h):
        area = r*h
        top = np.arcos((V[0]*a[0]+V[1]*a[1]+V[2]*a[2]))
        bottom = ((np.sqrt((a[0]**2)+(a[1]**2)+(a[1]**2)))*np.sqrt((V[0]**2)+(V[1]**2)+(V[1]**2)))
        area = area * (top/bottom)
        return area

    def drag(planet, T, h):  # P = Pressure /PA, T = temp(k), Vg = velocity
        F = 0.5 * ((planet.pressure(T, h) / (286 * T)) * (self.V ** 2) * self.Cd * self.drag_area(self.V, self.a, self.radius, self.length))  # Cd = Coefficient of drag, A = area in drag
        return F

    def die():
        return True









def make_planet(Planet, name, mass, radius, pos, V, a, p0, molMass):
    exec(str(name)+' = Planet('+str(mass)+','+str(radius)+','+str(pos)+','+str(V)+','+str(a)+','+'p0'+','+str(molMass)+')')
    exec('OBJECTS.append( ['+str(name)+', "planet"] )')
    

# funct:
def setup():
    global OBJECTS
    #make_planet(Planet, 'Earth', 5.972e24, 6371e3, [0, 0, 0], [0, 0, 0], [0, 0, 0], 101325, 0.02896)
    Earth = Planet(5.972e24, 6371e3, [0, 0, 0], [0, 0, 0], [0, 0, 0], 101325, 0.02896)
    OBJECTS.append([Earth, 'planet'])
    player = Rocket(100, 3, 0.5, 0, [6e24, 0, 0], [90, 0, 0], [0, 0, 0], [0, 0, 0], 30, 3100, 5000, 0.7, 50, 2, 10000) # VARIABLES !!!! Vg & Fuel set randomly, please change
    OBJECTS.append([player, 'player'])
    return player



def run(planet, player, response_t):
    global OBJECTS
    global data
    #print(player.pos)
    F = [0, 0, 0]
    player.F = [0, 0, 0]
    player.F = player.thrust(planet)*player.thm
    F = player.resolve_thrust()
    for i in OBJECTS:
        if i[1] == 'planet':
        #    F = F - player.drag(i[0], 285, player.distance(i[0] - i[0].radius)) # TEMPERATURE SET TO CONST 285K 
            F = [F[0]+player.get_grav_vector(i[0])[0], F[1]+player.get_grav_vector(i[0])[1],F[2]+player.get_grav_vector(i[0])[2]]

            if (i != 'player'):
                player.collision_test(i[0])
    player.F = F
    player.a = [player.F[0]/player.mass, player.F[1]/player.mass, player.F[2]/player.mass] # a = f/m
    u = player.V
    player.V = [player.V[0]+player.a[0]*response_t, player.V[1]+player.a[1]*response_t, player.V[2]+player.a[2]*response_t] # v = u+at
    s = [(u[0]*response_t) + (0.5*player.a[0]*(response_t**2)), (u[1]*response_t) + (0.5*player.a[1]*(response_t**2)), (u[2]*response_t) + (0.5*player.a[2]*(response_t**2))]
    player.pos = [player.pos[0]+s[0], player.pos[1]+s[1], player.pos[2]+s[2]]
    
    #print('F = '+str(player.F))
    #print('a = '+str(player.a))
    #print('v = '+str(player.V))
    #print('x = '+str(player.pos[0]))
    #print('y = '+str(player.pos[1]))
    #print('z = '+str(player.pos[2]))

    data['p_acc'] = player.a
    data['p_vel'] = player.V
    data['p_pos'] = player.pos
    data['p_ang'] = player.angle
    data['p_fue'] = 100 # ADD THIS
    data['p_thm'] = player.thm # ADD THIS
    data['p_sta'] = True # ADD THIS
    data['p_orb'] = False # ADD THIS


def update(player, data):
    global OBJECTS
    player.a = data['p_acc']
    player.V = data['p_vel']
    player.pos = data['p_pos']
    player.angle = data['p_ang']
    player.thm = data['p_thm']
    #FUE, THM, STA, ORB



# Create All objects E.g. Planets \/
# Create rocket \/
# Set up rocket \/
# make game.time variable (probably in main run script)
# funct:
# run calculations:
# STA Drag 3 - LAST
# STA Thrust 1
# STA Grav 2
# STA 

#Player = setup()
#print('ok')
#for object in OBJECTS:
#    if object[1] == 'planet':
#        for i in range(100):
#            print(i)
#            run(object[0], Player, 1)
            