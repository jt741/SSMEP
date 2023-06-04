from plotting_utils.extracted_data import WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y, WAVELY_FULL_X, WAVELY_FULL_Y

from plotting_utils.plotting_helper import plot_multiple_with_labels

from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response, end_to_end_get_ar_response_norm_velocity
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar


#from merchant_model.AR_cylindrical_EC import ar_resp_dict as merchant_ar_dict



effused_middle_ear_100_with_more_fluid = RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6)
f_eff_100_with_more_fluid, ar_p_list_eff_100_with_more_fluid = end_to_end_get_ar_response(effused_middle_ear_100_with_more_fluid)

effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
f_eff_100, ar_p_list_eff_100 = end_to_end_get_ar_response(effused_middle_ear_100)

effused_middle_ear_70 = RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)
f_eff_70, ar_p_list_eff_70 = end_to_end_get_ar_response(effused_middle_ear_70)

effused_middle_ear_50 = RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)
f_eff_50, ar_p_list_eff_50 = end_to_end_get_ar_response(effused_middle_ear_50)

effused_middle_ear_40 = RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)
f_eff_40, ar_p_list_eff_40 = end_to_end_get_ar_response(effused_middle_ear_40)

effused_middle_ear_25 = RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)
f_eff_25, ar_p_list_eff_25 = end_to_end_get_ar_response(effused_middle_ear_25)

normal_middle_ear = RaviczMiddleEar()
f_healthy, ar_p_list_healthy = end_to_end_get_ar_response(normal_middle_ear)
ar_resp_dict = {

    "healthy Ravicz": [
        f_healthy,
        ar_p_list_healthy,
    ],
    "healthy (extracted [Chan])": [
        WAVELY_HEALTHY_X,
        WAVELY_HEALTHY_Y,
    ],
    # "effused 100% Ravicz with more fluid": [
    #     f_eff_100_with_more_fluid,
    #     ar_p_list_eff_100_with_more_fluid,
    # ],
    "effused 100% Ravicz": [
        f_eff_100,
        ar_p_list_eff_100,
    ],
    # "effused 70% Ravicz": [
    #     f_eff_70,
    #     ar_p_list_eff_70,
    # ],
    # "effused 50% Ravicz": [
    #     f_eff_50,
    #     ar_p_list_eff_50,
    # ],
    # "effused 40% Ravicz": [
    #     f_eff_40,
    #     ar_p_list_eff_40,
    # ],
    # "effused 25% Ravicz": [
    #     f_eff_25,
    #     ar_p_list_eff_25,
    # ],
    "fully effused (extracted [Chan])": [
        WAVELY_FULL_X,
        WAVELY_FULL_Y,
    ],
    #"healthy Merchant" : merchant_ar_dict["healthy"],
    #"effused Merchant" : merchant_ar_dict["fully effused"]
    
}
plot_multiple_with_labels(
    "Pressure at measurement point vs Frequency",
    "Frequency (Hz)",
    "Pressure / Forward Wave Amplitude",
    ar_resp_dict,
)


# plotting norm v (this will just be the imepedance at the middle ear right?? compare with using a lumped inductor?)
f_healthy_u, ar_p_list_healthy_u = end_to_end_get_ar_response_norm_velocity(normal_middle_ear)
f_eff_100_u, ar_p_list_eff_100_u = end_to_end_get_ar_response_norm_velocity(effused_middle_ear_100)

ar_norm_u_resp_dict = {
    "healthy Ravicz et al.": [
        f_healthy_u,
        ar_p_list_healthy_u,
    ],
    "healthy (extracted [Chan et al.])": [
        WAVELY_HEALTHY_X,
        WAVELY_HEALTHY_Y,
    ],
     "effused 100% Ravicz et al.": [
        f_eff_100_u,
        ar_p_list_eff_100_u,
    ],
    "fully effused (extracted [Chan et al.])": [
        WAVELY_FULL_X,
        WAVELY_FULL_Y,
    ],
}
plot_multiple_with_labels(
    "Pressure at measurement point vs Frequency",
    "Frequency (Hz)",
    "Pressure / Velocity of source (assumed constant) ",
    ar_norm_u_resp_dict,
)