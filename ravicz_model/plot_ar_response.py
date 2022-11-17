from plotting_utils.extracted_data import WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y, WAVELY_FULL_X, WAVELY_FULL_Y

from plotting_utils.plotting_helper import plot_multiple_with_labels

from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar


#from merchant_model.AR_cylindrical_EC import ar_resp_dict as merchant_ar_dict

normal_middle_ear = RaviczMiddleEar()
f_healthy, ar_p_list_healthy = end_to_end_get_ar_response(normal_middle_ear)

effused_middle_ear_100 = RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)
f_eff_100, ar_p_list_eff_100 = end_to_end_get_ar_response(effused_middle_ear_100)


ar_resp_dict = {

    "healthy Ravicz": [
        f_healthy,
        ar_p_list_healthy,
    ],
    "healthy (extracted [Chan])": [
        WAVELY_HEALTHY_X,
        WAVELY_HEALTHY_Y,
    ],
    "effused 100% Ravicz": [
        f_eff_100,
        ar_p_list_eff_100,
    ],
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


