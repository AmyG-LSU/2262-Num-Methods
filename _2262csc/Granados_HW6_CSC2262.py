import matplotlib.pyplot as plt
import argparse


def v_t(v, dt, m, g, k):
    return v + dt * ((-m*g-k*v) / m)

################################################
def main():
    my_m = 10
    my_g = 9.81
    my_k = 0.47

        # starting conditions
    v0 = 0
    t0 = 0

        # these will store the time and velocity for each time step
    times = [t0]
    velocities = [v0]

    parser = argparse.ArgumentParser(description='Project 1 Eulers method:')
    parser.add_argument('d', type=int, help='Duration of the Simulation(in seconds):')
    parser.add_argument('dt', type=float, help='Step Siz(in seconds):')
    parser.add_argument('mode', type=str, help='Select Mode Eulers or Mid: ')
    args = parser.parse_args();

    #remeber there is a mutually exclusive feture which allows you to only select one.
        # run for as long as requested
    my_dt = args.dt
    t_stop = args.d

    if(args.mode == 'Eulers'):
        while times[-1] < t_stop:
            # calculate next time
            times.append(times[-1] + my_dt)
            # calculate next velocity
            velocities.append(v_t(velocities[-1], my_dt, my_m, my_g, my_k))



    plt.plot(times, velocities, color='k')
    plt.xlabel("Time (s)", size=16)
    plt.ylabel("Velocity (m/s)", size=16)
    plt.show()

if __name__ == "__main__":
    main()