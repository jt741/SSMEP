from lumped_element_utils.circuit_parts import Capacitor, Inductor, Resistor
from lumped_element_utils.impedance_helper import total_impedance_series

class RaviczMiddleEar:
    def __init__(self, C_TOC=2.7*10**-12, R_TOC=61*10**6, M_TOC=0.3*10**3, C_MEC=7.7*10**-12) -> None:
        # might be nice to convert the params into a dictionary form
        self.C_TOC = Capacitor(C_TOC) 
        self.R_TOC = Resistor(R_TOC)
        self.M_TOC = Inductor(M_TOC)
        self.C_MEC = Capacitor(C_MEC)

    def get_impedance(self, w):
        middle_ear_impedance = total_impedance_series(self.C_TOC.get_impedance(w), self.R_TOC.get_impedance(w), self.M_TOC.get_impedance(w), self.C_MEC.get_impedance(w))
        return middle_ear_impedance

    def set_r_toc(self, r_toc):
        self.R_TOC = Resistor(r_toc)