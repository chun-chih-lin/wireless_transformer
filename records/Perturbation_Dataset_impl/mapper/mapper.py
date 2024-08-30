import numpy as np

def get_angle(sym):
    return np.angle(sym, deg=True)

def bpsk(sym):
    print("BPSK---------------------------")
    magitude = np.max(np.abs(sym))
    sym = sym/magitude
    angle = get_angle(sym)
    print(f"{magitude = }, {angle = }, {sym = }")



    return False 
    pass

def qpsk(sym): 

    return False
    pass

def qam16(sym): 
    return False
    pass

def qam64(sym): 
    angle = get_angle(sym)
    print(angle, np.abs(sym))
    return False
    pass
