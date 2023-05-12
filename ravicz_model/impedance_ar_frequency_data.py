import csv
from acoustic_reflectometry_utils.acoustic_reflectometry_response import get_impedance_frequency_response, get_reflection_coeffs, get_acoustic_reflectometry_response
import numpy as np

from ravicz_model.RaviczMiddleEar import RaviczMiddleEar
def get_cylindrical_ear_canal_inductance():
    """model ear canal as narrow duct --> inductance analogy
    """
    roe = 1.225 # density of air
    l = 28 * 10**-3 #length of ear canal to measurement point
    A = 44.18 * 10**-6  # Merchant takes CSA to be 44.18mm^2
    c = 343 #speed of sound in air

    L = roe * l / A  # equivalent inductance
    
    return L

def get_z_ec(L, frequencies):
    impedances_of_ear_canal = 1j*L*2*np.pi*frequencies #oh no was the old data with just f :(
    return impedances_of_ear_canal

def get_total_impedance(z_ec, z_me):
    return z_ec + z_me


def get_data_to_give_to_max(model, start_f=1500, stop_f =5000, num=1000):
    f_list, z_me_list = get_impedance_frequency_response(model, start_f, stop_f, num)
    
    L = get_cylindrical_ear_canal_inductance()
    z_ec_array = get_z_ec(L, f_list)
    z_total = get_total_impedance(z_ec_array, np.array(z_me_list))

    refl_coeff_list = get_reflection_coeffs(z_me_list)
    ar_p_list = get_acoustic_reflectometry_response(f_list, refl_coeff_list)

    # print(abs(refl_coeff_list[0]), abs(refl_coeff_list[50]),abs( refl_coeff_list[-1]))
    # print(z_me_list[0], z_total[0], z_ec_array[0])
    return f_list, ar_p_list, z_total


middle_ear_models_effusion_state_TM_and_effusion_range = [
    ("0", RaviczMiddleEar()),
    ("25", RaviczMiddleEar(C_MEC=6.5*10**-12, M_TOC=0.4*10**3, R_TOC=103*10**6)),
    ("40", RaviczMiddleEar(C_MEC=6.1*10**-12, M_TOC=1.5*10**3, R_TOC=110*10**6)),
    ("50", RaviczMiddleEar(C_MEC=5.4*10**-12, M_TOC=25*10**3, R_TOC=95*10**6)),
    ("70", RaviczMiddleEar(C_MEC=5.0*10**-12, M_TOC=32*10**3, R_TOC=130*10**6)),
    ("100", RaviczMiddleEar(C_MEC=3.1*10**-12, M_TOC=190*10**3, R_TOC=160*10**6)),
    # ("100" , end_to_end_get_ar_response(RaviczMiddleEar(C_MEC=0.77*10**-12, M_TOC=610*10**3, R_TOC=310*10**6), start_f=2500, stop_f=3500, num=5000))
]

def go_through_effusions(list_of_ears):
    for ear in list_of_ears:
        print(f"****THIS IS DATA FOR {ear[0]}% effused ears****")
        get_data_to_give_to_max(ear[1])
        print("\n")

# go_through_effusions(middle_ear_models_effusion_state_TM_and_effusion_range)

def write_to_csv(f, p_norm, z_total, filename="healthy"):
    data=zip(f,p_norm, z_total)
    csv_file = f"ravicz_model/new_data_for_max/{filename}_effusion_impedance_and_acoustic_reflectometry_data.csv"

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["frequency (Hz)", "total pressure/forwards pressure", "acoustic impedance at measurement point (z_total = z_ec + z_me)"])

        for row in data:
            writer.writerow(row)


def generate_multiple_csv(list_of_ears):
    for ear in list_of_ears:
        f, p , z = get_data_to_give_to_max(ear[1])
        write_to_csv(f, p, z, ear[0])

generate_multiple_csv(middle_ear_models_effusion_state_TM_and_effusion_range)