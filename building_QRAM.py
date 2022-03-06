#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def qRAM(thetas):
    """Function that generates the superposition state explained above given the thetas angles.

    Args:
        - thetas (list(float)): list of angles to apply in the rotations.

    Returns:
        - (list(complex)): final state.
    """

    def RY(param):
        qml.RY(param,wires=3)
     
    CCCRY = qml.ctrl(RY, control=[0,1,2])

    def add_memory(state, param):

        bits = []
        for i in range(2,-1,-1):
            bits.append(state%2)
            state = state//2
            if bits[-1]==0:
                qml.PauliX(wires=i)
        CCCRY(param)
        for i in range(3):
            if bits[i]==0:
                qml.PauliX(wires=2-i)

    dev = qml.device("default.qubit", wires=range(4))

    @qml.qnode(dev)
    def circuit():

        for i in range(3):
            qml.Hadamard(wires=i)

        for i in range(8):
            add_memory(i,thetas[i])

        return qml.state()
    return circuit()


if __name__ == "__main__":
    inputs = sys.stdin.read().split(",")
    thetas = np.array(inputs, dtype=float)

    output = qRAM(thetas)
    output = [float(i.real.round(6)) for i in output]
    print(*output, sep=",")
