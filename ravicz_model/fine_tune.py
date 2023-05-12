from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from plotting_utils.plotting_helper import plot_multiple_with_labels
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
import matplotlib.pyplot as plt
import numpy as np
import math



middle_ear_effusion_state_spread = {
    "0% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000),
    "25% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000),
    "50% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000),
    "100% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000)
}

middle_ear_effusion_state_below_50 = {
    "0% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000),
    "25% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000),
    "40% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6),start_f=2500, stop_f=3500, num=5000),
    # "50% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000),
}

middle_ear_effusion_state_above_50 = {
    "50% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000),
    "70% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6),start_f=2500, stop_f=3500, num=5000),
    "100% TM covered" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000)
}

# plot_multiple_with_labels("Simulated Acoustic Reflectivity Response", "Frequency (Hz)", "Reflectivity Unit", middle_ear_effusion_state_spread)

def spectral_gradient(x_values, y_values):
    p=np.polyfit(x_values, y_values, deg=7)
    print(p)
    f=np.poly1d(p)

    fig,ax = plt.subplots()
    ax.plot(x_values,y_values)
    ax.plot(x_values,f(x_values))

    plt.show()

# spectral_gradient(middle_ear_effusion_state["100% effused"][0], middle_ear_effusion_state["100% effused"][1])
# spectral_gradient(middle_ear_effusion_state["25% effused"][0], middle_ear_effusion_state["25% effused"][1])

def find_min(x, y):
    current_min = y[0]
    min_index = 0
    for i in range(len(x)):
        if y[i] <= current_min:
            current_min = y[i]
            min_index=i
    
    min_f = x[min_index]

    # print(min_f)
    return min_index

# find_min(middle_ear_effusion_state["25% effused"][0], middle_ear_effusion_state["25% effused"][1])


def plot_straight_line_from_min_to_end(x,y):
    '''
    too simplistic
    '''
    min_index = find_min(x,y)

    fig,ax = plt.subplots()
    ax.plot(x,y)

    #y=mx+c
    m = (y[0]-y[min_index])/(x[0]-x[min_index])
    c=y[0]-m*x[0]

    ax.plot([x[0],x[min_index]], [y[0],y[min_index]],linestyle='--')
    ax.plot([x[min_index],x[-1]], [y[min_index],y[-1]],linestyle='--')
    plt.show()

# plot_straight_line_from_min_to_end(middle_ear_effusion_state["25% effused"][0], middle_ear_effusion_state["25% effused"][1])

#i could plot best line fit using a portion of the curve that doesn't quite get to the minimum (get m and c), then extend it until the minimum?
# inverse tan to get angle1 and angle2, then the angle inbetween is 180-angle1-angle2
# i don't specifically need to get the angle tho...

#other measures, find the width of the AR curve...

#use polynomial from numpy?

def polyfit_a_bit_away_from_min(x,y):
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

    fig,ax=plt.subplots()
    ax.plot(x,y)
    ax.plot(x[:min_index],f_left(x[:min_index]))
    ax.plot(x[min_index:],f_right(x[min_index:]))

    ax.set(title="Spectral Gradient AR ", xlabel="Frequency (Hz)", ylabel="reflectivity (normalised pressure field)")

    plt.show()

# polyfit_a_bit_away_from_min(middle_ear_effusion_state["0% effused"][0], middle_ear_effusion_state["0% effused"][1])
# polyfit_a_bit_away_from_min(middle_ear_effusion_state["25% effused"][0], middle_ear_effusion_state["25% effused"][1])
# polyfit_a_bit_away_from_min(middle_ear_effusion_state["100% effused"][0], middle_ear_effusion_state["100% effused"][1])



def polyfit_with_linear(ax, x,y, legend_label, colour, linestyle='-'):
    min_index=find_min(x,y)
    max_len=len(x)

    offset =int(5 * max_len/100)

    left= min_index-offset
   
    right = min_index+offset
    
    p_left=np.polyfit(x[:left], y[:left], deg=1)
    # print(f"left equation is: y={p_left[0]}x+{p_left[1]}")
    f_left=np.poly1d(p_left)
    left_angle = math.degrees(math.atan(p_left[0]*2000)) #scale by 2000
    # print(f"left angle is {left_angle}")

    
    p_right=np.polyfit(x[right:], y[right:], deg=1)
    # print(f"right equation is: y={p_right[0]}x+{p_right[1]}")
    f_right=np.poly1d(p_right)
    right_angle = math.degrees(math.atan(p_right[0]*2000))
    # print(f"right angle is {right_angle}")

    angle=180 - right_angle + left_angle
    # print(f"angle is {angle}")

    ax.plot(x,y, label=rf"{legend_label} \% effused $\vert$ spectral angle: {round(angle)}$^\circ$", color=colour, linestyle=linestyle)
    ax.plot(x[:min_index],f_left(x[:min_index]),color=colour, linestyle='--', alpha=0.4)
    ax.plot(x[min_index:],f_right(x[min_index:]),color=colour,linestyle='--', alpha=0.4)

    return ax



def plot_sg_ar(effused_dict, title="Spectral Gradient AR"):

    fig,ax = plt.subplots()
    colour=["tab:blue","tab:red","tab:green","tab:orange", "tab:purple", "tab:pink"]
    colour_i=0
    for legend_label, x_and_y in effused_dict.items():
        ax = polyfit_with_linear(ax, x_and_y[0], x_and_y[1], legend_label, colour[colour_i])
        colour_i+=1
    
    ax.set(title=title, xlabel="Frequency (Hz)", ylabel="reflectivity (normalised pressure field)")
    plt.legend()
    plt.show()

# plot_sg_ar(middle_ear_effusion_state_spread)
# plot_sg_ar(middle_ear_effusion_state_below_50)
# plot_sg_ar(middle_ear_effusion_state_above_50)


middle_ear_effusion_state_by_V_MEC = {
    # "0% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000),
    # "15% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12), start_f=2500, stop_f=3500, num=5000),
    "30% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12), start_f=2500, stop_f=3500, num=5000),
    "40% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.6*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "50% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.5*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "60% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "70% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.3*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "80% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.2*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    "90% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.1*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "95% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.05*7.7*10**-12), start_f=2500, stop_f=3500, num=5000),
    # "99% effusion" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.01*10**-12), start_f=2500, stop_f=3500, num=5000),
}
# plot_sg_ar(middle_ear_effusion_state_by_V_MEC, title="SGAR changing V_MEC (clay)")



middle_ear_effusion_state_TM_and_effusion = {
    "0% TM | 0% effused" : end_to_end_get_ar_response(RaviczMiddleEar(), start_f=2500, stop_f=3500, num=5000),
    "25% TM | 16% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6), start_f=2500, stop_f=3500, num=5000),
    "40% TM | 21% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6),start_f=2500, stop_f=3500, num=5000),
    # "50% TM | 30% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6), start_f=2500, stop_f=3500, num=5000),
    "70% TM | 35% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6),start_f=2500, stop_f=3500, num=5000),
    # "100% TM | 60% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6), start_f=2500, stop_f=3500, num=5000),
    "100% TM | 90% effused" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000)
}

# plot_sg_ar(middle_ear_effusion_state_TM_and_effusion)





middle_ear_effusion_state_truly_mass_only = {
    #"0" : end_to_end_get_ar_response(RaviczMiddleEar()),
    #"1mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=0.4*10**3, R_TOC=103*10**6)),
    "1mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=0.4*10**3)),
    "5mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=1.5*10**3 )),
    "22mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=6*10**3)),
    #"45mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=12*10**3, R_TOC=95*10**6)),
    "90mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=25*10**3)), #this is 50%
    #"120mg" : end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)),
    #"170mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=47.5*10**3, R_TOC=160*10**6)),
    #"340mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=95*10**3, R_TOC=160*10**6)),
    #"680mg" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=190*10**3, R_TOC=160*10**6)),
    #"2200mg extra" : end_to_end_get_ar_response(RaviczMiddleEar(M_TOC=610*10**3, R_TOC=310*10**6)), #this has hardly anychange
} #only changing m above 50% TM doesn't seem to do anything...
