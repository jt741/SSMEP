
import matplotlib.pyplot as plt
import numpy as np

#lol ml hell

#if you need to make same plots over and over again with different data:
# https://matplotlib.org/3.5.0/tutorials/introductory/usage.html#the-object-oriented-interface-and-the-pyplot-interface

# building blocks for more complicated plots / for quick data visualisation
def simple_plot(title, x_data, x_label,  y_data, y_label ):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set(title=title, xlabel=x_label, ylabel=y_label)
    #plt.show()
    return ax

def log_plot(ax:plt.Axes, logx:bool=True, logy:bool=True):
    if logx:
        ax.set_xscale('log')
    if logy:
        ax.set_yscale('log')
    plt.show()




# from ml for ref
def extract_single_state(full_state_matrix, idx_to_extract):
    extracted_state = []
    for state in full_state_matrix:
        extracted_state.append(state[idx_to_extract])
    return extracted_state

def plot_quad(pred, simu, max_step, initial_state, dt):
    fig, axes = plt.subplots(2, 2, figsize=(15,8))
    pretty_initial_state = [round(x, 3) for x in initial_state]

    # Set general font size
    plt.rcParams['font.size'] = '16'



    fig.suptitle(f"Time Evolution \n "
                 f"Initial State {pretty_initial_state}")

    plot_labels_y = {
        0: r"$x$ / $m$",
        1: r"$\dot{x}$ / $ms^{-1}$",
        2: r"$\theta$ / $rad$",
        3: r"$\dot{\theta}$ / $rads^{-1}$"
    }

    scan_var = {
        0: "Cart Location",
        1: "Cart Velocity",
        2: "Pole Angle",
        3: "Pole Angular Velocity"
    }
    mean_squared_error = {}

    for idx, ax in enumerate(axes.flat):
        # Set tick font size
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(16)

        predicted = extract_single_state(pred, idx)
        ax.plot(np.arange(0, max_step*dt,dt), predicted,
                label="prediction",
                color="tab:red")

        simulated = extract_single_state(simu, idx)
        ax.plot(np.arange(0, max_step*dt,dt), simulated, label="simulated",
                color="tab:blue")

        squared_error_total = 0
        for i in range(max_step):
            squared_error_total += (predicted[i] - simulated[i]) ** 2
        mean_squared_error[idx] = squared_error_total / max_step

        ax.set(
            ylabel=plot_labels_y[idx],
            xlabel="seconds / s",
            title=f"Predicting {scan_var[idx]} \n "
                  f"MSE = {round(mean_squared_error[idx],4)}"
        )

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.tight_layout(rect=(0, 0, 1, 0.98))
    plt.show()