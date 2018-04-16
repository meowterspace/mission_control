import numpy as np

OBJECTS = [] # a list of all the objects instantiated into the simulation

data = {
  'p_acc' : [None, None, None],    #player accelleration
  'p_vel' : [None, None, None],    #player velocity
  'p_pos' : [None, None, None],    #player position
  'p_ang' : [None, None, None],    #player angle
  'p_fue' : '',    #player fuel              
  'p_thm' : 0,    #player thrust multiplier 
  'p_sta' : True,    #player status           
  'p_orb' : False,    #player orbit 
}

# Resolves a 3 Dimentional vector into a 1D scalar
def resolve(vector):
    r = np.sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))

# This superclass is for every object in this game (planet, rocket etc)
class GameObject():
    def __init__(self, mass, radius, pos, V, a): # setup key variables required for
        self.mass, self.radius = mass, radius    # every gameObject.
        self.pos, self.V, self.a = pos, V, a

# This function calculates the scalar distance between two objects in the game
    def distance(self, obj):
        d = [None, None, None]
        d[0] = self.pos[0]-obj.pos[0]
        d[1] = self.pos[1]-obj.pos[1]
        d[2] = self.pos[2]-obj.pos[2]
        r = np.sqrt((d[0]**2)+(d[1]**2)+(d[2]**2))
        return r

# This function calculates the gravitational attraction one objected experiences 
# as a result of another's mass in the game
    def gravity(self, obj):
        F = (6.67408e-11 * obj.mass * self.mass) / (self.distance(obj)**2)
        return F

# This can split a scalar gravitational attraction from the above function into a 3D vector
# product.
    def get_grav_vector(self, obj):
        Fgrav = self.gravity(obj)
        Fgravx = self.pos[0]/self.distance(obj)*Fgrav
        Fgravy = self.pos[1]/self.distance(obj)*Fgrav
        Fgravz = self.pos[2]/self.distance(obj)*Fgrav
        return [Fgravx, Fgravy, Fgravz]

# This function tests if two object's overlapp by comparing their distance from each other and 
# taking away the radius of both to see if they are colliding.
    def collision_test(self, object): #rocket, planet
        if (self.length > self.radius):
            brad = self.length
        else:
            brad = self.radius
        d = self.distance(object) - brad - object.radius
        if (d == 0):
            if (np.mod(resolve(self.V)-resolve(object.V)) < 10):  # if it is resting on a surface
                velocity_ratio = [None, None, None]               # but not moving this uses momentum
                velocity_ratio[0] = self.v[0] / resolve(self.V)   # to equal out the forces (so a rocket
                velocity_ratio[1] = body.v[1] / resolve(self.V)   # could sit on earth without falling 
                velocity_ratio[2] = body.v[2] / resolve(self.V)   # through it)
                pb = self.mass * resolve(self.V)
                po = object.mass * resolve(object.V)
                vr = (pb + po) / (object.mass + self.mass)
                self.V = [vr*velocity_ratio[0], vr*velocity_ratio[1], vr*velocity_ratio[2]]
                object.V = [vr*velocity_ratio[0], vr*velocity_ratio[1], vr*velocity_ratio[2]]
            else:
                print('Player died: Speed of Collision') # if the player hits another object too fast
                pass
       elif (d < 0): # If the player is inside another object
            print('Player died: Collision')
                

# This class is for a Planet. It inherits from GameObject
class Planet(GameObject):
    class Atmosphere(GameObject): # This is the atmosphere class of the planet. It can be accessed by 
                                  # Planet.Atmosphere (Earth.Atmosphere)
        def __init__(self, mass, radius, pos, V, a, p0, molMass):  # Constructor
            super().__init__(mass, radius, pos, V, a)
            self.mass, self.p0, self.molMass = mass, p0, molMass 
        
        # Calculates the atmopheric pressure at a certain altitude above the planet
        def pressure(self, T, h):
            g = (self.mass*6.67408e-11)/(self.radius+h) # check this works, i'm a bit dubious
            P = self.p0 * np.exp((-1 * (self.molMass * g) / (8.3145 * T)) * h)
            return P

    def __init__(self, mass, radius, pos, V, a, p0, molMass):
        super().__init__(mass, radius, pos, V, a)
        atmosphere = self.Atmosphere(mass, radius, pos, V, a, p0, molMass)
        self.atmosphere = atmosphere

# This class is for the rocket game object. It inherits from GameObject
class Rocket(GameObject):
    def __init__(self, mass, length, radius, F, pos, angle, V, a, q, Ve, Pe, Cd, Vg, Ae, Fuel):
        super().__init__(mass, radius, pos, V, a)  # initiates gameObject's constructor
        self.length, self.F, self.angle = length, F, angle  # This constructor sets up all the key variables
        self.q, self.Ve, self.Pe, self.Ae = q, Ve, Pe, Ae   # needed for the rocket class
        self.Cd, self.Vg, self.fuel = Cd, Vg, Fuel
        self.thm = 0;

    # This function takes a scalar Thrust F and using the angle will convert it into a 3D vector force.
    def resolve_thrust(self): # yaw, pitch, roll -> x, y, z
        x = self.F*(np.cos(self.angle[0])*np.cos(self.angle[1]))
        y = self.F*(np.sin(self.angle[1]))
        z = self.F*(np.sin(self.angle[0])*np.cos(self.angle[1]))
        return [x, y, z]

    # This function calculates the Thrust of the rocket
    def thrust(self, planet): 
        F = self.q * self.Ve + (self.Pe - planet.atmosphere.pressure(285, self.distance(planet)-planet.radius)) * self.Ae  
 
    # This function calculates the area of the rocket that is in drag at any one time
    def drag_area(V, a, r, h):
        area = r*h
        top = np.arcos((V[0]*a[0]+V[1]*a[1]+V[2]*a[2]))
        bottom = ((np.sqrt((a[0]**2)+(a[1]**2)+(a[1]**2)))*np.sqrt((V[0]**2)+(V[1]**2)+(V[1]**2)))
        area = area * (top/bottom)
        return area

    # This function uses the drag_area from above to calculate the total drag force experienced by the rocket
    def drag(planet, T, h): 
        F = 0.5 * ((planet.pressure(T, h) / (286 * T)) * (self.V ** 2) * self.Cd * self.drag_area(self.V, self.a, self.radius, self.length))  # Cd = Coefficient of drag, A = area in drag
        return F



# This function is used to dynamically instantiate a Planet object if admin/host ever wants to throw in planets randomly 
# throughout the game, or if a nicer user interface comes into play at a later date to add planets from an array / dictionary
# rather than hard coding it in.
def make_planet(Planet, name, mass, radius, pos, V, a, p0, molMass):
    exec(str(name)+' = Planet('+str(mass)+','+str(radius)+','+str(pos)+','+str(V)+','+str(a)+','+'p0'+','+str(molMass)+')')
    exec('OBJECTS.append( ['+str(name)+', "planet"] )') # Appends planet to list of game objects
    

# This function sets up the simulation
def setup(): 
    global OBJECTS
    Earth = Planet(5.972e24, 6371e3, [0, 0, 0], [0, 0, 0], [0, 0, 0], 101325, 0.02896) # Instantiates planet Earth
    OBJECTS.append([Earth, 'planet']) # Adds earth to list of game objects so it can be itterated over
    player = Rocket(100, 3, 0.5, 0, [6e24, 0, 0], [90, 0, 0], [0, 0, 0], [0, 0, 0], 30, 3100, 5000, 0.7, 50, 2, 10000) # Sets up the player object
    OBJECTS.append([player, 'player']) # Adds player to the list of game obects
    return player # returns player so it can be used in the server thread.


# Below is the code that actually runs the simulation. It is called itteratively by the server.
# It combines all the different component foces and determines a resultant force.
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
    player.F = F # Resultant force calculated
    # This then converts the Force into accelleration of the rocket
    player.a = [player.F[0]/player.mass, player.F[1]/player.mass, player.F[2]/player.mass] 
    u = player.V

    # From the accelleration and the past position the below finds the new position in the game.
    player.V = [player.V[0]+player.a[0]*response_t, player.V[1]+player.a[1]*response_t, player.V[2]+player.a[2]*response_t] 
    s = [(u[0]*response_t) + (0.5*player.a[0]*(response_t**2)), (u[1]*response_t) + (0.5*player.a[1]*(response_t**2)), (u[2]*response_t) + (0.5*player.a[2]*(response_t**2))]
    player.pos = [player.pos[0]+s[0], player.pos[1]+s[1], player.pos[2]+s[2]]
    
    # This updates the data dictionary for the server to refer to.
    data['p_acc'] = player.a
    data['p_vel'] = player.V
    data['p_pos'] = player.pos
    data['p_ang'] = player.angle
    data['p_fue'] = 100 # ADD THIS
    data['p_thm'] = player.thm # ADD THIS
    data['p_sta'] = True # ADD THIS
    data['p_orb'] = False # ADD THIS

# This function allows the server to update information sent by the client to the server.
# it takes new data and updates only the angle and the thrust % because those are the only
# two user inputs available. If we updated the entire dataset recieved then users could
# send malicious websocket requests with different position data etc to either cheat or sabotage
# a game.
def update(player, data):
    global OBJECTS
    player.angle = data['p_ang']
    player.thm = data['p_thm']


