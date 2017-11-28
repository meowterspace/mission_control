
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

def thrust(q, Ve, Pe, Pa, Ae):  # q = rate of ejected mass flow, Ve = exhaust gas ejection speed
    F = q * Ve + (Pe - Pa) * Ae # Pe = pressure of exhaust gasses, Pa = pressure of ambient atmosphere
    return F                    # Ae = area of exit

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

