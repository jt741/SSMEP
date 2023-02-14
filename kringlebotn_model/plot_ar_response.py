from acoustic_reflectometry_utils.acoustic_reflectometry_response import end_to_end_get_ar_response
from kringlebotn_model.KringlebotnMiddleEar import KringlebotnMiddleEar
from plotting_utils.plotting_helper import plot_multiple_with_labels
from ravicz_model.RaviczMiddleEar import RaviczMiddleEar


model = KringlebotnMiddleEar()
f, p = end_to_end_get_ar_response(model, stop_f=9000)


ravicz_model = RaviczMiddleEar()
f_healthy, ar_p_list_healthy = end_to_end_get_ar_response(ravicz_model, stop_f=9000)


plot_multiple_with_labels(
    "Pressure at measurement point vs Frequency",
    "Frequency (Hz)",
    "Pressure / Forward Wave Amplitude",
    {"Kringlebotn model": [f,p],
     "ravicz model":[f_healthy, ar_p_list_healthy] },
)

# print(abs(ravicz_model.get_impedance(1000)))
print(abs(model.get_impedance(1000)))