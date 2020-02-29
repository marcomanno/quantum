import scipy.linalg
import math
import cmath
import numpy as np
import sympy as sp

theta = sp.symbols('theta')

X=np.matrix([[0, 1],[1, 0]])
Y=np.matrix([[0, -1j],[1j, 0]])
Z=np.matrix([[1, 0],[0, -1]])
H=np.matrix([[1, 1], [1, -1 ]]) / math.sqrt(2)
X05 = np.matrix([[0.5+0.5j, 0.5-0.5j], [0.5-0.5j, 0.5+0.5j]])
X05_inv = np.asmatrix(scipy.linalg.inv(X05))
X025 = np.asmatrix(scipy.linalg.fractional_matrix_power(X05,0.5))
X025_inv = np.asmatrix(scipy.linalg.inv(X025))
CX = np.matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 1],
               [0, 0, 1, 0]])

CX05 = np.matrix([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0j, 0j],
                  [0, 0, 0j, 0j]])
CX05[2:4,2:4] = X05

CZ = np.matrix([[1, 0, 0, 0],
                [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0,-1]])

SWP = np.matrix([[1, 0, 0, 0],
  [0, 0, 1, 0],
  [0, 1, 0, 0],
  [0, 0, 0, 1]])

def oo(state, label):
    print("===State: ", label)
    print(sorted(state.items(), key=lambda x: x[0]))
    prob = 0
    for substate, p in state.items():
        r, t = cmath.polar(p)
        prob += r * r
    print("States prob = ", prob)

def add_to_dictionary(my_dict, index, val):
    if not index in my_dict:
        my_dict[index] = 0
    my_dict[index] += val

def apply(state, M, n):
    new_state = dict()
    for substate, p in state.items():
        qbit = [0, 0]
        sel = 1 << n
        state_idx = 0
        if (substate & sel) != 0:
            state_idx += 1
        qbit[state_idx] = 1
        new_qbit = np.matmul(qbit, M)
        for i in range(new_qbit.shape[1]):
            if new_qbit[0, i] != 0:
                if i > 0:
                    new_substate = substate | sel
                else:
                    new_substate = substate & (~sel)
                add_to_dictionary(new_state, new_substate, new_qbit[0, i] * p)
    return new_state

def apply2(state, M, n, i_control):
    new_state = dict()
    for substate, p in state.items():
        qbit = [0, 0, 0, 0]
        state_idx = 0
        if (substate & (1 << n)) != 0:
            state_idx += 1
        if (substate & (1 << i_control)) != 0:
            state_idx += 2
        #print("substate", substate, "n", n, "i_control", i_control, "state_idx", state_idx)
        qbit[state_idx] = 1
        #print("qbit", qbit)
        new_qbit = np.matmul(qbit, M)
        #print("new_qbit", new_qbit)
        for i in range(new_qbit.shape[1]):
            if new_qbit[0, i] == 0:
                continue
            new_substate = substate
            if (i & 1) != 0:
                new_substate |= 1 << n
            else:
                new_substate &= ~(1 << n)
            if (i & 2) != 0:
                new_substate |= 1 << i_control
            else:
                new_substate &= ~(1 << i_control)
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

def measure(state):
    print("measure:")
    probs = [0, 0]
    for substate, p in state.items():
        prob = p.real**2+p.imag**2
        if prob > 0:
            print("State =" , "{0:04b}".format(substate), ",p = ", prob)
        a = (substate & 2) > 0
        b = (substate & 8) > 0
        ra = (substate & 1) > 0
        rb = (substate & 4) > 0
        success = ((ra ^ rb) == (a & b))
        probs[success] += prob

    print(probs)

