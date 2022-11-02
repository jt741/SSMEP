from plotting_helper import (
    generate_and_plot_me_impedance_freq_resp,
    compare_ear_impedances,
)

from middle_ear_maker import HEALTHY_PARAMS, FULL_PARAMS, MiddleEar


# healthy ear
healthy_middle_ear = MiddleEar(HEALTHY_PARAMS).get_middle_ear()
generate_and_plot_me_impedance_freq_resp("Healthy Middle Ear", healthy_middle_ear)

# full ear
fully_effused_middle_ear = MiddleEar(FULL_PARAMS).get_middle_ear()
generate_and_plot_me_impedance_freq_resp(
    "Fully Effused Middle Ear", fully_effused_middle_ear
)

# would be nice to plot these two on the same graph (we are comparing after all)!
ear_compare_dict = {
    "Healthy": healthy_middle_ear,
    "Fully Effused": fully_effused_middle_ear,
}
compare_ear_impedances(ear_compare_dict)

# you're comparing with figure 5 in Merchant

# TODO: do a full ear as well, first use cyclindrical duct for EC and see if you can get AR results back (do i need to have the EC model? just length maybe)
# TODO: then use the 6 tapered cones and compare graphs and do AR again and could also do Tympanometry
# TODO: could compare tapered cones to cylinder (with what tho.....)
