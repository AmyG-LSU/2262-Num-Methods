
import argparse
import matplotlib.pyplot as plt
import json
from math import exp
import numpy as np

f = open('jsonFILE.txt')

parser = argparse.ArgumentParser(description="Neuron Simulation")
parser.add_argument("-m", "--mode", required=True, choices={"spike", "current"},
                    help="Simulation mode: 'spike' or 'current'")
#The “spike” mode will simulate a neuron being excited by a series of input spikes
#The “current” mode will simulate a neuron being excited by a constant input current

parser.add_argument("-s", "--sim_time", required=True, type=int, help="Simmulation time in milliseconds or (ms)")
#Amount of time to run the simulation for in units of milliseconds.

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--spike_rate", type=float, help="Input spike rate in Hz (only for 'spike' mode)")
#Allows the user to specify the input spike rate in units of Hz (30Hz would be 30 spikes per second). Only used for “spike” mode.

group.add_argument("--current", type=float, help="Input current in nanoamps (nA) (only for 'current' mode)")
# Allows the user to specify the input current for the “current” mode. Units should be in nanoamps (nA).

args = parser.parse_args()


def main():
    #Loading constants from the JSON file
    data = json.load(f)
    v_r = data["v_r"]
    v_thr = data["v_thr"]
    v_spike = data["v_spike"]   ## main hoold eulers method
    v_rev = data["v_rev"]
    t_m = data["tao_m"]
    t_syn = data["tao_syn"]
    c_m = data["c_m"]
    g_bar = data["g_bar"]
    t_r = data["t_r"]
    w = data["w"]
    dt = data["dt"]


    mode = args.mode
    sim_time = args.sim_time * 1E-3

    print("Mode:", mode)
    print("Simulation time (Ms):", sim_time)

    if mode == "spike":
        spike_rate = args.spike_rate
        spikeTrain = np.arange(0, sim_time, sim_time / spike_rate)
    else:
        current = args.current * 1E-9
        print("Input current (nA):", current)

    times = [] #Time values are recorded
    spikeTimes = [] #Time of spikes
    v_mValues = [] #Values of v_m


    #Starting conditions
    t_s = 0 #Time since last spike
    t = 0 #Current time
    v_m = v_r


    #For spike
    #we are simulating another neurons "spike", and that feeds voltage into our own neuron
    # isyn would be set to the isyn() method, instead of current
    #main loop
    while t < sim_time:
        if mode == "current":
            isyn = current
        elif mode == "spike":
            current_spike_time = np.where((t - spikeTrain) >=0)[0][-1]
            t_0 = spikeTrain[current_spike_time]
            print("Current time: ", t, "Start of last presynaptic spike: ", t_0)
            isyn = Isyn(v_rev, w, v_m, g_bar, t_0, t_syn, t)
        cur_v_m = v_m + dt * ode(t, v_r, isyn, c_m, t_s, t_r, t_m, v_m)
        #print(cur_v_m)

        if (cur_v_m >= v_thr):
            v_mValues.append(cur_v_m)
            cur_v_m = v_r
            t_s = t
            spikeTimes.append(t)
        else:
            v_mValues.append(cur_v_m)
        v_m = cur_v_m
        times.append(t)
        t += dt

    plot(v_mValues, times, spikeTimes)


def plot(values, t, spikeTimes): #plotting
    plt.plot(t, values)
    plt.show()


def ode(t, v_r, I_syn, c_m, t_s, t_r, t_m, v_m):
    """
    :param t - time
    :param v_r - resting potential
    :param I_Syn - Total input to current
    :param c_m - Membrance capacitance
    :param t_s - Time of last spike
    :param t_r - Refactory period
    :param t_m - Decay constant
    """
    activate = activation(t, t_r, t_s)
    eval = ((-(v_m - v_r) / t_m) + (I_syn / c_m))#calcutaes the differential equations
    return eval * activate


def activation(t, t_r, t_s):
    x = t - t_s - t_r
    if x <= 0:
        return 0
    else: #check if the time of spike is not between the refactory periods
        return 1


def Isyn(v_rev, w, v_m, gbar, t_0, t_syn, t):
    """
     :param v_rev - reversal potential
     :param w - weight of synapse
     :param v_m - membrane voltage
     :param gbar - maximum conductance
     :param t_0 - time the spike started
     :param t - current time
     :param t_syn - decay time constant
     """
    return w * gbar * (v_rev - v_m) * ((t - t_0) / t_syn) * exp((-(t - t_0) / t_syn)) #part of the spike methos


main()


