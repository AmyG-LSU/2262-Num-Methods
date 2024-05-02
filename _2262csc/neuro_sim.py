import argparse
import math
from math import exp
import numpy as np
import matplotlib.pyplot as plt
import json

## functions

##AG
def I_syn(w,g_bar,v_rev,previous_y,t,t_0,t_syn):
    result = math.exp((-(t-t_0)/t_syn))
    result2 = p_nested((-(t-t_0)/t_syn),10)
    return w * g_bar * (v_rev - previous_y) * ((t-t_0)/t_syn) * result2 #this could be a source for the problem
def p_nested(x, n):
    """
    Nested multiplication for the Taylor Series of e^x centered at 0
    :param x: value(s) to evaluate function on
    :param n: order of polynomial
    :return: evaluated polynomial
    """
    # The n'th order coefficient
    poly = 1/math.factorial(n)
    # loop from highest to lowest order (starting at n1)
    for k in reversed(range(n)):
        # coefficient is just 1/factorial(k)
        poly = 1/math.factorial(k) + x * poly
    return poly
def sx(t,t_s,t_r):
    ss = t - t_s - t_r
    if ss <= 0:
        return 0
    else:
        return 1

def ODEresolution(previous_y, dt, v_r, tao_m, isyn, c_m, s_value):
    return previous_y + (dt * ((-((previous_y - v_r)/tao_m)+(isyn / c_m)) * s_value))

def generateSpike(sim_time,spike_rate):
    return np.arange(0, sim_time,(sim_time*spike_rate))

##RF
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

def main():
    ##Constants
    f = open('jsonFILE.txt')
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

    mode = args.mode
    sim_time = args.sim_time * 0.001


    if mode == "spike":
        v0 = v_r
        t0 = 0
        t_s = 0 ## keep out of loop

        times = [t0]
        mapping = [v0] #starts at resting rate
        clac = [v0]

        spike_rate = args.spike_rate
        spikess = np.arange(0, sim_time, (1 / spike_rate))

        while times[-1] < sim_time:
            times.append(times[-1]+dt)

            t0_index = np.where(( times[-1] - spikess) >= 0)[0][-1]
            t0 = spikess[t0_index]
            Isyn = I_syn(w, g_bar, v_rev, clac[-1], times[-1], t0, t_syn)

            s_value = sx(times[-1], t_s, t_r)  # could be a source of wrong

            vm = ODEresolution(clac[-1], dt, v_r, t_m, Isyn, c_m, s_value)

            if vm >= v_thr:
                #set back to spike
                vm = v_r
                t_s = times[-1]
                #add values to array
                mapping.append(v_spike)
                clac.append(vm)
            else:
                mapping.append(vm)
                clac.append(vm)
        plt.plot(times, mapping, color='k')
        plt.xlabel("Time (s)", size=16)
        plt.ylabel("Membrane Potential (volt)", size=16)
        plt.show()
    if mode == "current":

        t_s = 0 #Time since last spike
        t = 0 #Current time
        v_m = v_r

        times = [] #Time values are recorded
        spikeTimes = [] #Time of spikes
        v_mValues = [] #Values of v_m

        current = args.current * 1E-9

        while t < sim_time:
            isyn = current

            cur_v_m = v_m + dt * ode(t, v_r, isyn, c_m, t_s, t_r, t_m, v_m)

            if(cur_v_m >= v_thr):
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

if __name__ == '__main__':
    main()

