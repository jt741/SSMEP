import numpy as np
import matplotlib.pyplot as plt
from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar


# data
middle_ear_effusion_state_TM_and_effusion = [
    ("0", end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000)),
    ("25", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000)),
    ("40", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6),start_f=2500, stop_f=3500, num=5000)),
    ("50", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000)),
    ("70", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6),start_f=2500, stop_f=3500, num=5000)),
    ("100", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000)),
    # ("100" , end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000))
]

middle_ear_effusion_state_TM_and_effusion_range = [
    ("0", end_to_end_get_ar_response(RaviczMiddleEar())),
    ("25", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6))),
    ("40", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6))),
    ("50", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6))),
    ("70", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6))),
    ("100", end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6))),
    # ("100" , end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000))
]

# generate Q factors for the dip?
def get_q_factor_multiply(x,y,effusion):
    #find q factor for a minimum (multiply by root2)

    # Find the resonant frequency
    i_min = np.argmin(np.array(y))

    w0 = x[i_min]
    A0=y[i_min]

    # Find the double-power points
    A_half = (A0) * np.sqrt(2)

    i_left = np.argmin(np.abs(np.array(y[:i_min]) - A_half))
    i_right = np.argmin(np.abs(np.array(y[i_min:]) - A_half)) + i_min
    w_left = x[i_left]
    w_right = x[i_right]

    # Calculate the Q factor
    Q = w0 / (w_right - w_left)
    print(f'Q of {effusion}% effused plot = {Q:.2f}')

    A_half = A_half
    return Q, w_left, w0, w_right, A_half

def get_q_factor_negative(x,y,effusion):
    #find q factor using negative values of data? not sure....

    # Find the resonant frequency
    i_min = np.argmax(-np.array(y)) #1 minus x is a bit arbitrary ... 

    w0 = x[i_min]
    A0=y[i_min]
    # print(w0,A0)
    # Find the half-power points
    A_half = (-A0) * np.sqrt(2)
    # print(A_half)

    i_left = np.argmin(np.abs(-np.array(y[:i_min]) - A_half))
    i_right = np.argmin(np.abs(-np.array(y[i_min:]) - A_half)) + i_min
    w_left = x[i_left]
    w_right = x[i_right]

    # Calculate the Q factor
    Q = w0 / (w_right - w_left)
    print(f'Q of {effusion}% effused plot = {Q:.2f}')

    A_half = -A_half
    return Q, w_left, w0, w_right, A_half


def get_q_factor(x,y,effusion):
    #find q factor using 1-data to make it a maximum

    # Find the resonant frequency
    i_min = np.argmax(1-np.array(y)) #1 minus x is a bit arbitrary ... 
    w0 = x[i_min]
    A0=y[i_min]

    # Find the half-power points
    A_half = (1-A0) / np.sqrt(2)

    i_left = np.argmin(np.abs(1-np.array(y[:i_min]) - A_half))
    i_right = np.argmin(np.abs(1-np.array(y[i_min:]) - A_half)) + i_min
    w_left = x[i_left]
    w_right = x[i_right]

    # Calculate the Q factor
    Q = w0 / (w_right - w_left)
    print(f'Q of {effusion}% effused plot = {Q:.2f}')

    A_half = 1-A_half
    return Q, w_left, w0, w_right, A_half

def print_q_factors(middle_ear_data_list):
    for ear in middle_ear_data_list:
        _, _, _,_,_ = get_q_factor_multiply(ear[1][0], ear[1][1], ear[0])

print_q_factors(middle_ear_effusion_state_TM_and_effusion)

def plot_ar_with_q_factor(x,y, effusion):
    fig,ax=plt.subplots()
    Q, w_left, w0, w_right, A_half = get_q_factor(x,y, effusion)

    ax.plot(x,y, label=f"{effusion}% effused | Q={Q}")
    ax.axvline(x=w_left, c="green", ls="--")
    ax.axvline(x=w0,c="green", ls="--")
    ax.axvline(x=w_right,c="green", ls="--")

    ax.axhline(y=A_half,c="orange", ls="--")
    ax.set(title="Spectral Gradient AR ", xlabel="Frequency (Hz)", ylabel="reflectivity")
    plt.legend()
    plt.show()

def plot_all_with_q_factor(middle_ear_data_list):
    for ear in middle_ear_data_list:
        plot_ar_with_q_factor(ear[1][0], ear[1][1], ear[0])

# plot_all_with_q_factor(middle_ear_effusion_state_TM_and_effusion_range)


#width at half peak?
def get_width_of_dip(x,y, effusion):
    i_min = np.argmin(np.array(y))
    w0 = x[i_min]
    A0=y[i_min]

    double_A0 = 2*A0
    i_left = np.argmin(np.abs(np.array(y[:i_min]) - double_A0))
    i_right = np.argmin(np.abs(np.array(y[i_min:]) - double_A0)) + i_min
    w_left = x[i_left]
    w_right = x[i_right]

    width = w_right-w_left
    normalised_width = width/w0

    # print(f"width of {effusion}% effused plot = {width:2f}") 
          
    print(f"normalised width of {effusion}% effused plot = {normalised_width:2f}")
    return double_A0, w_left, w_right, width, normalised_width

def plot_ar_with_width(x,y, effusion):
    fig,ax=plt.subplots()
    double, w_left, w_right, width, normalised_width = get_width_of_dip(x,y, effusion)

    ax.plot(x,y, label=f"{effusion}% effused | width={width:2f} | normalised={normalised_width:2f}")
    ax.axvline(x=w_left, c="green", ls="--")
    # ax.axvline(x=w0,c="green", ls="--")
    ax.axvline(x=w_right,c="green", ls="--")

    ax.axhline(y=double,c="orange", ls="--")
    ax.set(title="Spectral Gradient AR ", xlabel="Frequency (Hz)", ylabel="reflectivity")
    plt.legend()
    plt.show()

def print_all_widths(middle_ear_data_list):
    for ear in middle_ear_data_list:
        _, _, _,_,_ = get_width_of_dip(ear[1][0], ear[1][1], ear[0])

def plot_all_with_width(middle_ear_data_list):
    for ear in middle_ear_data_list:
        plot_ar_with_width(ear[1][0], ear[1][1], ear[0])

# plot_all_with_width(middle_ear_effusion_state_TM_and_effusion_range)

# print_all_widths(middle_ear_effusion_state_TM_and_effusion_range)
