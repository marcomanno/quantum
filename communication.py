
from matrices import *

sp.var('a b')
state = dict({0 : a, 1 : b})
oo(state, "0")

state = apply(state, H, 1)
oo(state, "H1")

state = apply2(state, CNOT, 2, 1)
oo(state, "CNOT1")

state = apply2(state, CNOT, 1, 0)
oo(state, "CNOT2")

state = apply(state, H, 0)
oo(state, "H2")

select_state(state, [0, 0])
select_state(state, [1, 0])
select_state(state, [0, 1])
select_state(state, [1, 1])
print("=================")

state = apply2(state, CNOT, 2, 1)
oo(state, "CNOT3")

state = apply2(state, CZ, 2, 0)
oo(state, "CZ")
