def total_impedance_parallel(*impedances):
    running_sum = 0
    for indv_impedance in impedances:
        running_sum += 1/indv_impedance
    return 1/running_sum

def total_impedance_series(*impedances):
    running_sum = 0
    for indv_impedance in impedances:
        running_sum += indv_impedance
    return running_sum