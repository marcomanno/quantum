import numpy as np
import sympy as sp
import math

X=np.matrix([[0, 1],[1, 0]])
Y=np.matrix([[0, -1j],[1j, 0]])
Z=np.matrix([[1, 0],[0, -1]])
H=np.matrix([[1, 1], [1, -1 ]]) / math.sqrt(2)
NOT05 = np.matrix([[0.5+0.5j, 0.5-0.5j], [0.5-0.5j, 0.5+0.5j]])
CNOT = np.matrix([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1],
                  [0, 0, 1, 0]])

CZ = np.matrix([[1, 0, 0, 0],
                [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0,-1]])

SWP=np.matrix([[1, 0, 0, 0],
  [0, 0, 1, 0],
  [0, 1, 0, 0],
  [0, 0, 0, 1]])

def oo(state, label):
    print(label, ' = ', sorted(state.items(), key=lambda x: x[0]))

def add_to_dictionary(my_dict, index, val):
    if not index in my_dict:
        my_dict[index] = 0
    my_dict[index] += val

def apply(state, M, n):
    new_state = dict()
    for substate, p in state.items():
        qbit = [0,0]
        sel = 1 << n
        state_idx = 0
        if (substate & sel) != 0:
            state_idx += 1
        qbit[state_idx] = 1
        new_qbit = qbit * M
        for i in range(new_qbit.shape[1]):
            if new_qbit[0, i] == 0:
                continue
            if i > 0:  
                add_to_dictionary(new_state, substate | sel, new_qbit[0, i] * p)
            else:
                add_to_dictionary(new_state, substate & (~sel), new_qbit[0, i] * p)
    return new_state

def apply2(state, M, i0, i1):
    new_state = dict()
    for substate, p in state.items():
        qbit = [0, 0, 0, 0]
        state_idx = 0
        if (substate & (1 << i0)) != 0:
            state_idx += 1
        if (substate & (1 << i1)) != 0:
            state_idx += 2
        #print("substate", substate, "i0", i0, "i1", i1, "state_idx", state_idx)
        qbit[state_idx] = 1
        #print("qbit", qbit)
        new_qbit = qbit * M
        #print("new_qbit", new_qbit)
        for i in range(new_qbit.shape[1]):
            if new_qbit[0, i] == 0:
                continue
            new_substate = substate
            if (i & 1) != 0:
                new_substate |= 1 << i0
            else:
                new_substate &= ~(1 << i0)
            if (i & 2) != 0:
                new_substate |= 1 << i1
            else:
                new_substate &= ~(1 << i1)
            add_to_dictionary(new_state, new_substate, new_qbit[0, i] * p)
    return new_state

def select_state(state, bits):
    new_state = dict()
    for substate, p in state.items():
        i = 0
        for b in bits:
            if b >= 0 and b < 2 and ((substate >> i) & 1) != b:
                i = -1
                break
            i += 1
        if i > 0:
            new_state[substate] = p
    oo(new_state, bits)

