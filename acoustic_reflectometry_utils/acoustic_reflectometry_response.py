import numpy as np

# just need model to have a method of get_impedance which takes frequency as param

def get_impedance_frequency_response(model, start_f, stop_f):
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)

    impedances = []
    for f in frequencies:
        impedances.append(model.get_impedance(w=2*np.pi*f))

    return frequencies, impedances

def get_reflection_coeffs(impedances):
    roe = 1.225 # density of air
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    c = 343 #speed of sound in air
    Z_0 = roe * c / A  # characteristic impedance

    reflection_coeffs = []

    for Z_me in impedances:
        reflection_coeffs.append((Z_me - Z_0)/(Z_me + Z_0))

    return reflection_coeffs

def get_acoustic_reflectometry_response(frequencies, reflection_coeffs):
    x = -28*10**-3 #28? 25? :0
    c = 343

    p_list = []
    for i, f in enumerate(frequencies):
        forward = np.exp(1j * 2 * np.pi * f * (- x / c))
        backward = reflection_coeffs[i] * np.exp(1j * 2 * np.pi * f * (x / c))
        p = forward + backward
        p_list.append(abs(p)) # plot absolute instead of real value 

    return p_list



def end_to_end_get_ar_response(model, start_f=1500, stop_f=5000):
    f_list, Z_me_list = get_impedance_frequency_response(model, start_f, stop_f)
    refl_coeff_list = get_reflection_coeffs(Z_me_list)
    ar_p_list = get_acoustic_reflectometry_response(f_list, refl_coeff_list)

    return f_list, ar_p_list