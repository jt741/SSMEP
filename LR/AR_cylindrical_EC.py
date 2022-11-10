import numpy as np
from plotting_helper import plot_multiple_with_labels

from circuit_and_resonant_branches import CircuitHelpers
from middle_ear_maker import FULL_PARAMS, MiddleEar, HEALTHY_PARAMS
from extracted_data import FIG5_HEALTHY_X, FIG5_HEALTHY_Y, FIG5_FULL_X, FIG5_FULL_Y, WAVELY_FULL_X, WAVELY_FULL_Y, WAVELY_HEALTHY_X, WAVELY_HEALTHY_Y


def get_cylindrical_ear_canal_constants():
    """model ear canal as narrow duct --> inductance analogy
    also return the characteristic impedance.
    """
    roe = 1.225 # density of air
    l = 21 * 10**-3 #length of ear canal
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    c = 343 #speed of sound in air

    L = roe * l / A  # equivalent inductance

    Z0 = roe * c / A  # characteristic impedance

    return L, Z0


def get_acoustic_reflectometry_response(frequencies: list, reflection_coeffs: list):
    """trying to mimic what a microphone would measure x away from TM"""
    #x = -28.6 * 10**-3    # this is negative because of how the axes are defined
    x = -21*10**-3
    c = 343

    p_list = []
    for i, f in enumerate(frequencies):
        forward = np.exp(1j * 2 * np.pi * f * (- x / c))
        backward = reflection_coeffs[i] * np.exp(1j * 2 * np.pi * f * (x / c))
        p = forward + backward
        p_list.append(abs(p)) # plot absolute instead of real value 

    return p_list


def get_WAI_freq_resp(
    middle_ear_branches: list,
    start_f: int = 100,
    stop_f: int = 10000,
):
    """
    generate data for WAI frequency response
    """
    # generate reflection coeffs
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    _, Z_0 = get_cylindrical_ear_canal_constants() # L is not used at the moment

    reflection_coeffs = []

    absorbances = []  #not plotted at the moment

    middle_ear_impedances = []

    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(middle_ear_branches, f)
           
        middle_ear_impedances.append(Z_me)

        reflection_coeff_at_ear_drum = (Z_me - Z_0)/(Z_me + Z_0)

        reflection_coeffs.append(reflection_coeff_at_ear_drum)  
        absorbances.append(1 - abs(reflection_coeff_at_ear_drum) ** 2)

    return frequencies, reflection_coeffs, absorbances, middle_ear_impedances


fully_effused_middle_ear = MiddleEar(FULL_PARAMS).get_middle_ear()
frequencies, reflection_coeffs, absorbances, impedances = get_WAI_freq_resp(
    fully_effused_middle_ear
)

healthy_middle_ear = MiddleEar(HEALTHY_PARAMS).get_middle_ear()
frequencies_h, reflection_coeffs_h, absorbances_h, impedances_h = get_WAI_freq_resp(
    healthy_middle_ear
)


reflection_coeffs_dict = {
    "fully effused": [frequencies, reflection_coeffs],
    "healthy": [frequencies_h, reflection_coeffs_h],
}
plot_multiple_with_labels(
    "Reflection Coefficient at Ear Drum vs Frequency",
    "Frequency (Hz)",
    "Reflection Coefficient at Ear Drum",
    reflection_coeffs_dict,
)


ar_resp_dict = {
    "fully effused": [
        frequencies,
        get_acoustic_reflectometry_response(frequencies, reflection_coeffs),
    ],
    "healthy": [
        frequencies_h,
        get_acoustic_reflectometry_response(frequencies_h, reflection_coeffs_h),
    ],
    "fully effused (extracted [Chan])": [
        WAVELY_FULL_X,
        WAVELY_FULL_Y,
    ],
    "healthy (extracted [Chan])": [
        WAVELY_HEALTHY_X,
        WAVELY_HEALTHY_Y,
    ],
}
plot_multiple_with_labels(
    "Pressure at measurement point vs Frequency",
    "Frequency (Hz)",
    "Pressure / Forward Wave Amplitude",
    ar_resp_dict,
)


impedances_plotting_dict = {
    "fully effused": [frequencies, abs(np.array(impedances))],
    "healthy": [frequencies_h, abs(np.array(impedances_h))],
    # "healthy (extracted)": [FIG5_HEALTHY_X,FIG5_HEALTHY_Y],
    # "full (extracted)": [FIG5_FULL_X,FIG5_FULL_Y]
}
plot_multiple_with_labels(
    "Middle Ear Impedance vs Frequency",
    "Frequency (Hz)",
    "Middle Ear Impedance Magnitude (mks ohm)",
    impedances_plotting_dict,
    log_code="xy",
)

