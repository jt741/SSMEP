from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import matplotlib.pyplot as plt
from plotting_utils.extracted_data import WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y, WAVELY_FULL_X, WAVELY_FULL_Y
from plotting_utils.plotting_helper import set_size
labels = []

middle_ear_effusion_state = {
    #"0" : end_to_end_get_ar_response(RaviczMiddleEar()),
    "25" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)),
    #"40" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)),
    "50" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)),
    #"70" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)),
    "100" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)),
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

effused_alpha_dict = line_severity_colour_generator(middle_ear_effusion_state)
# plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

# SMALL_SIZE = 8
# MEDIUM_SIZE = 10
# BIGGISH_SIZE=12
# BIGGER_SIZE = 16
# plt.rc('font', size=BIGGISH_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=BIGGISH_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=BIGGISH_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=BIGGISH_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def plot_ravicz_trends(effused_dict, alphas, normal, latex=True):
    if latex:
        #Direct input 
        plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
        #Options
        params = {'text.usetex' : True,
                'font.size' : 12,
                'font.family' : 'lmodern',
                }
        plt.rcParams.update(params) 
    
    
    fig_dim = set_size(455.2,0.7)
    fig, ax = plt.subplots(figsize=(fig_dim[0]/0.7, fig_dim[1]))
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.18)
    # plt.subplots_adjust(top=0.95, right=0.72, left=0.12, bottom=0.18)
    
    if latex:
        ax.plot(normal[0], normal[1],':', color="tab:blue", label=f"0\% effused (healthy)")
    else:
        ax.plot(normal[0], normal[1],':', color="tab:blue", label=f"0% effused (healthy)")

    # for leg_lab, line in effused_dict.items():
    #     ax.plot(line[0], line[1], color="tab:red", alpha=alphas.get(leg_lab), label=f"{leg_lab}% effused")

    #using line styles for black and white display
    linesstyles = ['-.', '--', '-']
    i = 0
    for leg_lab, line in effused_dict.items():
        s=linesstyles[i]
        if latex:
            ax.plot(line[0], line[1],s, color="tab:red",alpha=alphas.get(leg_lab), label=f"{leg_lab}\% effused")
        else:
            ax.plot(line[0], line[1], s, color="tab:red", alpha=alphas.get(leg_lab), label=f"{leg_lab}% effused")
        i+=1
        

    ax.set(
        #title="Modelled acoustic reflectometry response with changing effusion level", 
        xlabel="Frequency (Hz)", 
        ylabel="Normalised Pressure Amplitude",
        )
    
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plt.legend(loc="lower right")
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # ax.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
    if latex:
        plt.savefig("ravicz_model/plots/different_effusions_latex.pdf")
    plt.show()

plot_ravicz_trends(middle_ear_effusion_state, effused_alpha_dict, end_to_end_get_ar_response(RaviczMiddleEar()), latex=True)

def compare_ravicz_with_real(ravicz_dict, measured_data, latex=False):
    
    if latex:
        #Direct input 
        plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
        #Options
        params = {'text.usetex' : True,
                'font.size' : 12,
                'font.family' : 'lmodern',
                }
        plt.rcParams.update(params) 
    
    
    fig_dim = set_size(455.2,0.7)
    # fig, ax = plt.subplots(figsize=fig_dim)
    # plt.subplots_adjust(top=0.95, right=0.95, bottom=0.15)
    # plt.subplots_adjust(top=0.95, right=0.95, left=0.15, bottom=0.18)
    fig, ax = plt.subplots(figsize=(fig_dim[0]/0.7, fig_dim[1]))
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.18)

    # plt.subplots_adjust(top=0.95, right=0.62, left=0.12, bottom=0.18)


    # ax.plot(ravicz_dict["0"][0], ravicz_dict["0"][1], color="tab:blue", label=f"modelled 0% effused (healthy)")
    # ax.plot(ravicz_dict["100"][0], ravicz_dict["100"][1], color="tab:red", label=f"modelled 100% effused")
    # ax.plot(measured_data["0"][0], measured_data["0"][1], color="tab:blue", label=f"measured healthy ear", linestyle="dashdot")
    # ax.plot(measured_data["100"][0], measured_data["100"][1], color="tab:red", label=f"measured effused ear", linestyle="dashdot")

    # std line styles for black and white printing
    if latex:
        ax.plot(ravicz_dict["0"][0], ravicz_dict["0"][1], '-',color="tab:blue", label=f"modelled 0\% effused")
        ax.plot(ravicz_dict["100"][0], ravicz_dict["100"][1],'--', color="tab:red", label=f"modelled 100\% effused")
        ax.plot(measured_data["0"][0], measured_data["0"][1], '-.',color="tab:blue", label=f"measured healthy ear")
        ax.plot(measured_data["100"][0], measured_data["100"][1],':', color="tab:red", label=f"measured effused ear")
    else:
        ax.plot(ravicz_dict["0"][0], ravicz_dict["0"][1], '-',color="tab:blue", label=f"modelled 0% effused (healthy)")
        ax.plot(ravicz_dict["100"][0], ravicz_dict["100"][1],'--', color="tab:red", label=f"modelled 100% effused")
        ax.plot(measured_data["0"][0], measured_data["0"][1], '-.',color="tab:blue", label=f"measured healthy ear")
        ax.plot(measured_data["100"][0], measured_data["100"][1],':', color="tab:red", label=f"measured effused ear")

    ax.set(
        #title="Comparing modelled and measured Acoustic Reflectometry", 
        xlabel="Frequency (Hz)", 
        #ylabel=r"$\dfrac{ \mathrm{Measured \ pressure \ field \ amplitude}}{\mathrm{Incident\ pressure\ wave\ amplitude}}$",
        #ylabel=r'$\dfrac{\mathrm{Measured pressure field amplitude}}{\mathrm{Incident pressure wave amplitude}}$'
        ylabel="Normalised Pressure Amplitude"
        )
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


    # plt.legend(loc="best")
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.savefig("ravicz_model/plots/comparison_xlim.svg")
    if latex:
        plt.savefig("ravicz_model/plots/comparison_latex.pdf")
    plt.show()

ravicz_dictionary = {
    "0": end_to_end_get_ar_response(RaviczMiddleEar()),
    "100": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6))
}

wavely_dictionary = {
    "0": (WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y),
    "100": (WAVELY_FULL_X, WAVELY_FULL_Y),
}

compare_ravicz_with_real(ravicz_dictionary,wavely_dictionary, latex=True)