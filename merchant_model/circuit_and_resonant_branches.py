from typing import Sequence
import numpy as np


class ResonantBranch:
    def __init__(self, K: int = 0, R: int = 0, M: int = 0):
        self.K = K * 10**8
        self.R = R * 10**5
        self.M = M * 10**2

    def get_impedance(self, omega):
        self.impedance = self.M * omega * 1j + self.R + self.K / (omega * 1j)
        return self.impedance


class CircuitHelpers:
    @staticmethod
    def parallel_impedances(z_list: tuple = ()):
        running_sum = 0
        for z in z_list:
            running_sum += 1 / z
        return 1 / running_sum

    @staticmethod
    def branch_parallel_impedances(branch_list:Sequence, f:int):
        running_sum = 0
        for branch in branch_list:
            running_sum += 1/branch.get_impedance(2*np.pi*f)
        
        return 1/running_sum



