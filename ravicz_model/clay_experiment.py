from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import matplotlib.pyplot as plt
from plotting_utils.extracted_data import WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y, WAVELY_FULL_X, WAVELY_FULL_Y

labels = []

middle_ear_effusion_state_by_V_MEC = {
    #"100" : end_to_end_get_ar_response(RaviczMiddleEar()),
    "85" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12)),
    #"70" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12)),
    "40" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12)),
    #"30" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.3*7.7*10**-12)),
    "20" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.2*7.7*10**-12)),
    "10" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.1*7.7*10**-12)),
    "5" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.05*7.7*10**-12)),
    "0" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.01*10**-12)),
}

# effused_middle_ear_100_with_more_fluid = RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6)
# effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
# effused_middle_ear_70 = RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)
# effused_middle_ear_50 = RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)
# effused_middle_ear_40 = RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)
# effused_middle_ear_25 = RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)
# normal_middle_ear = RaviczMiddleEar()

def line_severity_colour_generator(line_dict):
    """return alpha values for each line, assuming the input dict was in ascending order"""
    n = len(line_dict)-1
    min_alpha = 0.2
    max_alpha = 1.0
    fraction = (max_alpha-min_alpha)/n

    i=0
    alpha_dict = {}
    for key in line_dict.keys():
        alpha_dict[key] = min_alpha + i*fraction
        i+=1

    return alpha_dict

effused_alpha_dict = line_severity_colour_generator(middle_ear_effusion_state_by_V_MEC)
# plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGISH_SIZE=12
BIGGER_SIZE = 16
plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGISH_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def plot_ravicz_trends(effused_dict, alphas, normal):
    fig, ax = plt.subplots(figsize=(9,5))
    
    ax.plot(normal[0], normal[1], color="tab:blue", label=f"0% effused (healthy)")

    for leg_lab, line in effused_dict.items():
        ax.plot(line[0], line[1], color="tab:red", alpha=alphas.get(leg_lab), label=f"{leg_lab}% V_MEC remaining")

    ax.set(
        title="AR Ravicz LEM - varying V_MEC", 
        xlabel="Frequency (Hz)", 
        ylabel=r"$\frac{ \mathrm{Measured \ Pressure \ Amplitude}}{\mathrm{Forward\ Pressure\ Wave\ Amplitude}}$",
        )
        
    plt.legend()
    #plt.savefig("ravicz_model/plots/highres.svg")
    plt.show()

plot_ravicz_trends(middle_ear_effusion_state_by_V_MEC, effused_alpha_dict, end_to_end_get_ar_response(RaviczMiddleEar()))



#comparing with real
def compare_ravicz_with_real(ravicz_dict, measured_data):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.plot(ravicz_dict["0"][0], ravicz_dict["0"][1], color="tab:blue", label=f"modelled healthy")
    ax.plot(ravicz_dict["100"][0], ravicz_dict["100"][1], color="tab:red", label=f"modelled 5% V_MEC remaining")
    ax.plot(measured_data["0"][0], measured_data["0"][1], color="tab:blue", label=f"measured healthy ear", linestyle="dashdot")
    ax.plot(measured_data["100"][0], measured_data["100"][1], color="tab:red", label=f"measured effused ear", linestyle="dashdot")
    ax.set(
        title="Comparing modelled and measured Acoustic Reflectometry", 
        xlabel="Frequency (Hz)", 
        ylabel=r"$\frac{ \mathrm{Measured \ Pressure \ Amplitude}}{\mathrm{Forward\ Pressure\ Wave\ Amplitude}}$",
        )
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])

    plt.legend()
    #plt.savefig("ravicz_model/plots/comparison_xlim.svg")
    plt.show()

ravicz_dictionary = {
    "0": end_to_end_get_ar_response(RaviczMiddleEar()),
    "100": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.05*7.7*10**-12)) #this is actually 5% airleft
}

wavely_dictionary = {
    "0": (WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y),
    "100": (WAVELY_FULL_X, WAVELY_FULL_Y),
}

compare_ravicz_with_real(ravicz_dictionary,wavely_dictionary)