import numpy as np

from plotting_utils.plotting_helper import plot_multiple_with_labels
from plotting_utils.extracted_data import MERCHANT_FIG3_HEALTHY_X, MERCHANT_FIG3_HEALTHY_Y
from .MerchantMiddleEar import FULL_PARAMS, MiddleEar, HEALTHY_PARAMS
from .AR_cylindrical_EC import get_WAI_freq_resp

# the reason i am doing this is to see if i can capture other resonances and impedance 
# but how will i use the transmission matrices? :0 
# oh use them in those fractiony equations to get reflection coeff? total impedance for reflectivity and set x as 0? :/ idk


def get_throat_and_mouth_for_truncated_cone(s_in:float, s_out:float, sep_l:float):
    s_throat = min(s_in, s_out)
    s_mouth = max(s_in, s_out)

    x_throat = np.sqrt(s_throat)*sep_l/(np.sqrt(s_mouth) - np.sqrt(s_throat))

    x_mouth = x_throat + sep_l

    return x_throat, x_mouth, s_throat, s_mouth



def get_transmission_matrices_for_truncated_cone(s_in, s_out, textbook=False, start_f: int = 100, stop_f: int = 10000, ):
    l = (21 * 10 ** -3)/6  #6 truncated segments in m
    roe = 1.225
    c = 343

    s_in *= 10**-6 #convert mm2 to m2
    s_out *= 10**-6 #convert mm2 to m2

    is_cylinder = s_in == s_out # do this check to avoid divide by infinity
    is_tapered = s_in > s_out

    
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    transmission_matrix_list = []

    for f in frequencies:
        k = 2*np.pi*f / c

        if is_cylinder: #avoid divide by 0 or infinity
            Z_char_acou = roe * c / s_in # the characteristic acoustic impedance

            A = np.cos(k*l)
            B = 1j* Z_char_acou * np.sin(k*l)
            C = 1j * np.sin(k*l) / Z_char_acou
            D = A
        
        else:
            x_throat, x_mouth, s_throat, s_mouth = get_throat_and_mouth_for_truncated_cone(s_in, s_out, l)
            # might want to move this line out of for loop

            A = np.sqrt(s_mouth/s_throat) * (np.cos(k*l) - np.sin(k*l)/(k*x_mouth))
            B = 1j*roe*c*np.sin(k*l)/(np.sqrt(s_throat*s_mouth))
            C = 1j * np.sqrt(s_throat*s_mouth) / (roe*c)
            C *= (np.cos(k*l)*(1/(k*x_mouth)-1/(k*x_throat)) + np.sin(k*l)*(1+(1/(k**2 * x_mouth * x_throat))))
            D = np.sqrt(s_mouth/s_throat) * (np.cos(k*l) + np.sin(k*l)/(k*x_throat))


        backwards_transmission_matrix = np.array([[A, B],[C, D]])

        if is_tapered:
            # if it is a reversed cone, we need to use the inverse transmission matrix (the forwards one)
            
            backwards_transmission_matrix = np.linalg.inv(backwards_transmission_matrix)

            #try the typo? :0 oh no why is this correct!
            if textbook:
                backwards_transmission_matrix = np.array([[D, B], [C, A]]) / (A*D - B*C)

        transmission_matrix_list.append(backwards_transmission_matrix)

    return np.array(transmission_matrix_list)

def get_transmission_matrices_for_entire_ear_canal(cone_transmission_matrices_array):

    # cone_transmission_matrices_array = [[cone1 matrices [[],[]], [[],[]]...], [cone2 matrices] ...]
    number_of_cones, number_of_matrices, _, _ = cone_transmission_matrices_array.shape
    # excess shape 

    ear_canal_matrices_list = []
    for i in range(number_of_matrices):  # dot the matrices from 1 to 6
        ear_canal_matrix = np.identity(2)
        for j in range(number_of_cones):
            ear_canal_matrix = ear_canal_matrix.dot(cone_transmission_matrices_array[j][i])
        # here when multiplied all 6 cones
        ear_canal_matrices_list.append(ear_canal_matrix)
        # move onto next frequency

    return np.array(ear_canal_matrices_list)

#using inverse...
healthy_cone_1 = get_transmission_matrices_for_truncated_cone(22, 14)
healthy_cone_2 = get_transmission_matrices_for_truncated_cone(14, 18)
healthy_cone_3 = get_transmission_matrices_for_truncated_cone(18, 23)
healthy_cone_4 = get_transmission_matrices_for_truncated_cone(23, 23)
healthy_cone_5 = get_transmission_matrices_for_truncated_cone(23, 18)
healthy_cone_6 = get_transmission_matrices_for_truncated_cone(18, 25)

healthy_cones = np.array([
    healthy_cone_1,
    healthy_cone_2,
    healthy_cone_3,
    healthy_cone_4,
    healthy_cone_5,
    healthy_cone_6
    ])

healthy_ear_canal_transmission_matrices = get_transmission_matrices_for_entire_ear_canal(healthy_cones)


healthy_middle_ear = MiddleEar(HEALTHY_PARAMS).get_middle_ear()
frequencies_h, reflection_coeffs_h, absorbances_h, impedances_h = get_WAI_freq_resp(
    healthy_middle_ear
) # need to move driver code to different file!!! otherwise importing makes the plots :(

def transform_impedances(ear_drum_impedances, transmission_matrices):
    ear_canal_impedances = []
    for i, matrix in enumerate(transmission_matrices):
        first_row, second_row = matrix  #each transmission matrix is [[A,B], [C, D]]
        A, B = first_row
        C, D = second_row 

        Z_me = ear_drum_impedances[i]

        Z_ec = (A*Z_me + B)/(C*Z_me + D)

        ear_canal_impedances.append(Z_ec)
    
    return ear_canal_impedances

ec_impedances_healthy = transform_impedances(impedances_h, healthy_ear_canal_transmission_matrices)

# using textbook
healthy_cone_1 = get_transmission_matrices_for_truncated_cone(22, 14, textbook=True)
healthy_cone_2 = get_transmission_matrices_for_truncated_cone(14, 18, textbook=True)
healthy_cone_3 = get_transmission_matrices_for_truncated_cone(18, 23, textbook=True)
healthy_cone_4 = get_transmission_matrices_for_truncated_cone(23, 23, textbook=True)
healthy_cone_5 = get_transmission_matrices_for_truncated_cone(23, 18, textbook=True)
healthy_cone_6 = get_transmission_matrices_for_truncated_cone(18, 25, textbook=True)

healthy_cones = np.array([
    healthy_cone_1,
    healthy_cone_2,
    healthy_cone_3,
    healthy_cone_4,
    healthy_cone_5,
    healthy_cone_6
    ])

healthy_ear_canal_transmission_matrices = get_transmission_matrices_for_entire_ear_canal(healthy_cones)
ec_impedances_healthy_textbook = transform_impedances(impedances_h, healthy_ear_canal_transmission_matrices)


#this is what i think is correct
impedances_plotting_dict = {
    "healthy me": [frequencies_h, abs(np.array(impedances_h))],
    "healthy ec": [frequencies_h, abs(np.array(ec_impedances_healthy_textbook))],
    "healthy ec (extracted)" : [MERCHANT_FIG3_HEALTHY_X, MERCHANT_FIG3_HEALTHY_Y]
}
plot_multiple_with_labels(
    "Impedances vs Frequency",
    "Frequency (Hz)",
    "Impedance Magnitude (mks ohm)",
    impedances_plotting_dict,
    log_code="xy",
)




# impedances_plotting_dict = {
#     "healthy (using true inverse for tapered cones)": [frequencies_h, abs(np.array(ec_impedances_healthy))],
#     "healthy (using textbook for tapered cones)": [frequencies_h, abs(np.array(ec_impedances_healthy_textbook))],
# }
# plot_multiple_with_labels(
#     "Ear Canal Impedances vs Frequency",
#     "Frequency (Hz)",
#     "Impedance Magnitude (mks ohm)",
#     impedances_plotting_dict,
#     log_code="xy",
# )


# left to do
# refactor all this code so i can just call one function for ear type
# then try reflectance again ... unsure if this is worth the bother
#
