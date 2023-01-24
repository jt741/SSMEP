from typing import Final, Sequence

from merchant_model.circuit_and_resonant_branches import ResonantBranch



HEALTHY_PARAMS: Final = (
    {"K": 4792, "M":54, "R": 572},
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


