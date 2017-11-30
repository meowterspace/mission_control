import numpy as np


# import matplotlib.pyplot as mpl

def atmos_pressure(P0, Mm, T, h):  # P0 = Pressure at sea Level
    P = P0 * np.exp((-1 * (Mm * 9.807) / (8.3145 * T)) * h)
    return P


def drag(P, T, Vg, Cd, A):  # P = Pressure /PA, T = temp(k), Vg = flow velocity of gas

    F = 0.5 * ((P / (286 * T)) * (Vg ** 2) * Cd * A)  # Cd = Coefficient of drag, A = area in drag
    return F


def gravity(M, m, r):  # P = Pressure, T = temp(k), Vg = flow velocity of gas
    F = (6.67408e-11 * M * m) / (r ** 2)  # Cd = Coefficient of drag, A = area in drag
    return F


def thrust(q, Ve, Pe, Pa, Ae):  # q = rate of ejected mass flow, Ve = exhaust gas ejection speed
    F = q * Ve + (Pe - Pa) * Ae  # Pe = pressure of exhaust gasses, Pa = pressure of ambient atmosphere
    return F  # Ae = area of exit


# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

data = []
heights = []

for h in range(100000):
    P = atmos_pressure(101325, 0.02896, 288.15, h)
    F = thrust(30, 3100, 5000, P, 0.7)

    F = F - (gravity(5.927e24, 100, (6.371e6 + h)))
    r = drag(P, 288.15, 30, 0.5, 1)
    F = F - drag(P, 288.15, 30, 0.5, 1)

    print(r, F, h)
    data.append(r)
    heights.append(h)

mpl.plot(data, heights)
mpl.show()


