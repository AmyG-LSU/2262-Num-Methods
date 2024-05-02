#### test case 100 ms 100 hz rate
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import json


###################### Functions#### AMY ###############################
def I_syn(w,g_bar,v_rev,previous_y,t,t_0,t_syn):
    result = math.exp((-(t-t_0)/t_syn))
    return w * g_bar * (v_rev - previous_y) * ((t-t_0)/t_syn) * result #this could be a source for the problem

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
########################################################################


def main():
    #####################Constants###########################
    f = open('jsonFILE.txt')
    data = json.load(f)
    v_r = data["v_r"]
    v_thr = data["v_thr"]
    v_spike = data["v_spike"]
    v_rev = data["v_rev"]
    t_m = data["tao_m"]
    t_syn = data["tao_syn"]
    c_m = data["c_m"]
    g_bar = data["g_bar"]
    t_r = data["t_r"]
    w = data["w"]  #!!!!!!!!!! For this running test case to atually even remotely work must be changed to  0.01
    dt = data["dt"] ## clarify with teacher what the step is in whether ms or s

    ######################Starting Conditions and holding arrays################################
    # starting conditions
    v0 = v_r
    t0 = 0

    times = [t0]
    plot = [v0] #starts at resting rate
    clac = [v0]
############easy command line###################### just type milliseconds and spike rate
    parser = argparse.ArgumentParser(description='Project 1  method:')
    parser.add_argument('sim_time' , type=float)
    parser.add_argument('spike_rate', type=int)
    args = parser.parse_args()

##################needed for running #######################################################
    sim_time = args.sim_time * 0.001 # due to the input in ms this converts it to sec
    spike_rate = args.spike_rate
    spikess = np.arange(0, sim_time, (1 / spike_rate))
    t_s = 0 ## keep out of loop

#runs of times array using the inputed time period into the equations
    while times[-1] < sim_time:

        times.append(times[-1] + dt)

        ## creates the spike array for spike
        t0_index = np.where(( times[-1] - spikess) >= 0)[0][-1]
        t0 = spikess[t0_index]
        ## plug t0 to calulate isyn
        Isyn = I_syn(w, g_bar, v_rev, clac[-1], times[-1], t0, t_syn)
        # calulate s(x)
        s_value = sx(times[-1], t_s, t_r)  # could be a source of wrong


        ## plug in isyn and s(x) with constants provided to ode for eulers method
        vm = ODEresolution(clac[-1], dt, v_r, t_m, Isyn, c_m, s_value)

        if vm >= v_thr:

            plot.append(v_spike)
            vm = v_r
            t_s = times[-1]
            clac.append(vm)
        else:
            clac.append(vm)
            plot.append(vm)
            #vspike dont add to calculation
            #vspike add to plotting

####this is the end of list making


    plt.plot(times, plot, color='k')
    plt.xlabel("Time (s)", size=16)
    plt.ylabel("Membrane Potential (volt)", size=16)
    plt.show()

if __name__ == "__main__":
    main()