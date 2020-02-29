from matrices import *
from scipy import linalg

state = dict({0 : 0.5, 2 : 0.5, 8 : 0.5, 10 : 0.5})
oo(state, "INIT")

state = apply(state, H, 0)
state = apply2(state, CX, 2, 0)
oo(state, "HCX")

state = apply(state, X025_inv, 0)
oo(state, "X^-025")


state = apply(state, H, 1)
state = apply(state, H, 3)
oo(state, "H")

state = apply2(state, CX05, 0, 1)
state = apply2(state, CX05, 2, 3)
oo(state, "CX05")

measure(state)
