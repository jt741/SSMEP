from typing import Final
import matplotlib.pyplot as plt
import numpy as np
import cmath


from merchant_model.circuit_and_resonant_branches import CircuitHelpers



# if you need to make same plots over and over again with different data:
# https://matplotlib.org/3.5.0/tutorials/introductory/usage.html#the-object-oriented-interface-and-the-pyplot-interface

# colour constants
COLOUR_DICT: Final = {
    "fully effused" : "tab:red",
    "healthy": "tab:green"
}

def set_size(width, fraction=1):
    """
    helper function to avoid scaling in LaTeX
    width = \the\textwidth
    fraction = scaling you would have done in LateX
    """

    fig_width_pt = width * fraction

    inches_per_pt = 1/72.27

    golden_ratio = (5**0.5 -1)/2

    #figure width in inches
    fig_width_inch = fig_width_pt * inches_per_pt
    fig_height_inch = fig_width_inch * golden_ratio

    fig_dim = (fig_width_inch, fig_height_inch)
    return fig_dim


# building blocks for more complicated plots / for quick data visualisation
def simple_plot(title, x_data, x_label, y_data, y_label, log_code = None):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set(title=title, xlabel=x_label, ylabel=y_label)

    if log_code:
        ax = optional_log_scale_helper(ax, log_code)

    plt.show()



def optional_log_scale_helper(ax, log_code:str):
    if log_code == "x":
        ax.set_xscale("log")
    elif log_code == "y":
        ax.set_yscale("log")
    elif log_code == "xy":
        ax.set_xscale("log")
        ax.set_yscale("log")
    else:
        raise ValueError("incorrect log_code")

    return ax


def plot_multiple_with_labels(title, x_label, y_label, lines_labels_dict:dict[str,list], log_code=None):
    fig, ax = plt.subplots()
    for legend_label,line in lines_labels_dict.items():
        ax.plot(line[0], line[1], label=legend_label, color=COLOUR_DICT.get(legend_label.lower()))

    ax.set(title=title, xlabel=x_label, ylabel=y_label)

    if log_code:
        ax = optional_log_scale_helper(ax, log_code)

    plt.legend()
    plt.show()








def compare_ear_impedances(ear_dict:dict[str,list]):
    ear_impedance_dict = {}

    for ear_name, middle_ear in ear_dict.items():
        ear_impedance_dict[ear_name] = list(generate_me_impedance_freq_resp(middle_ear))

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle("Comparing Impedances")

    mag_ax = axes[0]
    phase_ax = axes[1]


    for ear_name, ear_data in ear_impedance_dict.items():
        #plot impedance magnitude data
        mag_ax.plot(ear_data[0], ear_data[1], label=ear_name, color=COLOUR_DICT.get(ear_name.lower()))

        #plot impedance phase data
        phase_ax.plot(ear_data[0], ear_data[2], label=ear_name, color=COLOUR_DICT.get(ear_name.lower()))

    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)


    phase_ax.set(ylabel="Phase (radians)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000])
    phase_ax.set_ylim(-0.4*2*np.pi, 0.4*2*np.pi)

    mag_ax.legend()
    phase_ax.legend()
    plt.show()


def generate_and_plot_me_impedance_freq_resp(ear_name:str, middle_ear_branches, start_f=100, stop_f=8000):
    # generate data to plot
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    middle_ear_impedances_magnitude = []
    middle_ear_impedances_phase = []
    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(middle_ear_branches, f)

        middle_ear_impedances_magnitude.append(abs(Z_me))
        middle_ear_impedances_phase.append(cmath.phase(Z_me))

    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1, figsize=(6,8))
    fig.suptitle(f"{ear_name} Impedance")

    mag_ax = axes[0]
    mag_ax.plot(frequencies, middle_ear_impedances_magnitude)
    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    phase_ax = axes[1]
    phase_ax.plot(frequencies, middle_ear_impedances_phase)
    phase_ax.set(ylabel="Phase (radians)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000])
    phase_ax.set_ylim(-0.4*2*np.pi, 0.4*2*np.pi)


    plt.show()






def generate_me_impedance_freq_resp(
    middle_ear_branches: list,
    start_f: int = 100,
    stop_f: int = 8000,
):

    # generate data to plot
    frequencies = np.linspace(start=start_f, stop=stop_f, num=1000)
    middle_ear_impedances_magnitude = []
    middle_ear_impedances_phase = []
    for f in frequencies:
        Z_me = CircuitHelpers.branch_parallel_impedances(middle_ear_branches, f)

        middle_ear_impedances_magnitude.append(abs(Z_me))
        middle_ear_impedances_phase.append(cmath.phase(Z_me))

    return frequencies, middle_ear_impedances_magnitude, middle_ear_impedances_phase

def plot_me_impedance_freq_resp(ear_name: str,frequencies, middle_ear_impedances_magnitude, middle_ear_impedances_phase):
    # plot mag and phase stacked
    fig, axes = plt.subplots(2, 1)
    fig.suptitle(f"{ear_name} Impedance")

    mag_ax = axes[0]
    mag_ax.plot(frequencies, middle_ear_impedances_magnitude)
    mag_ax.set(ylabel="Magnitude (mks ohm)", xlabel="Frequency (Hz)")
    mag_ax.set_xscale("log")
    mag_ax.set_xticks([100, 1000, 10000])
    mag_ax.set_yscale("log")
    mag_ax.set_ylim(10**7, 3*10**9)

    phase_ax = axes[1]
    phase_ax.plot(frequencies, middle_ear_impedances_phase)
    phase_ax.set(ylabel="Phase (radians)", xlabel="Frequency (Hz)")
    phase_ax.set_xscale("log")
    phase_ax.set_xticks([100, 1000, 10000])
    phase_ax.set_ylim(-0.4*2*np.pi, 0.4*2*np.pi)


    plt.show()


###################  from ml for ref
def extract_single_state(full_state_matrix, idx_to_extract):
    extracted_state = []
    for state in full_state_matrix:
        extracted_state.append(state[idx_to_extract])
    return extracted_state


def plot_quad(pred, simu, max_step, initial_state, dt):
    fig, axes = plt.subplots(2, 2, figsize=(15, 8))
    pretty_initial_state = [round(x, 3) for x in initial_state]

    # Set general font size
    plt.rcParams["font.size"] = "16"

    fig.suptitle(f"Time Evolution \n " f"Initial State {pretty_initial_state}")

    plot_labels_y = {
        0: r"$x$ / $m$",
        1: r"$\dot{x}$ / $ms^{-1}$",
        2: r"$\theta$ / $rad$",
        3: r"$\dot{\theta}$ / $rads^{-1}$",
    }

    scan_var = {
        0: "Cart Location",
        1: "Cart Velocity",
        2: "Pole Angle",
        3: "Pole Angular Velocity",
    }
    mean_squared_error = {}

    for idx, ax in enumerate(axes.flat):
        # Set tick font size
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(16)

        predicted = extract_single_state(pred, idx)
        ax.plot(
            np.arange(0, max_step * dt, dt),
            predicted,
            label="prediction",
            color="tab:red",
        )

        simulated = extract_single_state(simu, idx)
        ax.plot(
            np.arange(0, max_step * dt, dt),
            simulated,
            label="simulated",
            color="tab:blue",
        )

        squared_error_total = 0
        for i in range(max_step):
            squared_error_total += (predicted[i] - simulated[i]) ** 2
        mean_squared_error[idx] = squared_error_total / max_step

        ax.set(
            ylabel=plot_labels_y[idx],
            xlabel="seconds / s",
            title=f"Predicting {scan_var[idx]} \n "
            f"MSE = {round(mean_squared_error[idx],4)}",
        )

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")
    plt.tight_layout(rect=(0, 0, 1, 0.98))
    plt.show()
