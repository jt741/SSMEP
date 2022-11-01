import cmath

import numpy as np
from plotting_helper import log_plot, simple_plot

from circuit_and_resonant_branches import CircuitHelpers
from middle_ear_maker import HEALTHY_PARAMS, MiddleEar


def generate_impedance_frequency_response(
    branches,
    start_f=100,
    stop_f=8000,
):
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    middle_ear_impedances_magnitude = []
    middle_ear_impedances_phase = []
    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(branches, f)

        middle_ear_impedances_magnitude.append(abs(Z_me))
        middle_ear_impedances_phase.append(cmath.phase(Z_me))

    return frequencies, middle_ear_impedances_magnitude, middle_ear_impedances_phase


# healthy ear
healthy_middle_ear = MiddleEar(HEALTHY_PARAMS).get_middle_ear()



# might want to continue messing with these wrappers

healthy_f, healthy_zme_mag, healthy_zme_phase = generate_impedance_frequency_response(
    healthy_middle_ear
)
ax = simple_plot(
    "Healthy Ear Impedance",
    healthy_f,
    "frequency (Hz)",
    healthy_zme_mag,
    "Impedance (magnitude)",
)
log_plot(ax)

# to get the phase plot in cyc you would have to divide radians by 2pi
ax_ph = simple_plot(
    "Healthy Ear Impedance",
    healthy_f,
    "frequency (Hz)",
    healthy_zme_phase,
    "Impedance (phase) (radias)",
)
log_plot(ax_ph, logy=False)


# you're comparing with figure 5 in Merchant

# TODO: do a full ear as well, first use cyclindrical duct for EC and see if you can get AR results back (do i need to have the EC model? just length maybe)
# TODO: then use the 6 tapered cones and compare graphs and do AR again and could also do Tympanometry
# TODO: could compare tapered cones to cylinder (with what tho.....)
