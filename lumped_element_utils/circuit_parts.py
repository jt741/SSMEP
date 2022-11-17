
class Capacitor:
    def __init__(self, C) -> None:
        self.C = C

    def get_impedance(self, w):
        self.impedance = 1/(1j * w * self.C)
        return self.impedance

class Inductor:
    def __init__(self, L) -> None:
        self.L = L

    def get_impedance(self, w):
        self.impedance = 1j * w * self.L
        return self.impedance

class Resistor:
    #okay this feels a bit unnecessary --> NO very necessary to keep same API
    def __init__(self, R) -> None:
        self.R = R

    def get_impedance(self, w):
        self.impedance = self.R
        return self.impedance