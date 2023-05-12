from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import matplotlib.pyplot as plt
import numpy as np
import math


def find_min(x, y):
    current_min = y[0]
    min_index = 0
    for i in range(len(x)):
        if y[i] <= current_min:
            current_min = y[i]
            min_index=i
    
    #min_f = x[min_index]
    # print(min_f)
    return min_index

# now need to parameterise it so i'm plotting effusion state with the angle
# since we have decided it's not the effusion volume which is important, we should have % coverage of the TM on x axis .. for now...

def find_spectral_angle(x,y, scale_factor):
    min_index=find_min(x,y)

    max_len=len(x)
    offset =int(5 * max_len/100)
    # angle is found by using points before and after min (5% offset)
    # this method's validity looks alright from last week's analysis?

    left= min_index-offset
    right = min_index+offset
    
    p_left=np.polyfit(x[:left], y[:left], deg=1)
    left_angle = math.degrees(math.atan(p_left[0]*scale_factor)) 
    
    p_right=np.polyfit(x[right:], y[right:], deg=1)
    right_angle = math.degrees(math.atan(p_right[0]*scale_factor))

    angle=round(180 - right_angle + left_angle, 2)

    return angle


def angle_against_coverage(effused_list, suptitle="Spectral Angle vs TM coverage", scale_factor=2000, annotate=False):
    coverages = []
    angles=[]

    for coverage, x_and_y in effused_list:
        angle = find_spectral_angle(x_and_y[0], x_and_y[1], scale_factor)
        coverages.append(int(coverage))
        angles.append(angle)

    fig,ax = plt.subplots()
    ax.plot(coverages, angles, 'o')
    ax.set(title=f"Scaling factor: {scale_factor}", xlabel="TM coverage (%)", ylabel="Spectral Angle (degrees)")
    fig.suptitle(suptitle)

    if annotate:
        for i, angle in enumerate(angles):
            ax.annotate(angle, (coverages[i], angles[i]))
            
    plt.show()


middle_ear_effusion_state_TM_and_effusion = [
    ("0", end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000)),
    ("25", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000)),
    ("40", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6),start_f=2500, stop_f=3500, num=5000)),
    ("50", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000)),
    ("70", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6),start_f=2500, stop_f=3500, num=5000)),
    ("100", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000)),
    # ("100" , end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000))
]
# angle_against_coverage(middle_ear_effusion_state_TM_and_effusion)
# angle_against_coverage(middle_ear_effusion_state_TM_and_effusion, annotate=True)

def overlay_ravicz_damping(ax, annotate, colour_marker='ro'):
    ravciz_rtoc = [61, 103, 110, 95, 130, 160, 310]
    ravicz_angles = [84, 69, 69, 52, 52, 52, 52]
    ax.plot(ravciz_rtoc, ravicz_angles, colour_marker, label="Ravicz Data for effused ears")

    if annotate:
        labels = ["0%", "25%", "40%", "50%", "70%", "100%", "100%*"]
        for i, label in enumerate(labels):
            ax.annotate(label, (ravciz_rtoc[i], ravicz_angles[i]))

    return ax

def overlay_ravicz_mass(ax, annotate, colour_marker='ro'):
    ravciz_mtoc = [0.3, 0.4, 1.5, 25, 32]# 190, 610]
    ravicz_angles = [84, 69, 69, 52, 52]# 52, 52]
    ax.plot(ravciz_mtoc, ravicz_angles, colour_marker, label="Ravicz Data for effused ears")

    if annotate:
        labels = ["0%", "25%", "40%", "50%", "70%", "100%", "100%*"]
        for i, label in enumerate(labels):
            ax.annotate(label, (ravciz_mtoc[i], ravicz_angles[i]))

    return ax


def spectral_angle_damping_sensitivity(scale_factor=2000, plot_ravicz=False, annotate=False):
    #function for plotting angle as function of R_TOC?
    #for a healthy ear for now?
    r_toc_list = np.linspace(50, 300, 20)
    angle_list = []
    for r_toc in r_toc_list:
        response = end_to_end_get_ar_response(RaviczMiddleEar(R_TOC=r_toc*10**6), start_f=2500, stop_f=3500, num=5000)
        angle = find_spectral_angle(response[0], response[1], scale_factor)
        angle_list.append(angle)

    fig,ax = plt.subplots()
    ax.plot(r_toc_list, angle_list, 'bo', label="Healthy Ear vary R_TOC")
    ax.set(title=f"Scaling factor: {scale_factor}", xlabel="R_TOC (10^6 Pa s/m^3)", ylabel="Spectral Angle (degrees)")
    fig.suptitle("Spectral Angle vs R_TOC")

    # how to generate x values logarithmically? exponential curve fitting? :/
    if plot_ravicz:
        ax = overlay_ravicz_damping(ax, annotate)

    plt.legend()
    plt.show()

# spectral_angle_damping_sensitivity()


#adapt the above so that i can feed the different ears in and see how that works...

def spectral_angle_damping_all_ears(ears, scale_factor=2000, plot_ravicz=False, annotate=False, prelabel="TM cover: "):
    #function for plotting angle as function of R_TOC?
    r_toc_list = np.linspace(50, 300, 20) # for now?

    fig,ax = plt.subplots()

    for lab, ear_data in ears.items():
        middle_ear = RaviczMiddleEar(**ear_data)
        angle_list = []
        for r_toc in r_toc_list:
            middle_ear.set_r_toc(r_toc*10**6)
            # print(f"r toc is {middle_ear.R_TOC.get_impedance(0)}")
            response = end_to_end_get_ar_response(middle_ear, start_f=2500, stop_f=3500, num=5000)
            angle = find_spectral_angle(response[0], response[1], scale_factor)
            angle_list.append(angle)

        ax.plot(r_toc_list, angle_list, 'x', label=prelabel+lab)

    ax.set(title=f"Scaling factor: {scale_factor}", xlabel="R_TOC (10^6 Pa s/m^3)", ylabel="Spectral Angle (degrees)")  
    fig.suptitle("Spectral Angle vs R_TOC")

    # how to generate x values logarithmically? exponential curve fitting? :/
    if plot_ravicz:
        ax = overlay_ravicz_damping(ax, annotate)

    plt.legend()
    plt.show()


ravicz_data_dict ={
    "0%" : {},
    "25%": {"C_MEC":6.5*10**-12, "M_TOC":0.4*10**3, "R_TOC":103*10**6},
    "40%": {"C_MEC":6.1*10**-12, "M_TOC":1.5*10**3, "R_TOC":110*10**6},
    "50%":{"C_MEC":5.4*10**-12, "M_TOC":25*10**3, "R_TOC":95*10**6},
    "70%":{"C_MEC":5.0*10**-12, "M_TOC":32*10**3, "R_TOC":130*10**6},
    "100%":{"C_MEC":3.1*10**-12, "M_TOC":190*10**3, "R_TOC":160*10**6},
    # "100%*":{"C_MEC":0.77*10**-12, "M_TOC":610*10**3, "R_TOC":310*10**6}
}

# spectral_angle_damping_all_ears(ravicz_data_dict, scale_factor=2000, plot_ravicz=True, annotate=False)

modified_mass_dict = {
    # "0.1" : {"M_TOC":0.1*10**3},
    "0.3" : {"M_TOC":0.3*10**3},
    # "1" : {"M_TOC":1*10**3},
    "1.5" : {"M_TOC":1.5*10**3},
    # "3" : {"M_TOC":3*10**3},
    # "3.5" : {"M_TOC":3.5*10**3},
    # "4" : {"M_TOC":4*10**3},
    "5" : {"M_TOC":5*10**3},
    # "6" : {"M_TOC":6*10**3},
    # "10" : {"M_TOC":10*10**3},
    "25" : {"M_TOC":25*10**3},
    # "100" : {"M_TOC":100*10**3},
}

# spectral_angle_damping_all_ears(modified_mass_dict, scale_factor=2000, plot_ravicz=True, prelabel="M_TOC: ")




# do spectral angle vs mass
def spectral_angle_mass_all_ears(ears, scale_factor=2000, plot_ravicz=False, annotate=False, prelabel="TM cover: "):
    #function for plotting angle as function of R_TOC?
    m_toc_list = np.concatenate((np.linspace(0.3, 10, 30), np.linspace(10,35, 20)))

    fig,ax = plt.subplots()

    for lab, ear_data in ears.items():
        middle_ear = RaviczMiddleEar(**ear_data)
        angle_list = []
        for m_toc in m_toc_list:
            middle_ear.set_m_toc(m_toc*10**3)
            # print(f"r toc is {middle_ear.R_TOC.get_impedance(0)}")
            response = end_to_end_get_ar_response(middle_ear, start_f=2500, stop_f=3500, num=5000)
            angle = find_spectral_angle(response[0], response[1], scale_factor)
            angle_list.append(angle)

        ax.plot(m_toc_list, angle_list, '-', label=prelabel+lab)

    ax.set(title=f"Scaling factor: {scale_factor}", xlabel="M_TOC (10^3 kg/m^4)", ylabel="Spectral Angle (degrees)")  
    fig.suptitle("Spectral Angle vs M_TOC")

    # how to generate x values logarithmically? exponential curve fitting? :/
    if plot_ravicz:
        ax = overlay_ravicz_mass(ax, annotate)

    plt.legend()
    plt.show()

# spectral_angle_mass_all_ears(ravicz_data_dict, scale_factor=2000, plot_ravicz=True)






# i think i can just use the healthy ear? and maybe 50% if i feel like it
# COULD DO A CONTOUR PLOT varying mass and damping and seeing the effect on spectral angle
# need to remember that spectral angle is a proxy for why certain frequencies are reflected more than others?

