from typing import Final, Sequence
from lumped_element_utils.circuit_parts import Inductor, Capacitor, Resistor
from lumped_element_utils.impedance_helper import total_impedance_series, total_impedance_parallel


from merchant_model.circuit_and_resonant_branches import ResonantBranch



HEALTHY_PARAMS: Final = (
    {"K": 4762, "M":54, "R": 572},
    {"K": 32632, "M":58, "R": 968},
    {"K": 5256, "M":0, "R": 2040},
)

FULL_PARAMS: Final = (
    {"K": 10230, "M":403, "R": 2387},
    {"K": 99723, "M":57, "R": 2883},
    {"K": 7534, "M":0, "R": 44848},
)

class MiddleEar:
    """
    class to make middle ear given circuit parameters of Merchant's model of the middle ear (2021)

    
    need to be completely redone to work with the better way set out by Ravicz model!!!!!
    
    """
    def __init__(self, circuit_params: Sequence[dict]):
        self.circuit_params = circuit_params
        # TODO: could use a flag system with if-else and custom one? 


        #create middle ear upon initialisation
        self.middle_ear = []
        for branch in self.circuit_params:
            self.middle_ear.append(ResonantBranch(**branch))
        

    def get_middle_ear(self):
        return self.middle_ear


class MerchantMiddleEar:
    def __init__(self) -> None:

        self.K_1 = Capacitor(1/(4762 * 10**8))# 1/K? 
        self.R_1 =  Resistor(572 * 10**5)
        self.M_1 = Inductor(54 * 10**2) 
        
        self.K_2 = Capacitor(1/(32632 * 10**8))
        self.R_2 =  Resistor(968 * 10**5)
        self.M_2 = Inductor(58 * 10**2)

        self.K_3 = Capacitor(1/(5256 * 10**8))
        self.R_3 =  Resistor(2040 * 10**5)

    def get_impedance(self,w):
        branch_1 = total_impedance_series(self.K_1.get_impedance(w),self.M_1.get_impedance(w),self.R_1.get_impedance(w))
        branch_2 = total_impedance_series(self.K_2.get_impedance(w),self.M_2.get_impedance(w),self.R_2.get_impedance(w))
        branch_3 = total_impedance_series(self.K_3.get_impedance(w), self.R_3.get_impedance(w))

        total_impedance = total_impedance_parallel(branch_1, branch_2, branch_3)
        return total_impedance