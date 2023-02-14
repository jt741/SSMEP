from lumped_element_utils.circuit_parts import Capacitor, Inductor, Resistor
from lumped_element_utils.impedance_helper import total_impedance_series, total_impedance_parallel

class KringlebotnMiddleEar:
    def __init__(self):
        #Middle Ear Cavities
        self.L_a = Inductor(1*10**-3)
        self.C_a = Capacitor(3.9*10**-6)
        self.R_a = Resistor(60)

        self.C_t = Capacitor(0.4*10**-6)

        #eardrum inertance
        self.L_d = Inductor(7.5*10**-3)

        #eardrum suspension
        self.L_s = Inductor(66*10**-3)
        self.C_s = Capacitor(0.3*10**-6)
        self.R_s = Resistor(20)

        self.C_r = Capacitor(1.3*10**-6)
        self.R_r = Resistor(120)
        

        #coupling eardrum-manubrium
        self.C_m = Capacitor(0.38*10**-6)
        self.R_m = Resistor(120)
        

        #malleus incus ligaments tensor tympani
        self.L_o = Inductor(22*10**-3)
        # self.C_o = Capacitor(10000000) # infinity
        self.R_o = Resistor(20)
        

        # coupling incus-stapes
        self.C_i = Capacitor(0.3*10**-6)
        self.R_i = Resistor(6000)
    

        #cochlea stapes stapedius tendon windows
        self.L_c = Inductor(46*10*8-3)
        self.C_c = Capacitor(0.56*10**-6)
        self.R_c = Resistor(330)

    def z_1(self, w):
        z_mec = total_impedance_parallel(total_impedance_series(self.L_a.get_impedance(w), self.C_a.get_impedance(w), self.R_a.get_impedance(w)), self.C_t.get_impedance(w))
        z_ei = self.L_d.get_impedance(w)
        z_es = total_impedance_parallel(total_impedance_series(self.L_s.get_impedance(w), self.C_s.get_impedance(w), self.R_s.get_impedance(w)), total_impedance_series(self.C_r.get_impedance(w),self.R_r.get_impedance(w)))
        return total_impedance_series(z_mec, z_ei, z_es)

    def z_2(self, w):
        return total_impedance_series(self.C_m.get_impedance(w), self.R_m.get_impedance(w))

    def z_3(self, w):
        return total_impedance_series(self.L_o.get_impedance(w), self.R_o.get_impedance(w))

    def z_4(self,w):
        return total_impedance_series(self.C_i.get_impedance(w), self.R_i.get_impedance(w))
    
    def z_5(self,w):
        return total_impedance_series(self.L_c.get_impedance(w), self.C_c.get_impedance(w), self.R_c.get_impedance(w))

    def get_impedance(self, w):
        z_45 = total_impedance_parallel(self.z_5(w), self.z_4(w))
        z_345 = total_impedance_series(self.z_3(w), z_45)
        z_2345 = total_impedance_parallel(self.z_2(w), z_345)
        z_total = total_impedance_series(self.z_1(w), z_2345)
        return z_total
        
