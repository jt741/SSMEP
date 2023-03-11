from acoustic_reflectometry_utils.acoustic_reflectometry_response import get_impedance_frequency_response
from kringlebotn_model.KringlebotnMiddleEar import KringlebotnMiddleEar, KringlebotnMiddleEar_fixed_stapes
from lumped_element_utils.circuit_parts import Capacitor, Inductor, Resistor
from merchant_model.MerchantMiddleEar import MerchantMiddleEar
from plotting_utils.plotting_helper import plot_multiple_with_labels
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import numpy as np 
import matplotlib.pyplot as plt
import cmath

kb=KringlebotnMiddleEar()
rav = RaviczMiddleEar()


def generate_and_plot_impedance_bode_plot(ear_name:str, ear_model, no_plot=False, radians=False, start_f=100, stop_f=100000):
    # generate data to plot
    # frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    frequencies = np.logspace(start=2, stop=5, num=10000)
    middle_ear_impedances_magnitude = []
    middle_ear_impedances_phase = []
    for f in frequencies:
        Z_me = ear_model.get_impedance(2*np.pi*f)

        middle_ear_impedances_magnitude.append(abs(Z_me))
        if radians:
            middle_ear_impedances_phase.append(cmath.phase(Z_me))
        else:
            middle_ear_impedances_phase.append(cmath.phase(Z_me)*180/np.pi)

    if no_plot:
        return frequencies, middle_ear_impedances_magnitude, middle_ear_impedances_phase

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle(f"{ear_name} Impedance")

    mag_ax = axes[0]
    mag_ax.plot(frequencies, middle_ear_impedances_magnitude)
    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000]) # need to make this so it automatically adjusts with the start and stop f ???
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    phase_ax = axes[1]
    phase_ax.plot(frequencies, middle_ear_impedances_phase)

    if radians:
        phase_ax.set(ylabel="Phase (radians)", xlabel="Frequency (Hz)")
        phase_ax.set_xscale("log")
        phase_ax.set_xticks([100, 1000, 10000, 100000])
        phase_ax.set_yticks([-np.pi/2, -np.pi/4,0, np.pi/4, np.pi/2])
        phase_ax.set_ylim(-0.4*2*np.pi, 0.4*2*np.pi)
    else:
        phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
        phase_ax.set_xscale("log")
        phase_ax.set_xticks([100, 1000, 10000, 100000])
        phase_ax.set_yticks([-90, -45,0, 45, 90])
        phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)
    
    plt.show()

# mm = MerchantMiddleEar()
# generate_and_plot_impedance_bode_plot("Merch",mm)

# generate_and_plot_impedance_bode_plot("Kringlebotn", kb)
# generate_and_plot_impedance_bode_plot("Ravicz", rav)

def compare_ear_impedances_bode(ear_dict:dict, radians=False):
    ear_impedance_dict = {}

    for ear_name, ear_model in ear_dict.items():
        ear_impedance_dict[ear_name] = list(generate_and_plot_impedance_bode_plot(ear_name, ear_model, no_plot=True, radians=radians))

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle("Comparing Impedances")

    mag_ax = axes[0]
    phase_ax = axes[1]


    for ear_name, ear_data in ear_impedance_dict.items():
        #plot impedance magnitude data
        mag_ax.plot(ear_data[0], ear_data[1], label=ear_name)

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2], label=ear_name)

    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    if radians:
        phase_ax.set(ylabel="Phase (radians)", xlabel="Frequency (Hz)")
        phase_ax.set_xscale("log")
        phase_ax.set_xticks([100, 1000, 10000, 100000])
        phase_ax.set_ylim(-0.4*2*np.pi, 0.4*2*np.pi)
    else:
        phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
        phase_ax.set_xscale("log")
        phase_ax.set_xticks([100, 1000, 10000, 100000])
        phase_ax.set_yticks([-90, -45,0, 45, 90])
        phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)

    mag_ax.legend()
    phase_ax.legend()
    plt.show()


ear_dict_kr_rav = {"Kringlebotn": kb,
 "Ravicz": rav}

# compare_ear_impedances_bode(ear_dict_kr_rav)

effused_middle_ear_100_with_more_fluid = RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6)
effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
effused_middle_ear_70 = RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)
effused_middle_ear_50 = RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)
effused_middle_ear_40 = RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)
effused_middle_ear_25 = RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)
normal_middle_ear = RaviczMiddleEar()

ear_dict_rav_effu = {
    "0% TM coverage": normal_middle_ear,
    "25% TM coverage": effused_middle_ear_25,
    "50% TM coverage": effused_middle_ear_50,
    "100% TM coverage": effused_middle_ear_100,
}

# compare_ear_impedances_bode(ear_dict_rav_effu)


def generate_and_plot_EC_impedance_bode(ear_name, ear_model, no_plot=False):
    frequencies = np.logspace(start=2, stop=5, num=10000)
    ear_canal_impedances_magnitude = []
    ear_canal_impedances_phase = []
    for f in frequencies:
        Z_me = ear_model.get_impedance(2*np.pi*f)

        l = 28*10**-3 #~length of ear canal

        roe = 1.225 #density of air
        A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
        c = 343 #speed of sound in air
        Z_0 = roe * c / A  # characteristic impedance

        k = 2*np.pi*f / c

        #transmission matrix elements for cyclindrical EC
        A = np.cos(k*l)
        B = 1j* Z_0 * np.sin(k*l)
        C = 1j * np.sin(k*l) / Z_0
        D = A

        Z_ec = (A*Z_me + B)/(C*Z_me + D) #from lewis&neeley + stethoscope acoustics

        ear_canal_impedances_magnitude.append(abs(Z_ec))
        ear_canal_impedances_phase.append(cmath.phase(Z_ec)*180/np.pi)
    
    if no_plot:
        return frequencies, ear_canal_impedances_magnitude, ear_canal_impedances_phase

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle(f"{ear_name} Impedance")

    mag_ax = axes[0]
    mag_ax.plot(frequencies, ear_canal_impedances_magnitude)
    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000]) # need to make this so it automatically adjusts with the start and stop f ???
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**6, 3*10**9)

    phase_ax = axes[1]
    phase_ax.plot(frequencies, ear_canal_impedances_phase)
    phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000, 100000])
    phase_ax.set_yticks([-90, -45,0, 45, 90])
    phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)
    
    plt.show()

# generate_and_plot_impedance_bode_plot("Kringlebotn", kb)
# generate_and_plot_EC_impedance_bode("Kringlebotn", kb)
# generate_and_plot_impedance_bode_plot("Ravicz", rav)
# generate_and_plot_EC_impedance_bode("Ravicz", rav)



def compare_ec_impedances_bode(ear_dict:dict):
    ear_impedance_dict = {}

    for ear_name, ear_model in ear_dict.items():
        ear_impedance_dict[ear_name] = list(generate_and_plot_EC_impedance_bode(ear_name, ear_model, no_plot=True))

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle("Comparing Ear Canal Impedances")

    mag_ax = axes[0]
    phase_ax = axes[1]


    for ear_name, ear_data in ear_impedance_dict.items():
        #plot impedance magnitude data
        mag_ax.plot(ear_data[0], ear_data[1], label=ear_name)

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2], label=ear_name)

    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**6, 3*10**9)

    phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000, 100000])
    phase_ax.set_yticks([-90, -45,0, 45, 90])
    phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)

    mag_ax.legend()
    phase_ax.legend()
    plt.show()

# compare_ec_impedances_bode({"Kringlebotn": kb, "Ravicz":rav})




def compare_ANY_impedances_bode(ear_dict:dict):
    ear_impedance_dict = {}

    for ear_name, ear_model in ear_dict.items():
        if ear_name[-2:] == "EC": #impedance at ear canal
            ear_impedance_dict[ear_name] = list(generate_and_plot_EC_impedance_bode(ear_name, ear_model, no_plot=True))
        elif ear_name[-2:] == "ME": #impedance of middle ear
            ear_impedance_dict[ear_name] = list(generate_and_plot_impedance_bode_plot(ear_name, ear_model, no_plot=True))


    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle("Comparing Impedances")
    

    mag_ax = axes[0]
    phase_ax = axes[1]


    for ear_name, ear_data in ear_impedance_dict.items():
        #plot impedance magnitude data
        mag_ax.plot(ear_data[0], ear_data[1], label=ear_name)

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2], label=ear_name)

    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**6, 3*10**9)

    phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000, 100000])
    phase_ax.set_yticks([-90, -45,0, 45, 90])
    phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)

    mag_ax.legend()
    phase_ax.legend()
    plt.show()


me_ec_dict_kb={
    "Kringlebotn ME": kb,
    "Kringlebotn EC": kb
}
# compare_ANY_impedances_bode(me_ec_dict_kb)

me_ec_dict_rav={
    "Ravicz ME": rav,
    "Ravicz EC": rav
}
# compare_ANY_impedances_bode(me_ec_dict_rav)


me_ec_rav_effu = {
    # "0% TM coverage ME": normal_middle_ear,
    # "0% TM coverage EC": normal_middle_ear,
    # "25% TM coverage": effused_middle_ear_25,
    # "50% TM coverage ME": effused_middle_ear_50,
    # "50% TM coverage EC": effused_middle_ear_50,
    "100% TM coverage ME": effused_middle_ear_100,
    "100% TM coverage EC": effused_middle_ear_100,
}
# compare_ANY_impedances_bode(me_ec_rav_effu)

kb_stapes_fix = KringlebotnMiddleEar_fixed_stapes()

kb_compare_dict = {
    "Original Kringlebotn model ME": kb,
    "Fixed Stapes Kringlebotn ME": kb_stapes_fix
}
# compare_ANY_impedances_bode(kb_compare_dict)

mmm = MerchantMiddleEar()

co = {
    "Merchant ME": mmm,
    "Ravicz ME": rav,
    "Kringlebotn ME": kb
}
compare_ANY_impedances_bode(co)