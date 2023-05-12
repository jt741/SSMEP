import math
from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from kringlebotn_model.compare_impedance_values import generate_and_plot_EC_impedance_bode, generate_and_plot_impedance_bode_plot
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import matplotlib.pyplot as plt
from plotting_utils.extracted_data import WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y, WAVELY_FULL_X, WAVELY_FULL_Y
from plotting_utils.plotting_helper import set_size
import numpy as np
import cmath
from ravicz_model.fine_tune import find_min, polyfit_a_bit_away_from_min, polyfit_with_linear

from ravicz_model.spectral_gradient_plots import find_spectral_angle

effused_middle_ear_100_with_more_fluid = RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6)
effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
effused_middle_ear_70 = RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)
effused_middle_ear_50 = RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)
effused_middle_ear_40 = RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)
effused_middle_ear_25 = RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)
normal_middle_ear = RaviczMiddleEar()

middle_ear_effusion_state = {
    "0" : end_to_end_get_ar_response(normal_middle_ear),
    "25" : end_to_end_get_ar_response(effused_middle_ear_25),
    #"40" : end_to_end_get_ar_response(effused_middle_ear_40),
    "50" : end_to_end_get_ar_response(effused_middle_ear_50),
    #"70" : end_to_end_get_ar_response(effused_middle_ear_70),
    "100" : end_to_end_get_ar_response(effused_middle_ear_100),
}



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

# effused_alpha_dict = line_severity_colour_generator(middle_ear_effusion_state) #shouldn't include the healthy one

def set_latex_font_size():
    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    #Options
    params = {'text.usetex' : True,
            'font.size' : 12,
            'font.family' : 'lmodern',
            }
    plt.rcParams.update(params) 


def set_figure_scaling_for_latex(scaling_fraction=0.7, y_dim_extra_scaling=1 ):
    textwidth = 455.2
    fig_dim = set_size(textwidth,scaling_fraction) 
    fig, ax = plt.subplots(figsize=(fig_dim[0]/scaling_fraction, fig_dim[1]*y_dim_extra_scaling))
    
    #this will likely need to be set manually
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.145)

    return fig,ax


def plot_ravicz_changing_effusion_for_latex(effused_dict):
    """
    plotting Modelled acoustic reflectometry response with changing effusion level for Latex
    legend and scaling here is a bit weird - i might redo since i have more space in my report? but redo at the end
    """

    set_latex_font_size()
    

    fig, ax = set_figure_scaling_for_latex(y_dim_extra_scaling=1.3)
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.18)
    # plt.subplots_adjust(top=0.95, right=0.72, left=0.12, bottom=0.18)
    
    
    # ax.plot(normal[0], normal[1],':', color="tab:blue", label=f"0\% effused (healthy)")

    #using line styles for black and white display
    linesstyles = [':', '-.', '--', '-']
    i = 0
    for leg_lab, line in effused_dict.items():
        s=linesstyles[i]
        ax.plot(line[0], line[1],linestyle=s, label=f"{leg_lab}\% effused")
        i+=1
        
    ax.set(
        #title="Modelled acoustic reflectometry response with changing effusion level", 
        xlabel="Frequency (Hz)", 
        ylabel="Normalised Pressure Amplitude",
        )
    
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])
    
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

    # Put a legend to the right of the current axis
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.legend(loc="lower right")
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # ax.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
    
    plt.savefig("ravicz_model/final_report_plots/different_effusions_latex.pdf")
    plt.show()

# plot_ravicz_changing_effusion_for_latex(middle_ear_effusion_state)


def compare_ravicz_with_real_for_latex(ravicz_dict, measured_data):
    """
    Comparing modelled and measured Acoustic Reflectometry
    """
    
    set_latex_font_size()
    
    fig, ax = set_figure_scaling_for_latex(y_dim_extra_scaling=1.3)
    # plt.subplots_adjust(top=0.95, right=0.95, bottom=0.15)
    # plt.subplots_adjust(top=0.95, right=0.95, left=0.15, bottom=0.18)
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.18)


    # std line styles for black and white printing  
    ax.plot(ravicz_dict["0"][0], ravicz_dict["0"][1], ':',color="tab:blue", label=f"Modelled 0\% effused")
    ax.plot(ravicz_dict["100"][0], ravicz_dict["100"][1],'-', color="tab:red", label=f"Modelled 100\% effused")
    ax.plot(measured_data["0"][0], measured_data["0"][1], linestyle=(0, (3, 5, 1, 5)),color="tab:blue", label=f"Measured healthy ear")
    ax.plot(measured_data["100"][0], measured_data["100"][1],linestyle=(0, (5, 1)), color="tab:red", label=f"Measured effused ear")
   
    ax.set(
        #title="Comparing modelled and measured Acoustic Reflectometry", 
        xlabel="Frequency (Hz)", 
        #ylabel=r"$\dfrac{ \mathrm{Measured \ pressure \ field \ amplitude}}{\mathrm{Incident\ pressure\ wave\ amplitude}}$",
        #ylabel=r'$\dfrac{\mathrm{Measured pressure field amplitude}}{\mathrm{Incident pressure wave amplitude}}$'
        ylabel="Normalised Pressure Amplitude"
        )
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])

    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

    # Put a legend to the right of the current axis
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.legend(loc="upper center")
    plt.savefig("ravicz_model/final_report_plots/comparison_latex.pdf")
    plt.show()

ravicz_dictionary = {
    "0": end_to_end_get_ar_response(RaviczMiddleEar()),
    "100": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6))
}

wavely_dictionary = {
    "0": (WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y),
    "100": (WAVELY_FULL_X, WAVELY_FULL_Y),
}

# compare_ravicz_with_real_for_latex(ravicz_dictionary,wavely_dictionary)


def generate_EC_impedance_bode_plot_data_using_pure_inductance(ear_model):
    """model ear canal as narrow duct --> inductance analogy
    """
    roe = 1.225 # density of air
    l = 28 * 10**-3 #length of ear canal to measurement point
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    c = 343 #speed of sound in air

    L = roe * l / A  # equivalent inductance
    
    frequencies = np.logspace(start=2, stop=5, num=10000)
    imp_mag_at_measurement_point = []
    imp_phase_at_measurement_point = []
    for f in frequencies:
        z_me = ear_model.get_impedance(2*np.pi*f)
        z_ec = 1j*L*2*np.pi*f

        z_total = z_me+z_ec
        imp_mag_at_measurement_point.append(abs(z_total))
        imp_phase_at_measurement_point.append(cmath.phase(z_total)*180/np.pi)
    
    return frequencies, imp_mag_at_measurement_point, imp_phase_at_measurement_point

def compare_ravicz_impedances_for_latex(ear_dict:dict, ear_canal=False):
    """
    Comparing middle ear Impedance bode plots for different levels of effusion for Ravicz model
    """
    set_latex_font_size()

    textwidth = 455.2
    scaling_fraction = 0.7
    fig_dim = set_size(textwidth, scaling_fraction) 

    #need to do a golden ratio for portrait plots!?
    fig, axes = plt.subplots(2, 1,sharex=True, figsize=(fig_dim[0]/scaling_fraction, fig_dim[0]*1.5))
    # plt.subplots_adjust(top=0.95, right=0.95, bottom=0.15)
    # plt.subplots_adjust(top=0.95, right=0.95, left=0.15, bottom=0.18)
    plt.subplots_adjust(top=0.97, right=0.96, left=0.12, bottom=0.102, hspace=0.055)

    ear_impedance_dict = {}

    for ear_name, ear_model in ear_dict.items():
        if ear_canal:
            ear_impedance_dict[ear_name] = list(generate_EC_impedance_bode_plot_data_using_pure_inductance(ear_model))
        else:
            ear_impedance_dict[ear_name] = list(generate_and_plot_impedance_bode_plot(ear_name, ear_model, no_plot=True, radians=False))

    # plot mag and phase stacked
    # fig, axes = plt.subplots(2, 1, figsize=(6,8))

    mag_ax = axes[0]
    phase_ax = axes[1]

    #using line styles for black and white display (ugly?)
    line_styles = [":",'-.', '--', '-',]
    i = 0
    for ear_name, ear_data in ear_impedance_dict.items():
        #plot impedance magnitude data
        line_style = line_styles[i]
        mag_ax.plot(ear_data[0], ear_data[1], line_style, label=f"{ear_name}\% effused")

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2],line_style, label=f"{ear_name}\% effused")
        i+=1

    mag_ax.set(ylabel="Magnitude (mks ohm)")#, xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    
    phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000, 100000])
    phase_ax.set_yticks([-90, -45,0, 45, 90])
    phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)

    # mag_ax.legend(loc='lower right')
    phase_ax.legend()

    impedance_type = "me" if not ear_canal else "ec"
    plt.savefig(f"ravicz_model/final_report_plots/{impedance_type}_impedance_bode_ravicz_latex.pdf")
    plt.show()


ear_dict_rav_effu = {
    "0": normal_middle_ear,
    "25": effused_middle_ear_25,
    "50": effused_middle_ear_50,
    "100": effused_middle_ear_100,
}
# compare_ravicz_impedances_for_latex(ear_dict_rav_effu, ear_canal=False)



def spectral_angle_calculation():
    """
    you can change the way you calculate spectral angle
    your life will be easier if you make it work like this
    angle = find_spectral_angle(response[0], response[1], scale_factor)
    resp0 and rep1 are from ar response......
    """
    #do what you are currently doing first

    #try q factor? doesn't it need to be illustarted

    #try what the patent actually says (increase by 20% from null value)
    pass

def spectral_angle_v_r_toc(ear_dict:dict, plot_ravicz=False, annotate=False):
    #function for plotting angle as function of R_TOC?
    
    set_latex_font_size()

    textwidth = 455.2
    scaling_fraction = 0.7
    fig_dim = set_size(textwidth,scaling_fraction) 
    fig, ax = plt.subplots(figsize=(fig_dim[0]/scaling_fraction, fig_dim[1]*1.5))
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.145)
    
    scale_factor=2000

    marker_style = ['+b', 'xm']
    i=0
    for ear_name, middle_ear in ear_dict.items():
        angle_list = []
        r_toc_list = np.linspace(50, 300, 20) # for now?
        for r_toc in r_toc_list:
            middle_ear.set_r_toc(r_toc*10**6)
            response = end_to_end_get_ar_response(middle_ear, start_f=2500, stop_f=3500, num=5000)
            angle = find_spectral_angle(response[0], response[1], scale_factor)
            angle_list.append(angle)

        ax.plot(r_toc_list, angle_list, marker_style[i], label=f"{ear_name}\% effused model parameters")
        i+=1
    
    ax.set(
        xlabel=r"$R_{\mathrm{TOC}}~(10^6~\mathrm{Pa~s/m^3})$", 
        ylabel="Spectral Angle (degrees)"
        )  
    
    if plot_ravicz:
        ravciz_rtoc = [61, 103, 110, 95, 130, 160, 310]
        ravicz_angles = [84, 69, 69, 52, 52, 52, 52]
        ax.plot(ravciz_rtoc, ravicz_angles, 'ro', label="Actual modelled datapoints")

        if annotate:
            labels = ["0%", "25%", "40%", "50%", "70%", "100%", "100%*"]
            for i, label in enumerate(labels):
                ax.annotate(label, (ravciz_rtoc[i], ravicz_angles[i]))

    plt.legend()
    plt.savefig("ravicz_model/final_report_plots/spectral_angle_v_r_toc.pdf")
    plt.show()

ear_dict_rav_sgar = {
    "0": normal_middle_ear,
    "50": effused_middle_ear_50,
}
spectral_angle_v_r_toc(ear_dict_rav_sgar, plot_ravicz=True)


def spectral_angle_v_tm_coverage_for_latex(effusion_ar_resp:dict):
    #just to show angle decreasing / becoming sharper with increasing levels of effusion.
    #also handy to refer to as the overlaid points
    set_latex_font_size()

    fig, ax = set_figure_scaling_for_latex(y_dim_extra_scaling=1.4)

    coverages = []
    angles=[]
    scale_factor=2000
    for coverage, x_and_y in effusion_ar_resp.items():
        angle = find_spectral_angle(x_and_y[0], x_and_y[1], scale_factor)
        coverages.append(int(coverage))
        angles.append(angle)

    ax.plot(coverages, angles, 'ro')
    ax.set(xlabel="Percentage of Eardrum Covered by Effusion (\%)", ylabel="Spectral Angle (degrees)")

    plt.savefig("ravicz_model/final_report_plots/spectral_angle_v_tm_cover.pdf")            
    plt.show()


tm_and_effusion_modified_range_for_spectral_angle = {
    "0": end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000),
    "25": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000),
    "40": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6),start_f=2500, stop_f=3500, num=5000),
    "50": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000),
    "70": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6),start_f=2500, stop_f=3500, num=5000),
    "100": end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000),
    # "100" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000)
}
# spectral_angle_v_tm_coverage_for_latex(tm_and_effusion_modified_range_for_spectral_angle)


def illustrate_how_angle_is_calculated(effused_dict):
    set_latex_font_size()
    fig, ax = set_figure_scaling_for_latex(y_dim_extra_scaling=1.5)

    colour=["tab:blue","tab:orange","tab:red"]
    line_styles=[':', '-.', '-']
    i=0
    for legend_label, x_and_y in effused_dict.items():
        ax = polyfit_with_linear(ax, x_and_y[0], x_and_y[1], legend_label, colour[i], linestyle=line_styles[i])
        i+=1
    
    ax.set(xlabel="Frequency (Hz)", ylabel="Normalised Pressure Amplitude")
    plt.legend()
    plt.savefig("ravicz_model/final_report_plots/illustrate_sgar.pdf")
    plt.show()


select_eff_sgar_dict = {
    "0": tm_and_effusion_modified_range_for_spectral_angle["0"], 
    "25": tm_and_effusion_modified_range_for_spectral_angle["25"], 
    "100": tm_and_effusion_modified_range_for_spectral_angle["100"],
    }
# illustrate_how_angle_is_calculated(select_eff_sgar_dict)

def illustrate_issues_with_angle_calculation(ar_resp):
    x=ar_resp[0]
    y=ar_resp[1]
    
    min_index=find_min(x,y)
    max_len=len(x)

    offset =int(5 * max_len/100)

    left= min_index-offset
   
    right = min_index+offset
    
    p_left=np.polyfit(x[:left], y[:left], deg=1)
    print(f"left equation is: y={p_left[0]}x+{p_left[1]}")
    f_left=np.poly1d(p_left)
    left_angle = math.degrees(math.atan(p_left[0]*2000)) #scale by 2000
    print(f"left angle is {left_angle}")

    
    p_right=np.polyfit(x[right:], y[right:], deg=1)
    print(f"right equation is: y={p_right[0]}x+{p_right[1]}")
    f_right=np.poly1d(p_right)
    right_angle = math.degrees(math.atan(p_right[0]*2000))
    print(f"right angle is {right_angle}")

    angle=180 - right_angle + left_angle
    print(f"angle is {angle}")

    
    set_latex_font_size()
    textwidth = 455.2
    scaling_fraction=0.7
    fig_dim = set_size(textwidth,scaling_fraction) 
    fig, (ax0,ax1) = plt.subplots(1, 2, sharey=False, gridspec_kw={"width_ratios": [3, 1]}, figsize=(fig_dim[0]/scaling_fraction, fig_dim[1]*1.5))
    
    #this will likely need to be set manually
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.145, wspace=0.345)


    ax0.plot(x,y, linestyle='-.', color="tab:orange")
    ax0.plot(x[:min_index-1],f_left(x[:min_index-1]),linestyle='--', alpha=0.4,color="tab:orange")
    ax0.plot(x[min_index:],f_right(x[min_index:]),linestyle='--', alpha=0.4,color="tab:orange")

    ax0.set(xlabel="Frequency (Hz)", ylabel="Normalised Pressure Amplitude")

    ax1.plot(x,y, linestyle='-.', color="tab:orange")
    ax1.plot(x[:min_index-1],f_left(x[:min_index-1]),linestyle='--', alpha=0.4,color="tab:orange")
    ax1.plot(x[min_index:],f_right(x[min_index:]),linestyle='--', alpha=0.4,color="tab:orange")

    ax1.set(xlabel="Frequency (Hz)", ylabel="Normalised Pressure Amplitude")
    plt.savefig("ravicz_model/final_report_plots/illustrate_issue_with_angle.pdf")
    plt.show()

# illustrate_issues_with_angle_calculation(select_eff_sgar_dict["25"])


def week5plots():
    #need to do quite a few: (further show that we can divide responses into 0 vs above 50% effused)
    #just use google slides as ref
    pass


def healthy_ear_changing_one_parameter_impedance(ear_dict:dict, ear_canal=False):
    """
    plot healthy ear impedance with m_toc set at 25 

    plot with normal healthy ear , 50% and 100?
    """

    set_latex_font_size()

    textwidth = 455.2
    scaling_fraction = 0.7
    fig_dim = set_size(textwidth, scaling_fraction) 

    #need to do a golden ratio for portrait plots!?
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(fig_dim[0]/scaling_fraction, fig_dim[0]*1.5))
    # plt.subplots_adjust(top=0.95, right=0.95, bottom=0.15)
    # plt.subplots_adjust(top=0.95, right=0.95, left=0.15, bottom=0.18)
    plt.subplots_adjust(top=0.97, right=0.96, left=0.12, bottom=0.102, hspace=0.055)

    ear_impedance_dict = {}

    for ear_name, ear_model in ear_dict.items():
        if ear_canal:
            ear_impedance_dict[ear_name] = list(generate_EC_impedance_bode_plot_data_using_pure_inductance(ear_model))
        else:
            ear_impedance_dict[ear_name] = list(generate_and_plot_impedance_bode_plot(ear_name, ear_model, no_plot=True, radians=False))

    # plot mag and phase stacked
    # fig, axes = plt.subplots(2, 1, figsize=(6,8))

    mag_ax = axes[0]
    phase_ax = axes[1]

    #using line styles for black and white display (ugly?)
    line_styles = [":",'-.', '--', '-',]
    i = 0
    for ear_name, ear_data in ear_impedance_dict.items():
        if ear_name=="changed":
            #trying to think of a catchy label for this curve
            # r"0\% effused with $M_{TOC}=25 \times 10^3$" is a bit too long
            mag_ax.plot(ear_data[0], ear_data[1], color="tab:purple", linestyle=(0, (3, 1, 1, 1, 1, 1)), label=r"0\% effused at critical $M_{\mathrm{TOC}}$")
            phase_ax.plot(ear_data[0], ear_data[2], color="tab:purple",linestyle=(0, (3, 1, 1, 1, 1, 1)), label=r"0\% effused at critical $M_{\mathrm{TOC}}$")

            continue

        #plot impedance magnitude data
        line_style = line_styles[i]
        mag_ax.plot(ear_data[0], ear_data[1], line_style, label=f"{ear_name}\% effused")

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2],line_style, label=f"{ear_name}\% effused")
        i+=1

    mag_ax.set(ylabel="Magnitude (mks ohm)")#, xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000, 100000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    
    phase_ax.set(ylabel="Phase (degrees)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000, 100000])
    phase_ax.set_yticks([-90, -45,0, 45, 90])
    phase_ax.set_ylim(-0.4*2*180, 0.4*2*180)

    # mag_ax.legend(loc='lower right')
    phase_ax.legend()

    impedance_type = "me" if not ear_canal else "ec"
    plt.savefig(f"ravicz_model/final_report_plots/{impedance_type}_impedance_bode_parametric.pdf")
    plt.show()

one_changed_ear = {
    "0": normal_middle_ear,
    "25": effused_middle_ear_25,
    "changed": RaviczMiddleEar(M_TOC=25*10**3),
    "50": effused_middle_ear_50,
    "100": effused_middle_ear_100,
}

# healthy_ear_changing_one_parameter_impedance(one_changed_ear, ear_canal=False)

def healthy_ear_changing_one_parameter_acoustic_reflectometry(effused_dict:dict):
    """
    plot healthy ear Ar response with m_toc set at 25 

    plot with normal healthy ear , 50% and 100?
    i think use this method to redo ur other acoustic reflectometry responses
    this is just a general acoustic reflect plotter realistically

    REDO the chan one ... should be easy....
    """

    set_latex_font_size()
    

    fig, ax = set_figure_scaling_for_latex(y_dim_extra_scaling=1.3)
    plt.subplots_adjust(top=0.95, right=0.96, left=0.12, bottom=0.18)
    # plt.subplots_adjust(top=0.95, right=0.72, left=0.12, bottom=0.18)
    
    
    # ax.plot(normal[0], normal[1],':', color="tab:blue", label=f"0\% effused (healthy)")

    #using line styles for black and white display
    linesstyles = [':', '-']
    colours=["tab:blue", "tab:red" ]
    i = 0
    for ear_name, line in effused_dict.items():
        if ear_name=="changed":
            ax.plot(line[0], line[1], color="tab:purple", linestyle=(0, (3, 1, 1, 1, 1, 1)), label=r"0\% effused at critical $M_{\mathrm{TOC}}$")
            continue
        s=linesstyles[i]
        ax.plot(line[0], line[1],linestyle=s, color=colours[i], label=f"{ear_name}\% effused")
        i+=1
        
    ax.set(
        xlabel="Frequency (Hz)", 
        ylabel="Normalised Pressure Amplitude",
        )
    
    ax.set_xlim([1600, 4500])
    ax.set_ylim([-0.1, 1.1])
    

    plt.legend()
    
    plt.savefig("ravicz_model/final_report_plots/param_binary_output_latex.pdf")
    plt.show()


binary_dict = {
    "0": middle_ear_effusion_state["0"],
    "changed": end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=25*10**3)),
    "100": middle_ear_effusion_state["100"],
}

# healthy_ear_changing_one_parameter_acoustic_reflectometry(binary_dict)