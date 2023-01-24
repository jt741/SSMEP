from plotting_utils.plotting_helper import (
    generate_and_plot_me_impedance_freq_resp,
    compare_ear_impedances,
    plot_multiple_with_labels
)

from merchant_model.MerchantMiddleEar import HEALTHY_PARAMS, FULL_PARAMS, MiddleEar


# healthy ear
healthy_middle_ear = MiddleEar(HEALTHY_PARAMS).get_middle_ear()
generate_and_plot_me_impedance_freq_resp("Healthy Middle Ear", healthy_middle_ear)

# full ear
fully_effused_middle_ear = MiddleEar(FULL_PARAMS).get_middle_ear()
generate_and_plot_me_impedance_freq_resp(
    "Fully Effused Middle Ear", fully_effused_middle_ear
)

# comparison
ear_compare_dict = {
    "Healthy": healthy_middle_ear,
    "Fully Effused": fully_effused_middle_ear,
}
compare_ear_impedances(ear_compare_dict)

# you're comparing with figure 5 in Merchant

