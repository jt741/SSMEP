import numpy as np


def convert_p_to_c(p_list):
    c_list = []
    # TODO: define how p relates to c in the ear canal
    # convert -300Pa to 300Pa to corresponding c_list changes
    return c_list

# just need model to have a method of get_impedance which takes frequency as param
def get_impedance_of_middle_ear(model, frequency=226):
    return model.get_impedance(w=2*np.pi*frequency)

def get_reflection_coeffs_as_function_of_c(c_list, Z_me):
    roe = 1.225 # density of air
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    
    reflection_coeffs = []
    for c in c_list:
        Z_0 = roe * c / A  # characteristic impedance
        reflection_coeffs.append((Z_me - Z_0)/(Z_me + Z_0))

    return reflection_coeffs

def get_tympanometry_response(c_list, reflection_coeffs):
    roe = 1.225 #density of air (in Ear Canal)
    y_list =[]
    for i in range(len(reflection_coeffs)):
        c, r = c_list[i], reflection_coeffs[i]
        y = ((1-r)/(1+r))/(roe*c)
        y_list.append(abs(y))
        # admittance will be complex
        # but since low frequency is stiffness dominated, we can just take real part to approimate to absolute
    
    return y_list


def end_to_end_tympanometry_response(model, start_p, stop_p):
    p_list = np.linspace(start_p, stop_p)
    c_list = convert_p_to_c(p_list)
    Z_me = get_impedance_of_middle_ear(model)
    refl_coeff_list = get_reflection_coeffs_as_function_of_c(c_list, Z_me)
    y_list = get_tympanometry_response(c_list, refl_coeff_list)
    
    # for plotting we would actually return p_list
    return p_list, y_list