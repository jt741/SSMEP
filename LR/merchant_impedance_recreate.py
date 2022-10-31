import numpy as np
from plotting_helper import simple_plot, log_plot
import cmath

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
    def branch_parallel_impedances(branch_list:tuple, f:int):
        running_sum = 0
        for branch in branch_list:
            running_sum += 1/branch.get_impedance(2*np.pi*f)
        
        return 1/running_sum


def generate_impedance_frequency_response(branches, start_f=100, stop_f=8000,):
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    middle_ear_impedances_magnitude = []
    middle_ear_impedances_phase = []
    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(branches, f)

        middle_ear_impedances_magnitude.append(abs(Z_me))
        middle_ear_impedances_phase.append(cmath.phase(Z_me))
    
    return frequencies, middle_ear_impedances_magnitude, middle_ear_impedances_phase

# healthy ear
healthy_rb1 = ResonantBranch(K=4762, M=54, R=572)
healthy_rb2 = ResonantBranch(K=32632, M=58, R=968)
healthy_rb3 = ResonantBranch(K=5256, M=0, R=2040)

healthy_middle_ear = (
    healthy_rb1,
    healthy_rb2,
    healthy_rb3,
)

#might want to continue messing with these wrappers

healthy_f, healthy_zme_mag, healthy_zme_phase = generate_impedance_frequency_response(healthy_middle_ear)
ax = simple_plot("Healthy Ear Impedance", healthy_f, "frequency (Hz)", healthy_zme_mag, "Impedance (magnitude)")
log_plot(ax)

#to get the phase plot in cyc you would have to divide radians by 2pi
ax_ph = simple_plot("Healthy Ear Impedance", healthy_f, "frequency (Hz)", healthy_zme_phase, "Impedance (phase) (radias)")
log_plot(ax_ph, logy=False)


#you're comparing with figure 5 in Merchant



