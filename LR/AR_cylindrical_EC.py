import numpy as np
from plotting_helper import plot_multiple_with_labels

from circuit_and_resonant_branches import CircuitHelpers
from middle_ear_maker import FULL_PARAMS, MiddleEar, HEALTHY_PARAMS


def get_cylindrical_ear_canal_constants():
    """model ear canal as narrow duct --> inductance analogy
    also return the characteristic impedance.
    """
    roe = 1.204
    l = 21 * 10**-3
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    c = 343

    L = roe * l / A  # inductance

    Z0 = roe * c / A  # characteristic impedance

    return L, Z0


def get_acoustic_reflectometry_response(frequencies: list, reflection_coeffs: list):
    """trying to mimic what a microphone would measure x away from TM
    need to check the logic of what i am doing (confused about reflection coefficients)
    """
    x = 21 * 10**-3
    c = 343

    p_list = []
    for i, f in enumerate(frequencies):
        forward = np.exp(1j * 2 * np.pi * f * (-1 * x / c))
        backward = reflection_coeffs[i] * np.exp(1j * 2 * np.pi * f * (x / c))
        p = forward + backward
        p_list.append(p.real)

    return p_list


def get_WAI_freq_resp(
    middle_ear_branches: list,
    start_f: int = 100,
    stop_f: int = 8000,
):
    """
    generate data for WAI frequency response
    """
    # generate reflection coeffs
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    L, Z_0 = get_cylindrical_ear_canal_constants()

    reflection_coeffs = []

    absorbances = []

    impedances = []

    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(middle_ear_branches, f)
        Z_ec = 1j * 2 * np.pi * f * L

        Z_total = Z_ec + Z_me

        impedances.append(abs(Z_total))

        reflection_coeff = (Z_total - Z_0) / (
            Z_total + Z_0
        )  # also known as 'reflectance' in Merchant's paper

        reflection_coeffs.append(reflection_coeff)  
        absorbances.append(1 - abs(reflection_coeff) ** 2)

    return frequencies, reflection_coeffs, absorbances, impedances


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
    "Reflection coeff vs Frequency",
    "Frequency (Hz)",
    "Reflection coeff",
    reflection_coeffs_dict,
)


energy_reflectance_dict = {
    "fully effused": [frequencies, 1-np.array(absorbances)],
    "healthy": [frequencies_h, 1-np.array(absorbances_h)],
}
plot_multiple_with_labels(
    "Energy Reflectance vs Frequency",
    "Frequency (Hz)",
    "Energy Reflectance",
    energy_reflectance_dict,
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
}
plot_multiple_with_labels(
    "pressure field at measurement point vs Frequency",
    "Frequency (Hz)",
    "Pressure ()",
    ar_resp_dict,
)


absorbance_plotting_dict = {
    "fully effused": [frequencies, absorbances],
    "healthy": [frequencies_h, absorbances_h],
}
# Absorbance will NOT match paper bc we are using different model for EC
plot_multiple_with_labels(
    "Absorbance vs Frequency",
    "Frequency (Hz)",
    "Absorbance",
    absorbance_plotting_dict,
    log_code="x",
)


impedances_plotting_dict = {
    "fully effused": [frequencies, impedances],
    "healthy": [frequencies_h, impedances_h],
}
# This is technically the total impedance (Zec + Zme), but it will be dominated by Zme, and since that was taken from Merchant directly, we expect it to match
plot_multiple_with_labels(
    "Total Impedance vs Frequency",
    "Frequency (Hz)",
    "Impedance Magnitude (mks ohm)",
    impedances_plotting_dict,
    log_code="xy",
)


####################### SCraps ############


# reflectance_plotting_dict = {
#     "fully effused": [frequencies, reflection_coeffs, "tab:red"],
#     "healthy": [frequencies_h, reflection_coeffs_h, "tab:green"],
# }
# plot_multiple_with_labels("Reflectance vs Frequency", "Frequency (Hz)", "Reflectance", reflectance_plotting_dict, log_code="x")
