from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from kringlebotn_model.compare_impedance_values import generate_and_plot_impedance_bode_plot, compare_ear_impedances_bode
from plotting_utils.plotting_helper import plot_multiple_with_labels
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
from ravicz_model.fine_tune import plot_sg_ar

#trying to just have strange mtoc changes and see waht teh ar response looks like + spectral angle...

healthy_rav = RaviczMiddleEar()
mtoc_25_healthy_rav = RaviczMiddleEar(M_TOC=25*10**3)

# generate_and_plot_impedance_bode_plot("mtoc 25 healthy ear", mtoc_25_healthy_rav)
# generate_and_plot_impedance_bode_plot("healthy ear", healthy_rav)

effused_middle_ear_100_with_more_fluid = RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6)
effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
effused_middle_ear_70 = RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)
effused_middle_ear_50 = RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)
effused_middle_ear_40 = RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)
effused_middle_ear_25 = RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)
normal_middle_ear = RaviczMiddleEar()


mtoc_25_dom = {
    "Healthy Ear": normal_middle_ear,
    "Healthy Ear with M_TOC=25": mtoc_25_healthy_rav,
    # "50% TM cover": effused_middle_ear_50,
    # "70% TM cover": effused_middle_ear_70,
    "100% TM cover": effused_middle_ear_100,
    # "100%* TM cover": effused_middle_ear_100_with_more_fluid,
    
}
compare_ear_impedances_bode(mtoc_25_dom)




# middle_ear_effusion_state_above_50 = {
#     "Healthy Ear with M_TOC=25": end_to_end_get_ar_response(mtoc_25_healthy_rav, start_f=2500, stop_f=3500, num=5000),
#     "50% TM covered" : end_to_end_get_ar_response(effused_middle_ear_50, start_f=2500, stop_f=3500, num=5000),
#     "70% TM covered" : end_to_end_get_ar_response(effused_middle_ear_70,start_f=2500, stop_f=3500, num=5000),
#     "100% TM covered" : end_to_end_get_ar_response(effused_middle_ear_100, start_f=2500, stop_f=3500, num=5000)
# }
# plot_sg_ar(middle_ear_effusion_state_above_50)

middle_ear_effusion_state_above_50_full = {
    "Healthy Ear": end_to_end_get_ar_response(normal_middle_ear),
    "Healthy Ear with M_TOC=25": end_to_end_get_ar_response(mtoc_25_healthy_rav),
    # "50% TM covered" : end_to_end_get_ar_response(effused_middle_ear_50),
    # "70% TM covered" : end_to_end_get_ar_response(effused_middle_ear_70),
    "100% TM covered" : end_to_end_get_ar_response(effused_middle_ear_100)
}
plot_multiple_with_labels(
    "Acoustic Reflectometry Response",
    "Frequency (Hz)",
    "Normalised Pressure",
    middle_ear_effusion_state_above_50_full,
)